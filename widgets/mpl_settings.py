from PyQt6.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QWidget,
    QFormLayout,
    QLineEdit,
    QCheckBox,
    QComboBox,
)
from widgets.collapsible_box import CollapsibleBox


class MplSettings(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        box = CollapsibleBox("Global Settings")
        layout.addWidget(box)
        box_layout = QFormLayout()

        # Title
        self.title_mpl = QLineEdit()
        self.title_mpl.textChanged.connect(self.change_title)
        box_layout.addRow("Title:", self.title_mpl)

        # Label
        self.xlabel_mpl = QLineEdit()
        self.xlabel_mpl.textChanged.connect(self.change_xlabel)
        box_layout.addRow("x Label:", self.xlabel_mpl)
        self.ylabel_mpl = QLineEdit()
        self.ylabel_mpl.textChanged.connect(self.change_ylabel)
        box_layout.addRow("y Label:", self.ylabel_mpl)

        # Grid
        self.show_grid_mpl = QCheckBox()
        self.show_grid_mpl.stateChanged.connect(self.show_grid)
        box_layout.addRow("Show Grid:", self.show_grid_mpl)

        # Scale
        self.xscale_mpl = QComboBox()
        self.xscale_mpl.addItems(["linear", "log", "symlog"])  # miss: "logit"
        self.xscale_mpl.currentTextChanged.connect(self.change_xscale)
        box_layout.addRow("X scale:", self.xscale_mpl)
        self.yscale_mpl = QComboBox()
        self.yscale_mpl.addItems(["linear", "log", "symlog"])  # miss: "logit"
        self.yscale_mpl.currentTextChanged.connect(self.change_yscale)
        box_layout.addRow("Y scale:", self.yscale_mpl)

        box.setContentLayout(box_layout)

    def change_title(self, new_title):
        app = QApplication.activeWindow()
        app.plot.set_title(new_title)
        app.canvas_plot.update_plot_settings()

    def change_xlabel(self, new_xlabel):
        app = QApplication.activeWindow()
        app.plot.set_xlabel(new_xlabel)
        app.canvas_plot.update_plot_settings()

    def change_ylabel(self, new_ylabel):
        app = QApplication.activeWindow()
        app.plot.set_ylabel(new_ylabel)
        app.canvas_plot.update_plot_settings()

    def show_grid(self, flag):
        app = QApplication.activeWindow()
        app.plot.set_show_grid(bool(flag))
        app.canvas_plot.update_plot_settings()

    def change_xscale(self, new_xscale):
        app = QApplication.activeWindow()
        app.plot.set_xscale(new_xscale)
        app.canvas_plot.update_plot_settings()

    def change_yscale(self, new_yscale):
        app = QApplication.activeWindow()
        app.plot.set_yscale(new_yscale)
        app.canvas_plot.update_plot_settings()
