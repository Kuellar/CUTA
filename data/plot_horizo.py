class PlotHorizo:
    def __init__(
        self,
        names: list[str],
        x: list[float],
        z: float = 0.0,
        names_y: float = 0.1,
        names_color: str = "black",
        linestyles: str = "--",
        colors: str = "blue",
        label_colors: str = "black",
        width: float = 1,
        show_names: bool = True,
        filename: str = "",
    ) -> None:
        indexes = sorted(range(len(x)), key=x.__getitem__)
        self.x = list(map(x.__getitem__, indexes))
        self.names = list(map(names.__getitem__, indexes))

        self.names_y = names_y
        self.names_color = names_color
        self.z = z
        self.linestyles = linestyles
        self.colors = colors
        self.label_colors = label_colors
        self.width = width
        self.show_names = show_names
        self.filename = filename

    def set_colors(self, color: str) -> None:
        self.colors = color

    def set_label_colors(self, color: str) -> None:
        self.label_colors = color

    def set_z(self, new_z: float) -> None:
        self.z = new_z

    def set_show_names(self, flag: bool) -> None:
        self.show_names = flag

    def set_names_y(self, pos: float) -> None:
        self.names_y = pos
