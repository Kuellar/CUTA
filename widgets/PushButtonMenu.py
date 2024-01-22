import qtawesome as qta
from PyQt6.QtWidgets import QPushButton


class PushButtonMenu(QPushButton):
    def __init__(self, text, normal=False):
        icon = qta.icon("fa5.file")
        if not normal:
            icon = qta.icon("fa5.file-alt")
        super(QPushButton, self).__init__(icon, text)  #  Fix with css...
        self.filename = text

    def autopress(self, window):
        window.openFile(self.filename)
