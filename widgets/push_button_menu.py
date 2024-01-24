import qtawesome as qta
from PyQt6.QtWidgets import QPushButton


class PushButtonMenu(QPushButton):
    def __init__(self, text, file_type="normal"):
        icon = qta.icon("fa5.file")
        if file_type == "alt":
            icon = qta.icon("fa5.file-alt")
        if file_type == "image":
            icon = qta.icon("fa5.file-image", color="#a86832")
        super().__init__(icon, text)
        self.filename = text

    def autopress(self, window):
        window.open_file(self.filename)
