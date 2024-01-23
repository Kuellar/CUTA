from PyQt6.QtWidgets import QApplication
from data import PlotPoints, Points, PlotHorizo

PRINT_LINES = 5


def check_number(string: str) -> bool:
    try:
        float(string)
        return True
    except ValueError:
        return False


def open_data(window, file_name):
    app = QApplication.activeWindow()
    with open(file_name, encoding="utf-8") as f:
        names = []
        xhorizo = []

        x = []
        y = []
        z = []
        err = 0

        res = None
        lines_to_print = 0
        for line in f:
            if lines_to_print < PRINT_LINES:
                app.output_console.print_output(f"{lines_to_print}: {line[:-1]}")
                lines_to_print += 1
            if lines_to_print == PRINT_LINES:
                app.output_console.print_output(f"{lines_to_print}: ...")
                lines_to_print += 1
            try:
                line_list = line.split()
                if not check_number(line_list[0]) and len(line_list) == 2:
                    names.append(line_list[0])
                    xhorizo.append(float(line_list[1]))
                else:
                    x.append(float(line_list[0]))
                    y.append(float(line_list[1]))
                    z.append(float(line_list[2]))
            except:  # pylint: disable=W0702
                err += 1

        if len(names) > 0:
            if app.plot_horizo:
                res = PlotHorizo(
                    names=names,
                    x=xhorizo,
                    z=0,
                    names_y=app.plot_horizo.names_y,
                    names_color=app.plot_horizo.names_color,
                    linestyles=app.plot_horizo.linestyles,
                    colors=app.plot_horizo.colors,
                    label_colors=app.plot_horizo.label_colors,
                    width=app.plot_horizo.width,
                    show_names=app.plot_horizo.show_names,
                    filename=file_name,
                )
            else:
                res = PlotHorizo(names, xhorizo)
        else:
            if app.plot_points:
                res = PlotPoints(
                    name=file_name.split("/")[-1],
                    points=Points(x, y, z),
                    color=app.plot_points.color,
                    plot_line=app.plot_points.plot_line,
                    marker=app.plot_points.marker,
                    marker_color=app.plot_points.marker_color,
                    show_error=app.plot_points.show_error,
                    error_color=app.plot_points.error_color,
                    drawstyle=app.plot_points.drawstyle,
                )
            else:
                res = PlotPoints(file_name.split("/")[-1], Points(x, y, z))
            window.setWindowTitle(file_name.split("/")[-1] + " - CUTA")

        if err == 0:
            return res, None

        return (
            res,
            {"error": 1, "msg": f"Incorrect format in {err} lines."},
        )
