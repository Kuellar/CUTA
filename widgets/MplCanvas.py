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

        # Data
        self.pointPlot = None
        self.horizoPlot = None

        # Settings
        self.globalSettings = None
        self.plotSettings = None
        self.verticalSettings = None

        #  Flags
        self.mousePressed = False
        self.zoomInit = None
        self.zoomRectangle = None
        self.moveInit = None
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
            and self.parent.buttonSettings.active == "zoom"
        ):
            if event.xdata and event.ydata:
                self.mousePressed = True
                self.zoomInit = [event.xdata, event.ydata]

        if (
            event.button is MouseButton.LEFT
            and self.parent.buttonSettings.active == "move"
        ):
            if event.xdata and event.ydata:
                self.mousePressed = True
                self.moveInit = [event.xdata, event.ydata]

    def button_release_event(self, event):
        app = QApplication.activeWindow()
        if (
            event.button is MouseButton.LEFT
            and self.parent.buttonSettings.active == "zoom"
        ):
            self.mousePressed = False
            if self.zoomRectangle:
                if (
                    self.zoomInit[0] != event.xdata
                    and event.xdata
                    and event.ydata
                    and self.zoomInit[1] != event.ydata
                ):
                    valueX = [
                        min(self.zoomInit[0], event.xdata),
                        max(self.zoomInit[0], event.xdata),
                    ]
                    valueY = [
                        min(self.zoomInit[1], event.ydata),
                        max(self.zoomInit[1], event.ydata),
                    ]
                    # Set limits in canvas
                    app.plotPoints.set_x_limit(valueX)
                    self.update_xlim()
                    app.plotPoints.set_y_limit(valueY)
                    self.update_ylim()
                    # Set limits slider
                    app.canvasPlotBottomSlider.setValue(valueX)
                    app.canvasPlotLeftSlider.setValue(valueY)

                # Clean
                self.zoomRectangle.remove()
                self.zoomRectangle = None
                self.zoomInit = None
                self.draw_texts()

        if (
            event.button is MouseButton.LEFT
            and self.parent.buttonSettings.active == "move"
        ):
            self.mousePressed = False

    def on_move(self, event):
        app = QApplication.activeWindow()
        if (
            event.inaxes
            and self.fig.canvas.mousePressed
            and self.parent.buttonSettings.active == "zoom"
        ):
            if self.zoomInit:
                if self.zoomRectangle:
                    self.zoomRectangle.remove()
                self.zoomRectangle = self.axes.add_patch(
                    Rectangle(
                        (self.zoomInit[0], self.zoomInit[1]),
                        event.xdata - self.zoomInit[0],
                        event.ydata - self.zoomInit[1],
                        fill=False,
                        linestyle="--",
                    )
                )
                self.draw()

        if (
            event.inaxes
            and self.fig.canvas.mousePressed
            and self.parent.buttonSettings.active == "move"
        ):
            if self.moveInit:
                x_moved = -(event.xdata - self.moveInit[0]) / 2
                y_moved = -(event.ydata - self.moveInit[1]) / 2
                new_xlimit = [
                    self.axes.get_xlim()[0] + x_moved,
                    self.axes.get_xlim()[1] + x_moved,
                ]
                new_ylimit = [
                    self.axes.get_ylim()[0] + y_moved,
                    self.axes.get_ylim()[1] + y_moved,
                ]
                x_original = app.plotPoints.x_range
                y_original = app.plotPoints.y_range

                if new_xlimit[0] > x_original[0] and new_xlimit[1] < x_original[1]:
                    app.plotPoints.set_x_limit(new_xlimit)
                    self.update_xlim()
                    # Set limits slider
                    app.canvasPlotBottomSlider.setValue(new_xlimit)

                if new_ylimit[0] > y_original[0] and new_ylimit[1] < y_original[1]:
                    app.plotPoints.set_y_limit(new_ylimit)
                    self.update_ylim()
                    # Set limits slider
                    app.canvasPlotLeftSlider.setValue(new_ylimit)

                self.moveInit = [event.xdata, event.ydata]
                self.draw_texts()

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

        if self.axes.get_xlim() is not app.plotPoints.x_limit:
            self.axes.set_xlim(app.plotPoints.x_limit)
            self.draw()

    def update_ylim(self):
        app = QApplication.activeWindow()
        if not app:
            return

        if self.axes.get_ylim() is not app.plotPoints.y_limit:
            self.axes.set_ylim(app.plotPoints.y_limit)
            self.draw()

    def draw_texts(self):
        for text in self.axes.texts:
            text.remove()
        if self.horizoPlot:
            base_pos = (
                self.axes.get_ylim()[0]
                + (self.axes.get_ylim()[1] - self.axes.get_ylim()[0])
                * self.horizoPlot.names_y
            )
            last_text = None
            for name_i, x in enumerate(
                [(1 + self.horizoPlot.z) * elem for elem in self.horizoPlot.x]
            ):
                if x > self.pointPlot.x_limit[0] and x < self.pointPlot.x_limit[1]:
                    last_text = self.axes.text(
                        x,
                        base_pos,
                        self.horizoPlot.names[name_i],
                        color=self.horizoPlot.label_colors,
                    )
                    self.draw()

                    # Check if collide with other text
                    last_text_bbox = self.axes.transData.inverted().transform_bbox(
                        last_text.get_window_extent()
                    )
                    bbox = None

                    for text in self.axes.texts[:-1]:
                        bbox = self.axes.transData.inverted().transform_bbox(
                            text.get_window_extent()
                        )
                        if (
                            last_text_bbox.x0 >= bbox.x0
                            and last_text_bbox.x0 <= bbox.x1
                            and last_text_bbox.y0 == bbox.y0
                        ):
                            last_text.set_position(
                                (x, last_text.get_position()[1] + bbox.y1 - bbox.y0)
                            )
                            self.draw()
                            last_text_bbox = (
                                self.axes.transData.inverted().transform_bbox(
                                    last_text.get_window_extent()
                                )
                            )
                        elif (
                            last_text_bbox.x1 >= bbox.x0
                            and last_text_bbox.x1 <= bbox.x1
                            and last_text_bbox.y0 == bbox.y0
                        ):
                            last_text.set_position(
                                (x, last_text.get_position()[1] + bbox.y1 - bbox.y0)
                            )
                            self.draw()
                            last_text_bbox = (
                                self.axes.transData.inverted().transform_bbox(
                                    last_text.get_window_extent()
                                )
                            )

    def update_plot(self):
        app = QApplication.activeWindow()
        if not app:
            return

        self.parent.canvasPlotBottomSlider.setRange(app.plotPoints.x_range)
        self.parent.canvasPlotLeftSlider.setRange(app.plotPoints.y_range)

        # New data is plotted
        self.axes.cla()
        if app.plotPoints.show_error:
            self.axes.errorbar(
                app.plotPoints.points.x,
                app.plotPoints.points.y,
                yerr=app.plotPoints.points.error,
                ecolor=app.plotPoints.error_color,
                color=app.plotPoints.color,
                linestyle=app.plotPoints.plot_line,
                marker=app.plotPoints.marker,
                markeredgecolor=app.plotPoints.marker_color,
                markerfacecolor=app.plotPoints.marker_color,
                drawstyle=app.plotPoints.drawstyle,
            )
        else:
            self.axes.plot(
                app.plotPoints.points.x,
                app.plotPoints.points.y,
                color=app.plotPoints.color,
                linestyle=app.plotPoints.plot_line,
                marker=app.plotPoints.marker,
                markeredgecolor=app.plotPoints.marker_color,
                markerfacecolor=app.plotPoints.marker_color,
                drawstyle=app.plotPoints.drawstyle,
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
        if app.plotHorizo:
            self.axes.vlines(
                x=[(1 + app.plotHorizo.z) * elem for elem in app.plotHorizo.x],
                ymin=app.plotPoints.y_range[0],
                ymax=app.plotPoints.y_range[1],
                linestyles=app.plotHorizo.linestyles,
                colors=app.plotHorizo.colors,
                linewidth=app.plotHorizo.width,
            )

        # Fix lim
        self.update_xlim()
        self.update_ylim()
        self.draw_texts()

    def init_plot(self, plotPoints):
        self.axes.plot(
            plotPoints.points.x,
            plotPoints.points.y,
            color="blue",
        )
        # Fix lim
        self.parent.canvasPlotBottomSlider.setRange(plotPoints.x_range)
        self.parent.canvasPlotLeftSlider.setRange(plotPoints.y_range)
        self.axes.set_xlim(plotPoints.x_limit)
        self.axes.set_ylim(plotPoints.y_limit)
