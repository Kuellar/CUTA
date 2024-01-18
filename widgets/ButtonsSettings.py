import qtawesome as qta
from .CustomButton import CustomButton
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QStyleOption, QStyle
from PyQt6.QtGui import QPainter, QIcon
from PyQt6.QtCore import Qt, QSize


class ButtonsSettings(QWidget):
    def __init__(self, win):
        super(QWidget, self).__init__()
        self.IconSize = QSize(48, 48)
        self.buttonsSettingsLayout = QHBoxLayout()
        self.buttonsSettingsLayout.setContentsMargins(0, 0, 0, 0)
        self.buttonsSettingsLayout.setSpacing(0)
        self.setLayout(self.buttonsSettingsLayout)
        self.win = win

        # Permissions: "move", "zoom"
        self.active = None

        # Stretch
        self.buttonsSettingsLayout.addStretch()

        # Set square
        self.squareButton = CustomButton("fa5.square")
        self.squareButton.clicked.connect(lambda: self.set_square())
        self.buttonsSettingsLayout.addWidget(self.squareButton, Qt.AlignCenter)

        # Move
        self.moveButton = CustomButton("fa5.hand-paper")
        self.moveButton.clicked.connect(lambda: self.allow_move())
        self.buttonsSettingsLayout.addWidget(self.moveButton, Qt.AlignCenter)

        # Zoom
        self.zoomButton = CustomButton("fa5s.search")
        self.zoomButton.clicked.connect(lambda: self.allow_zoom())
        self.buttonsSettingsLayout.addWidget(self.zoomButton, Qt.AlignCenter)

        # Return
        self.returnButton = CustomButton("fa5s.undo")
        self.returnButton.clicked.connect(lambda: self.set_original())
        self.buttonsSettingsLayout.addWidget(self.returnButton, Qt.AlignCenter)

        # ScreenShot
        self.screenshotButton = CustomButton("fa5s.camera")
        self.screenshotButton.clicked.connect(lambda: self.take_screenshot())
        self.buttonsSettingsLayout.addWidget(self.screenshotButton, Qt.AlignCenter)

        # Stretch
        self.buttonsSettingsLayout.addStretch()

    def set_square(self):
        self.moveButton.set_active(False)
        self.zoomButton.set_active(False)
        self.active = None

        oldHeight = self.win.canvasPlotGridHeight
        newHeight = self.win.canvasPlotGrid.frameGeometry().height()
        newWidthAll = (
            self.win.canvasWorkspaceLayoutSplitter.sizes()[0]
            + self.win.canvasWorkspaceLayoutSplitter.sizes()[1]
        )
        newPlotWidth = self.win.ratioPlotSettings[0] * newHeight / oldHeight
        newSettWidth = newWidthAll - newPlotWidth
        self.win.canvasWorkspaceLayoutSplitter.setSizes(
            [int(newPlotWidth), int(newSettWidth)]
        )

    def allow_move(self):
        if self.active != "move":
            self.active = "move"
            self.moveButton.set_active()
            self.zoomButton.set_active(False)
        else:
            self.active = None
            self.moveButton.set_active(False)

    def allow_zoom(self):
        if self.active != "zoom":
            self.active = "zoom"
            self.zoomButton.set_active()
            self.moveButton.set_active(False)
        else:
            self.active = None
            self.zoomButton.set_active(False)

    def set_original(self):
        self.moveButton.set_active(False)
        self.zoomButton.set_active(False)
        self.active = None

        x_original = self.win.canvasPlotBottomSlider.getRange()
        y_original = self.win.canvasPlotLeftSlider.getRange()
        self.win.canvasPlotBottomSlider.setValue(x_original)
        self.win.canvasPlotLeftSlider.setValue(y_original)
        self.win.canvasPlot.change_xlim(x_original)
        self.win.canvasPlot.change_ylim(y_original)
        self.win.canvasPlot.draw_texts()

    def take_screenshot(self):
        self.moveButton.set_active(False)
        self.zoomButton.set_active(False)
        self.active = None
        if self.win.lastDirOpen:
            self.win.canvasPlot.fig.savefig(self.win.lastFileOpen[:-4])

    def paintEvent(self, event):
        o = QStyleOption()
        o.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, o, p, self)
