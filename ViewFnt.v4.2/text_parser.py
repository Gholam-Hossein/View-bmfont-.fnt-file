# text_parser.py
from character import FontCharacter


def parse_text_fnt(filename, chars, pages):
    """پردازش فایل فونت با فرمت متنی"""
    with open(filename, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("page"):
                parts = line.split()
                page_id = None
                page_file = None
                for p in parts:
                    if p.startswith("id="):
                        page_id = int(p.split("=")[1])
                    if p.startswith("file="):
                        page_file = p.split("=")[1].strip('"')
                if page_id is not None and page_file:
                    pages[page_id] = page_file
            elif line.startswith("char"):
                parts = line.split()
                info = {}
                for p in parts:
                    if "=" in p:
                        k, v = p.split("=")
                        info[k] = v
                c = FontCharacter(
                    id=int(info.get("id", 0)),
                    x=int(info.get("x", 0)),
                    y=int(info.get("y", 0)),
                    width=int(info.get("width", 0)),
                    height=int(info.get("height", 0)),
                    xoffset=int(info.get("xoffset", 0)),
                    yoffset=int(info.get("yoffset", 0)),
                    xadvance=int(info.get("xadvance", 0)),
                    page=int(info.get("page", 0)),
                )
                chars[c.id] = c
