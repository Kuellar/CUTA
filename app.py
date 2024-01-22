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
from utils import open_data
from data import Points, PlotPoints, PlotHorizo, Plot


class Window(QMainWindow):
    def __init__(self):
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

        # Create layout -> TODO: organize
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
        canvas_workspace = QWidget()
        self.controls = QWidget()
        self.canvas_plot = MplCanvas(self, width=10, height=8, dpi=100)
        canvas_workspace_layout = QHBoxLayout()
        self.canvas_workspace_layout_splitter = QSplitter()
        canvas_workspace.setLayout(canvas_workspace_layout)
        self.canvas_plot_grid = QWidget()
        canvas_plot_grid_layout = QGridLayout()
        canvas_plot_grid_layout.setContentsMargins(0, 0, 10, 0)
        self.canvas_plot_grid.setLayout(canvas_plot_grid_layout)
        self.canvas_plot_left_slider = SliderZoom(horizontal=False)
        self.canvas_plot_bottom_slider = SliderZoom(horizontal=True)
        self.canvas_plot_bottom_slider.setMaximumHeight(40)
        canvas_plot_null = QWidget()
        canvas_plot_grid_layout.addWidget(self.canvas_plot_left_slider, 0, 0, 1, 1)
        canvas_plot_grid_layout.addWidget(self.canvas_plot_bottom_slider, 1, 1, 1, 1)
        canvas_plot_grid_layout.addWidget(canvas_plot_null, 1, 0, 1, 1)
        self.canvas_workspace_layout_splitter.addWidget(self.canvas_plot_grid)
        self.canvas_workspace_layout_splitter.addWidget(self.controls)
        canvas_plot_grid_layout.addWidget(self.canvas_plot, 0, 1, 1, 1)
        canvas_workspace_layout.addWidget(self.canvas_workspace_layout_splitter)
        content_layout_splitter.addWidget(canvas_workspace)
        self.output_console = ConsoleOutput()
        content_layout_splitter.addWidget(self.output_console)
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

        if isinstance(plot_data, PlotPoints):
            self.plot_points = plot_data
            self.output_console.print_output(
                f"{len(self.plot_points.points.x)} data points."
            )

        if isinstance(plot_data, PlotHorizo):
            self.plot_horizo = plot_data
            self.add_vertical_settings()
            self.output_console.print_output(
                f"{len(self.plot_horizo.names)} functions."
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
        self.controls_layout.insertWidget(3, mpl_plot_vertical)


if __name__ == "__main__":
    app = QApplication([])
    win = Window()
    css_path = (Path(__file__).parent / "./ui/style.css").resolve()
    with open(css_path, "r", encoding="utf-8") as fh:
        app.setStyleSheet(fh.read())
    win.show()
    sys.exit(app.exec())
