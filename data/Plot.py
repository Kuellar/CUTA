class Plot:
    def __init__(self) -> None:
        self.title = ""
        self.xlabel = ""
        self.ylabel = ""
        self.xscale = "linear"
        self.yscale = "linear"
        self.show_grid = False

    def set_title(self, new_title: str) -> None:
        self.title = new_title

    def set_xlabel(self, new_xlabe: str) -> None:
        self.xlabel = new_xlabe

    def set_ylabel(self, new_ylabe: str) -> None:
        self.ylabel = new_ylabe

    def set_xscale(self, new_xscale: str) -> None:
        self.xscale = new_xscale

    def set_yscale(self, new_yscale: str) -> None:
        self.yscale = new_yscale

    def set_show_grid(self, new_show_grid: bool) -> None:
        self.show_grid = new_show_grid
