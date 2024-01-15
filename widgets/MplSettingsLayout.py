import qtawesome as qta
from PyQt6.QtWidgets import (
    QFormLayout,
    QLineEdit,
    QCheckBox,
    QComboBox,
)


class MplSettingsLayout(QFormLayout):
    def __init__(self, window, mlpCanvas):
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

        # Specific
        self.plotColorMpl = QComboBox()
        self.plotColorMpl.addItems(
            ["blue", "green", "red", "cyan", "magenta", "yellow", "black", "white"]
        )
        self.plotColorMpl.currentTextChanged.connect(
            lambda: mlpCanvas.update_plot(
                window.xdata, window.ydata, window.zdata, self
            )
        )
        self.addRow("Plot Color:", self.plotColorMpl)

        self.plotLineMpl = QComboBox()
        self.plotLineMpl.addItems(["-", "--", "-.", ":"])
        self.plotLineMpl.currentTextChanged.connect(
            lambda: mlpCanvas.update_plot(
                window.xdata, window.ydata, window.zdata, self
            )
        )
        self.addRow("Line Style:", self.plotLineMpl)

        self.plotMarkerMpl = QComboBox()
        self.plotMarkerMpl.addItems(["", ".", "o", "s", "p", "*", "x", "|"])
        self.plotMarkerMpl.currentTextChanged.connect(
            lambda: mlpCanvas.update_plot(
                window.xdata, window.ydata, window.zdata, self
            )
        )
        self.addRow("Marker:", self.plotMarkerMpl)

        self.plotMarkerColorMpl = QComboBox()
        self.plotMarkerColorMpl.addItems(
            ["blue", "green", "red", "cyan", "magenta", "yellow", "black", "white"]
        )
        self.plotMarkerColorMpl.currentTextChanged.connect(
            lambda: mlpCanvas.update_plot(
                window.xdata, window.ydata, window.zdata, self
            )
        )
        self.addRow("Plot Color:", self.plotMarkerColorMpl)

        self.showErrorMpl = QCheckBox()
        self.showErrorMpl.stateChanged.connect(
            lambda: mlpCanvas.update_plot(
                window.xdata, window.ydata, window.zdata, self
            )
        )
        self.addRow("Show Error:", self.showErrorMpl)

        self.errorColorMpl = QComboBox()
        self.errorColorMpl.addItems(
            ["blue", "green", "red", "cyan", "magenta", "yellow", "black", "white"]
        )
        self.errorColorMpl.currentTextChanged.connect(
            lambda: mlpCanvas.update_plot(
                window.xdata, window.ydata, window.zdata, self
            )
        )
        self.addRow("Error Color:", self.errorColorMpl)

        self.drawStyleMpl = QComboBox()
        self.drawStyleMpl.addItems(
            ["default", "steps", "steps-pre", "steps-mid", "steps-post"]
        )
        self.drawStyleMpl.currentTextChanged.connect(
            lambda x: mlpCanvas.change_drawstyle(x)
        )
        self.addRow("Draw Style:", self.drawStyleMpl)

        self.showGridMpl = QCheckBox()
        self.showGridMpl.stateChanged.connect(lambda x: mlpCanvas.show_grid(x))
        self.addRow("Show Grid:", self.showGridMpl)
