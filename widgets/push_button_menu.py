import qtawesome as qta
from PyQt6.QtWidgets import QPushButton


class PushButtonMenu(QPushButton):
    def __init__(self, text, normal=False):
        icon = qta.icon("fa5.file")
        if not normal:
            icon = qta.icon("fa5.file-alt")
        super().__init__(icon, text)
        self.filename = text

    def autopress(self, window):
        window.open_file(self.filename)
