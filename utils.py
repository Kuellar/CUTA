import os
from widgets.IconLabel import IconLabel
from widgets.PushButtonMenu import PushButtonMenu
from functools import partial


def open_data(window, file_name):
    f = open(file_name)
    x = []
    y = []
    z = []
    err = 0
    for line in f:
        try:
            line_list = line.split()
            x.append(float(line_list[0]))
            y.append(float(line_list[1]))
            z.append(float(line_list[2]))
        except:
            err += 1

    window.setWindowTitle(file_name.split("/")[-1] + " - CUTA")

    if err == 0:
        return x, y, z, None
    else:
        return x, y, z, {"error": 1, "msg": f"Incorrect format in {err} lines"}


# TODO: Change window for FilesMenu widget
def open_folder(window, folder_name):
    # Clean first
    for i in reversed(range(window.filesMenu.filesFoldersLayout.count())):
        window.filesFoldersLayout.itemAt(i).widget().setParent(None)

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
