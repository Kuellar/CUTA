import qtawesome as qta
from PyQt6.QtCore import (
    QSize,
)
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QIcon


class CustomButton(QPushButton):
    IconSize = QSize(16, 16)

    def __init__(self, qta_id):
        super().__init__()

        icon = QIcon(qta.icon(qta_id).pixmap(self.IconSize))
        self.setIcon(icon)

    def set_active(self, active=True):
        if active:
            self.setStyleSheet("background-color: #6e6e6e")
        else:
            self.setStyleSheet("")
