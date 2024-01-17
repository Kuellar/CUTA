class Points:
    def __init__(self):
        self.x = []
        self.y = []
        self.error = []
        self.x_border = [None, None]
        self.y_border = [None, None]

    def __init__(self, x: list[float], y: list[float], error: list[float]):
        self.x = x
        self.y = y
        self.error = error
        self.x_border = [min(x), max(x)]
        self.y_border = [min(y), max(y)]
