import re
from data import PlotPoints, Points, PlotHorizo
from PyQt6.QtWidgets import QApplication

PRINT_LINES = 5


def check_number(string: str) -> bool:
    try:
        float(string)
        return True
    except ValueError:
        return False


def open_data(window, file_name):
    app = QApplication.activeWindow()
    f = open(file_name)
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
            app.outputConsole.printOutput(f"{lines_to_print}: {line[:-1]}")
            lines_to_print += 1
        if lines_to_print == PRINT_LINES:
            app.outputConsole.printOutput(f"{lines_to_print}: ...")
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
        except:
            err += 1

    if len(names) > 0:
        res = PlotHorizo(names, xhorizo)
    else:
        res = PlotPoints(file_name.split("/")[-1], Points(x, y, z))
        window.setWindowTitle(file_name.split("/")[-1] + " - CUTA")

    if err == 0:
        return res, None
    else:
        return (
            res,
            {"error": 1, "msg": f"Incorrect format in {err} lines."},
        )
