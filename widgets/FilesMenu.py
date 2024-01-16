import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFrame, QLabel, QStyleOption, QStyle
from PyQt6.QtGui import QPainter
from widgets.IconLabel import IconLabel
from widgets.PushButtonMenu import PushButtonMenu
from widgets.CollapsibleBox import CollapsibleBox
from functools import partial


class FilesMenu(QWidget):
    def __init__(self, window):
        super(QWidget, self).__init__()
        self.win = window
        self.rootFolder = None
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
        self.filesFoldersLayout.setContentsMargins(0, 0, 0, 0)
        self.filesFolders.setLayout(self.filesFoldersLayout)
        self.filesMenuLayout.addStretch()

    def paintEvent(self, event):
        o = QStyleOption()
        o.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, o, p, self)

    def open_folder(self, folder_name):
        # Clean first
        for i in reversed(range(self.filesFoldersLayout.count())):
            self.filesFoldersLayout.itemAt(i).widget().setParent(None)

        # Add title
        self.rootFolder = CollapsibleBox(folder_name.split("/")[-1])
        rootFolderLayout = QVBoxLayout()
        files = os.listdir(folder_name)
        files.sort()
        for file in files:
            if file.endswith(".dat"):
                file_widget = PushButtonMenu(file)
                file_widget.clicked.connect(partial(self.win.openFile, file_name=file))
                rootFolderLayout.addWidget(file_widget)

        self.filesFoldersLayout.addWidget(self.rootFolder)
        self.rootFolder.setContentLayout(rootFolderLayout)

        # Open CollapsibleBox
        self.rootFolder.toggle_button.pressed.emit()
        self.rootFolder.toggle_button.setChecked(True)
