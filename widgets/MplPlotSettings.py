from PyQt6.QtWidgets import (
    QWidget,
    QFormLayout,
    QCheckBox,
    QComboBox,
    QVBoxLayout,
    QApplication,
)
from widgets.CollapsibleBox import CollapsibleBox


class MplPlotSettings(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        box = CollapsibleBox("Plot Settings")
        layout.addWidget(box)
        boxLayout = QFormLayout()

        # COLOR
        self.plotColorMpl = QComboBox()
        self.plotColorMpl.addItems(
            ["blue", "green", "red", "cyan", "magenta", "yellow", "black", "white"]
        )
        self.plotColorMpl.currentTextChanged.connect(
            lambda x: self.change_color(x)
        )
        boxLayout.addRow("Plot Color:", self.plotColorMpl)

        # Line Style
        self.plotLineMpl = QComboBox()
        self.plotLineMpl.addItems(["-", "--", "-.", ":"])
        self.plotLineMpl.currentTextChanged.connect(
            lambda x: self.change_plot_line(x)
        )
        boxLayout.addRow("Line Style:", self.plotLineMpl)

        # Marker
        self.plotMarkerMpl = QComboBox()
        self.plotMarkerMpl.addItems(["", ".", "o", "s", "p", "*", "x", "|"])
        self.plotMarkerMpl.currentTextChanged.connect(
            lambda x: self.change_marker(x)
        )
        boxLayout.addRow("Marker:", self.plotMarkerMpl)

        # Marker Color
        self.plotMarkerColorMpl = QComboBox()
        self.plotMarkerColorMpl.addItems(
            ["blue", "green", "red", "cyan", "magenta", "yellow", "black", "white"]
        )
        self.plotMarkerColorMpl.currentTextChanged.connect(
            lambda x: self.change_marker_color(x)
        )
        boxLayout.addRow("Marker Color:", self.plotMarkerColorMpl)

        # Error
        self.showErrorMpl = QCheckBox()
        self.showErrorMpl.stateChanged.connect(
            lambda x: self.show_error(x)
        )
        boxLayout.addRow("Show Error:", self.showErrorMpl)

        # Error Color
        self.errorColorMpl = QComboBox()
        self.errorColorMpl.addItems(
            ["blue", "green", "red", "cyan", "magenta", "yellow", "black", "white"]
        )
        self.errorColorMpl.currentTextChanged.connect(
            lambda x: self.change_error_color(x)
        )
        boxLayout.addRow("Error Color:", self.errorColorMpl)

        # Draw Style
        self.drawStyleMpl = QComboBox()
        self.drawStyleMpl.addItems(
            ["default", "steps", "steps-pre", "steps-mid", "steps-post"]
        )
        self.drawStyleMpl.currentTextChanged.connect(
            lambda x: self.change_draw_style(x)
        )
        boxLayout.addRow("Draw Style:", self.drawStyleMpl)

        box.setContentLayout(boxLayout)

    def change_color(self, new_color):
        app = QApplication.activeWindow()
        app.plotPoints.set_color(new_color)
        app.canvasPlot.update_plot()

    def change_plot_line(self, new_plot_line):
        app = QApplication.activeWindow()
        app.plotPoints.set_plot_line(new_plot_line)
        app.canvasPlot.update_plot()

    def change_marker(self, new_marker):
        app = QApplication.activeWindow()
        app.plotPoints.set_marker(new_marker)
        app.canvasPlot.update_plot()

    def change_marker_color(self, new_marker_color):
        app = QApplication.activeWindow()
        app.plotPoints.set_marker_color(new_marker_color)
        app.canvasPlot.update_plot()

    def show_error(self, flag):
        app = QApplication.activeWindow()
        app.plotPoints.set_show_error(True if flag else False)
        app.canvasPlot.update_plot()

    def change_error_color(self, new_error_color):
        app = QApplication.activeWindow()
        app.plotPoints.set_error_color(new_error_color)
        app.canvasPlot.update_plot()

    def change_draw_style(self, new_draw_style):
        app = QApplication.activeWindow()
        app.plotPoints.set_drawstyle(new_draw_style)
        app.canvasPlot.update_plot()
