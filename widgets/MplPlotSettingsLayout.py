from PyQt6.QtWidgets import (
    QFormLayout,
    QCheckBox,
    QComboBox,
)


class MplPlotSettingsLayout(QFormLayout):
    def __init__(self, window, mlpCanvas, globalSettings):
        super(QFormLayout, self).__init__()
        self.globalSettings = globalSettings

        # COLOR
        self.plotColorMpl = QComboBox()
        self.plotColorMpl.addItems(
            ["blue", "green", "red", "cyan", "magenta", "yellow", "black", "white"]
        )
        self.plotColorMpl.currentTextChanged.connect(
            lambda: mlpCanvas.update_plot(
                window.xdata, window.ydata, window.zdata, self.globalSettings, self
            )
        )
        self.addRow("Plot Color:", self.plotColorMpl)

        # Line Style
        self.plotLineMpl = QComboBox()
        self.plotLineMpl.addItems(["-", "--", "-.", ":"])
        self.plotLineMpl.currentTextChanged.connect(
            lambda: mlpCanvas.update_plot(
                window.xdata, window.ydata, window.zdata, self.globalSettings, self
            )
        )
        self.addRow("Line Style:", self.plotLineMpl)

        # Marker
        self.plotMarkerMpl = QComboBox()
        self.plotMarkerMpl.addItems(["", ".", "o", "s", "p", "*", "x", "|"])
        self.plotMarkerMpl.currentTextChanged.connect(
            lambda: mlpCanvas.update_plot(
                window.xdata, window.ydata, window.zdata, self.globalSettings, self
            )
        )
        self.addRow("Marker:", self.plotMarkerMpl)

        # Marker Color
        self.plotMarkerColorMpl = QComboBox()
        self.plotMarkerColorMpl.addItems(
            ["blue", "green", "red", "cyan", "magenta", "yellow", "black", "white"]
        )
        self.plotMarkerColorMpl.currentTextChanged.connect(
            lambda: mlpCanvas.update_plot(
                window.xdata, window.ydata, window.zdata, self.globalSettings, self
            )
        )
        self.addRow("Marker Color:", self.plotMarkerColorMpl)

        # Error
        self.showErrorMpl = QCheckBox()
        self.showErrorMpl.stateChanged.connect(
            lambda: mlpCanvas.update_plot(
                window.xdata, window.ydata, window.zdata, self.globalSettings, self
            )
        )
        self.addRow("Show Error:", self.showErrorMpl)

        # Error Color
        self.errorColorMpl = QComboBox()
        self.errorColorMpl.addItems(
            ["blue", "green", "red", "cyan", "magenta", "yellow", "black", "white"]
        )
        self.errorColorMpl.currentTextChanged.connect(
            lambda: mlpCanvas.update_plot(
                window.xdata, window.ydata, window.zdata, self.globalSettings, self
            )
        )
        self.addRow("Error Color:", self.errorColorMpl)

        # Draw Style
        self.drawStyleMpl = QComboBox()
        self.drawStyleMpl.addItems(
            ["default", "steps", "steps-pre", "steps-mid", "steps-post"]
        )
        self.drawStyleMpl.currentTextChanged.connect(
            lambda x: mlpCanvas.change_drawstyle(x)
        )
        self.addRow("Draw Style:", self.drawStyleMpl)
