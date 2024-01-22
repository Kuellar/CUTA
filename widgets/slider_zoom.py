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
from .rotable_container import RotatableContainer


class SliderZoom(QWidget):
    def __init__(self, horizontal=True):
        super().__init__()
        self.horizontal = horizontal

        self.slider_layout = QHBoxLayout() if horizontal else QVBoxLayout()
        self.setLayout(self.slider_layout)
        self.first_input = QLineEdit(alignment=Qt.AlignCenter)
        self.slider = QDoubleRangeSlider(
            Qt.Orientation.Horizontal if horizontal else Qt.Orientation.Vertical
        )
        self.second_input = QLineEdit(alignment=Qt.AlignCenter)

        # Not the best idea...
        first_input_font = self.first_input.font()
        first_input_font.setPointSize(8)
        self.first_input.setFont(first_input_font)
        second_input_font = self.second_input.font()
        second_input_font.setPointSize(8)
        self.second_input.setFont(second_input_font)

        self.slider.sliderPressed.connect(self.slider_pressed)
        self.slider.sliderMoved.connect(self.slider_moved)
        self.slider.sliderReleased.connect(self.slider_released)
        self.first_input.textEdited.connect(self.first_input_changed)
        self.first_input.editingFinished.connect(self.first_input_editing_finished)
        self.second_input.textEdited.connect(self.second_input_changed)
        self.second_input.editingFinished.connect(self.second_input_editing_finished)

        if not horizontal:
            self.first_input.setStyleSheet("max-width: 65px")
            first_container = RotatableContainer(self, self.first_input, 0)
            first_container.setStyleSheet(
                "background-color:transparent; max-width: 25px"
            )
            first_container.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            first_container.rotate(-90)
            self.second_input.setStyleSheet("max-width: 65px")
            second_container = RotatableContainer(self, self.second_input, 0)
            second_container.setStyleSheet(
                "background-color:transparent; max-width: 25px"
            )
            second_container.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            second_container.rotate(-90)
            self.slider_layout.addWidget(
                first_container, alignment=Qt.AlignCenter, stretch=120
            )
            self.slider_layout.addWidget(self.slider, stretch=850)
            self.slider_layout.addWidget(
                second_container, alignment=Qt.AlignCenter, stretch=110
            )
        else:
            self.slider_layout.addWidget(self.first_input, stretch=130)
            self.slider_layout.addWidget(self.slider, stretch=850)
            self.slider_layout.addWidget(self.second_input, stretch=100)

    def set_range(self, new_range):
        if self.horizontal:
            self.first_input.setText(f"{new_range[0]:.4f}")
            self.slider.setRange(new_range[0], new_range[1])
            self.slider.setValue((new_range[0], new_range[1]))
            self.second_input.setText(f"{new_range[1]:.4f}")
        else:
            self.first_input.setText(f"{new_range[1]:.4f}")
            self.slider.setRange(new_range[0], new_range[1])
            self.slider.setValue((new_range[0], new_range[1]))
            self.second_input.setText(f"{new_range[0]:.4f}")

    def set_value(self, value):
        if self.horizontal:
            self.first_input.setText(f"{value[0]:.4f}")
            self.slider.setValue((value[0], value[1]))
            self.second_input.setText(f"{value[1]:.4f}")
        else:
            self.first_input.setText(f"{value[1]:.4f}")
            self.slider.setValue((value[0], value[1]))
            self.second_input.setText(f"{value[0]:.4f}")

    def slider_pressed(self):
        app = QApplication.activeWindow()
        if not app:
            return
        app.canvas_plot.remove_texts()

    def slider_moved(self, new_range):
        app = QApplication.activeWindow()
        if not app:
            return
        if self.horizontal:
            self.first_input.setText(f"{new_range[0]:.4f}")
            self.second_input.setText(f"{new_range[1]:.4f}")
            app.plot_points.set_x_limit(new_range)
            app.canvas_plot.update_xlim()
        else:
            self.first_input.setText(f"{new_range[1]:.4f}")
            self.second_input.setText(f"{new_range[0]:.4f}")
            app.plot_points.set_y_limit(new_range)
            app.canvas_plot.update_ylim()

    def slider_released(self):
        app = QApplication.activeWindow()
        if not app:
            return
        app.canvas_plot.draw_texts()

    def first_input_changed(self, value):
        app = QApplication.activeWindow()
        if not app:
            return
        if not value or value == "-":
            return
        last_char = value[len(value) - 1]
        if (
            re.match(r"^-?[0-9]\d*(\.\d+)?$", value) is not None or last_char == "."
        ) and value.count(".") < 2:
            if last_char != ".":
                if self.horizontal:
                    if float(value) >= app.plot_points.x_range[0]:
                        if float(value) <= float(self.second_input.text()):
                            app.plot_points.set_x_limit(
                                [float(value), app.canvas_plot.axes.get_xlim()[1]]
                            )
                            app.canvas_plot.update_xlim()
                            self.slider.setValue(
                                (float(value), app.canvas_plot.axes.get_xlim()[1])
                            )
                        else:
                            app.plot_points.set_x_limit(
                                [
                                    float(self.second_input.text()) - 0.001,
                                    app.canvas_plot.axes.get_xlim()[1],
                                ]
                            )
                            app.canvas_plot.update_xlim()
                            self.slider.setValue(
                                (
                                    float(self.second_input.text()) - 0.001,
                                    app.canvas_plot.axes.get_xlim()[1],
                                )
                            )
                    else:
                        app.plot_points.set_x_limit(
                            [
                                app.plot_points.x_range[0],
                                app.canvas_plot.axes.get_xlim()[1],
                            ]
                        )
                        app.canvas_plot.update_xlim()
                        self.slider.setValue(
                            (
                                app.plot_points.x_range[0],
                                app.canvas_plot.axes.get_xlim()[1],
                            )
                        )
                else:
                    if float(value) <= app.plot_points.y_range[1]:
                        if float(value) >= float(self.second_input.text()):
                            app.plot_points.set_y_limit(
                                [app.canvas_plot.axes.get_ylim()[0], float(value)]
                            )
                            app.canvas_plot.update_ylim()
                            self.slider.setValue(
                                (app.canvas_plot.axes.get_ylim()[0], float(value))
                            )
                        else:
                            app.plot_points.set_y_limit(
                                [
                                    app.canvas_plot.axes.get_ylim()[0],
                                    float(self.second_input.text()) + 0.001,
                                ]
                            )
                            app.canvas_plot.update_ylim()
                            self.slider.setValue(
                                (
                                    app.canvas_plot.axes.get_ylim()[0],
                                    float(self.second_input.text()) + 0.001,
                                )
                            )
                    else:
                        app.plot_points.set_y_limit(
                            [
                                app.canvas_plot.axes.get_ylim()[0],
                                app.plot_points.y_range[1],
                            ]
                        )
                        app.canvas_plot.update_ylim()
                        self.slider.setValue(
                            (
                                app.canvas_plot.axes.get_ylim()[0],
                                app.plot_points.y_range[1],
                            )
                        )
        else:
            self.first_input.setText(value[: len(value) - 1])

    def first_input_editing_finished(self):
        app = QApplication.activeWindow()
        if not app:
            return
        if self.horizontal:
            if (
                self.first_input.text() == ""
                or self.first_input.text() == "-"
                or float(self.first_input.text()) < app.plot_points.x_limit[0]
            ):
                self.first_input.setText(f"{app.plot_points.x_limit[0]:.4f}")
            elif float(self.first_input.text()) > float(self.second_input.text()):
                self.first_input.setText(
                    f"{(float(self.second_input.text()) - 0.001):.4f}"
                )
        else:
            if (
                self.first_input.text() == ""
                or self.first_input.text() == "-"
                or float(self.first_input.text()) > app.plot_points.y_limit[1]
            ):
                self.first_input.setText(f"{app.plot_points.y_limit[1]:.4f}")
            elif float(self.first_input.text()) < float(self.second_input.text()):
                self.first_input.setText(
                    f"{(float(self.second_input.text()) + 0.001):.4f}"
                )

    def second_input_changed(self, value):
        app = QApplication.activeWindow()
        if not app or not value or value == "-":
            return
        last_char = value[len(value) - 1]
        if (
            (re.match(r"^-?[0-9]\d*(\.\d+)?$", value) is not None or last_char == ".")
            and value.count(".") < 2
            and last_char != "."
        ):
            if self.horizontal:
                if float(value) <= app.plot_points.x_range[1]:
                    if float(value) >= float(self.first_input.text()):
                        app.plot_points.set_x_limit(
                            [app.canvas_plot.axes.get_xlim()[0], float(value)]
                        )
                        app.canvas_plot.update_xlim()
                        self.slider.setValue(
                            (app.canvas_plot.axes.get_xlim()[0], float(value))
                        )
                    else:
                        app.plot_points.set_x_limit(
                            [
                                app.canvas_plot.axes.get_xlim()[0],
                                float(self.first_input.text()) + 0.001,
                            ]
                        )
                        app.canvas_plot.update_xlim()
                        self.slider.setValue(
                            (
                                app.canvas_plot.axes.get_xlim()[0],
                                float(self.first_input.text()) + 0.001,
                            )
                        )
                else:
                    app.plot_points.set_x_limit(
                        [
                            app.canvas_plot.axes.get_xlim()[0],
                            app.plot_points.x_range[1],
                        ]
                    )
                    app.canvas_plot.update_xlim()
                    self.slider.setValue(
                        (
                            app.canvas_plot.axes.get_xlim()[0],
                            app.plot_points.x_range[1],
                        )
                    )
            else:
                if float(value) >= app.plot_points.y_range[0]:
                    if float(value) <= float(self.first_input.text()):
                        app.plot_points.set_y_limit(
                            [float(value), app.canvas_plot.axes.get_ylim()[1]]
                        )
                        app.canvas_plot.update_ylim()
                        self.slider.setValue(
                            (float(value), app.canvas_plot.axes.get_ylim()[1])
                        )
                    else:
                        app.plot_points.set_y_limit(
                            [
                                float(self.first_input.text()) - 0.001,
                                app.canvas_plot.axes.get_ylim()[1],
                            ]
                        )
                        app.canvas_plot.update_ylim()
                        self.slider.setValue(
                            (
                                float(self.first_input.text()) - 0.001,
                                app.canvas_plot.axes.get_ylim()[1],
                            )
                        )
                else:
                    app.plot_points.set_y_limit(
                        [
                            app.plot_points.y_range[0],
                            app.canvas_plot.axes.get_ylim()[1],
                        ]
                    )
                    app.canvas_plot.update_ylim()
                    self.slider.setValue(
                        (
                            app.plot_points.y_range[0],
                            app.canvas_plot.axes.get_ylim()[1],
                        )
                    )
        else:
            self.second_input.setText(value[: len(value) - 1])

    def second_input_editing_finished(self):
        app = QApplication.activeWindow()
        if not app:
            return
        if self.horizontal:
            if (
                self.second_input.text() == ""
                or self.second_input.text() == "-"
                or float(self.second_input.text()) > app.plot_points.x_limit[1]
            ):
                self.second_input.setText(f"{app.plot_points.x_limit[1]:.4f}")
            elif float(self.second_input.text()) < float(self.first_input.text()):
                self.second_input.setText(
                    f"{(float(self.first_input.text()) + 0.001):.4f}"
                )
        else:
            if (
                self.second_input.text() == ""
                or self.second_input.text() == "-"
                or float(self.second_input.text()) < app.plot_points.y_limit[0]
            ):
                self.second_input.setText(f"{app.plot_points.y_limit[0]:.4f}")
            elif float(self.second_input.text()) > float(self.first_input.text()):
                self.second_input.setText(
                    f"{(float(self.first_input.text()) - 0.001):.4f}"
                )

    def paintEvent(self, _):  # pylint: disable=C0103
        o = QStyleOption()
        o.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, o, p, self)
