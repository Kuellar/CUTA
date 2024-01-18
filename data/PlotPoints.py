from .Points import Points


RANGE = 5 / 100


class PlotPoints:
    def __init__(self, name: str, points: Points) -> None:
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
        self.x_limit = self.x_range
        self.y_limit = self.y_range

    def set_x_limit(self, new_x_limit: list[float]) -> None:
        self.x_limit = new_x_limit

    def set_y_limit(self, new_y_limit: list[float]) -> None:
        self.y_limit = new_y_limit
