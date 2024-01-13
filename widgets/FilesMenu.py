from PyQt6.QtWidgets import QWidget, QVBoxLayout, QFrame, QLabel


class FilesMenu(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()

        # Add things to Files Menu
        self.filesMenuLayout = QVBoxLayout()
        self.setLayout(self.filesMenuLayout)
        self.setObjectName("widgetFilesMenu")
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
