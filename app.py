import sys
from os.path import expanduser
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QMainWindow,
    QMenu,
    QFileDialog,
)
from PyQt6.QtGui import QAction
from widgets.MplSettingsLayout import MplSettingsLayout
from widgets.ConsoleOutput import ConsoleOutput
from widgets.FilesMenu import FilesMenu
from widgets.MplCanvas import MplCanvas
from widgets.CollapsibleBox import CollapsibleBox
from utils import open_data, open_folder


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CUTA")

        # Global vars
        self.lastDirOpen = None

        self._createActions()
        self._createMenuBar()

        # Create layout -> TODO: organize
        mainLayout = QHBoxLayout()
        self.filesMenu = FilesMenu()
        mainLayout.addWidget(self.filesMenu)
        self.widgetContent = QWidget()
        self.contentLayout = QVBoxLayout()
        self.widgetContent.setLayout(self.contentLayout)
        mainLayout.addWidget(self.widgetContent)
        self.canvasWorkspace = QWidget()
        self.controls = QWidget()
        self.canvasWorkspaceLayout = QHBoxLayout()
        self.canvasWorkspace.setLayout(self.canvasWorkspaceLayout)
        self.canvasPlot = MplCanvas(self, width=10, height=8, dpi=100)
        self.canvasWorkspaceLayout.addWidget(self.canvasPlot)
        self.canvasWorkspaceLayout.addWidget(self.controls)
        self.contentLayout.addWidget(self.canvasWorkspace)
        self.outputConsole = ConsoleOutput()
        self.contentLayout.addWidget(self.outputConsole)

        # Add things to Controls
        self.controlsLayout = QVBoxLayout()
        self.controls.setLayout(self.controlsLayout)
        self.controls.setObjectName("controls")
        self.mplSettingsBox = CollapsibleBox("Matplotlib Settings")
        self.mplSettingsLayout = MplSettingsLayout(self, self.canvasPlot)
        self.controlsLayout.addWidget(self.mplSettingsBox)
        self.mplSettingsBox.setContentLayout(self.mplSettingsLayout)

        self.controlsLayout.addStretch()

        # Create main widget and assign layout
        widget = QWidget()
        widget.setLayout(mainLayout)
        self.setCentralWidget(widget)

        # Plot
        self.xdata = [0, 1, 2, 3]
        self.ydata = [0, 1, 2, 3]
        self.zdata = [0, 0.1, 0, 0]
        self.canvasPlot.update_plot(
            self.xdata, self.ydata, self.zdata, self.mplSettingsLayout
        )
        self.show()

    def _createMenuBar(self):
        menuBar = self.menuBar()
        # File Menu
        fileMenu = QMenu("&File", self)
        menuBar.addMenu(fileMenu)
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.openFolderAction)
        # View Menu
        viewMenu = QMenu("&View", self)
        menuBar.addMenu(viewMenu)
        viewMenu.addAction(self.consoleAction)
        # Help Menu
        helpMenu = menuBar.addMenu("&Help")

    def _createActions(self):
        self.openAction = QAction("&Open File...", self)
        self.openAction.triggered.connect(self.openFileDialog)
        self.openFolderAction = QAction("&Open Folder...", self)
        self.openFolderAction.triggered.connect(self.openFolderDialog)
        self.consoleAction = QAction("&Console", self)
        self.consoleAction.triggered.connect(
            lambda: self.outputConsole.show()
            if self.outputConsole.isHidden()
            else self.outputConsole.hide()
        )

    def openFileDialog(self):
        file_name = QFileDialog.getOpenFileName(
            self,
            "Open File",
            self.lastDirOpen if self.lastDirOpen else expanduser("~"),
            "dat (*.dat)",
        )
        if file_name[0]:
            file_name_open = file_name[0].split("/")[-1]
            file_dir_open = "/".join(file_name[0].split("/")[:-1])
            self.openFile(file_name=file_name_open, file_dir=file_dir_open)

    def openFile(self, file_name=None, file_dir=None):
        file_to_open = (file_dir if file_dir else self.lastDirOpen) + "/" + file_name
        self.outputConsole.printOutput("Opening File " + file_to_open)
        if file_dir:
            self.lastDirOpen = file_dir
        self.xdata, self.ydata, self.zdata, error = open_data(self, file_to_open)
        if error:
            self.outputConsole.printOutput(error["msg"])
        self.outputConsole.printOutput(f"{len(self.xdata)} data points")
        self.canvasPlot.update_plot(
            self.xdata, self.ydata, self.zdata, self.mplSettingsLayout
        )

    def openFolderDialog(self):
        folder_name = QFileDialog.getExistingDirectory(
            self,
            "Open Directory",
            self.lastDirOpen if self.lastDirOpen else expanduser("~"),
            options=QFileDialog.Option.ShowDirsOnly,
        )
        if folder_name:
            self.lastDirOpen = folder_name
            self.outputConsole.printOutput("Opening Folder " + folder_name)
            _ = open_folder(self, folder_name)


if __name__ == "__main__":
    app = QApplication([])
    win = Window()
    with open("./ui/style.css", "r") as fh:
        app.setStyleSheet(fh.read())
    win.show()
    sys.exit(app.exec())
