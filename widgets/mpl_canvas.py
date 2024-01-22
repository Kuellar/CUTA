from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.backend_bases import MouseButton
from matplotlib.patches import Rectangle
from PyQt6.QtWidgets import QApplication


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, window=None, width=5, height=4, dpi=100):
        self.parent = window
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)

        #  Flags
        self.mouse_pressed = False
        self.zoom_init = None
        self.zoom_rectangle = None
        self.move_init = None
        super().__init__(self.fig)

        # Connect events
        self.figure.canvas.mpl_connect("motion_notify_event", self.on_move)
        self.figure.canvas.mpl_connect("button_press_event", self.button_press_event)
        self.figure.canvas.mpl_connect(
            "button_release_event", self.button_release_event
        )

    def button_press_event(self, event):
        if (
            event.button is MouseButton.LEFT
            and self.parent.button_settings.active == "zoom"
        ):
            if event.xdata and event.ydata:
                self.mouse_pressed = True
                self.zoom_init = [event.xdata, event.ydata]

        if (
            event.button is MouseButton.LEFT
            and self.parent.button_settings.active == "move"
        ):
            if event.xdata and event.ydata:
                self.mouse_pressed = True
                self.move_init = [event.xdata, event.ydata]
                self.remove_texts()

    def button_release_event(self, event):
        app = QApplication.activeWindow()
        if (
            event.button is MouseButton.LEFT
            and self.parent.button_settings.active == "zoom"
        ):
            self.mouse_pressed = False
            if self.zoom_rectangle:
                if (
                    self.zoom_init[0] != event.xdata
                    and event.xdata
                    and event.ydata
                    and self.zoom_init[1] != event.ydata
                ):
                    value_x = [
                        min(self.zoom_init[0], event.xdata),
                        max(self.zoom_init[0], event.xdata),
                    ]
                    value_y = [
                        min(self.zoom_init[1], event.ydata),
                        max(self.zoom_init[1], event.ydata),
                    ]
                    # Set limits in canvas
                    app.plot_points.set_x_limit(value_x)
                    self.update_xlim()
                    app.plot_points.set_y_limit(value_y)
                    self.update_ylim()
                    # Set limits slider
                    app.canvas_plot_bottom_slider.set_value(value_x)
                    app.canvas_plot_left_slider.set_value(value_y)

                # Clean
                self.zoom_rectangle.remove()
                self.zoom_rectangle = None
                self.zoom_init = None
                self.remove_texts()
                self.draw_texts()

        if (
            event.button is MouseButton.LEFT
            and self.parent.button_settings.active == "move"
        ):
            self.mouse_pressed = False
            self.draw_texts()

    def on_move(self, event):
        app = QApplication.activeWindow()
        if (
            event.inaxes
            and self.mouse_pressed
            and self.parent.button_settings.active == "zoom"
        ):
            if self.zoom_init:
                if self.zoom_rectangle:
                    self.zoom_rectangle.remove()
                self.zoom_rectangle = self.axes.add_patch(
                    Rectangle(
                        (self.zoom_init[0], self.zoom_init[1]),
                        event.xdata - self.zoom_init[0],
                        event.ydata - self.zoom_init[1],
                        fill=False,
                        linestyle="--",
                    )
                )
                self.draw()

        if (
            event.inaxes
            and self.mouse_pressed
            and self.parent.button_settings.active == "move"
        ):
            if self.move_init:
                x_moved = -(event.xdata - self.move_init[0]) / 2
                y_moved = -(event.ydata - self.move_init[1]) / 2
                new_xlimit = [
                    self.axes.get_xlim()[0] + x_moved,
                    self.axes.get_xlim()[1] + x_moved,
                ]
                new_ylimit = [
                    self.axes.get_ylim()[0] + y_moved,
                    self.axes.get_ylim()[1] + y_moved,
                ]
                x_original = app.plot_points.x_range
                y_original = app.plot_points.y_range

                if new_xlimit[0] > x_original[0] and new_xlimit[1] < x_original[1]:
                    app.plot_points.set_x_limit(new_xlimit)
                    self.update_xlim()
                    # Set limits slider
                    app.canvas_plot_bottom_slider.set_value(new_xlimit)

                if new_ylimit[0] > y_original[0] and new_ylimit[1] < y_original[1]:
                    app.plot_points.set_y_limit(new_ylimit)
                    self.update_ylim()
                    # Set limits slider
                    app.canvas_plot_left_slider.set_value(new_ylimit)

                self.move_init = [event.xdata, event.ydata]

    def update_plot_settings(self):
        app = QApplication.activeWindow()
        if not app:
            return

        self.axes.set_title(app.plot.title)
        self.axes.set_xlabel(app.plot.xlabel)
        self.axes.set_ylabel(app.plot.ylabel)
        self.axes.set_xscale(app.plot.xscale)
        self.axes.set_yscale(app.plot.yscale)
        self.axes.grid(app.plot.show_grid)

        self.draw()

    def update_xlim(self):
        app = QApplication.activeWindow()
        if not app:
            return

        if self.axes.get_xlim() is not app.plot_points.x_limit:
            self.axes.set_xlim(app.plot_points.x_limit)
            self.draw()

    def update_ylim(self):
        app = QApplication.activeWindow()
        if not app:
            return

        if self.axes.get_ylim() is not app.plot_points.y_limit:
            self.axes.set_ylim(app.plot_points.y_limit)
            self.draw()

    def remove_texts(self):
        for text in self.axes.texts:
            text.remove()

    def draw_texts(self):
        app = QApplication.activeWindow()
        if app.plot_horizo and app.plot_horizo.show_names:
            base_pos = (
                self.axes.get_ylim()[0]
                + (self.axes.get_ylim()[1] - self.axes.get_ylim()[0])
                * app.plot_horizo.names_y
            )
            new_text = None
            used_space = [-1] * len(app.plot_horizo.x)
            last_valid = None
            init_list = None

            for name_i, x in enumerate(
                [(1 + app.plot_horizo.z) * elem for elem in app.plot_horizo.x]
            ):
                if app.plot_points.x_limit[0] < x < app.plot_points.x_limit[1]:
                    # print(app.plot_horizo.names[name_i], name_i, x)
                    if not new_text:
                        used_space[0] = name_i
                        init_list = name_i
                        last_valid = name_i
                        new_text = self.axes.text(
                            x,
                            base_pos,
                            app.plot_horizo.names[name_i],
                            color=app.plot_horizo.label_colors,
                        )
                        continue

                    new_text = self.axes.text(
                        x,
                        base_pos,
                        app.plot_horizo.names[name_i],
                        color=app.plot_horizo.label_colors,
                    )
                    new_text_bbox = self.axes.transData.inverted().transform_bbox(
                        new_text.get_window_extent()
                    )

                    # Check collision
                    coll = False
                    for j, old_text in enumerate(
                        self.axes.texts[last_valid - init_list : -1]
                    ):
                        if coll:
                            break
                        # print(old_text.get_text())
                        old_text_bbox = self.axes.transData.inverted().transform_bbox(
                            old_text.get_window_extent()
                        )
                        if (
                            new_text_bbox.x0 >= old_text_bbox.x0
                            and new_text_bbox.x0 <= old_text_bbox.x1
                        ):
                            coll = True
                            last_valid = j + last_valid
                            # print("Collision, check last valid: ", last_valid)
                            for i, val in enumerate(used_space):
                                if val < last_valid:
                                    used_space[i] = name_i
                                    new_text.set_position(
                                        (
                                            x,
                                            base_pos
                                            + (new_text_bbox.y1 - new_text_bbox.y0) * i,
                                        )
                                    )
                                    break
                    if not coll:
                        last_valid = name_i
                        used_space[0] = name_i

                    # print(used_space, init_list, last_valid)
        self.draw()

    def update_plot(self):
        app = QApplication.activeWindow()
        if not app:
            return

        self.parent.canvas_plot_bottom_slider.set_range(app.plot_points.x_range)
        self.parent.canvas_plot_left_slider.set_range(app.plot_points.y_range)

        # New data is plotted
        self.axes.cla()
        if app.plot_points.show_error:
            self.axes.errorbar(
                app.plot_points.points.x,
                app.plot_points.points.y,
                yerr=app.plot_points.points.error,
                ecolor=app.plot_points.error_color,
                color=app.plot_points.color,
                linestyle=app.plot_points.plot_line,
                marker=app.plot_points.marker,
                markeredgecolor=app.plot_points.marker_color,
                markerfacecolor=app.plot_points.marker_color,
                drawstyle=app.plot_points.drawstyle,
            )
        else:
            self.axes.plot(
                app.plot_points.points.x,
                app.plot_points.points.y,
                color=app.plot_points.color,
                linestyle=app.plot_points.plot_line,
                marker=app.plot_points.marker,
                markeredgecolor=app.plot_points.marker_color,
                markerfacecolor=app.plot_points.marker_color,
                drawstyle=app.plot_points.drawstyle,
            )

        # Check all matplotlib configurations
        self.axes.set_title(app.plot.title)
        self.axes.set_title(app.plot.title)
        self.axes.set_xlabel(app.plot.xlabel)
        self.axes.set_ylabel(app.plot.ylabel)
        self.axes.set_xscale(app.plot.xscale)
        self.axes.set_yscale(app.plot.yscale)
        self.axes.grid(app.plot.show_grid)

        # Check horizo
        if app.plot_horizo:
            self.axes.vlines(
                x=[(1 + app.plot_horizo.z) * elem for elem in app.plot_horizo.x],
                ymin=app.plot_points.y_range[0],
                ymax=app.plot_points.y_range[1],
                linestyles=app.plot_horizo.linestyles,
                colors=app.plot_horizo.colors,
                linewidth=app.plot_horizo.width,
            )

        # Fix lim
        self.update_xlim()
        self.update_ylim()
        self.remove_texts()
        if app.plot_horizo.show_names:
            self.draw_texts()

    def init_plot(self, plot_points):
        self.axes.plot(
            plot_points.points.x,
            plot_points.points.y,
            color="blue",
        )
        # Fix lim
        self.parent.canvas_plot_bottom_slider.set_range(plot_points.x_range)
        self.parent.canvas_plot_left_slider.set_range(plot_points.y_range)
        self.axes.set_xlim(plot_points.x_limit)
        self.axes.set_ylim(plot_points.y_limit)
