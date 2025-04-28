import sys  
import struct  
import os  
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QScrollArea  
from PyQt5.QtGui import QPixmap, QPainter, QColor, QImage  
from PyQt5.QtCore import QRect, Qt  

# --------- خواندن فایل متنی BMFont --------------  
def parse_fnt_text(fnt_path):  
    font_info = {}  
    pages = {}  
    chars = {}  

    with open(fnt_path, 'r', encoding='utf-8') as f:  
        for line in f:  
            line = line.strip()  
            if line.startswith('info '):  
                continue  
            elif line.startswith('common '):  
                parts = line.split()  
                for part in parts[1:]:  
                    if '=' in part:  
                        k,v = part.split('=')  
                        font_info[k] = int(v)  
            elif line.startswith('page '):  
                parts = line.split()  
                id_ = None  
                file_ = None  
                for part in parts[1:]:  
                    if part.startswith('id='):  
                        id_ = int(part[3:])  
                    elif part.startswith('file='):  
                        file_ = part[5:].strip('"')  
                if id_ is not None and file_ is not None:  
                    pages[id_] = file_  
            elif line.startswith('char '):  
                parts = line.split()  
                ch_info = {}  
                ch_id = None  
                for part in parts[1:]:  
                    if '=' in part:  
                        k,v = part.split('=')  
                        if k == 'id':  
                            ch_id = int(v)  
                        else:  
                            ch_info[k] = int(v)  
                if ch_id is not None:  
                    chars[ch_id] = ch_info  

    return font_info, pages, chars  

# --------- خواندن فایل باینری BMFont نسخه 3 --------------  
class BitmapFontBinary:  

    def __init__(self, filepath):  
        self.filepath = filepath  
        self.info = {}  
        self.common = {}  
        self.pages = {}  
        self.chars = {}  
        self.textures = {}  
        self.load()  

    def load(self):  
        with open(self.filepath, 'rb') as f:  
            header = f.read(4)  
            if len(header) < 4 or header[:3] != b'BMF':  
                raise Exception("This is not a valid BMFont file (missing 'BMF' header)")  

            version = header[3]  
            if version != 3:  
                raise Exception(f"Unsupported BMFont binary version: {version}")  

            while True:  
                block_header = f.read(5)  
                if len(block_header) < 5:  
                    break  

                block_id = block_header[0]  
                block_size = struct.unpack('<I', block_header[1:])[0]  
                block_data = f.read(block_size)  

                if block_id == 1:   # info block  
                    font_size = struct.unpack('<h', block_data[:2])[0]  
                    self.info['fontSize'] = font_size  
                    # خیلی اطلاعات را اینجا نمی‌خوانیم چون لازم نیست  
                elif block_id == 2:  # common block  
                    if len(block_data) >= 15:  
                        unpacked = struct.unpack('<HHHHHBBBBB', block_data[:15])  
                        self.common['lineHeight'] = unpacked[0]  
                        self.common['base'] = unpacked[1]  
                        self.common['scaleW'] = unpacked[2]  
                        self.common['scaleH'] = unpacked[3]  
                        self.common['pages'] = unpacked[4]  
                        self.common['packed'] = unpacked[5]  
                        self.common['alphaChnl'] = unpacked[6]  
                        self.common['redChnl'] = unpacked[7]  
                        self.common['greenChnl'] = unpacked[8]  
                        self.common['blueChnl'] = unpacked[9]  
                elif block_id == 3:  # pages block  
                    # هر صفحه نام 0 ترمی دارد  
                    offset = 0  
                    for i in range(self.common.get('pages', 0)):  
                        end_index = block_data.find(b'\x00', offset)  
                        if end_index == -1:  
                            raise Exception("Invalid pages block (no null terminator)")  
                        page_name = block_data[offset:end_index].decode('utf-8')  
                        self.pages[i] = page_name  
                        offset = end_index + 1  
                elif block_id == 4:  # chars block  
                    char_struct_size = 20  
                    count = block_size // char_struct_size  
                    for i in range(count):  
                        offset = i*char_struct_size  
                        # هر رکورد 20 بایت است  
                        char_data = block_data[offset:offset+char_struct_size]  
                        (char_id, x, y, width, height,  
                         xoffset, yoffset, xadvance,  
                         page, chnl) = struct.unpack('<IHHHHhhhbB', char_data)  
                        self.chars[char_id] = {  
                            "x": x,  
                            "y": y,  
                            "width": width,  
                            "height": height,  
                            "xoffset": xoffset,  
                            "yoffset": yoffset,  
                            "xadvance": xadvance,  
                            "page": page,  
                            "chnl": chnl  
                        }  
                else:  
                    # بلاک‌های دیگر در اینجا نخوانده می‌شوند  
                    pass  

        # بارگذاری تصاویر صفحه  
        base_path = os.path.dirname(self.filepath)  
        for pid, fname in self.pages.items():  
            img_path = os.path.join(base_path, fname)  
            if not os.path.isfile(img_path):  
                print(f"Warning: Image page file not found: {img_path} (ممکن است لازم باشد DDS به PNG تبدیل شود)")  
                self.textures[pid] = None  
            else:  
                pix = QPixmap(img_path)  
                if pix.isNull():  
                    print(f"Warning: Failed to load image page: {img_path}")  
                    self.textures[pid] = None  
                else:  
                    self.textures[pid] = pix  

    def draw_text(self, text):  
        if not self.common:  
            raise Exception("Common block not loaded!")  

        lineHeight = self.common.get('lineHeight', 0)  
        scaleW = self.common.get('scaleW', 0)  
        scaleH = self.common.get('scaleH', 0)  

        # تقریب ساده، اندازه تصویر قاعدتا باید اندازه صفحه فونت باشد  
        # اندازه تقریبی کل متن را پیدا می‌کنیم  
        width = 0  
        for ch in text:  
            ch_id = ord(ch)  
            info = self.chars.get(ch_id)  
            if info:  
                width += info['xadvance']  
        height = lineHeight  

        image = QImage(width, height, QImage.Format_ARGB32)  
        image.fill(Qt.transparent)  

        painter = QPainter(image)  
        painter.setPen(QColor(255, 255, 255))  

        pen_x = 0  
        pen_y = self.common.get('base', 0)  # پایه خط  

        for ch in text:  
            ch_id = ord(ch)  
            info = self.chars.get(ch_id)  
            if not info:  
                pen_x += lineHeight // 2  # فاصله پیش‌فرض برای حروف ناشناخته  
                continue  
            page = info['page']  
            tex = self.textures.get(page)  
            if tex is None:  
                pen_x += info['xadvance']  
                continue  
            rect = QRect(info['x'], info['y'], info['width'], info['height'])  
            target_pos = QPoint(pen_x + info['xoffset'], pen_y - info['yoffset'] - info['height'])  
            painter.drawPixmap(target_pos, tex, rect)  

            pen_x += info['xadvance']  

        painter.end()  
        return QPixmap.fromImage(image)  

