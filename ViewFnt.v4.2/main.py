# main.py
import sys
import os
from PyQt5.QtWidgets import QApplication, QFileDialog
from font import BitmapFont
from ui import FontRendererWidget  # فعلاً فرض می‌کنم ViewFnt همونه، اگه فرق داره بگو


if __name__ == "__main__":
    app = QApplication(sys.argv)

    if len(sys.argv) < 2:
        # دیالوگ انتخاب فایل با دایرکتوری پیش‌فرض و فیلتر
        fnt_file, _ = QFileDialog.getOpenFileName(
            None,
            "Select BMFont File",
            os.path.expanduser("~"),  # دایرکتوری خانگی کاربر
            "BMFont Files (*.fnt);;All Files (*)"
        )
        if not fnt_file:
            sys.exit(0)
    else:
        fnt_file = sys.argv[1]

    # بررسی وجود فایل
    if not os.path.isfile(fnt_file):
        print(f"Error: File '{fnt_file}' does not exist.")
        sys.exit(1)

    # تنظیم images_folder به دایرکتوری فایل .fnt
    images_folder = os.path.dirname(fnt_file)

    try:
        font = BitmapFont(fnt_file, images_folder)
        viewer = FontRendererWidget(font)  # اگه ViewFnt کلاس جدیده، اینجا جایگزین کن
        viewer.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Error loading font: {e}")
        sys.exit(1)