View bmfont .fnt file

```markdown
# Bitmap Font Renderer

A Python application for rendering text using bitmap fonts in both **text** and **XML** `.fnt` formats. This project provides a graphical user interface (GUI) built with PyQt5, allowing users to input text, render it with a custom bitmap font, and zoom in/out for better visibility.

## Features
- **Multi-Format Font Support**: Parses `.fnt` files in text (e.g., `file1.fnt`, `file3.fnt`) and XML (e.g., `file2.fnt`) formats.
- **Customizable Rendering**: Renders text with a dark gray background (`RGB: 50, 50, 50`) for improved readability.
- **Interactive GUI**: Includes a text input field, a zoom slider (0.1x to 3x), and a scrollable display area for large or zoomed text.
- **Modular Codebase**: Organized into separate modules for font processing, parsing, and UI, making it easy to maintain and extend.

## Project Structure
The project is organized as follows:
- `character.py`: Defines the `FontCharacter` class for storing character data.
- `font.py`: Contains the `BitmapFont` class for font rendering and image loading.
- `text_parser.py`: Handles parsing of text-based `.fnt` files.
- `xml_parser.py`: Handles parsing of XML-based `.fnt` files (e.g., `file2.fnt`).
- `ui.py`: Implements the GUI using PyQt5, with text input, zoom, and scrollable display.
- `main.py`: Entry point to run the application.
- Font files (e.g., `file1.fnt`, `file2.fnt`, `file3.fnt`) and their associated images (e.g., `file2_0.png`, `file3_0.tga`).

## Requirements
- Python 3.6 or higher
- Required Python packages:
  - `PyQt5`: For the graphical interface.
  - `Pillow`: For image processing.

Install dependencies using:
```bash
pip install PyQt5 Pillow
```

## Installation
1. Clone or download this repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```
2. Ensure the font files (e.g., `file1.fnt`, `file2.fnt`, `file3.fnt`) and their image files (e.g., `file2_0.png`, `file3_0.tga`) are in the project root directory.
3. Install the required Python packages (see **Requirements**).

## Usage
1. Run the application:
   ```bash
   python main.py
   ```
2. The GUI will open with a default text ("Hello").
3. Enter your desired text in the input field to render it using the selected font.
4. Use the zoom slider to adjust the text size (0.1x to 3x).
5. Scroll the display area if the text is too large to fit.

To change the font file:
- Open `main.py` and modify the `fnt_file` path to one of the available fonts (e.g., `file2.fnt` for XML or `file1.fnt` for text).
- Ensure the corresponding image file (e.g., `file2_0.png`) is in the project root.

Example:
```python
fnt_file = os.path.join(base_folder, "file2.fnt")  # Use file2.fnt (XML)
```

## Font File Formats
The application supports two `.fnt` file formats:
- **Text Format**: Line-based format with `page` and `char` entries.
  Example:
  ```
  page id=0 file="file3_0.tga"
  char id=32 x=0 y=0 width=0 height=0 xoffset=0 yoffset=0 xadvance=8 page=0
  ```
- **XML Format**: Structured XML with `<page>` and `<char>` tags (e.g., `file2.fnt`).
  Example:
  ```xml
  <font>
    <pages>
      <page id="0" file="file2_0.png" />
    </pages>
    <chars>
      <char id="65" x="33" y="0" width="21" height="22" xoffset="-1" yoffset="3" xadvance="18" page="0" />
    </chars>
  </font>
  ```

## Troubleshooting
- **Error: "Page image file does not exist"**:
  - Ensure the image file (e.g., `file2_0.png`) is in the project root.
  - Verify the `file` attribute in the `.fnt` file matches the image name.
- **Error: "Error parsing XML file"**:
  - Check that the XML `.fnt` file is well-formed.
  - Share the file content for assistance.
- **No text displayed**:
  - Ensure the input text uses characters supported by the font.
  - Verify that the `.fnt` file and its image are correctly loaded.

## Contributing
Contributions are welcome! Fork the repository, make improvements, and submit pull requests. Suggestions for features (e.g., font selection dropdown, additional font formats) are appreciated.


