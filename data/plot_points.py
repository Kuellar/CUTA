from .points import Points


RANGE = 5 / 100


class PlotPoints:
    def __init__(
        self,
        name: str,
        points: Points,
        color: str = "blue",
        plot_line: str = "-",
        marker: str = "",
        marker_color: str = "blue",
        show_error: bool = False,
        error_color: str = "blue",
        drawstyle: str = "default",
    ) -> None:
        self.name = name
        self.points = points
        self.x_range = [
            points.x_border[0] - (points.x_border[1] - points.x_border[0]) * RANGE,
            points.x_border[1] + (points.x_border[1] - points.x_border[0]) * RANGE,
        ]
        self.y_range = [
            points.y_border[0] - (points.y_border[1] - points.y_border[0]) * RANGE,
            points.y_border[1] + (points.y_border[1] - points.y_border[0]) * RANGE,
        ]
        self.x_range_original = self.x_range
        self.y_range_original = self.y_range
        self.x_limit = self.x_range
        self.y_limit = self.y_range
        self.color = color
        self.plot_line = plot_line
        self.marker = marker
        self.marker_color = marker_color
        self.show_error = show_error
        self.error_color = error_color
        self.drawstyle = drawstyle

    def set_x_range(self, new_x_range: list[float]) -> None:
        self.x_range = new_x_range

    def set_y_range(self, new_y_range: list[float]) -> None:
        self.y_range = new_y_range

    def set_x_limit(self, new_x_limit: list[float]) -> None:
        self.x_limit = new_x_limit

    def set_y_limit(self, new_y_limit: list[float]) -> None:
        self.y_limit = new_y_limit

    def set_color(self, new_color: str) -> None:
        self.color = new_color

    def set_plot_line(self, new_plot_line: str) -> None:
        self.plot_line = new_plot_line

    def set_marker(self, new_marker: str) -> None:
        self.marker = new_marker

    def set_marker_color(self, new_marker_color: str) -> None:
        self.marker_color = new_marker_color

    def set_show_error(self, new_show_error: bool) -> None:
        self.show_error = new_show_error

    def set_error_color(self, new_error_color: str) -> None:
        self.error_color = new_error_color

    def set_drawstyle(self, new_draw_style: str) -> None:
        self.drawstyle = new_draw_style
