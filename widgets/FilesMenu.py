import os
import qtawesome as qta
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QFrame,
    QLabel,
    QStyleOption,
    QStyle,
    QScrollArea,
)
from PyQt6.QtGui import QPainter, QIcon
from PyQt6.QtCore import (
    QSize,
)
from widgets.PushButtonMenu import PushButtonMenu
from functools import partial
from superqt import QCollapsible


INVALID_FOLDER = ["env", "venv", "ENV", "env.bak", "venv.bak", "node_modules"]


class FilesMenu(QWidget):
    def __init__(self, window):
        super(QWidget, self).__init__()
        self.win = window
        self.rootFolder = None
        self.iconSize = QSize(16, 16)
        self.iconClosed = QIcon(qta.icon("fa5s.chevron-right").pixmap(self.iconSize))
        self.iconOpen = QIcon(qta.icon("fa5s.chevron-down").pixmap(self.iconSize))

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
        self.filesMenuScroll = QScrollArea()
        self.filesMenuScroll.setWidgetResizable(True)
        self.filesMenuScroll.setStyleSheet("border: none")

        self.filesFolders = QWidget()
        self.filesMenuLayout.addWidget(self.filesMenuScroll)
        self.filesFoldersLayout = QVBoxLayout()  #
        self.filesFoldersLayout.setContentsMargins(0, 0, 0, 0)
        self.filesFolders.setLayout(self.filesFoldersLayout)

    def paintEvent(self, event):
        o = QStyleOption()
        o.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, o, p, self)

    def _open_folder_recursive(self, box, folder_name, deepth=0):
        files = os.listdir(folder_name)
        files.sort()
        for file in files:
            if file.endswith(".dat"):
                file_widget = PushButtonMenu(file)
                file_widget.clicked.connect(
                    partial(self.win.openFile, file_name=file, file_dir=folder_name)
                )
                box.addWidget(file_widget)

            if (
                os.path.isdir(folder_name + "/" + file)
                and not "." in file
                and file not in INVALID_FOLDER
                and not "cache" in file
                and deepth < 4
            ):
                folder_name_rec = folder_name + "/" + file
                _box = QCollapsible(file)
                _box.setCollapsedIcon(self.iconClosed)
                _box.setExpandedIcon(self.iconOpen)
                _box.layout().setContentsMargins(0, 0, 0, 0)
                _box.setStyleSheet("padding-left: 10px;")
                self._open_folder_recursive(_box, folder_name_rec, deepth=deepth + 1)
                box.addWidget(_box)

    def open_folder(self, folder_name):
        if not folder_name.startswith("/home"):
            self.win.outputConsole.printOutput(f"Invalid folder.")
            return
        # Clean first
        for i in reversed(range(self.filesFoldersLayout.count())):
            self.filesFoldersLayout.itemAt(i).widget().setParent(None)

        # Add box
        self.rootFolder = QCollapsible(folder_name.split("/")[-1])
        self.rootFolder.setCollapsedIcon(self.iconClosed)
        self.rootFolder.setExpandedIcon(self.iconOpen)
        self._open_folder_recursive(self.rootFolder, folder_name)
        self.filesFoldersLayout.addWidget(self.rootFolder)
        self.filesMenuScroll.setWidget(self.filesFolders)

        # Open CollapsibleBox
        self.rootFolder.expand()