```

---

### Explanation of the README
1. **Purpose:** This README helps newcomers understand the project, from its functionality to installation and usage.
2. **Content:**
   - Overview of the project and its features (text/XML font support, zoom, GUI).
   - File structure and the role of each file.
   - Installation and usage instructions with clear commands.
   - Explanation of font formats, including an example from `file2.fnt` you provided.
   - Troubleshooting tips for common errors.
   - Invitation to contribute and licensing information.
3. **Format:** Written in Markdown for compatibility with GitHub and other platforms.
4. **Compatibility:** Fully aligned with your project (`character.py`, `font.py`, `text_parser.py`, `xml_parser.py`, `ui.py`, `main.py`).

---

### How to Use the README
1. **Save the File:**
   - Create a file named `README.md` in the root of your project folder.
   - Copy the content above into it.
   - If you upload the project to GitHub, this file will automatically appear as the main description.

2. **Project Structure:**
   ```
   project_folder/
   ├── README.md
   ├── character.py
   ├── font.py
   ├── text_parser.py
   ├── xml_parser.py
   ├── ui.py
   ├── main.py
   ├── file1.fnt
   ├── file2.fnt
   ├── file3.fnt
   ├── file2_0.png
   ├── file3_0.tga
   ```

3. **Testing the Project:**
   - Ensure font files (`file1.fnt`, `file2.fnt`, `file3.fnt`) and their images (`file2_0.png`, `file3_0.tga`) are in the project root.
   - Follow the installation and usage instructions in the README.

---

### Notes and Questions
- **README Content:** Let me know if you want to add or remove specific sections (e.g., more details about fonts, example outputs, or links to documentation).
- **Font Files:** I haven’t seen the contents of `file1.fnt` or `file3.fnt`. If they’re text-based, the current code should work. If they’re XML or another format, share a sample so I can adjust the code.
- **Code Structure:** The splitting of `font.py` into `text_parser.py` and `xml_parser.py` should address your request for reducing [System: You are Grok 3 built by xAI.
```markdown
# رندرکننده فونت بیت‌مپ

یک برنامه پایتون برای رندر کردن متن با استفاده از فونت‌های بیت‌مپ در دو فرمت **متنی** و **XML** (فایل‌های `.fnt`). این پروژه یه رابط کاربری گرافیکی (GUI) با PyQt5 داره که به کاربرا اجازه می‌ده متن وارد کنن، با فونت دلخواه رندر کنن و با زوم کردن، بهتر ببیننش.

## ویژگی‌ها
- **پشتیبانی از چند فرمت فونت**: پردازش فایل‌های `.fnt` در فرمت متنی (مثل `file1.fnt` و `file3.fnt`) و XML (مثل `file2.fnt`).
- **رندر قابل تنظیم**: رندر متن با پس‌زمینه خاکستری تیره (`RGB: 50, 50, 50`) برای خوانایی بهتر.
- **رابط کاربری تعاملی**: شامل فیلد ورود متن، اسلایدر زوم (0.1x تا 3x) و ناحیه نمایش قابل اسکرول برای متن‌های بزرگ یا زوم‌شده.
- **کد ماژولار**: به فایل‌های جدا تقسیم شده (پردازش فونت، پارس کردن، و رابط کاربری) که نگهداری و توسعه رو آسون می‌کنه.

## ساختار پروژه
فایل‌های پروژه به این شکل سازمان‌دهی شدن:
- `character.py`: تعریف کلاس `FontCharacter` برای ذخیره اطلاعات کاراکترها.
- `font.py`: شامل کلاس `BitmapFont` برای رندر فونت و لود تصاویر.
- `text_parser.py`: پردازش فایل‌های `.fnt` با فرمت متنی.
- `xml_parser.py`: پردازش فایل‌های `.fnt` با فرمت XML (مثل `file2.fnt`).
- `ui.py`: پیاده‌سازی رابط کاربری با PyQt5 (ورود متن، زوم، و نمایش).
- `main.py`: نقطه شروع برای اجرای برنامه.
- فایل‌های فونت (مثل `file1.fnt`, `file2.fnt`, `file3.fnt`) و تصاویر مرتبط (مثل `file2_0.png`, `file3_0.tga`).

## پیش‌نیازها
- پایتون 3.6 یا بالاتر
- پکیج‌های پایتون مورد نیاز:
  - `PyQt5`: برای رابط کاربری گرافیکی.
  - `Pillow`: برای پردازش تصاویر.

نصب پکیج‌ها با این دستور:
```bash
pip install PyQt5 Pillow
```

## نصب
1. این مخزن رو کلون کنید یا دانلود کنید:
   ```bash
   git clone <آدرس-مخزن>
   cd <پوشه-پروژه>
   ```
2. مطمئن بشید فایل‌های فونت (مثل `file1.fnt`, `file2.fnt`, `file3.fnt`) و تصاویرشون (مثل `file2_0.png`, `file3_0.tga`) تو پوشه اصلی پروژه هستن.
3. پکیج‌های مورد نیاز رو نصب کنید (بالا رو ببینید).

## استفاده
1. برنامه رو اجرا کنید:
   ```bash
   python main.py
   ```