# -------- کلاس ویجت نمایش فونت ----------  
class FontViewerWindow(QWidget):  
    def __init__(self, fontpath):  
        super().__init__()  
        self.setWindowTitle("نمایش فونت BMFont")  
        self.layout = QVBoxLayout(self)  

        # Scroll Area  
        self.scroll = QScrollArea(self)  
        self.container = QLabel()  
        self.container.setAlignment(Qt.AlignLeft | Qt.AlignTop)  
        self.scroll.setWidgetResizable(True)  
        self.scroll.setWidget(self.container)  

        self.layout.addWidget(self.scroll)  

        self.font_binary = None  
        self.font_text_info = {}  
        self.font_text_pages = {}  
        self.font_text_chars = {}  

        ext = os.path.splitext(fontpath)[1].lower()  
        if ext == '.fnt':  
            # متنی  
            self.font_text_info, self.font_text_pages, self.font_text_chars = parse_fnt_text(fontpath)  
            self.base_path = os.path.dirname(fontpath)  
            self.show_text_font()  
        else:  
            # باینری  
            try:  
                self.font_binary = BitmapFontBinary(fontpath)  
                self.show_binary_font()  
            except Exception as e:  
                self.container.setText(f"خطا در بارگذاری فونت باینری:\n{e}")  

    def show_text_font(self):  
        # بارگذاری صفحات (تصاویر)  
        self.textures = {}  
        for pid, fname in self.font_text_pages.items():  
            img_path = os.path.join(self.base_path, fname)  
            if not os.path.isfile(img_path):  
                self.container.setText(f"تصویر صفحه فونت پیدا نشد: {img_path}\nممکن است لازم باشد DDS را به PNG تبدیل کنید.")  
                return  
            pix = QPixmap(img_path)  
            if pix.isNull():  
                self.container.setText(f"بارگذاری تصویر صفحه فونت شکست خورد: {img_path}")  
                return  
            self.textures[pid] = pix  

        # رسم متن نمونه  
        text = "سلام دنیا! Hello BMFont"  

        image = self.render_text(text)  
        self.container.setPixmap(image)  

    def render_text(self, text):  
        lineHeight = self.font_text_info.get('lineHeight', 0)  
        base = self.font_text_info.get('base', 0)  

        # محاسبه عرض کل متن:  
        width = 0  
        for ch in text:  
            ch_id = ord(ch)  
            info = self.font_text_chars.get(ch_id)  
            if info:  
                width += info.get('xadvance', 0)  
            else:  
                width += lineHeight // 2  # پیش‌فرض  
        height = lineHeight  

        image = QImage(width, height, QImage.Format_ARGB32)  
        image.fill(Qt.transparent)  

        painter = QPainter(image)  
        painter.setPen(QColor(255, 255, 255))  

        pen_x = 0  
        pen_y = base  

        for ch in text:  
            ch_id = ord(ch)  
            info = self.font_text_chars.get(ch_id)  
            if not info:  
                pen_x += lineHeight // 2  
                continue  
            page = info.get('page', 0)  
            tex = self.textures.get(page)  
            if tex is None:  
                pen_x += info.get('xadvance', 0)  
                continue  

            rect = QRect(info['x'], info['y'], info['width'], info['height'])  
            target_pos = QPoint(pen_x + info.get('xoffset',0), pen_y - info.get('yoffset',0) - info.get('height',0))  
            painter.drawPixmap(target_pos, tex, rect)  
            pen_x += info.get('xadvance', 0)  

        painter.end()  
        return QPixmap.fromImage(image)  

    def show_binary_font(self):  
        # رسم نمونه متن  
        text = "سلام دنیا! Hello BMFont"  
        pix = self.font_binary.draw_text(text)  
        self.container.setPixmap(pix)  


# ---- برنامه اصلی ----  
if __name__ == "__main__":  
    if len(sys.argv) < 2:  
        print("Usage: python bmfont_viewer.py <file1.fnt | font_file.bin>")  
        sys.exit(1)  

    app = QApplication(sys.argv)  
    viewer = FontViewerWindow(sys.argv[1])  
    viewer.resize(800, 200)  
    viewer.show()  
    sys.exit(app.exec_())
