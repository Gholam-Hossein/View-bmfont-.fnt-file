# main.py
import sys
import os
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox
from font import BitmapFont
from ui import FontRendererWidget


if __name__ == "__main__":
    app = QApplication(sys.argv)

    if len(sys.argv) < 2:
        fnt_file, _ = QFileDialog.getOpenFileName(
            None,
            "Select BMFont File",
            os.path.expanduser("~"),
            "BMFont Files (*.fnt);;All Files (*)"
        )
        if not fnt_file:
            sys.exit(0)
    else:
        fnt_file = sys.argv[1]

    if not os.path.isfile(fnt_file):
        QMessageBox.critical(None, "Error", f"File '{fnt_file}' does not exist.")
        sys.exit(1)

    images_folder = os.path.dirname(fnt_file)
    try:
        font = BitmapFont(fnt_file, images_folder)
        viewer = FontRendererWidget(font)
        viewer.show()
        app.exec_()  # بدون sys.exit برای ادامه در صورت خطا
    except Exception as e:
        QMessageBox.critical(None, "Error", f"Failed to load font: {e}")