from qtpy.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QFormLayout,
    QVBoxLayout,
    QComboBox,
    QApplication,
    QLineEdit,
    QCheckBox,
)
from widgets.CollapsibleBox import CollapsibleBox
from superqt import QDoubleSlider
from utils import check_number


class MplPlotVertical(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        box = CollapsibleBox("Plot vertical")
        layout.addWidget(box)
        boxLayout = QFormLayout()

        # Add Plot Color
        self.plotColorMpl = QComboBox()
        self.plotColorMpl.addItems(
            ["blue", "green", "red", "cyan", "magenta", "yellow", "black", "white"]
        )
        self.plotColorMpl.currentTextChanged.connect(lambda x: self.change_color(x))
        boxLayout.addRow("Plot Color:", self.plotColorMpl)

        # Show Label
        self.showLabelMpl = QCheckBox()
        self.showLabelMpl.setChecked(True)
        self.showLabelMpl.stateChanged.connect(lambda x: self.show_label(x))
        boxLayout.addRow("Show Label:", self.showLabelMpl)

        # Add Label Color
        self.plotLabelColorMpl = QComboBox()
        self.plotLabelColorMpl.addItems(
            ["black", "blue", "green", "red", "cyan", "magenta", "yellow", "white"]
        )
        self.plotLabelColorMpl.currentTextChanged.connect(lambda x: self.change_label_color(x))
        boxLayout.addRow("Label Color:", self.plotLabelColorMpl)

        # Add label position
        self.labelPosMpl = QLineEdit("0.1")
        self.labelPosMpl.textChanged.connect(lambda x: self.change_label_pos(x))
        boxLayout.addRow("Label Position [0,1]:", self.labelPosMpl)

        # Add z value
        self.zMpl = QLineEdit("0")
        self.zMpl.textChanged.connect(lambda x: self.change_z(x))
        boxLayout.addRow("z:", self.zMpl)

        app = QApplication.activeWindow()
        self.min_z = None
        self.max_z = None
        if app:
            self.z_slider = QDoubleSlider(Qt.Orientation.Horizontal)
            range_x = app.plotPoints.x_range
            self.min_z = range_x[0]/app.plotHorizo.x[-1]-1
            self.max_z = range_x[1]/app.plotHorizo.x[0]-1
            self.z_slider.setRange(self.min_z, self.max_z)
            self.z_slider.setValue(0)
            boxLayout.addWidget(self.z_slider)
            self.z_slider.sliderReleased.connect(lambda: self.sliderReleased())

        box.setContentLayout(boxLayout)

    def change_color(self, new_color):
        app = QApplication.activeWindow()
        app.plotHorizo.set_colors(new_color)
        app.canvasPlot.update_plot()

    def show_label(self, flag):
        app = QApplication.activeWindow()
        app.plotHorizo.set_show_names(True if flag else False)
        if not flag:
            app.canvasPlot.remove_texts()
        app.canvasPlot.update_plot()

    def change_label_color(self, new_color):
        app = QApplication.activeWindow()
        app.plotHorizo.set_label_colors(new_color)
        app.canvasPlot.update_plot()

    def change_label_pos(self, new_pos):
        if not check_number(new_pos):
            return
        new_pos = float(new_pos)
        if new_pos < 0:
            new_pos = 0
        if new_pos > 1:
            new_pos = 1
        app = QApplication.activeWindow()
        app.plotHorizo.set_names_y(new_pos)
        app.canvasPlot.remove_texts()
        app.canvasPlot.draw_texts()

    def change_z(self, new_z):
        if not check_number(new_z):
            return
        new_z = float(new_z)
        app = QApplication.activeWindow()
        app.plotHorizo.set_z(new_z)
        self.showLabelMpl.setChecked(False)
        app.canvasPlot.update_plot()
        if new_z>self.min_z and new_z<self.max_z:
            self.z_slider.setValue(new_z)

    def sliderReleased(self):
        self.zMpl.setText("{:.4f}".format(self.z_slider.value()))
        # self.change_z(self.z_slider.value())
