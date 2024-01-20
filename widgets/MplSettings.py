from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget, QFormLayout, QLineEdit, QCheckBox, QComboBox
from widgets.CollapsibleBox import CollapsibleBox

class MplSettings(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        box = CollapsibleBox("Global Settings")
        layout.addWidget(box)
        boxLayout = QFormLayout()

        # Title
        self.titleMpl = QLineEdit()
        self.titleMpl.textChanged.connect(lambda x: self.change_title(x))
        boxLayout.addRow("Title:", self.titleMpl)

        # Label
        self.xlabelMpl = QLineEdit()
        self.xlabelMpl.textChanged.connect(lambda x: self.change_xlabel(x))
        boxLayout.addRow("x Label:", self.xlabelMpl)
        self.ylabelMpl = QLineEdit()
        self.ylabelMpl.textChanged.connect(lambda x: self.change_ylabel(x))
        boxLayout.addRow("y Label:", self.ylabelMpl)

        # Grid
        self.showGridMpl = QCheckBox()
        self.showGridMpl.stateChanged.connect(lambda x: self.show_grid(x))
        boxLayout.addRow("Show Grid:", self.showGridMpl)

        # Scale
        self.xscaleMpl = QComboBox()
        self.xscaleMpl.addItems(["linear", "log", "symlog"])  # miss: "logit"
        self.xscaleMpl.currentTextChanged.connect(lambda x: self.change_xscale(x))
        boxLayout.addRow("X scale:", self.xscaleMpl)
        self.yscaleMpl = QComboBox()
        self.yscaleMpl.addItems(["linear", "log", "symlog"])  # miss: "logit"
        self.yscaleMpl.currentTextChanged.connect(lambda x: self.change_yscale(x))
        boxLayout.addRow("Y scale:", self.yscaleMpl)

        box.setContentLayout(boxLayout)

    def change_title(self, new_title):
        app = QApplication.activeWindow()
        app.plot.set_title(new_title)
        app.canvasPlot.update_plot_settings()

    def change_xlabel(self, new_xlabel):
        app = QApplication.activeWindow()
        app.plot.set_xlabel(new_xlabel)
        app.canvasPlot.update_plot_settings()

    def change_ylabel(self, new_ylabel):
        app = QApplication.activeWindow()
        app.plot.set_ylabel(new_ylabel)
        app.canvasPlot.update_plot_settings()

    def show_grid(self, flag):
        app = QApplication.activeWindow()
        app.plot.set_show_grid(True if flag else False)
        app.canvasPlot.update_plot_settings()

    def change_xscale(self, new_xscale):
        app = QApplication.activeWindow()
        app.plot.set_xscale(new_xscale)
        app.canvasPlot.update_plot_settings()

    def change_yscale(self, new_yscale):
        app = QApplication.activeWindow()
        app.plot.set_yscale(new_yscale)
        app.canvasPlot.update_plot_settings()
