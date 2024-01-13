from datetime import datetime
from PyQt6.QtWidgets import QTextBrowser


class ConsoleOutput(QTextBrowser):
    def __init__(self):
        super(QTextBrowser, self).__init__()

    def printOutput(self, line_text="Test"):
        now = datetime.now().strftime("[%H:%M:%S] ")
        if self.toPlainText() == "":
            new_text = self.toPlainText() + now + line_text
        else:
            new_text = self.toPlainText() + "\n" + now + line_text
        self.setText(new_text)
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())
