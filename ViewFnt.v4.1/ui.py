# ui.py
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QLabel,
    QSlider,
    QScrollArea,
)
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt


class FontRendererWidget(QWidget):
    def __init__(self, font):
        super().__init__()
        self.font = font
        self.zoom_factor = 1.0
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

        scroll_area = QScrollArea(self)
        scroll_area.setWidget(self.label)
        scroll_area.setWidgetResizable(True)

        hbox = QHBoxLayout()
        zoom_label = QLabel("Zoom:")
        self.zoom_slider = QSlider(Qt.Horizontal)
        self.zoom_slider.setMinimum(10)  # 0.1x
        self.zoom_slider.setMaximum(300)  # 3x
        self.zoom_slider.setValue(100)  # 1x
        self.zoom_slider.valueChanged.connect(self.on_zoom_changed)
        hbox.addWidget(zoom_label)
        hbox.addWidget(self.zoom_slider)

        vbox.addWidget(self.line_edit)
        vbox.addLayout(hbox)
        vbox.addWidget(scroll_area)
        self.setLayout(vbox)
        self.on_text_changed(self.line_edit.text())

    def on_zoom_changed(self):
        self.zoom_factor = self.zoom_slider.value() / 100.0
        self.on_text_changed(self.line_edit.text())

    def on_text_changed(self, text):
        img = self.font.render_text(text)
        if img is None:
            self.label.clear()
            return
        data = img.tobytes("raw", "RGBA")
        qimg = QImage(data, img.width, img.height, QImage.Format_RGBA8888)
        pixmap = QPixmap.fromImage(qimg)
        scaled_pixmap = pixmap.scaled(
            int(pixmap.width() * self.zoom_factor),
            int(pixmap.height() * self.zoom_factor),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation,
        )
        self.label.setPixmap(scaled_pixmap)
        self.label.resize(scaled_pixmap.width(), scaled_pixmap.height())
