class PlotHorizo:
    def __init__(self, names: list[str], x: list[float], z: float = 0.0) -> None:
        indexes = sorted(range(len(x)), key=x.__getitem__)
        self.x = list(map(x.__getitem__, indexes))
        self.names = list(map(names.__getitem__, indexes))

        self.names_y = 0.25
        self.names_color = "black"
        self.z = z
        self.linestyles = "--"
        self.colors = "blue"
        self.label_colors = "black"
        self.width = 1
        self.show_names = True

    def set_colors(self, color: str) -> None:
        self.colors = color

    def set_label_colors(self, color: str) -> None:
        self.label_colors = color

    def set_z(self, new_z: float) -> None:
        self.z = new_z

    def set_show_names(self, flag) -> None:
        self.show_names = flag

