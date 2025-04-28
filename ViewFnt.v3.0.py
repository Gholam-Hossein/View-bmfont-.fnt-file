import sys  
import os  
import struct  
from PyQt5.QtWidgets import (  
    QApplication, QWidget, QVBoxLayout, QLineEdit, QLabel, QSlider, QHBoxLayout  
)  
from PyQt5.QtGui import QPixmap, QImage, QColor  
from PyQt5.QtCore import Qt  
from PIL import Image  

class FontCharacter:  
    def __init__(self, id, x, y, width, height, xoffset, yoffset, xadvance, page):  
        self.id = id  
        self.x = x  
        self.y = y  
        self.width = width  
        self.height = height  
        self.xoffset = xoffset  
        self.yoffset = yoffset  
        self.xadvance = xadvance  
        self.page = page  

class BitmapFont:  
    def __init__(self, fnt_file, images_folder):  
        self.chars = {}  # id -> FontCharacter  
        self.pages = {}  # id -> PIL Image or file name(str) to load later  
        self.images_folder = images_folder  
        self.info = {}  
        self.line_height = 0  
        self.base = 0  

        # شناسایی نوع فایل بر اساس محتوای اولیه و اکستنشن  
        if fnt_file.lower().endswith(".fnt"):  
            with open(fnt_file, "rb") as fb:  
                sign = fb.read(3)  
                fb.seek(0)  
                if sign == b"BMF":  
                    # باینری است  
                    self.parse_binary_fnt(fb)  
                else:  
                    # متن است  
                    self.parse_text_fnt(fnt_file)  
        elif fnt_file.lower().endswith(".xml"):  
            self.parse_xml_fnt(fnt_file)  
        else:  
            self.parse_text_fnt(fnt_file)  

        self.load_pages()  

    def parse_text_fnt(self, filename):  
        with open(filename, encoding='utf-8') as f:  
            for line in f:  
                line = line.strip()  
                if line.startswith("info"):  
                    # مثال: info face="SomeFont" size=32 ...  
                    # میتونیم پارس کنیم اما فعلا نیاز نیست  
                    pass  
                elif line.startswith("common"):  
                    # common lineHeight=28 base=19 scaleW=256 scaleH=256 pages=4 packed=0  
                    parts = line.split()  
                    for p in parts[1:]:  
                        if '=' in p:  
                            k,v = p.split('=')  
                            if k=="lineHeight":  
                                self.line_height = int(v)  
                            elif k=="base":  
                                self.base = int(v)  
                elif line.startswith("page"):  
                    parts = line.split()  
                    page_id = None  
                    page_file = None  
                    for p in parts:  
                        if p.startswith("id="):  
                            page_id = int(p.split('=')[1])  
                        if p.startswith("file="):  
                            page_file = p.split('=')[1].strip('"')  
                    if page_id is not None and page_file:  
                        self.pages[page_id] = page_file  
                elif line.startswith("char"):  
                    parts = line.split()  
                    info = {}  
                    for p in parts:  
                        if '=' in p:  
                            k,v = p.split('=')  
                            info[k] = v  
                    c = FontCharacter(  
                        id=int(info.get("id", 0)),  
                        x=int(info.get("x",0)),  
                        y=int(info.get("y",0)),  
                        width=int(info.get("width",0)),  
                        height=int(info.get("height",0)),  
                        xoffset=int(info.get("xoffset",0)),  
                        yoffset=int(info.get("yoffset",0)),  
                        xadvance=int(info.get("xadvance",0)),  
                        page=int(info.get("page",0)),  
                    )  
                    self.chars[c.id] = c  

    def parse_xml_fnt(self, filename):  
        # اگر نیاز بود اضافه می‌کنیم - اینجا نداریم فعلا  
        import xml.etree.ElementTree as ET  
        tree = ET.parse(filename)  
        root = tree.getroot()  
        common = root.find("common")  
        if common is not None:  
            self.line_height = int(common.attrib.get("lineHeight", 0))  
            self.base = int(common.attrib.get("base", 0))  
        pages = root.find("pages")  
        if pages is not None:  
            for page in pages.findall("page"):  
                id = int(page.attrib.get("id", "0"))  
                file = page.attrib.get("file", "")  
                if file != "":  
                    self.pages[id] = file  
        chars = root.find("chars")  
        if chars is not None:  
            for ch in chars.findall("char"):  
                c = FontCharacter(  
                    id=int(ch.attrib.get("id", 0)),  
                    x=int(ch.attrib.get("x", 0)),  
                    y=int(ch.attrib.get("y", 0)),  
                    width=int(ch.attrib.get("width", 0)),  
                    height=int(ch.attrib.get("height", 0)),  
                    xoffset=int(ch.attrib.get("xoffset", 0)),  
                    yoffset=int(ch.attrib.get("yoffset", 0)),  
                    xadvance=int(ch.attrib.get("xadvance", 0)),  
                    page=int(ch.attrib.get("page", 0)),  
                )  
                self.chars[c.id] = c  

    def parse_binary_fnt(self, fb):  
        # گرفتن سرآغاز BMF (3 bytes)  
        sign = fb.read(3)  
        if sign != b'BMF':  
            raise ValueError("Not a valid BMFont binary file")  
        version = fb.read(1)  
        if version != b'\x03':  
            # این کد برای نسخه 3 طراحی شده  
            raise ValueError("Only BMFont binary version 3 supported")  

        # بلوک‌ها به صورت  
        # block_type (1 byte) + block_size (4 bytes) + data  
        while True:  
            block_header = fb.read(5)  
            if len(block_header) < 5:  
                break  
            block_type = block_header[0]  
            block_size = struct.unpack("<I", block_header[1:])[0]  
            data = fb.read(block_size)  
            if block_type == 1:  
                # Info block (ما فعلا نیاز به info نداریم)  
                pass  
            elif block_type == 2:  
                # Common  
                # lineHeight(2), base(2), scaleW(2), scaleH(2), pages(2), packed(1), alphaChnl(1), redChnl(1), greenChnl(1), blueChnl(1)  
                vals = struct.unpack("<HHHHHHBBBB", data[:16])  
                self.line_height = vals[0]  
                self.base = vals[1]  
                self.pages_count = vals[4]  
            elif block_type == 3:  
                # Pages (list of null-terminated strings)  
                # به تعداد pages_count فایل ها در داده وجود دارد  
                page_names = []  
                start = 0  
                for _ in range(self.pages_count):  
                    end_i = data.find(b'\x00', start)  
                    if end_i == -1:  
                        break  
                    name = data[start:end_i].decode("utf-8")  
                    page_names.append(name)  
                    start = end_i + 1  
                for i, n in enumerate(page_names):  
                    self.pages[i] = n  
            elif block_type == 4:  
                # Chars (بلوک 20 بایت مثلاً، تعداد مشخص نشده اما block_size مشخص است)  
                # ساختار هر char: id(4), x(2), y(2), width(2), height(2), xoffset(2), yoffset(2), xadvance(2), page(1), chnl(1)  
                N = block_size // 20  
                for i in range(N):  
                    chunk = data[i*20:(i+1)*20]  
                    (  
                        id,  
                        x, y,  
                        width, height,  
                        xoffset, yoffset,  
                        xadvance,  
                        page,  
                        chnl  
                    ) = struct.unpack("<IHHHHhhHBb", chunk)  
                    c = FontCharacter(id, x, y, width, height, xoffset, yoffset, xadvance, page)  
                    self.chars[id] = c  

            else:  
                # سایر بلوک‌ها را فعلا رد می‌کنیم  
                pass  

    def load_pages(self):  
        # بارگذاری صفحه‌های فونت (تصاویر)  
        for pid, fname in list(self.pages.items()):  
            if isinstance(fname, Image.Image):  
                # اگر قبلاً بارگذاری شده بود رد کنیم  
                continue  
            path = os.path.join(self.images_folder, fname)  
            if os.path.isfile(path):  
                try:  
                    im = Image.open(path).convert("RGBA")  
                    self.pages[pid] = im  
                except Exception as e:  
                    print(f"Error loading {path}: {e}")  
                    self.pages[pid] = None  
            else:  
                print(f"Page image file does not exist: {path}")  
                self.pages[pid] = None  

    def render_text(self, text, scale=1.0):  
        # محاسبه ابعاد  
        width = 0  
        max_top = 0  
        max_bottom = 0  

        chars_for_render = []  

        for ch in text:  
            cid = ord(ch)  
            c = self.chars.get(cid)  
            if not c:  
                space = self.chars.get(ord(' '))  
                if space:  
                    width += space.xadvance  
                continue  
            chars_for_render.append(c)  
            width += c.xadvance  
            top = -c.yoffset  
            bottom = c.height - c.yoffset  # اصلاح شده به bottom درست  
            if top > max_top:  
                max_top = top  
            if bottom > max_bottom:  
                max_bottom = bottom  

        if width == 0 or max_top + max_bottom == 0:  
            return None  

        height = max_top + max_bottom  

        # ابعاد رندر شده با توجه به scale  
        width = int(width * scale)  
        height = int(height * scale)  

        img = Image.new("RGBA", (width, height), (0, 0, 0, 0))  

        cursor_x = 0  
        for c in chars_for_render:  
            page_img = self.pages.get(c.page)  
            if page_img is None:  
                continue  
            char_img = page_img.crop((c.x, c.y, c.x + c.width, c.y + c.height))  
            if scale != 1.0:  
                new_w = int(c.width * scale)  
                new_h = int(c.height * scale)  
                if new_w == 0 or new_h == 0:  
                    continue  
                char_img = char_img.resize((new_w, new_h), Image.ANTIALIAS)  

            pos_x = int(cursor_x + c.xoffset * scale)  
            pos_y = int(max_top * scale + c.yoffset * scale)  
            img.alpha_composite(char_img, (pos_x, pos_y))  
            cursor_x += c.xadvance * scale  

        return img
