# xml_parser.py
import xml.etree.ElementTree as ET
from character import FontCharacter


def parse_xml_fnt(filename, chars, pages):
    """پردازش فایل فونت با فرمت XML"""
    try:
        tree = ET.parse(filename)
        root = tree.getroot()

        # پردازش صفحات
        for page in root.findall(".//page"):
            page_id = int(page.get("id", "0"))
            page_file = page.get("file", "").strip('"')
            if page_id is not None and page_file:
                pages[page_id] = page_file

        # پردازش کاراکترها
        for char in root.findall(".//char"):
            c = FontCharacter(
                id=int(char.get("id", "0")),
                x=int(char.get("x", "0")),
                y=int(char.get("y", "0")),
                width=int(char.get("width", "0")),
                height=int(char.get("height", "0")),
                xoffset=int(char.get("xoffset", "0")),
                yoffset=int(char.get("yoffset", "0")),
                xadvance=int(char.get("xadvance", "0")),
                page=int(char.get("page", "0")),
            )
            chars[c.id] = c
    except ET.ParseError as e:
        print(f"Error parsing XML file {filename}: {e}")
