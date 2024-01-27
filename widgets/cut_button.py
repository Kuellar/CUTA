from PyQt6.QtWidgets import QApplication
from widgets.custom_button import CustomButton


class CutButton(CustomButton):
    def __init__(self):
        super().__init__("fa5s.cut")

        self.clicked.connect(self.cut_slider)

    def cut_slider(self):
        app = QApplication.activeWindow()

        slider_bottom = app.canvas_plot_bottom_slider
        value_buttom = slider_bottom.slider.value()
        slider_bottom.set_range(value_buttom)
        slider_left = app.canvas_plot_left_slider
        value_left = slider_left.slider.value()
        slider_left.set_range(value_left)

        app.plot_points.set_x_range([value_buttom[0], value_buttom[1]])
        app.plot_points.set_y_range([value_left[0], value_left[1]])
