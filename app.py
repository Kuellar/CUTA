import sys
from os.path import expanduser
from pathlib import Path
from numpy.random import randint
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
    QTabWidget,
    QTabBar,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from widgets.mpl_settings import MplSettings
from widgets.mpl_plot_settings import MplPlotSettings
from widgets.buttons_settings import ButtonsSettings
from widgets.console_output import ConsoleOutput
from widgets.files_menu import FilesMenu
from widgets.mpl_canvas import MplCanvas
from widgets.slider_zoom import SliderZoom
from widgets.mpl_plot_vertical import MplPlotVertical
from widgets.image_viewer import ImageViewer
from widgets.cut_button import CutButton
from utils import open_data
from data import Points, PlotPoints, PlotHorizo, Plot


class Window(QMainWindow):  # pylint: disable=R0902
    def __init__(self):  # pylint: disable=R0915
        super().__init__()
        self.setWindowTitle("CUTA")

        # Global vars
        self.last_dir_open = None
        self.last_file_open = None
        self.plot = Plot()
        self.plot_points = None
        self.plot_horizo = PlotHorizo(names=[], x=[])

        self._create_actions()
        self._create_menu_bar()

        # Create layout
        main_layout = QHBoxLayout()
        main_layout_splitter = QSplitter()
        self.files_menu = FilesMenu(self)
        main_layout_splitter.addWidget(self.files_menu)
        widget_content = QWidget()
        content_layout = QVBoxLayout()
        content_layout_splitter = QSplitter(Qt.Vertical)
        widget_content.setLayout(content_layout)
        main_layout_splitter.addWidget(widget_content)
        main_layout.addWidget(main_layout_splitter)

        # Workspace (plot + controls)
        canvas_workspace = QWidget()
        self.controls = QWidget()
        canvas_workspace_layout = QHBoxLayout()
        canvas_workspace_layout.setContentsMargins(0, 0, 0, 0)
        self.canvas_workspace_layout_splitter = QSplitter()
        canvas_workspace.setLayout(canvas_workspace_layout)

        # Canvas plot (with tabs)
        self.tabs = QTabWidget(movable=False, tabsClosable=True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.canvas_plot = MplCanvas(self, width=10, height=8, dpi=100)
        self.canvas_plot_grid = QWidget()
        canvas_plot_grid_layout = QGridLayout()
        canvas_plot_grid_layout.setContentsMargins(0, 10, 10, 0)
        self.canvas_plot_grid.setLayout(canvas_plot_grid_layout)
        self.canvas_plot_left_slider = SliderZoom(horizontal=False)
        self.canvas_plot_bottom_slider = SliderZoom(horizontal=True)
        self.canvas_plot_bottom_slider.setMaximumHeight(40)
        canvas_plot_cut_button = CutButton()
        canvas_plot_cut_button.setObjectName("cut_button")
        canvas_plot_grid_layout.addWidget(self.canvas_plot_left_slider, 0, 0, 1, 1)
        canvas_plot_grid_layout.addWidget(self.canvas_plot_bottom_slider, 1, 1, 1, 1)
        canvas_plot_grid_layout.addWidget(canvas_plot_cut_button, 1, 0, 1, 1)
        canvas_plot_grid_layout.addWidget(self.canvas_plot, 0, 1, 1, 1)
        self.tabs.addTab(self.canvas_plot_grid, "Matplotlib")
        self.tabs.tabBar().setTabButton(0, QTabBar.RightSide, None)

        # Splitter Canvas and Settings
        self.canvas_workspace_layout_splitter.addWidget(self.tabs)
        self.canvas_workspace_layout_splitter.addWidget(self.controls)

        # Canvas Controls
        canvas_workspace_layout.addWidget(self.canvas_workspace_layout_splitter)
        content_layout_splitter.addWidget(canvas_workspace)
        content_layout.addWidget(content_layout_splitter)
        # Add things to Controls
        self.controls_layout = QVBoxLayout()
        self.controls.setLayout(self.controls_layout)
        self.controls_layout.setContentsMargins(1, 0, 1, 0)
        self.controls.setObjectName("controls")
        # Buttons Settings
        self.button_settings = ButtonsSettings()
        self.controls_layout.addWidget(self.button_settings)
        # Global Settings
        self.mpl_settings = MplSettings()
        self.controls_layout.addWidget(self.mpl_settings)
        # Plot Setting
        self.mpl_plot_settings = MplPlotSettings()
        self.controls_layout.addWidget(self.mpl_plot_settings)

        self.controls_layout.addStretch()

        # Console output (after canvas plot)
        self.output_console = ConsoleOutput()
        content_layout_splitter.addWidget(self.output_console)

        # Create main widget and assign layout
        widget = QWidget()
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)

        # Plot
        xdata = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        ydata = randint(0, 10, 10)
        errordata = [0, 0.1, 0, 0, 0.3, 0.2, 0, 0, 0.5, 0]
        self.plot_points = PlotPoints("Start Plot", Points(xdata, ydata, errordata))

        self.canvas_plot.init_plot(self.plot_points)
        self.show()

        # Save splitter values
        self.ratio_plot_settings = self.canvas_workspace_layout_splitter.sizes()
        self.canvas_plot_grid_height = self.canvas_plot_grid.frameGeometry().height()

    def _create_menu_bar(self):
        menu_bar = self.menuBar()
        # File Menu
        file_menu = QMenu("&File", self)
        menu_bar.addMenu(file_menu)
        file_menu.addAction(self.open_action)
        file_menu.addAction(self.open_folder_action)
        # View Menu
        view_menu = QMenu("&View", self)
        menu_bar.addMenu(view_menu)
        view_menu.addAction(self.console_action)
        # Help Menu
        _ = menu_bar.addMenu("&Help")

    def _create_actions(self):
        self.open_action = QAction("&Open File...", self)
        self.open_action.triggered.connect(self.open_file_dialog)
        self.open_folder_action = QAction("&Open Folder...", self)
        self.open_folder_action.triggered.connect(self.open_folder_dialog)
        self.console_action = QAction("&Console", self)
        self.console_action.triggered.connect(
            lambda: self.output_console.show()
            if self.output_console.isHidden()
            else self.output_console.hide()
        )

    def open_file_dialog(self):
        file_name = QFileDialog.getOpenFileName(
            self,
            "Open File",
            self.last_dir_open if self.last_dir_open else expanduser("~"),
            "dat (*.dat)",
        )
        if file_name[0]:
            file_name_open = file_name[0].split("/")[-1]
            file_dir_open = "/".join(file_name[0].split("/")[:-1])
            self.open_file(file_name=file_name_open, file_dir=file_dir_open)

    def open_file(self, file_name=None, file_dir=None):
        file_to_open = (file_dir if file_dir else self.last_dir_open) + "/" + file_name
        self.output_console.print_output("Opening File " + file_to_open)
        if file_dir:
            self.last_dir_open = file_dir
        plot_data, error = open_data(self, file_to_open)

        if error:
            self.output_console.print_output(error["msg"])

        mpl_plot_vertical = self.findChild(MplPlotVertical, "mpl_plot_vertical")

        if isinstance(plot_data, PlotPoints):
            self.plot_points = plot_data
            self.output_console.print_output(
                f"{len(self.plot_points.points.x)} data points."
            )

        if isinstance(plot_data, PlotHorizo):
            self.plot_horizo = plot_data
            mpl_plot_vertical = self.findChild(MplPlotVertical, "mpl_plot_vertical")
            if not mpl_plot_vertical:
                self.add_vertical_settings()
                mpl_plot_vertical = self.findChild(MplPlotVertical, "mpl_plot_vertical")

            self.output_console.print_output(
                f"{len(self.plot_horizo.names)} functions."
            )

        if mpl_plot_vertical:
            mpl_plot_vertical.set_new_file(
                filename=self.plot_horizo.filename.split("/")[-1]
            )

        self.canvas_plot.update_plot()
        self.last_file_open = file_to_open

    def open_folder_dialog(self):
        folder_name = QFileDialog.getExistingDirectory(
            self,
            "Open Directory",
            self.last_dir_open if self.last_dir_open else expanduser("~"),
            options=QFileDialog.Option.ShowDirsOnly,
        )
        if folder_name:
            self.last_dir_open = folder_name
            self.output_console.print_output("Opening Folder " + folder_name)
            self.files_menu.open_folder(folder_name)

    def add_vertical_settings(self):
        # Plot Vertical Lines
        mpl_plot_vertical = MplPlotVertical()
        mpl_plot_vertical.setObjectName("mpl_plot_vertical")
        self.controls_layout.insertWidget(3, mpl_plot_vertical)

    def open_image(self, file_name):
        image = ImageViewer(file_name)
        self.tabs.addTab(image, file_name.split("/")[-1])
        self.tabs.setCurrentIndex(self.tabs.count() - 1)

    def close_tab(self, idx):
        self.tabs.removeTab(idx)

    def reload_files(self):
        self.files_menu.open_folder(self.last_dir_open)


if __name__ == "__main__":
    app = QApplication([])
    win = Window()
    css_path = (Path(__file__).parent / "./ui/style.css").resolve()
    with open(css_path, "r", encoding="utf-8") as fh:
        app.setStyleSheet(fh.read())
    win.show()
    sys.exit(app.exec())
