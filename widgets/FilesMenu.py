from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFrame, QLabel, QStyleOption, QStyle
from PyQt6.QtGui import QPainter


class FilesMenu(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()
        # Add things to Files Menu
        self.filesMenuLayout = QVBoxLayout()
        self.setLayout(self.filesMenuLayout)
        titleLabelFilesMenu = QLabel("EXPLORER")
        lineMenu = QFrame()
        lineMenu.setFrameStyle(QFrame.Shape.HLine)
        lineMenu.setObjectName("lineMenu")
        self.filesMenuLayout.addWidget(titleLabelFilesMenu)
        self.filesMenuLayout.addWidget(lineMenu)

        # Files and Folders
        self.filesFolders = QWidget()
        self.filesMenuLayout.addWidget(self.filesFolders)
        self.filesFoldersLayout = QVBoxLayout()
        self.filesFolders.setLayout(self.filesFoldersLayout)
        self.filesMenuLayout.addStretch()

    def paintEvent(self, event):
        o = QStyleOption()
        o.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, o, p, self)
