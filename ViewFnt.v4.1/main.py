# main.py
import sys
import os
from PyQt5.QtWidgets import QApplication
from font import BitmapFont
from ui import FontRendererWidget


if __name__ == "__main__":
    app = QApplication(sys.argv)
    base_folder = "./"
    # فایل فونت مورد نظر رو انتخاب کن
    fnt_file = os.path.join(base_folder, "file3.fnt")  # مثلاً file2.fnt که XMLه
    images_folder = base_folder

    font = BitmapFont(fnt_file, images_folder)
    window = FontRendererWidget(font)
    window.show()

    sys.exit(app.exec_())
