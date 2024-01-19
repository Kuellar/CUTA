from PyQt6.QtWidgets import (
    QWidget,
    QFormLayout,
    QVBoxLayout,
    QComboBox,
    QMainWindow,
)
from widgets.CollapsibleBox import CollapsibleBox
from widgets.MplCanvas import MplCanvas


class MplPlotVertical(QWidget):
    def __init__(self, app: QMainWindow, plotCanvas: MplCanvas):
        super(QWidget, self).__init__()
        self.plotCanvas = plotCanvas
        self.app = app

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        box = CollapsibleBox("Plot vertical")
        layout.addWidget(box)
        boxLayout = QFormLayout()

        # Add things
        self.plotColorMpl = QComboBox()
        self.plotColorMpl.addItems(
            ["blue", "green", "red", "cyan", "magenta", "yellow", "black", "white"]
        )
        self.plotColorMpl.currentTextChanged.connect(lambda x: self.change_color(x))
        boxLayout.addRow("Plot Color:", self.plotColorMpl)

        box.setContentLayout(boxLayout)

    def change_color(self, new_color):
        self.app.plotHorizo.set_colors(new_color)
        self.plotCanvas.update_plot(
            plotHorizo=self.app.plotHorizo,
        )

