import qtawesome as qta
from PyQt6.QtWidgets import (
    QFormLayout,
    QLineEdit,
    QCheckBox,
)


class MplSettingsLayout(QFormLayout):
    def __init__(self, mlpCanvas):
        super(QFormLayout, self).__init__()

        # Global
        self.titleMpl = QLineEdit()
        self.titleMpl.textChanged.connect(lambda x: mlpCanvas.change_title(x))
        self.addRow("Title:", self.titleMpl)
        self.xlabelMpl = QLineEdit()
        self.xlabelMpl.textChanged.connect(lambda x: mlpCanvas.change_xlabel(x))
        self.addRow("x Label:", self.xlabelMpl)
        self.ylabelMpl = QLineEdit()
        self.ylabelMpl.textChanged.connect(lambda x: mlpCanvas.change_ylabel(x))
        self.addRow("y Label:", self.ylabelMpl)
        self.showGridMpl = QCheckBox()
        self.showGridMpl.stateChanged.connect(lambda x: mlpCanvas.show_grid(x))
        self.addRow("Show Grid:", self.showGridMpl)
