import os  
from PIL import Image  
from text_parser import parse_text_fnt  
from xml_parser import parse_xml_fnt  
from binary_parser import parse_binary_fnt  # اضافه شده برای پشتیبانی باینری  

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
        self.chars = {}  # دیکشنری id -> FontCharacter  
        self.pages = {}  # دیکشنری id -> فایل تصویر یا تصویر بارگذاری شده  
        self.images_folder = images_folder  

        self.parse_fnt(fnt_file)  
        self.load_pages()  

    def _is_xml_file(self, filename):  
        try:  
            with open(filename, encoding="utf-8") as f:  
                first_line = f.readline().strip()  
                return first_line.startswith("<?xml") or first_line.startswith("<font")  
        except Exception:  
            return False  

    def _is_binary_file(self, filename):  
        try:  
            with open(filename, "rb") as f:  
                header = f.read(4)  
                return header == b"BMF\x03"  
        except Exception:  
            return False  

    def parse_fnt(self, filename):  
        """پردازش فایل فونت با تشخیص نوع فرمت"""  
        if self._is_binary_file(filename):  
            parse_binary_fnt(filename, self.chars, self.pages)  
        elif self._is_xml_file(filename):  
            parse_xml_fnt(filename, self.chars, self.pages)  
        else:  
            parse_text_fnt(filename, self.chars, self.pages)  

    def load_pages(self):  
        for pid, fname in list(self.pages.items()):  
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

    def render_text(self, text, background_color=(50, 50, 50, 255)):  
        width = 0  
        max_top = 0  
        max_bottom = 0  
        chars_for_render = []  

        for ch in text:  
            cid = ord(ch)  
            c = self.chars.get(cid)  
            if not c:  
                space = self.chars.get(ord(" "))  
                if space:  
                    width += space.xadvance  
                continue  
            chars_for_render.append(c)  
            width += c.xadvance  
            top = -c.yoffset  
            bottom = c.height + c.yoffset  
            if top > max_top:  
                max_top = top  
            if bottom > max_bottom:  
                max_bottom = bottom  

        height = max_top + max_bottom  
        if height == 0:  
            height = 20  

        out_img = Image.new("RGBA", (width, height), background_color)  

        x_cursor = 0  
        for c in chars_for_render:  
            img_page = self.pages.get(c.page)  
            if img_page is None:  
                x_cursor += c.xadvance  
                continue  
            char_img = img_page.crop((c.x, c.y, c.x + c.width, c.y + c.height))  
            y_pos = max_top + c.yoffset  
            out_img.paste(char_img, (x_cursor + c.xoffset, y_pos), char_img)  
            x_cursor += c.xadvance  

        return out_img