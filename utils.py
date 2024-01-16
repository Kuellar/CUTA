import os
from widgets.IconLabel import IconLabel
from widgets.PushButtonMenu import PushButtonMenu
from functools import partial


def open_data(window, file_name):
    f = open(file_name)
    x = []
    y = []
    z = []
    min_x = float("inf")
    max_x = float("-inf")
    min_y = float("inf")
    max_y = float("-inf")
    err = 0
    for line in f:
        try:
            line_list = line.split()

            # x value
            new_x = float(line_list[0])
            x.append(new_x)
            if new_x < min_x:
                min_x = new_x
            if new_x > max_x:
                max_x = new_x

            # y value
            new_y = float(line_list[1])
            y.append(new_y)
            if new_y < min_y:
                min_y = new_y
            if new_y > max_y:
                max_y = new_y

            # error value
            z.append(float(line_list[2]))
        except:
            err += 1

    lim_x = [min_x-(max_x-min_x)*5/100, max_x+(max_x-min_x)*5/100]
    lim_y = [min_y-(max_y-min_y)*5/100, max_y+(max_y-min_y)*5/100]

    window.setWindowTitle(file_name.split("/")[-1] + " - CUTA")

    if err == 0:
        return x, y, z, lim_x, lim_y, None
    else:
        return (
            x,
            y,
            z,
            lim_x,
            lim_y,
            {"error": 1, "msg": f"Incorrect format in {err} lines"},
        )


# TODO: Change window for FilesMenu widget
def open_folder(window, folder_name):
    # Clean first
    for i in reversed(range(window.filesMenu.filesFoldersLayout.count())):
        window.filesMenu.filesFoldersLayout.itemAt(i).widget().setParent(None)

    # Add title
    folder_title = IconLabel("fa.angle-down", folder_name.split("/")[-1])
    window.filesMenu.filesFoldersLayout.addWidget(folder_title)
    files = os.listdir(folder_name)
    files.sort()
    for file in files:
        if file.endswith(".dat"):
            file_widget = PushButtonMenu(file)
            file_widget.clicked.connect(partial(window.openFile, file_name=file))
            window.filesMenu.filesFoldersLayout.addWidget(file_widget)
