![Description](https://github.com/Gholam-Hossein/View-bmfont-.fnt-file/blob/main/Image/Screenshot%202025-05-02%20165457.png)
![Description](https://github.com/Gholam-Hossein/View-bmfont-.fnt-file/blob/main/Image/Screenshot%202025-05-02%20165546.png)
![Description](https://github.com/Gholam-Hossein/View-bmfont-.fnt-file/blob/main/Image/Screenshot%202025-05-02%20165633.png)
![Description](https://github.com/Gholam-Hossein/View-bmfont-.fnt-file/blob/main/Image/View-bmfont-.fnt-file-icon.png)
```markdown
# Custom Bitmap Font Renderer

## Overview
A Python application built with PyQt5 to render text using custom bitmap fonts (.fnt files) in text, XML, and binary formats. It provides a user-friendly interface to load, manage, and render multiple fonts with customizable background color and zoom.

## Features
- Load and render .fnt files (text, XML, binary formats).
- Support for multiple fonts with individual text fields.
- Remove additional fonts (except the initial font).
- Change background color via a color picker.
- Zoom slider for adjusting text size.
- File menu with Open, Add .fnt, Open Recent (up to 5 files), and Remove All Fonts.
- Persistent "last folder" for file dialogs.
- Recent files stored in `recent_files.json`.
- Vertical text rendering.

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd project_folder
   ```
2. Install dependencies:
   ```bash
   pip install PyQt5
   ```
3. Ensure sample .fnt files (`file1.fnt`, `file2.fnt`, `file3.fnt`) and their images (`file2_0.png`, `file3_0.tga`) are in the `Test-fnt` folder.
4. Run the application:
   ```bash
   python main.py
   ```

## Usage
1. Launch the application (`python main.py`).
2. Select an initial .fnt file from the `Test-fnt` folder via the file dialog.
3. Use the interface:
   - Enter text in the text field (default: "Hello").
   - Use **File > Open** to replace the initial font.
   - Use **File > Add .fnt** to add more fonts (with removable text fields).
   - Use **File > Open Recent** to load recent files (stored in `recent_files.json`).
   - Use **File > Remove All Fonts** to clear extra fonts.
   - Click **Change Color** to pick a background color.
   - Adjust the zoom slider to resize text.
4. View the rendered text in the scrollable output area.

## Project Structure
```
project_folder/
├── README.md               Documentation
├── main.py                 Entry point
├── ui.py                   User interface
├── renderer.py             Text rendering
├── font_manager.py         Font and field management
├── recent_files.py         Recent files management
├── font.py                 Font processing
├── text_parser.py          Text .fnt parser
├── xml_parser.py           XML .fnt parser
├── binary_parser.py        Binary .fnt parser
├── recent_files.json       Recent files storage
├── Test-fnt/
│   ├── file1.fnt           Sample font file
│   ├── file2.fnt           Sample font file (XML)
│   ├── file3.fnt           Sample font file
│   ├── file2_0.png         Font image for file2.fnt
│   ├── file3_0.tga         Font image for file3.fnt
```

## Contributing
Contributions are welcome! Please submit a pull request or open an issue to discuss improvements.

---

# رندر فونت بیت‌مپ سفارشی

## مرور
این برنامه پایتون با PyQt5 برای رندر متن با استفاده از فونت‌های بیت‌مپ سفارشی (فایل‌های .fnt) در فرمت‌های متنی، XML، و باینری طراحی شده است. رابط کاربری ساده‌ای برای بارگذاری، مدیریت، و رندر چندین فونت با رنگ پس‌زمینه و زوم قابل تنظیم ارائه می‌دهد.

## ویژگی‌ها
- بارگذاری و رندر فایل‌های .fnt (فرمت‌های متنی، XML، باینری).
- پشتیبانی از چندین فونت با فیلدهای متنی مجزا.
- حذف فونت‌های اضافی (به جز فونت اولیه).
- تغییر رنگ پس‌زمینه با انتخاب‌گر رنگ.
- اسلایدر زوم برای تنظیم اندازه متن.
- منوی فایل با گزینه‌های باز کردن، افزودن .fnt، باز کردن اخیر (تا 5 فایل)، و حذف همه فونت‌ها.
- ذخیره آخرین پوشه برای دیالوگ‌های فایل.
- ذخیره فایل‌های اخیر در `recent_files.json`.
- رندر عمودی متن.

## نصب
1. مخزن را کلون کنید:
   ```bash
   git clone <آدرس-مخزن>
   cd project_folder
   ```
2. وابستگی‌ها را نصب کنید:
   ```bash
   pip install PyQt5
   ```
3. مطمئن شوید فایل‌های نمونه .fnt (`file1.fnt`, `file2.fnt`, `file3.fnt`) و تصاویرشان (`file2_0.png`, `file3_0.tga`) در پوشه `Test-fnt` هستند.
4. برنامه را اجرا کنید:
   ```bash
   python main.py
   ```

## استفاده
1. برنامه را اجرا کنید (`python main.py`).
2. یک فایل .fnt اولیه از پوشه `Test-fnt` از طریق دیالوگ فایل انتخاب کنید.
3. از رابط کاربری استفاده کنید:
   - متن را در فیلد متنی وارد کنید (پیش‌فرض: "Hello").
   - از **File > Open** برای جایگزینی فونت اولیه استفاده کنید.
   - از **File > Add .fnt** برای افزودن فونت‌های بیشتر (با فیلدهای قابل حذف) استفاده کنید.
   - از **File > Open Recent** برای بارگذاری فایل‌های اخیر (ذخیره در `recent_files.json`) استفاده کنید.
   - از **File > Remove All Fonts** برای پاک کردن فونت‌های اضافی استفاده کنید.
   - روی **Change Color** کلیک کنید تا رنگ پس‌زمینه را انتخاب کنید.
   - اسلایدر زوم را برای تغییر اندازه متن تنظیم کنید.
4. متن رندرشده را در منطقه خروجی قابل اسکرول ببینید.

## ساختار پروژه
```
project_folder/
├── README.md               مستندات
├── main.py                 نقطه شروع
├── ui.py                   رابط کاربری
├── renderer.py             رندر متن
├── font_manager.py         مدیریت فونت و فیلدها
├── recent_files.py         مدیریت فایل‌های اخیر
├── font.py                 پردازش فونت
├── text_parser.py          پارس‌کننده .fnt متنی
├── xml_parser.py           پارس‌کننده .fnt XML
├── binary_parser.py        پارس‌کننده .fnt باینری
├── recent_files.json       ذخیره فایل‌های اخیر
├── Test-fnt/
│   ├── file1.fnt           فایل فونت نمونه
│   ├── file2.fnt           فایل فونت نمونه (XML)
│   ├── file3.fnt           فایل فونت نمونه
│   ├── file2_0.png         تصویر فونت برای file2.fnt
│   ├── file3_0.tga         تصویر فونت برای file3.fnt
```

## مشارکت
مشارکت‌ها استقبال می‌شوند! لطفاً یک درخواست کش ارسال کنید یا یک مسئله برای بحث درباره بهبودها باز کنید.
```

**توضیحات README:**
- **ساختار:** اول کل محتوا به انگلیسی (معرفی، ویژگی‌ها، نصب، استفاده، ساختار پروژه، مشارکت)، بعد همون محتوا به فارسی.
- **بدون مجوز:** بخش مجوز حذف شده.
- **به‌روز شده:** ساختار پروژه با پوشه `Test-fnt` هماهنگه.
- **ساده و واضح:** حدود 100 خط (50 خط انگلیسی + 50 خط فارسی)، مناسب برای کاربران.
- اگه بخوای چیزی اضافه یا کم بشه (مثلاً تصاویر، نمونه خروجی، یا بخش سوالات متداول)، بگو.

---

### نکته مهم درباره پوشه `Test-fnt`
چون فایل‌های `.fnt` و تصاویر رو به `Test-fnt` منتقل کردی، باید مطمئن بشیم که برنامه هنوز می‌تونه این فایل‌ها رو پیدا کنه:
- تو `font_manager.py`، متد `load_font` از `self.last_folder` برای دیالوگ فایل استفاده می‌کنه. این باید درست کار کنه، چون مسیر رو ذخیره می‌کنه.
- تو `main.py`، فایل `.fnt` اولیه از آرگومان خط فرمان یا دیالوگ فایل گرفته می‌شه. اگه برنامه فایل‌ها رو تو `Test-fnt` پیدا نمی‌کنه، باید `main.py` رو به‌روز کنیم تا از این پوشه شروع کنه.

**پیشنهاد برای `main.py`:**
اگه می‌خوای دیالوگ اولیه از `Test-fnt` شروع کنه، می‌تونم `main.py` رو اصلاح کنم. یه نمونه تغییرات:

```python
# main.py
import sys
import os
from PyQt5.QtWidgets import QApplication, QFileDialog
from ui import FontRendererWidget
from font import BitmapFont


def main():
    app = QApplication(sys.argv)
    initial_font = None
    initial_folder = os.path.join(os.getcwd(), "Test-fnt")  # شروع از Test-fnt
    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        try:
            initial_font = BitmapFont(sys.argv[1], os.path.dirname(sys.argv[1]))
        except Exception as e:
            print(f"Error loading font: {e}")
    if not initial_font:
        fnt_file, _ = QFileDialog.getOpenFileName(
            None, "Select BMFont File", initial_folder, "BMFont Files (*.fnt);;All Files (*)"
        )
        if fnt_file:
            try:
                initial_font = BitmapFont(fnt_file, os.path.dirname(fnt_file))
            except Exception as e:
                print(f"Error loading font: {e}")
                sys.exit(1)
        else:
            sys.exit(1)
    window = FontRendererWidget(initial_font)
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
```

**تغییرات پیشنهادی:**
- اضافه کردن `initial_folder` که به `Test-fnt` اشاره می‌کنه.
- تنظیم دیالوگ فایل اولیه برای شروع از `Test-fnt`.
- اگه می‌خوای این تغییرات اعمال بشه، تأیید کن یا بگو چطور مسیر فایل‌ها رو مدیریت کنم.

---

### چطور تست کنیم؟
1. **ساختار دایرکتوری:** مطمئن شو که با نقشه بالا مطابقت داره:
   ```
   project_folder/
   ├── README.md
   ├── main.py
   ├── ui.py
   ├── renderer.py
   ├── font_manager.py
   ├── recent_files.py
   ├── font.py
   ├── text_parser.py
   ├── xml_parser.py
   ├── binary_parser.py
   ├── recent_files.json
   ├── Test-fnt/
   │   ├── file1.fnt
   │   ├── file2.fnt
   │   ├── file3.fnt
   │   ├── file2_0.png
   │   ├── file3_0.tga
   ```