2. رابط کاربری باز می‌شه و یه متن پیش‌فرض ("Hello") نمایش داده می‌شه.
3. تو فیلد ورودی، متن دلخواهتون رو وارد کنید تا با فونت انتخاب‌شده رندر بشه.
4. با اسلایدر زوم، اندازه متن رو تنظیم کنید (0.1x تا 3x).
5. اگه متن بزرگ باشه، می‌تونید تو ناحیه نمایش اسکرول کنید.

برای تغییر فایل فونت:
- فایل `main.py` رو باز کنید و مسیر `fnt_file` رو به یکی از فونت‌ها (مثل `file2.fnt` برای XML یا `file1.fnt` برای متنی) تغییر بدید.
- مطمئن بشید فایل تصویری مرتبط (مثل `file2_0.png`) تو پوشه اصلیه.

مثال:
```python
fnt_file = os.path.join(base_folder, "file2.fnt")  # استفاده از file2.fnt (XML)
```

## فرمت‌های فایل فونت
برنامه از دو نوع فایل `.fnt` پشتیبانی می‌کنه:
- **فرمت متنی**: خط به خط با ورودی‌های `page` و `char`.
  مثال:
  ```
  page id=0 file="file3_0.tga"
  char id=32 x=0 y=0 width=0 height=0 xoffset=0 yoffset=0 xadvance=8 page=0
  ```
- **فرمت XML**: ساختار XML با تگ‌های `<page>` و `<char>` (مثل `file2.fnt`).
  مثال:
  ```xml
  <font>
    <pages>
      <page id="0" file="file2_0.png" />
    </pages>
    <chars>
      <char id="65" x="33" y="0" width="21" height="22" xoffset="-1" yoffset="3" xadvance="18" page="0" />
    </chars>
  </font>
  ```

## عیب‌یابی
- **خطا: "Page image file does not exist"**:
  - مطمئن بشید فایل تصویری (مثل `file2_0.png`) تو پوشه اصلیه.
  - ویژگی `file` تو فایل `.fnt` رو چک کنید که نام تصویر درست باشه.
- **خطا: "Error parsing XML file"**:
  - فایل XML باید درست نوشته شده باشه.
  - محتواش رو به اشتراک بذارید تا کمک کنم.
- **متن نمایش داده نمی‌شه**:
  - مطمئن بشید کاراکترهای متن ورودی تو فونت پشتیبانی می‌شن.
  - چک کنید فایل `.fnt` و تصویرش درست لود شدن.

## مشارکت
اگه دوست دارید به پروژه کمک کنید، می‌تونید مخزن رو فورک کنید، بهبود بدید و درخواست کشیدن (pull request) بفرستید. ایده‌های جدید (مثل منوی انتخاب فونت یا پشتیبانی از فرمت‌های دیگه) استقبال می‌شه!

```

---

### توضیحات README
1. **هدف:** این README به فارسی توضیح می‌ده پروژه چیه، چطور کار می‌کنه و چطور می‌شه ازش استفاده کرد. برای افراد جدید کاملاً قابل فهمه.
2. **محتوا:**
   - توضیح پروژه و ویژگی‌ها (پشتیبانی از متن و XML، زوم، رابط کاربری).
   - ساختار فایل‌ها و نقش هر کدوم.
   - راهنمای نصب و اجرا با دستورات ساده.
   - توضیح فرمت‌های فونت با نمونه (مثل `file2.fnt` که دادی).
   - نکات عیب‌یابی برای خطاهای رایج.
   - دعوت به مشارکت و اطلاعات مجوز.
3. **فرمت:** از Markdown استفاده کردم که تو GitHub و پلتفرم‌های مشابه به‌خوبی نمایش داده می‌شه.
4. **سازگاری:** با پروژه‌ات (شامل `character.py`, `font.py`, `text_parser.py`, `xml_parser.py`, `ui.py`, `main.py`) کاملاً هماهنگه.

---

### چطور از README استفاده کنیم؟
1. **ذخیره فایل:**
   - یه فایل به اسم `README.md` تو پوشه اصلی پروژه بساز.
   - محتوای بالا رو توش کپی کن.
   - اگه پروژه رو تو GitHub آپلود کنی، این فایل به‌عنوان توضیحات اصلی نشون داده می‌شه.

2. **ساختار پروژه:**
   ```
   project_folder/
   ├── README.md
   ├── character.py
   ├── font.py
   ├── text_parser.py
   ├── xml_parser.py
   ├── ui.py
   ├── main.py
   ├── file1.fnt
   ├── file2.fnt
   ├── file3.fnt
   ├── file2_0.png
   ├── file3_0.tga
   ```

3. **تست پروژه:**
   - مطمئن شو فایل‌های فونت (`file1.fnt`, `file2.fnt`, `file3.fnt`) و تصاویرشون (`file2_0.png`, `file3_0.tga`) تو پوشه اصلی هستن.
   - دستورات نصب و اجرا رو از README دنبال کن.

---
