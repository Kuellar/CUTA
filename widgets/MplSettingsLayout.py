from PyQt6.QtWidgets import QFormLayout, QLineEdit, QCheckBox, QComboBox


class MplSettingsLayout(QFormLayout):
    def __init__(self, mlpCanvas):
        super(QFormLayout, self).__init__()

        # Title
        self.titleMpl = QLineEdit()
        self.titleMpl.textChanged.connect(lambda x: mlpCanvas.change_title(x))
        self.addRow("Title:", self.titleMpl)

        # Label
        self.xlabelMpl = QLineEdit()
        self.xlabelMpl.textChanged.connect(lambda x: mlpCanvas.change_xlabel(x))
        self.addRow("x Label:", self.xlabelMpl)
        self.ylabelMpl = QLineEdit()
        self.ylabelMpl.textChanged.connect(lambda x: mlpCanvas.change_ylabel(x))
        self.addRow("y Label:", self.ylabelMpl)

        # Grid
        self.showGridMpl = QCheckBox()
        self.showGridMpl.stateChanged.connect(lambda x: mlpCanvas.show_grid(x))
        self.addRow("Show Grid:", self.showGridMpl)

        # Scale
        self.xscaleMpl = QComboBox()
        self.xscaleMpl.addItems(["linear", "log", "symlog"])  # miss: "logit"
        self.xscaleMpl.currentTextChanged.connect(lambda x: mlpCanvas.change_xscale(x))
        self.addRow("X scale:", self.xscaleMpl)
        self.yscaleMpl = QComboBox()
        self.yscaleMpl.addItems(["linear", "log", "symlog"])  # miss: "logit"
        self.yscaleMpl.currentTextChanged.connect(lambda x: mlpCanvas.change_yscale(x))
        self.addRow("Y scale:", self.yscaleMpl)
