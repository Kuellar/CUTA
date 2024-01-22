class Points:
    def __init__(
        self, x: list[float] = None, y: list[float] = None, error: list[float] = None
    ) -> None:
        self.x = x
        self.y = y
        self.error = error
        self.x_border = [
            min(x) if x is not None else None,
            max(x) if x is not None else None,
        ]
        self.y_border = [
            min(y) if y is not None else None,
            max(y) if y is not None else None,
        ]
