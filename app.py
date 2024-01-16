import sys
from numpy.random import randint
from os.path import expanduser
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QMainWindow,
    QMenu,
    QFileDialog,
    QSplitter,
    QGridLayout,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from widgets.MplSettingsLayout import MplSettingsLayout
from widgets.MplPlotSettingsLayout import MplPlotSettingsLayout
from widgets.ButtonsSettings import ButtonsSettings
from widgets.ConsoleOutput import ConsoleOutput
from widgets.FilesMenu import FilesMenu
from widgets.MplCanvas import MplCanvas
from widgets.CollapsibleBox import CollapsibleBox
from widgets.SliderZoom import SliderZoom
from utils import open_data, open_folder


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CUTA")

        # Global vars
        self.lastDirOpen = None
        self.lastFileOpen = None

        self._createActions()
        self._createMenuBar()

        # Create layout -> TODO: organize
        mainLayout = QHBoxLayout()
        self.mainLayoutSplitter = QSplitter()
        self.filesMenu = FilesMenu()
        self.mainLayoutSplitter.addWidget(self.filesMenu)
        self.widgetContent = QWidget()
        self.contentLayout = QVBoxLayout()
        self.contentLayoutSplitter = QSplitter(Qt.Vertical)
        self.widgetContent.setLayout(self.contentLayout)
        self.mainLayoutSplitter.addWidget(self.widgetContent)
        mainLayout.addWidget(self.mainLayoutSplitter)
        self.canvasWorkspace = QWidget()
        self.controls = QWidget()
        self.canvasPlot = MplCanvas(self, width=10, height=8, dpi=100)
        self.canvasWorkspaceLayout = QHBoxLayout()
        self.canvasWorkspaceLayoutSplitter = QSplitter()
        self.canvasWorkspace.setLayout(self.canvasWorkspaceLayout)
        self.canvasPlotGrid = QWidget()
        self.canvasPlotGridLayout = QGridLayout()
        self.canvasPlotGrid.setLayout(self.canvasPlotGridLayout)
        self.canvasPlotLeftSlider = SliderZoom(
            horizontal=False, mplCanvas=self.canvasPlot
        )
        self.canvasPlotBottomSlider = SliderZoom(
            horizontal=True, mplCanvas=self.canvasPlot
        )
        self.canvasPlotBottomSlider.setMaximumHeight(40)  # TODO: FIX
        self.canvasPlotNull = QWidget()
        self.canvasPlotGridLayout.addWidget(self.canvasPlotLeftSlider, 0, 0, 1, 1)
        self.canvasPlotGridLayout.addWidget(self.canvasPlotBottomSlider, 1, 1, 1, 1)
        self.canvasPlotGridLayout.addWidget(self.canvasPlotNull, 1, 0, 1, 1)
        self.canvasWorkspaceLayoutSplitter.addWidget(self.canvasPlotGrid)
        self.canvasWorkspaceLayoutSplitter.addWidget(self.controls)
        self.canvasPlotGridLayout.addWidget(self.canvasPlot, 0, 1, 1, 1)
        self.canvasWorkspaceLayout.addWidget(self.canvasWorkspaceLayoutSplitter)
        self.contentLayoutSplitter.addWidget(self.canvasWorkspace)
        self.outputConsole = ConsoleOutput()
        self.contentLayoutSplitter.addWidget(self.outputConsole)
        self.contentLayout.addWidget(self.contentLayoutSplitter)

        # Add things to Controls
        self.controlsLayout = QVBoxLayout()
        self.controls.setLayout(self.controlsLayout)
        self.controlsLayout.setContentsMargins(0, 0, 0, 0)
        self.controls.setObjectName("controls")
        # Buttons Settings
        self.buttonSettings = ButtonsSettings(self)
        self.controlsLayout.addWidget(self.buttonSettings)
        # Global Settings
        self.mplSettingsBox = CollapsibleBox("Global Settings")
        self.mplSettingsLayout = MplSettingsLayout(self.canvasPlot)
        self.controlsLayout.addWidget(self.mplSettingsBox)
        self.mplSettingsBox.setContentLayout(self.mplSettingsLayout)
        # Plot Setting
        self.mplPlotSettingsBox = CollapsibleBox("Plot Settings")
        self.mplPlotSettingsLayout = MplPlotSettingsLayout(
            self, self.canvasPlot, self.mplSettingsLayout
        )
        self.controlsLayout.addWidget(self.mplPlotSettingsBox)
        self.mplPlotSettingsBox.setContentLayout(self.mplPlotSettingsLayout)

        self.controlsLayout.addStretch()

        # Create main widget and assign layout
        widget = QWidget()
        widget.setLayout(mainLayout)
        self.setCentralWidget(widget)

        # Plot
        self.xdata = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.ydata = randint(0, 10, 10)
        self.zdata = [0, 0.1, 0, 0, 0.3, 0.2, 0, 0, 0.5, 0]
        self.canvasPlot.update_plot(
            self.xdata,
            self.ydata,
            self.zdata,
            self.mplSettingsLayout,
            self.mplPlotSettingsLayout,
            [0 - 9 * 5 / 100, 9 + 9 * 5 / 100],  #  Give 5% more
            [
                self.ydata.min() - (self.ydata.max() - self.ydata.min()) * 5 / 100,
                self.ydata.max() + (self.ydata.max() - self.ydata.min()) * 5 / 100,
            ],
        )
        self.show()

        # Save splitter values
        self.ratioPlotSettings = self.canvasWorkspaceLayoutSplitter.sizes()
        self.canvasPlotGridHeight = self.canvasPlotGrid.frameGeometry().height()

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
        self.xdata, self.ydata, self.zdata, self.xlimit, self.ylimit, error = open_data(
            self, file_to_open
        )
        if error:
            self.outputConsole.printOutput(error["msg"])
        self.outputConsole.printOutput(f"{len(self.xdata)} data points")
        self.canvasPlot.update_plot(
            self.xdata,
            self.ydata,
            self.zdata,
            self.mplSettingsLayout,
            self.mplPlotSettingsLayout,
            self.xlimit,
            self.ylimit,
        )
        self.lastFileOpen = file_to_open

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
