from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt


class ImageViewer(QLabel):
    def __init__(self, filename, container):
        super().__init__()
        self.container = container
        self.setPixmap(
            QPixmap(filename).scaled(
                container.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
        )
        self.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
