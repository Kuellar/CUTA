from qtpy.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QFormLayout,
    QVBoxLayout,
    QComboBox,
    QApplication,
    QLineEdit,
    QCheckBox,
)
from superqt import QDoubleSlider
from widgets.collapsible_box import CollapsibleBox
from utils import check_number


class MplPlotVertical(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        box = CollapsibleBox("Plot vertical")
        layout.addWidget(box)
        box_layout = QFormLayout()

        # Add filename
        self.filename_mpl = QLineEdit("")
        self.filename_mpl.setReadOnly(True)
        box_layout.addRow("Filename:", self.filename_mpl)

        # Add Plot Vertical Color
        self.plot_vertical_color_mpl = QComboBox()
        self.plot_vertical_color_mpl.addItems(
            ["blue", "green", "red", "cyan", "magenta", "yellow", "black", "white"]
        )
        self.plot_vertical_color_mpl.currentTextChanged.connect(self.change_color)
        box_layout.addRow("Plot Color:", self.plot_vertical_color_mpl)

        # Show Label
        self.show_label_mpl = QCheckBox()
        self.show_label_mpl.setChecked(True)
        self.show_label_mpl.stateChanged.connect(self.show_label)
        box_layout.addRow("Show Label:", self.show_label_mpl)

        # Add Label Color
        self.plot_label_color_mpl = QComboBox()
        self.plot_label_color_mpl.addItems(
            ["black", "blue", "green", "red", "cyan", "magenta", "yellow", "white"]
        )
        self.plot_label_color_mpl.currentTextChanged.connect(self.change_label_color)
        box_layout.addRow("Label Color:", self.plot_label_color_mpl)

        # Add label position
        self.label_pos_mpl = QLineEdit("0.1")
        self.label_pos_mpl.textChanged.connect(self.change_label_pos)
        box_layout.addRow("Label Position [0,1]:", self.label_pos_mpl)

        # Add z value
        self.z_mpl = QLineEdit("0")
        self.z_mpl.textChanged.connect(self.change_z)
        box_layout.addRow("z:", self.z_mpl)

        self.min_z = None
        self.max_z = None
        self.z_slider = QDoubleSlider(Qt.Orientation.Horizontal)
        box_layout.addWidget(self.z_slider)
        self.z_slider.sliderReleased.connect(self.slider_released)

        box.setContentLayout(box_layout)

    def change_color(self, new_color):
        app = QApplication.activeWindow()
        app.plot_horizo.set_colors(new_color)
        app.canvas_plot.update_plot()

    def show_label(self, flag):
        app = QApplication.activeWindow()
        app.plot_horizo.set_show_names(bool(flag))
        if not flag:
            app.canvas_plot.remove_texts()
        app.canvas_plot.update_plot()

    def change_label_color(self, new_color):
        app = QApplication.activeWindow()
        app.plot_horizo.set_label_colors(new_color)
        app.canvas_plot.update_plot()

    def change_label_pos(self, new_pos):
        if not check_number(new_pos):
            return
        new_pos = float(new_pos)
        new_pos = max(new_pos, 0)
        new_pos = min(new_pos, 1)
        app = QApplication.activeWindow()
        app.plot_horizo.set_names_y(new_pos)
        app.canvas_plot.remove_texts()
        app.canvas_plot.draw_texts()

    def change_z(self, new_z):
        if not check_number(new_z):
            return
        new_z = float(new_z)
        app = QApplication.activeWindow()
        app.plot_horizo.set_z(new_z)
        self.show_label_mpl.setChecked(False)
        app.canvas_plot.update_plot()
        if self.min_z < new_z < self.max_z:
            self.z_slider.setValue(new_z)

    def slider_released(self):
        self.z_mpl.setText(f"{self.z_slider.value():.4f}")

    def set_new_file(self, filename):
        app = QApplication.activeWindow()
        self.filename_mpl.setText(filename)
        self.z_mpl.setText("0")
        range_x = app.plot_points.x_range_original
        self.min_z = range_x[0] / app.plot_horizo.x[-1] - 1
        self.max_z = range_x[1] / app.plot_horizo.x[0] - 1
        self.z_slider.setRange(self.min_z, self.max_z)
        self.z_slider.setValue(0)
