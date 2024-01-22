import os
from functools import partial
import qtawesome as qta
from superqt import QCollapsible
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
from PyQt6.QtCore import QSize
from widgets.push_button_menu import PushButtonMenu
from utils import check_number


INVALID_FOLDER = ["env", "venv", "ENV", "env.bak", "venv.bak", "node_modules"]


class FilesMenu(QWidget):
    def __init__(self, window):
        super(QWidget, self).__init__()
        self.win = window
        self.root_folder = None
        icon_size = QSize(16, 16)
        self.icon_closed = QIcon(qta.icon("fa5s.chevron-right").pixmap(icon_size))
        self.icon_open = QIcon(qta.icon("fa5s.chevron-down").pixmap(icon_size))

        # Add things to Files Menu
        self.files_menu_layout = QVBoxLayout()
        self.setLayout(self.files_menu_layout)
        title_label_files_menu = QLabel("EXPLORER")
        line_menu = QFrame()
        line_menu.setFrameStyle(QFrame.Shape.HLine)
        line_menu.setObjectName("lineMenu")
        self.files_menu_layout.addWidget(title_label_files_menu)
        self.files_menu_layout.addWidget(line_menu)

        # Files and Folders
        self.files_menu_scroll = QScrollArea()
        self.files_menu_scroll.setWidgetResizable(True)
        self.files_menu_scroll.setStyleSheet("border: none")

        self.files_folders = QWidget()
        self.files_menu_layout.addWidget(self.files_menu_scroll)
        self.files_folders_layout = QVBoxLayout()  #
        self.files_folders_layout.setContentsMargins(0, 0, 0, 0)
        self.files_folders.setLayout(self.files_folders_layout)

    def paintEvent(self, _):  # pylint: disable=C0103
        o = QStyleOption()
        o.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, o, p, self)

    def _open_folder_recursive(self, box, folder_name, deepth=0):
        files = os.listdir(folder_name)
        files.sort()
        for file in files:
            if file.endswith(".dat"):
                normal_plot = False
                try:
                    with open(folder_name + "/" + file, encoding="utf-8") as f:
                        first_line = f.readline().split()
                        if len(first_line) == 3 and check_number(first_line[0]):
                            normal_plot = True
                except:  # pylint: disable=W0702
                    print("Unexpected error.")
                file_widget = PushButtonMenu(file, normal_plot)
                file_widget.clicked.connect(
                    partial(self.win.open_file, file_name=file, file_dir=folder_name)
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
                _box.setCollapsedIcon(self.icon_closed)
                _box.setExpandedIcon(self.icon_open)
                _box.layout().setContentsMargins(0, 0, 0, 0)
                _box.setStyleSheet("padding-left: 10px;")
                self._open_folder_recursive(_box, folder_name_rec, deepth=deepth + 1)
                box.addWidget(_box)

    def open_folder(self, folder_name):
        if not folder_name.startswith("/home"):
            self.win.outputConsole.print_output("Invalid folder.")
            return
        # Clean first
        for i in reversed(range(self.files_folders_layout.count())):
            self.files_folders_layout.itemAt(i).widget().setParent(None)

        # Add box
        self.root_folder = QCollapsible(folder_name.split("/")[-1])
        self.root_folder.setCollapsedIcon(self.icon_closed)
        self.root_folder.setExpandedIcon(self.icon_open)
        self._open_folder_recursive(self.root_folder, folder_name)
        self.files_folders_layout.addWidget(self.root_folder)
        self.files_menu_scroll.setWidget(self.files_folders)

        # Open CollapsibleBox
        self.root_folder.expand()
