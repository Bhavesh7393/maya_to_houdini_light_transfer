import sys
import hou
from PySide2 import QtCore, QtWidgets, QtGui

from logic import houdini_logic
if sys.version[0] == "3":
    import importlib
    importlib.reload(houdini_logic)
else:
    reload(houdini_logic)


def hou_main_window():
    """
    Houdini Main Window QWidget Pointer
    :return: Houdini Window Pointer
    """
    return hou.qt.mainWindow()


class HoudiniUI(QtWidgets.QWidget):
    def __init__(self, parent=hou_main_window()):
        super(HoudiniUI, self).__init__(parent)

        self.setWindowTitle("Arnold to Mantra Light Transfer")

        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint | QtCore.Qt.Window)
        self.setFixedSize(500, 130)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

        self.import_line.setText(r"C:/Users/bhave/Documents/maya/projects/default/data/test.json")

    def create_widgets(self):
        self.header = QtWidgets.QLabel("Arnold to Mantra Light Transfer")
        self.header.setAlignment(QtCore.Qt.AlignHCenter)
        self.header.setFont(QtGui.QFont("Arial", 16))
        self.import_label = QtWidgets.QLabel("Json File:")
        self.import_line = QtWidgets.QLineEdit()
        self.import_open = QtWidgets.QPushButton("Open Json File")
        self.import_btn = QtWidgets.QPushButton("Import Lights")
        self.scale_label = QtWidgets.QLabel("Scale:")
        self.scale_double_spin = QtWidgets.QDoubleSpinBox()
        self.scale_double_spin.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.scale_double_spin.setValue(1)
        self.scale_double_spin.setDecimals(3)
        self.scale_double_spin.setRange(0.001, 1000)

    def create_layouts(self):
        self.grid_layout = QtWidgets.QGridLayout()
        self.grid_layout.addWidget(self.import_label, 0, 0)
        self.grid_layout.addWidget(self.import_line, 0, 1)
        self.grid_layout.addWidget(self.import_open, 0, 2)
        self.grid_layout.addWidget(self.scale_label, 1, 0)
        self.grid_layout.addWidget(self.scale_double_spin, 1, 1)
        self.grid_layout.addWidget(self.import_btn, 1, 2)
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.addWidget(self.header)
        self.main_layout.addLayout(self.grid_layout)
        self.setLayout(self.main_layout)

    def create_connections(self):
        self.import_open.clicked.connect(self.import_json_file_path)
        self.import_btn.clicked.connect(self.import_lights)

    def import_json_file_path(self):
        current_directory = hou.homeHoudiniDirectory()
        save_file, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open", current_directory, "JSON Files (*.json)")
        self.import_line.setText(save_file)

    def import_lights(self):
        houdini_logic.import_json_file(self.import_line.text(), self.scale_double_spin.value())
        self.close()
        self.deleteLater()


if __name__ == "builtins":
    hou_ui = HoudiniUI()
    hou_ui.show()
