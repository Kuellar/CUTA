from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.backend_bases import MouseButton
from matplotlib.patches import Rectangle
from data import PlotPoints


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, window=None, width=5, height=4, dpi=100):
        self.parent = window
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        self.pointPlot = None
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
                    self.change_xlim(valueX)
                    self.change_ylim(valueY)
                    # Set limits slider
                    self.parent.canvasPlotBottomSlider.setValue(valueX)
                    self.parent.canvasPlotLeftSlider.setValue(valueY)

                # Clean
                self.zoomRectangle.remove()
                self.zoomRectangle = None
                self.zoomInit = None
                self.draw()

        if (
            event.button is MouseButton.LEFT
            and self.parent.buttonSettings.active == "move"
        ):
            self.mousePressed = False

    def on_move(self, event):
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
                x_original = self.parent.canvasPlotBottomSlider.getRange()
                y_original = self.parent.canvasPlotLeftSlider.getRange()

                if new_xlimit[0] > x_original[0] and new_xlimit[1] < x_original[1]:
                    self.pointPlot.set_x_limit(new_xlimit)
                    self.change_xlim(new_xlimit)
                    # Set limits in canvas
                    self.change_xlim(new_xlimit)
                    # Set limits slider
                    self.parent.canvasPlotBottomSlider.setValue(new_xlimit)

                if new_ylimit[0] > y_original[0] and new_ylimit[1] < y_original[1]:
                    self.pointPlot.set_y_limit(new_ylimit)
                    self.change_ylim(new_ylimit)
                    # Set limits in canvas
                    self.change_ylim(new_ylimit)
                    # Set limits slider
                    self.parent.canvasPlotLeftSlider.setValue(new_ylimit)

                self.moveInit = [event.xdata, event.ydata]

    def change_title(self, new_title):
        self.axes.set_title(new_title)
        self.draw()

    def change_xlabel(self, new_xlabel):
        self.axes.set_xlabel(new_xlabel)
        self.draw()

    def change_ylabel(self, new_ylabel):
        self.axes.set_ylabel(new_ylabel)
        self.draw()

    def change_drawstyle(self, new_drawstyle):
        self.axes.get_lines()[0].set_drawstyle(new_drawstyle)
        self.draw()

    def change_xlim(self, new_xlim):
        if self.axes.get_xlim() is not new_xlim:
            self.axes.set_xlim(new_xlim)
            self.draw()

    def change_ylim(self, new_ylim):
        if self.axes.get_ylim() is not new_ylim:
            self.axes.set_ylim(new_ylim)
            self.draw()

    def change_xscale(self, new_xscale):
        self.axes.set_xscale(new_xscale)
        self.draw()

    def change_yscale(self, new_yscale):
        self.axes.set_yscale(new_yscale)
        self.draw()

    def show_grid(self, show=True):
        self.axes.grid(show)
        self.draw()

    def update_plot(self, plotPoints: PlotPoints, globalSettings, specificSettings):
        self.pointPlot = plotPoints

        self.parent.canvasPlotBottomSlider.setRange(plotPoints.x_range)
        self.parent.canvasPlotLeftSlider.setRange(plotPoints.y_range)

        # New data is plotted
        self.axes.cla()
        if specificSettings.showErrorMpl.isChecked():
            self.axes.errorbar(
                plotPoints.points.x,
                plotPoints.points.y,
                yerr=plotPoints.points.error,
                ecolor=specificSettings.errorColorMpl.currentText(),
                color=specificSettings.plotColorMpl.currentText(),
                linestyle=specificSettings.plotLineMpl.currentText(),
                marker=specificSettings.plotMarkerMpl.currentText(),
                markeredgecolor=specificSettings.plotMarkerColorMpl.currentText(),
                markerfacecolor=specificSettings.plotMarkerColorMpl.currentText(),
                drawstyle=specificSettings.drawStyleMpl.currentText(),
            )
        else:
            self.axes.plot(
                plotPoints.points.x,
                plotPoints.points.y,
                color=specificSettings.plotColorMpl.currentText(),
                linestyle=specificSettings.plotLineMpl.currentText(),
                marker=specificSettings.plotMarkerMpl.currentText(),
                markeredgecolor=specificSettings.plotMarkerColorMpl.currentText(),
                markerfacecolor=specificSettings.plotMarkerColorMpl.currentText(),
                drawstyle=specificSettings.drawStyleMpl.currentText(),
            )

        # Check all matplotlib configurations
        title = globalSettings.titleMpl.text()
        self.axes.set_title(title)
        xlabel = globalSettings.xlabelMpl.text()
        self.axes.set_xlabel(xlabel)
        ylabel = globalSettings.ylabelMpl.text()
        self.axes.set_ylabel(ylabel)
        self.axes.grid(globalSettings.showGridMpl.isChecked())
        self.axes.set_xscale(globalSettings.xscaleMpl.currentText())
        self.axes.set_yscale(globalSettings.yscaleMpl.currentText())

        self.draw()
