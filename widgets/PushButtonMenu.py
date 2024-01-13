import qtawesome as qta
from PyQt6.QtWidgets import QPushButton


class PushButtonMenu(QPushButton):
    def __init__(self, text):
        super(QPushButton, self).__init__(qta.icon("fa.file"), text)  #  Fix with css...
        self.filename = text

    def autopress(self, window):
        window.openFile(self.filename)
