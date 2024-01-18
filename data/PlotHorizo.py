class PlotHorizo:
    def __init__(self, names: list[str], x: list[float], z: float = 0.0) -> None:
        self.names = names
        self.names_y = 0.25
        self.names_color = "black"
        self.x = x
        self.z = z
        self.linestyles = "--"
        self.colors = "blue"
        self.width = 1
