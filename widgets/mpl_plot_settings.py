from PyQt6.QtWidgets import (
    QWidget,
    QFormLayout,
    QCheckBox,
    QComboBox,
    QVBoxLayout,
    QApplication,
)
from widgets.collapsible_box import CollapsibleBox


class MplPlotSettings(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        box = CollapsibleBox("Plot Settings")
        layout.addWidget(box)
        box_layout = QFormLayout()

        # COLOR
        self.plot_color_mpl = QComboBox()
        self.plot_color_mpl.addItems(
            ["blue", "green", "red", "cyan", "magenta", "yellow", "black", "white"]
        )
        self.plot_color_mpl.currentTextChanged.connect(self.change_color)
        box_layout.addRow("Plot Color:", self.plot_color_mpl)

        # Line Style
        self.plot_line_mpl = QComboBox()
        self.plot_line_mpl.addItems(["-", "--", "-.", ":"])
        self.plot_line_mpl.currentTextChanged.connect(self.change_plot_line)
        box_layout.addRow("Line Style:", self.plot_line_mpl)

        # Marker
        self.plot_marker_mpl = QComboBox()
        self.plot_marker_mpl.addItems(["", ".", "o", "s", "p", "*", "x", "|"])
        self.plot_marker_mpl.currentTextChanged.connect(self.change_marker)
        box_layout.addRow("Marker:", self.plot_marker_mpl)

        # Marker Color
        self.plot_marker_color_mpl = QComboBox()
        self.plot_marker_color_mpl.addItems(
            ["blue", "green", "red", "cyan", "magenta", "yellow", "black", "white"]
        )
        self.plot_marker_color_mpl.currentTextChanged.connect(self.change_marker_color)
        box_layout.addRow("Marker Color:", self.plot_marker_color_mpl)

        # Error
        self.show_error_mpl = QCheckBox()
        self.show_error_mpl.stateChanged.connect(self.show_error)
        box_layout.addRow("Show Error:", self.show_error_mpl)

        # Error Color
        self.error_color_mpl = QComboBox()
        self.error_color_mpl.addItems(
            ["blue", "green", "red", "cyan", "magenta", "yellow", "black", "white"]
        )
        self.error_color_mpl.currentTextChanged.connect(self.change_error_color)
        box_layout.addRow("Error Color:", self.error_color_mpl)

        # Draw Style
        self.draw_style_mpl = QComboBox()
        self.draw_style_mpl.addItems(
            ["default", "steps", "steps-pre", "steps-mid", "steps-post"]
        )
        self.draw_style_mpl.currentTextChanged.connect(self.change_draw_style)
        box_layout.addRow("Draw Style:", self.draw_style_mpl)

        box.setContentLayout(box_layout)

    def change_color(self, new_color):
        app = QApplication.activeWindow()
        app.plot_points.set_color(new_color)
        app.canvas_plot.update_plot()

    def change_plot_line(self, new_plot_line):
        app = QApplication.activeWindow()
        app.plot_points.set_plot_line(new_plot_line)
        app.canvas_plot.update_plot()

    def change_marker(self, new_marker):
        app = QApplication.activeWindow()
        app.plot_points.set_marker(new_marker)
        app.canvas_plot.update_plot()

    def change_marker_color(self, new_marker_color):
        app = QApplication.activeWindow()
        app.plot_points.set_marker_color(new_marker_color)
        app.canvas_plot.update_plot()

    def show_error(self, flag):
        app = QApplication.activeWindow()
        app.plot_points.set_show_error(True if flag else False)
        app.canvas_plot.update_plot()

    def change_error_color(self, new_error_color):
        app = QApplication.activeWindow()
        app.plot_points.set_error_color(new_error_color)
        app.canvas_plot.update_plot()

    def change_draw_style(self, new_draw_style):
        app = QApplication.activeWindow()
        app.plot_points.set_drawstyle(new_draw_style)
        app.canvas_plot.update_plot()
