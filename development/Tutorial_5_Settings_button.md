## Make the button do things

1. Connect the button to a function.

```
from widgets.custom_button import CustomButton


class CutButton(CustomButton):
    def __init__(self):
        super().__init__("fa5s.cut")

        self.clicked.connect(self.cut_slider)

    def cut_slider(self):
        print("Hello world :)")

```

2. Get a reference for the slider.
* app.py -> self.canvas_plot_left_slider
* app.py -> self.canvas_plot_bottom_slider

```
from PyQt6.QtWidgets import QApplication
from widgets.custom_button import CustomButton


class CutButton(CustomButton):
    def __init__(self):
        super().__init__("fa5s.cut")

        self.clicked.connect(self.cut_slider)

    def cut_slider(self):
        app = QApplication.activeWindow()

        slider_bottom = app.canvas_plot_bottom_slider
        slider_left = app.canvas_plot_left_slider
```

3. Save the current value.
```
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
        print(value_buttom)
        slider_left = app.canvas_plot_left_slider
        value_left = slider_left.slider.value()
        print(value_left)

```

4. Set the range as the current value.
```
def cut_slider(self):
    app = QApplication.activeWindow()

    slider_bottom = app.canvas_plot_bottom_slider
    value_buttom = slider_bottom.slider.value()
    slider_bottom.set_range(value_buttom)
    slider_left = app.canvas_plot_left_slider
    value_left = slider_left.slider.value()
    slider_left.set_range(value_left)
```

5. Save the new range in the global data.
```
def cut_slider(self):
    app = QApplication.activeWindow()

    slider_bottom = app.canvas_plot_bottom_slider
    value_buttom = slider_bottom.slider.value()
    slider_bottom.set_range(value_buttom)
    slider_left = app.canvas_plot_left_slider
    value_left = slider_left.slider.value()
    slider_left.set_range(value_left)

    app.plot_points.set_x_range([value_buttom[0],value_buttom[1]])
    app.plot_points.set_y_range([value_left[0],value_left[1]])
```

6. Fix all posible bugs...

7. Commit and Push... https://github.com/Kuellar/CUTA/commit/39e70c83099def9003f433413563495d859f4c22


### Previous step
---

- [Create a class for the button](./Tutorial_4_Create_a_class.md)

### Next step
---

- [Create a Pull request](./Tutorial_6_Pull_request.md)
