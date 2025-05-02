# font_manager.py
import os
from PyQt5.QtWidgets import QLineEdit, QPushButton, QFileDialog, QMessageBox, QHBoxLayout
from font import BitmapFont
from renderer import render_fonts
import recent_files


class FontManager:
    def __init__(self, initial_font):
        self.fonts = [initial_font]
        self.text_fields = []
        self.field_layouts = []
        self.text_fields_layout = None
        self.update_callback = None
        self.last_folder = os.path.expanduser("~")

    def add_text_field(self, parent_layout, update_callback):
        """اضافه کردن فیلد متنی با دکمه ضربدر (فقط برای فونت‌های اضافی)"""
        field_layout = QHBoxLayout()
        text_field = QLineEdit("Hello")
        text_field.textChanged.connect(update_callback)
        field_layout.addWidget(text_field)
        if len(self.text_fields) > 0:
            remove_button = QPushButton("X")
            remove_button.setFixedWidth(20)
            remove_button.clicked.connect(lambda: self.remove_font_by_field(text_field))
            field_layout.addWidget(remove_button)
        parent_layout.addLayout(field_layout)
        self.text_fields.append(text_field)
        self.field_layouts.append(field_layout)

    def load_font(self, parent_layout, update_callback, mode="add", fnt_file=None):
        """بارگذاری فونت (اضافه کردن، باز کردن، یا اخیر)"""
        if not fnt_file:
            fnt_file, _ = QFileDialog.getOpenFileName(
                None, "Select BMFont File", self.last_folder, "BMFont Files (*.fnt);;All Files (*)"
            )
        if not fnt_file:
            return
        try:
            font = BitmapFont(fnt_file, os.path.dirname(fnt_file))
            if mode == "add":
                self.fonts.append(font)
            else:  # open یا recent
                self.fonts = [font]
                self.clear_fields(parent_layout)
                self.text_fields = []
                self.field_layouts = []
            self.add_text_field(parent_layout, update_callback)
            recent_files.save_recent_file(fnt_file)
            self.last_folder = os.path.dirname(fnt_file)
            self.set_layout(parent_layout, update_callback)
            self.update_callback()
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Failed to load font: {e}")

    def add_font(self, parent_layout, update_callback):
        """اضافه کردن فونت جدید"""
        self.load_font(parent_layout, update_callback, mode="add")

    def open_font(self, parent_layout, update_callback):
        """باز کردن فونت جدید"""
        self.load_font(parent_layout, update_callback, mode="open")

    def load_recent_font(self, fnt_file, parent_layout, update_callback):
        """بارگذاری فونت از Open Recent"""
        self.load_font(parent_layout, update_callback, mode="recent", fnt_file=fnt_file)

    def remove_font_by_field(self, text_field):
        """حذف فونت و فیلد"""
        try:
            index = self.text_fields.index(text_field)
            if len(self.fonts) <= 1 or index == 0:
                return
            self.fonts.pop(index)
            self.text_fields.pop(index)
            field_layout = self.field_layouts.pop(index)
            self.text_fields_layout.removeItem(field_layout)
            for i in range(field_layout.count()):
                if widget := field_layout.itemAt(i).widget():
                    widget.deleteLater()
            field_layout.deleteLater()
            self.update_callback()
        except ValueError:
            QMessageBox.critical(None, "Error", "Failed to remove font")

    def remove_all_fonts(self):
        """حذف همه فونت‌های اضافی"""
        if len(self.fonts) <= 1:
            return
        self.fonts = [self.fonts[0]]
        self.clear_fields(self.text_fields_layout)
        self.text_fields = []
        self.field_layouts = []
        self.add_text_field(self.text_fields_layout, self.update_callback)
        self.update_callback()

    def clear_fields(self, parent_layout):
        """پاک کردن فیلدها"""
        for field_layout in self.field_layouts:
            parent_layout.removeItem(field_layout)
            while field_layout.count():
                if widget := field_layout.itemAt(0).widget():
                    widget.deleteLater()
                field_layout.removeItem(field_layout.itemAt(0))
            field_layout.deleteLater()

    def set_layout(self, layout, callback):
        """تنظیم layout و callback"""
        self.text_fields_layout = layout
        self.update_callback = callback

    def render(self, background_color, zoom_factor):
        return render_fonts(self.fonts, self.text_fields, background_color, zoom_factor)