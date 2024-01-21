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

        # Add z value
        self.zMpl = QLineEdit()
        self.zMpl.textChanged.connect(lambda x: self.change_z(x))
        boxLayout.addRow("z:", self.zMpl)

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

    def change_z(self, new_z):
        if not check_number(new_z):
            return

        app = QApplication.activeWindow()
        app.plotHorizo.set_z(float(new_z))
        self.showLabelMpl.setChecked(False)
        app.canvasPlot.update_plot()
