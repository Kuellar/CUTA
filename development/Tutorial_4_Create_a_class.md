## Create a class for the button

1. Create a file for the button class /widget/cut_button.py

2. Create a class. ("fa5s.cut" is the icon)

```
from widgets.custom_button import CustomButton


class CutButton(CustomButton):
    def __init__(self):
        super().__init__("fa5s.cut")

```

3. Change the button from the previous step (app.py)
```
30  from widgets.cut_button import CutButton
...
81  canvas_plot_cut_button = CutButton()
```

4. Rename the style in ui/style.css
```
CutButton {
  max-width: 25px;
  max-height: 25px;
  margin-left: 10px;
  margin-bottom: 10px;
}
```

5. Everything should look the same.

6. Commit and Push... https://github.com/Kuellar/CUTA/commit/cbe823a586329a16e288678253d4761478bfcd14

### Previous step
---

- [Create a button](./Tutorial_3_Create_a_button.md)

### Next step
---

- [Make the button do things](./Tutorial_5_Settings_button.md)