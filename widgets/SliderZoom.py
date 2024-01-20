import re
from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLineEdit,
    QStyleOption,
    QStyle,
    QApplication,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter
from superqt import QDoubleRangeSlider
from .RotableContainer import RotatableContainer


class SliderZoom(QWidget):
    def __init__(self, horizontal=True):
        super(QWidget, self).__init__()
        self.horizontal = horizontal

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
        app = QApplication.activeWindow()
        if not app:
            return
        if self.horizontal:
            self.firstInput.setText("{:.4f}".format(range[0]))
            self.secondInput.setText("{:.4f}".format(range[1]))
            app.plotPoints.set_x_limit(range)
            app.canvasPlot.update_xlim()
            app.canvasPlot.draw_texts()
        else:
            self.firstInput.setText("{:.4f}".format(range[1]))
            self.secondInput.setText("{:.4f}".format(range[0]))
            app.plotPoints.set_y_limit(range)
            app.canvasPlot.update_ylim()
            app.canvasPlot.draw_texts()

    def firstInputChanged(self, value):
        app = QApplication.activeWindow()
        if not app:
            return
        if not value or value == "-":
            return
        lastChar = value[len(value) - 1]
        if (
            re.match(r"^-?[0-9]\d*(\.\d+)?$", value) is not None or lastChar == "."
        ) and value.count(".") < 2:
            if lastChar != ".":
                if self.horizontal:
                    if float(value) >= app.plotPoints.x_range[0]:
                        if float(value) <= float(self.secondInput.text()):
                            app.plotPoints.set_x_limit(
                                [float(value), app.canvasPlot.axes.get_xlim()[1]]
                            )
                            app.canvasPlot.update_xlim()
                            self.slider.setValue(
                                (float(value), app.canvasPlot.axes.get_xlim()[1])
                            )
                        else:
                            app.plotPoints.set_x_limit(
                                [
                                    float(self.secondInput.text()) - 0.001,
                                    app.canvasPlot.axes.get_xlim()[1],
                                ]
                            )
                            app.canvasPlot.update_xlim()
                            self.slider.setValue(
                                (
                                    float(self.secondInput.text()) - 0.001,
                                    app.canvasPlot.axes.get_xlim()[1],
                                )
                            )
                    else:
                        app.plotPoints.set_x_limit(
                            [
                                app.plotPoints.x_range[0],
                                app.canvasPlot.axes.get_xlim()[1],
                            ]
                        )
                        app.canvasPlot.update_xlim()
                        self.slider.setValue(
                            (
                                app.plotPoints.x_range[0],
                                app.canvasPlot.axes.get_xlim()[1],
                            )
                        )
                else:
                    if float(value) <= app.plotPoints.y_range[1]:
                        if float(value) >= float(self.secondInput.text()):
                            app.plotPoints.set_y_limit(
                                [app.canvasPlot.axes.get_ylim()[0], float(value)]
                            )
                            app.canvasPlot.update_ylim()
                            self.slider.setValue(
                                (app.canvasPlot.axes.get_ylim()[0], float(value))
                            )
                        else:
                            app.plotPoints.set_y_limit(
                                [
                                    app.canvasPlot.axes.get_ylim()[0],
                                    float(self.secondInput.text()) + 0.001,
                                ]
                            )
                            app.canvasPlot.update_ylim()
                            self.slider.setValue(
                                (
                                    app.canvasPlot.axes.get_ylim()[0],
                                    float(self.secondInput.text()) + 0.001,
                                )
                            )
                    else:
                        app.plotPoints.set_y_limit(
                            [
                                app.canvasPlot.axes.get_ylim()[0],
                                app.plotPoints.y_range[1],
                            ]
                        )
                        app.canvasPlot.update_ylim()
                        self.slider.setValue(
                            (
                                app.canvasPlot.axes.get_ylim()[0],
                                app.plotPoints.y_range[1],
                            )
                        )
        else:
            self.firstInput.setText(value[: len(value) - 1])

    def firstInputEditingFinished(self):
        app = QApplication.activeWindow()
        if not app:
            return
        if self.horizontal:
            if (
                self.firstInput.text() == ""
                or self.firstInput.text() == "-"
                or float(self.firstInput.text()) < app.plotPoints.x_limit[0]
            ):
                self.firstInput.setText("{:.4f}".format(app.plotPoints.x_limit[0]))
            elif float(self.firstInput.text()) > float(self.secondInput.text()):
                self.firstInput.setText(
                    "{:.4f}".format(float(self.secondInput.text()) - 0.001)
                )
        else:
            if (
                self.firstInput.text() == ""
                or self.firstInput.text() == "-"
                or float(self.firstInput.text()) > app.plotPoints.y_limit[1]
            ):
                self.firstInput.setText("{:.4f}".format(app.plotPoints.y_limit[1]))
            elif float(self.firstInput.text()) < float(self.secondInput.text()):
                self.firstInput.setText(
                    "{:.4f}".format(float(self.secondInput.text()) + 0.001)
                )

    def secondInputChanged(self, value):
        app = QApplication.activeWindow()
        if not app:
            return
        if not value or value == "-":
            return
        lastChar = value[len(value) - 1]
        if (
            re.match(r"^-?[0-9]\d*(\.\d+)?$", value) is not None or lastChar == "."
        ) and value.count(".") < 2:
            if lastChar != ".":
                if self.horizontal:
                    if float(value) <= app.plotPoints.x_range[1]:
                        if float(value) >= float(self.firstInput.text()):
                            app.plotPoints.set_x_limit(
                                [app.canvasPlot.axes.get_xlim()[0], float(value)]
                            )
                            app.canvasPlot.update_xlim()
                            self.slider.setValue(
                                (app.canvasPlot.axes.get_xlim()[0], float(value))
                            )
                        else:
                            app.plotPoints.set_x_limit(
                                [
                                    app.canvasPlot.axes.get_xlim()[0],
                                    float(self.firstInput.text()) + 0.001,
                                ]
                            )
                            app.canvasPlot.update_xlim()
                            self.slider.setValue(
                                (
                                    app.canvasPlot.axes.get_xlim()[0],
                                    float(self.firstInput.text()) + 0.001,
                                )
                            )
                    else:
                        app.plotPoints.set_x_limit(
                            [
                                app.canvasPlot.axes.get_xlim()[0],
                                app.plotPoints.x_range[1],
                            ]
                        )
                        app.canvasPlot.update_xlim()
                        self.slider.setValue(
                            (
                                app.canvasPlot.axes.get_xlim()[0],
                                app.plotPoints.x_range[1],
                            )
                        )
                else:
                    if float(value) >= app.plotPoints.y_range[0]:
                        if float(value) <= float(self.firstInput.text()):
                            app.plotPoints.set_y_limit(
                                [float(value), app.canvasPlot.axes.get_ylim()[1]]
                            )
                            app.canvasPlot.update_ylim()
                            self.slider.setValue(
                                (float(value), app.canvasPlot.axes.get_ylim()[1])
                            )
                        else:
                            app.plotPoints.set_y_limit(
                                [
                                    float(self.firstInput.text()) - 0.001,
                                    app.canvasPlot.axes.get_ylim()[1],
                                ]
                            )
                            app.canvasPlot.update_ylim()
                            self.slider.setValue(
                                (
                                    float(self.firstInput.text()) - 0.001,
                                    app.canvasPlot.axes.get_ylim()[1],
                                )
                            )
                    else:
                        app.plotPoints.set_y_limit(
                            [
                                app.plotPoints.y_range[0],
                                app.canvasPlot.axes.get_ylim()[1],
                            ]
                        )
                        app.canvasPlot.update_ylim()
                        self.slider.setValue(
                            (
                                app.plotPoints.y_range[0],
                                app.canvasPlot.axes.get_ylim()[1],
                            )
                        )
        else:
            self.secondInput.setText(value[: len(value) - 1])

    def secondInputEditingFinished(self):
        app = QApplication.activeWindow()
        if not app:
            return
        if self.horizontal:
            if (
                self.secondInput.text() == ""
                or self.secondInput.text() == "-"
                or float(self.secondInput.text()) > app.plotPoints.x_limit[1]
            ):
                self.secondInput.setText("{:.4f}".format(app.plotPoints.x_limit[1]))
            elif float(self.secondInput.text()) < float(self.firstInput.text()):
                self.secondInput.setText(
                    "{:.4f}".format(float(self.firstInput.text()) + 0.001)
                )
        else:
            if (
                self.secondInput.text() == ""
                or self.secondInput.text() == "-"
                or float(self.secondInput.text()) < app.plotPoints.y_limit[0]
            ):
                self.secondInput.setText("{:.4f}".format(app.plotPoints.y_limit[0]))
            elif float(self.secondInput.text()) > float(self.firstInput.text()):
                self.secondInput.setText(
                    "{:.4f}".format(float(self.firstInput.text()) - 0.001)
                )

    def paintEvent(self, event):
        o = QStyleOption()
        o.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, o, p, self)
