from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, window=None, width=5, height=4, dpi=100):
        self.parent = window
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.xlimit = None
        self.ylimit = None
        super().__init__(fig)

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

    def show_grid(self, show=True):
        self.axes.grid(show)
        self.draw()

    def update_plot(self, xdata, ydata, zdata, settings, xlimit=None, ylimit=None):
        if xlimit:
            self.xlimit = xlimit
            self.parent.canvasPlotBottomSlider.setRange(xlimit)
        if ylimit:
            self.ylimit = ylimit
            self.parent.canvasPlotLeftSlider.setRange(ylimit)

        # New data is plotted
        self.axes.cla()
        if settings.showErrorMpl.isChecked():
            self.axes.errorbar(
                xdata,
                ydata,
                yerr=zdata,
                ecolor=settings.errorColorMpl.currentText(),
                color=settings.plotColorMpl.currentText(),
                linestyle=settings.plotLineMpl.currentText(),
                marker=settings.plotMarkerMpl.currentText(),
                markeredgecolor=settings.plotMarkerColorMpl.currentText(),
                markerfacecolor=settings.plotMarkerColorMpl.currentText(),
                drawstyle=settings.drawStyleMpl.currentText(),
            )
        else:
            self.axes.plot(
                xdata,
                ydata,
                color=settings.plotColorMpl.currentText(),
                linestyle=settings.plotLineMpl.currentText(),
                marker=settings.plotMarkerMpl.currentText(),
                markeredgecolor=settings.plotMarkerColorMpl.currentText(),
                markerfacecolor=settings.plotMarkerColorMpl.currentText(),
                drawstyle=settings.drawStyleMpl.currentText(),
            )

        # Check all matplotlib configurations
        title = settings.titleMpl.text()
        self.axes.set_title(title)
        xlabel = settings.xlabelMpl.text()
        self.axes.set_xlabel(xlabel)
        ylabel = settings.ylabelMpl.text()
        self.axes.set_ylabel(ylabel)
        self.axes.grid(settings.showGridMpl.isChecked())

        self.draw()
