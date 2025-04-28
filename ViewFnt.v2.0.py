import sys  
import os  
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QLabel  
from PyQt5.QtGui import QPixmap, QImage  
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
        self.pages = {}  # id -> PIL Image  
        self.images_folder = images_folder  
        self.parse_fnt(fnt_file)  
        self.load_pages()  

    def parse_fnt(self, filename):  
        with open(filename, encoding='utf-8') as f:  
            for line in f:  
                line = line.strip()  
                if line.startswith("page"):  
                    # مثال: page id=0 file="file3_0.tga"  
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

    def load_pages(self):  
        # بارگذاری تصاویر صفحات فونت از فایل‌های تصویری  
        for pid, fname in self.pages.items():  
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

    def render_text(self, text):  
        # محاسبه ابعاد کل تصویر خروجی  
        width = 0  
        max_top = 0  
        max_bottom = 0  

        chars_for_render = []  

        for ch in text:  
            cid = ord(ch)  
            c = self.chars.get(cid)  
            if not c:  
                # اگر حرف موجود نبود، فرض کنید space یا عبور است (advance برابر space)  
                space = self.chars.get(ord(' '))  
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
            height = 20  # حداقلی بگذاریم  

        # ایجاد تصویر خالی برای خروجی  
        out_img = Image.new("RGBA", (width, height), (1,1,1,1))  

        x_cursor = 0  
        for c in chars_for_render:  
            img_page = self.pages.get(c.page)  
            if img_page is None:  
                # تصویر صفحه بارگذاری نشده  
                x_cursor += c.xadvance  
                continue  
            # برش حرف  
            char_img = img_page.crop((c.x, c.y, c.x + c.width, c.y + c.height))  
            y_pos = max_top + c.yoffset  
            out_img.paste(char_img, (x_cursor + c.xoffset, y_pos), char_img)  
            x_cursor += c.xadvance  

        return out_img  

# کلاس QWidget ساده با QLineEdit برای تایپ متن و QLabel برای نمایش تصویر فونت  
class FontRendererWidget(QWidget):  
    def __init__(self, font):  
        super().__init__()  
        self.font = font  
        self.init_ui()  

    def init_ui(self):  
        self.setWindowTitle("Custom Bitmap Font Renderer")  
        self.resize(800, 200)  
        vbox = QVBoxLayout()  
        self.line_edit = QLineEdit(self)  
        self.line_edit.setText("Hello")  
        self.line_edit.textChanged.connect(self.on_text_changed)  
        self.label = QLabel(self)  
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignTop)  
        vbox.addWidget(self.line_edit)  
        vbox.addWidget(self.label)  
        self.setLayout(vbox)  
        self.on_text_changed(self.line_edit.text())  

    def on_text_changed(self, text):  
        # رندر متن به صورت تصویر PIL  
        img = self.font.render_text(text)  
        if img is None:  
            self.label.clear()  
            return  
        # تبدیل PIL Image به QImage  
        data = img.tobytes("raw", "RGBA")  
        qimg = QImage(data, img.width, img.height, QImage.Format_RGBA8888)  
        pixmap = QPixmap.fromImage(qimg)  
        self.label.setPixmap(pixmap)  
        self.label.resize(pixmap.width(), pixmap.height())  

if __name__ == "__main__":  
    app = QApplication(sys.argv)  

    # مسیر فولدر و نام فایل فونت خودتان را اینجا اصلاح کنید:  
    base_folder = "./"  
    fnt_file = os.path.join(base_folder, "file1.fnt")  # مثلا file3.fnt هست  
    images_folder = base_folder  

    font = BitmapFont(fnt_file, images_folder)  

    window = FontRendererWidget(font)  
    window.show()  

    sys.exit(app.exec_())
