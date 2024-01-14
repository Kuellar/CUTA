from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
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

    def update_plot(self, xdata, ydata, zdata, settings):
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

        self.draw()
