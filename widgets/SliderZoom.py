import re
from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLineEdit,
    QStyleOption,
    QStyle,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter
from superqt import QDoubleRangeSlider
from .RotableContainer import RotatableContainer


class SliderZoom(QWidget):
    def __init__(self, horizontal=True, mplCanvas=None):
        super(QWidget, self).__init__()
        self.range = None
        self.horizontal = horizontal
        self.mplCanvas = mplCanvas

        self.layoutSlider = QHBoxLayout() if horizontal else QVBoxLayout()
        self.setLayout(self.layoutSlider)
        self.firstInput = QLineEdit(alignment=Qt.AlignCenter)
        self.slider = QDoubleRangeSlider(
            Qt.Orientation.Horizontal if horizontal else Qt.Orientation.Vertical
        )
        self.secondInput = QLineEdit(alignment=Qt.AlignCenter)

        # Not the best idea...
        firstInputFont = self.firstInput.font()
        firstInputFont.setPointSize(8)
        self.firstInput.setFont(firstInputFont)
        secondInputFont = self.secondInput.font()
        secondInputFont.setPointSize(8)
        self.secondInput.setFont(secondInputFont)

        self.slider.sliderMoved.connect(lambda x: self.sliderMoved(x))
        self.firstInput.textEdited.connect(lambda x: self.firstInputChanged(x))
        self.firstInput.editingFinished.connect(
            lambda: self.firstInputEditingFinished()
        )
        self.secondInput.textEdited.connect(lambda x: self.secondInputChanged(x))
        self.secondInput.editingFinished.connect(
            lambda: self.secondInputEditingFinished()
        )

        if not horizontal:
            self.firstInput.setStyleSheet("max-width: 65px")
            firstContainer = RotatableContainer(self, self.firstInput, 0)
            firstContainer.setStyleSheet(
                "background-color:transparent; max-width: 25px"
            )
            firstContainer.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            firstContainer.rotate(-90)
            self.secondInput.setStyleSheet("max-width: 65px")
            secondContainer = RotatableContainer(self, self.secondInput, 0)
            secondContainer.setStyleSheet(
                "background-color:transparent; max-width: 25px"
            )
            secondContainer.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            secondContainer.rotate(-90)
            self.layoutSlider.addWidget(
                firstContainer, alignment=Qt.AlignCenter, stretch=120
            )
            self.layoutSlider.addWidget(self.slider, stretch=850)
            self.layoutSlider.addWidget(
                secondContainer, alignment=Qt.AlignCenter, stretch=110
            )
        else:
            self.layoutSlider.addWidget(self.firstInput, stretch=130)
            self.layoutSlider.addWidget(self.slider, stretch=850)
            self.layoutSlider.addWidget(self.secondInput, stretch=100)

    def setRange(self, range):
        self.range = range
        if self.horizontal:
            self.firstInput.setText("{:.4f}".format(range[0]))
            self.slider.setRange(range[0], range[1])
            self.slider.setValue((range[0], range[1]))
            self.secondInput.setText("{:.4f}".format(range[1]))
        else:
            self.firstInput.setText("{:.4f}".format(range[1]))
            self.slider.setRange(range[0], range[1])
            self.slider.setValue((range[0], range[1]))
            self.secondInput.setText("{:.4f}".format(range[0]))

    def getRange(self):
        return self.range

    def setValue(self, value):
        if self.horizontal:
            self.firstInput.setText("{:.4f}".format(value[0]))
            self.slider.setValue((value[0], value[1]))
            self.secondInput.setText("{:.4f}".format(value[1]))
        else:
            self.firstInput.setText("{:.4f}".format(value[1]))
            self.slider.setValue((value[0], value[1]))
            self.secondInput.setText("{:.4f}".format(value[0]))

    def sliderMoved(self, range):
        if self.horizontal:
            self.firstInput.setText("{:.4f}".format(range[0]))
            self.secondInput.setText("{:.4f}".format(range[1]))
            self.mplCanvas.change_xlim(range)
        else:
            self.firstInput.setText("{:.4f}".format(range[1]))
            self.secondInput.setText("{:.4f}".format(range[0]))
            self.mplCanvas.change_ylim(range)

    def firstInputChanged(self, value):
        if not value or value == "-":
            return
        lastChar = value[len(value) - 1]
        if (
            re.match(r"^-?[0-9]\d*(\.\d+)?$", value) is not None or lastChar == "."
        ) and value.count(".") < 2:
            if lastChar != ".":
                if self.horizontal:
                    if float(value) >= self.mplCanvas.pointPlot.x_limit[0]:
                        if float(value) <= float(self.secondInput.text()):
                            self.mplCanvas.change_xlim(
                                [float(value), self.mplCanvas.axes.get_xlim()[1]]
                            )
                            self.slider.setValue(
                                (float(value), self.mplCanvas.axes.get_xlim()[1])
                            )
                        else:
                            self.mplCanvas.change_xlim(
                                [
                                    float(self.secondInput.text()) - 0.001,
                                    self.mplCanvas.axes.get_xlim()[1],
                                ]
                            )
                            self.slider.setValue(
                                (
                                    float(self.secondInput.text()) - 0.001,
                                    self.mplCanvas.axes.get_xlim()[1],
                                )
                            )
                    else:
                        self.mplCanvas.change_xlim(
                            [
                                self.mplCanvas.pointPlot.x_limit[0],
                                self.mplCanvas.axes.get_xlim()[1],
                            ]
                        )
                        self.slider.setValue(
                            (
                                self.mplCanvas.pointPlot.x_limit[0],
                                self.mplCanvas.axes.get_xlim()[1],
                            )
                        )
                else:
                    if float(value) <= self.mplCanvas.pointPlot.y_limit[1]:
                        if float(value) >= float(self.secondInput.text()):
                            self.mplCanvas.change_ylim(
                                [self.mplCanvas.axes.get_ylim()[0], float(value)]
                            )
                            self.slider.setValue(
                                (self.mplCanvas.axes.get_ylim()[0], float(value))
                            )
                        else:
                            self.mplCanvas.change_ylim(
                                [
                                    self.mplCanvas.axes.get_ylim()[0],
                                    float(self.secondInput.text()) + 0.001,
                                ]
                            )
                            self.slider.setValue(
                                (
                                    self.mplCanvas.axes.get_ylim()[0],
                                    float(self.secondInput.text()) + 0.001,
                                )
                            )
                    else:
                        self.mplCanvas.change_ylim(
                            [
                                self.mplCanvas.axes.get_ylim()[0],
                                self.mplCanvas.pointPlot.y_limit[1],
                            ]
                        )
                        self.slider.setValue(
                            (
                                self.mplCanvas.axes.get_ylim()[0],
                                self.mplCanvas.pointPlot.y_limit[1],
                            )
                        )
        else:
            self.firstInput.setText(value[: len(value) - 1])

    def firstInputEditingFinished(self):
        if self.horizontal:
            if (
                self.firstInput.text() == ""
                or self.firstInput.text() == "-"
                or float(self.firstInput.text()) < self.mplCanvas.pointPlot.x_limit[0]
            ):
                self.firstInput.setText("{:.4f}".format(self.mplCanvas.pointPlot.x_limit[0]))
            elif float(self.firstInput.text()) > float(self.secondInput.text()):
                self.firstInput.setText(
                    "{:.4f}".format(float(self.secondInput.text()) - 0.001)
                )
        else:
            if (
                self.firstInput.text() == ""
                or self.firstInput.text() == "-"
                or float(self.firstInput.text()) > self.mplCanvas.pointPlot.y_limit[1]
            ):
                self.firstInput.setText("{:.4f}".format(self.mplCanvas.pointPlot.y_limit[1]))
            elif float(self.firstInput.text()) < float(self.secondInput.text()):
                self.firstInput.setText(
                    "{:.4f}".format(float(self.secondInput.text()) + 0.001)
                )

    def secondInputChanged(self, value):
        if not value or value == "-":
            return
        lastChar = value[len(value) - 1]
        if (
            re.match(r"^-?[0-9]\d*(\.\d+)?$", value) is not None or lastChar == "."
        ) and value.count(".") < 2:
            if lastChar != ".":
                if self.horizontal:
                    if float(value) <= self.mplCanvas.pointPlot.x_limit[1]:
                        if float(value) >= float(self.firstInput.text()):
                            self.mplCanvas.change_xlim(
                                [self.mplCanvas.axes.get_xlim()[0], float(value)]
                            )
                            self.slider.setValue(
                                (self.mplCanvas.axes.get_xlim()[0], float(value))
                            )
                        else:
                            self.mplCanvas.change_xlim(
                                [
                                    self.mplCanvas.axes.get_xlim()[0],
                                    float(self.firstInput.text()) + 0.001,
                                ]
                            )
                            self.slider.setValue(
                                (
                                    self.mplCanvas.axes.get_xlim()[0],
                                    float(self.firstInput.text()) + 0.001,
                                )
                            )
                    else:
                        self.mplCanvas.change_xlim(
                            [
                                self.mplCanvas.axes.get_xlim()[0],
                                self.mplCanvas.pointPlot.x_limit[1],
                            ]
                        )
                        self.slider.setValue(
                            (
                                self.mplCanvas.axes.get_xlim()[0],
                                self.mplCanvas.pointPlot.x_limit[1],
                            )
                        )
                else:
                    if float(value) >= self.mplCanvas.pointPlot.y_limit[0]:
                        if float(value) <= float(self.firstInput.text()):
                            self.mplCanvas.change_ylim(
                                [float(value), self.mplCanvas.axes.get_ylim()[1]]
                            )
                            self.slider.setValue(
                                (float(value), self.mplCanvas.axes.get_ylim()[1])
                            )
                        else:
                            self.mplCanvas.change_ylim(
                                [
                                    float(self.firstInput.text()) - 0.001,
                                    self.mplCanvas.axes.get_ylim()[1],
                                ]
                            )
                            self.slider.setValue(
                                (
                                    float(self.firstInput.text()) - 0.001,
                                    self.mplCanvas.axes.get_ylim()[1],
                                )
                            )
                    else:
                        self.mplCanvas.change_ylim(
                            [
                                self.mplCanvas.pointPlot.y_limit[0],
                                self.mplCanvas.axes.get_ylim()[1],
                            ]
                        )
                        self.slider.setValue(
                            (
                                self.mplCanvas.pointPlot.y_limit[0],
                                self.mplCanvas.axes.get_ylim()[1],
                            )
                        )
        else:
            self.secondInput.setText(value[: len(value) - 1])

    def secondInputEditingFinished(self):
        if self.horizontal:
            if (
                self.secondInput.text() == ""
                or self.secondInput.text() == "-"
                or float(self.secondInput.text()) > self.mplCanvas.pointPlot.x_limit[1]
            ):
                self.secondInput.setText("{:.4f}".format(self.mplCanvas.pointPlot.x_limit[1]))
            elif float(self.secondInput.text()) < float(self.firstInput.text()):
                self.secondInput.setText(
                    "{:.4f}".format(float(self.firstInput.text()) + 0.001)
                )
        else:
            if (
                self.secondInput.text() == ""
                or self.secondInput.text() == "-"
                or float(self.secondInput.text()) < self.mplCanvas.pointPlot.y_limit[0]
            ):
                self.secondInput.setText("{:.4f}".format(self.mplCanvas.pointPlot.y_limit[0]))
            elif float(self.secondInput.text()) > float(self.firstInput.text()):
                self.secondInput.setText(
                    "{:.4f}".format(float(self.firstInput.text()) - 0.001)
                )

    def paintEvent(self, event):
        o = QStyleOption()
        o.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, o, p, self)
