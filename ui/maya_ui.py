import os
import sys
from PySide2 import QtWidgets, QtCore, QtGui
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui
import maya.cmds as cmds

from logic import maya_logic
if sys.version[0] == "3":
    import importlib
    importlib.reload(maya_logic)
else:
    reload(maya_logic)


def maya_main_window():
    """
    Maya Main Window Pointer
    :return: QtWidgets.QWidget Object
    """
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


class MayaUI(QtWidgets.QWidget):
    def __init__(self, parent=maya_main_window()):
        super(MayaUI, self).__init__(parent)

        self.setWindowTitle("Arnold to Mantra Light Transfer")

        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint | QtCore.Qt.Window)
        self.setFixedSize(500, 100)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

        self.export_line.setText(r"C:/Users/bhave/Documents/maya/projects/default/data/test.json")

    def create_widgets(self):
        self.header = QtWidgets.QLabel("Arnold to Mantra Light Transfer")
        self.header.setAlignment(QtCore.Qt.AlignHCenter)
        self.header.setFont(QtGui.QFont("Arial", 16))
        self.export_label = QtWidgets.QLabel("Json File:")
        self.export_line = QtWidgets.QLineEdit()
        self.export_open = QtWidgets.QPushButton("Save Json File")
        self.export_btn = QtWidgets.QPushButton("Export Lights")

    def create_layouts(self):
        self.export_layout = QtWidgets.QHBoxLayout()
        self.export_layout.addWidget(self.export_label)
        self.export_layout.addWidget(self.export_line)
        self.export_layout.addWidget(self.export_open)
        self.export_layout.addWidget(self.export_btn)
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.addWidget(self.header)
        self.main_layout.addLayout(self.export_layout)

    def create_connections(self):
        self.export_open.clicked.connect(self.get_json_file_path)
        self.export_btn.clicked.connect(self.export_json_file)

    def get_json_file_path(self):
        current_directory = cmds.workspace(q=True, rd=True)
        data_folder = os.path.join(current_directory, "data")
        if os.path.exists(data_folder):
            current_directory = data_folder
        save_file, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save", current_directory, "JSON Files (*.json)")
        self.export_line.setText(save_file)

    def export_json_file(self):
        maya_logic.export_json_file(self.export_line.text())
        self.close()
        self.deleteLater()


if __name__ == "__main__":
    maya_ui = MayaUI()
    maya_ui.show()
