class PlotHorizo:
    def __init__(self, names: list[str], x: list[float], z: float = 0.0) -> None:
        self.names = names
        self.names_y = 0.25
        self.names_color = "black"
        self.x = x
        self.z = z
        self.linestyles = "--"
        self.colors = "blue"
        self.label_colors = "black"
        self.width = 1

    def set_colors(self, color: str) -> None:
        self.colors = color

    def set_label_colors(self, color: str) -> None:
        self.label_colors = color

    def set_z(self, new_z: float) -> None:
        self.z = new_z
