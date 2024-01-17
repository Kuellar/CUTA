from data import PlotPoints, Points


def open_data(window, file_name):
    f = open(file_name)
    x = []
    y = []
    z = []
    err = 0
    for line in f:
        try:
            line_list = line.split()

            # x value
            x.append(float(line_list[0]))

            # y value
            y.append(float(line_list[1]))

            # error value
            z.append(float(line_list[2]))
        except:
            err += 1

    newPlotPoints = PlotPoints(file_name.split("/")[-1], Points(x, y, z))
    window.setWindowTitle(file_name.split("/")[-1] + " - CUTA")

    if err == 0:
        return newPlotPoints, None
    else:
        return (
            newPlotPoints,
            {"error": 1, "msg": f"Incorrect format in {err} lines"},
        )
