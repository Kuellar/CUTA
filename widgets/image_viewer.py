from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt


class ImageViewer(QLabel):
    def __init__(self, filename):
        super().__init__()
        self.setPixmap(QPixmap(filename))
        self.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
