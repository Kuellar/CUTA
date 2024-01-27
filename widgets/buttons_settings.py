from datetime import datetime
from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QStyleOption, QStyle, QApplication
from PyQt6.QtCore import Qt, QSize
from .custom_button import CustomButton


class ButtonsSettings(QWidget):
    def __init__(self):
        super().__init__()
        self.icon_size = QSize(48, 48)
        self.buttons_settings_layout = QHBoxLayout()
        self.buttons_settings_layout.setContentsMargins(0, 0, 0, 0)
        self.buttons_settings_layout.setSpacing(0)
        self.setLayout(self.buttons_settings_layout)

        # Permissions: "move", "zoom"
        self.active = None

        # Stretch
        self.buttons_settings_layout.addStretch()

        # Set square
        self.square_button = CustomButton("fa5.square")
        self.square_button.clicked.connect(self.set_square)
        self.buttons_settings_layout.addWidget(self.square_button, Qt.AlignCenter)

        # Move
        self.move_button = CustomButton("fa5.hand-paper")
        self.move_button.clicked.connect(self.allow_move)
        self.buttons_settings_layout.addWidget(self.move_button, Qt.AlignCenter)

        # Zoom
        self.zoom_button = CustomButton("fa5s.search")
        self.zoom_button.clicked.connect(self.allow_zoom)
        self.buttons_settings_layout.addWidget(self.zoom_button, Qt.AlignCenter)

        # Return
        self.return_button = CustomButton("fa5s.undo")
        self.return_button.clicked.connect(self.set_original)
        self.buttons_settings_layout.addWidget(self.return_button, Qt.AlignCenter)

        # ScreenShot
        self.screenshot_button = CustomButton("fa5s.camera")
        self.screenshot_button.clicked.connect(self.take_screenshot)
        self.buttons_settings_layout.addWidget(self.screenshot_button, Qt.AlignCenter)

        # Stretch
        self.buttons_settings_layout.addStretch()

    def set_square(self):
        app = QApplication.activeWindow()
        self.move_button.set_active(False)
        self.zoom_button.set_active(False)
        self.active = None

        old_height = app.canvas_plot_grid_height
        new_height = app.canvas_plot_grid.frameGeometry().height()
        new_width_all = (
            app.canvas_workspace_layout_splitter.sizes()[0]
            + app.canvas_workspace_layout_splitter.sizes()[1]
        )
        new_plot_width = app.ratio_plot_settings[0] * new_height / old_height
        new_sett_width = new_width_all - new_plot_width
        app.canvas_workspace_layout_splitter.setSizes(
            [int(new_plot_width), int(new_sett_width)]
        )

    def allow_move(self):
        if self.active != "move":
            self.active = "move"
            self.move_button.set_active()
            self.zoom_button.set_active(False)
        else:
            self.active = None
            self.move_button.set_active(False)

    def allow_zoom(self):
        if self.active != "zoom":
            self.active = "zoom"
            self.zoom_button.set_active()
            self.move_button.set_active(False)
        else:
            self.active = None
            self.zoom_button.set_active(False)

    def set_original(self):
        self.move_button.set_active(False)
        self.zoom_button.set_active(False)
        self.active = None

        app = QApplication.activeWindow()
        x_original = app.plot_points.x_range_original
        y_original = app.plot_points.y_range_original
        app.plot_points.set_x_range(x_original)
        app.plot_points.set_y_range(y_original)
        app.plot_points.set_x_limit(x_original)
        app.plot_points.set_y_limit(y_original)
        app.canvas_plot_bottom_slider.set_value(x_original)
        app.canvas_plot_left_slider.set_value(y_original)
        app.canvas_plot.update_xlim()
        app.canvas_plot.update_ylim()
        app.canvas_plot.remove_texts()
        app.canvas_plot.draw_texts()

    def take_screenshot(self):
        app = QApplication.activeWindow()

        self.move_button.set_active(False)
        self.zoom_button.set_active(False)
        self.active = None
        name_file = (
            app.last_dir_open
            + "/"
            + app.plot_points.name.split(".")[0]
            + "-"
            + datetime.now().strftime("%b:%-d-%H:%M:%S")
        )
        if (
            app.last_dir_open
            and app.last_file_open
            and app.plot_points.name != "Start Plot"
        ):
            app.canvas_plot.fig.savefig(name_file)
            app.reload_files()
            app.open_image(name_file)

    def paintEvent(self, _):  # pylint: disable=C0103
        o = QStyleOption()
        o.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, o, p, self)
