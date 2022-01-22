"""

houdini_ui.py

Loads UI inside Houdini

"""

from PySide2 import QtCore, QtWidgets, QtGui

from logic.houdini_logic import *


def hou_main_window():
    """
    Houdini Main Window QWidget Pointer
    :return: Houdini Window Pointer
    """
    return hou.qt.mainWindow()


class HoudiniUI(QtWidgets.QWidget):
    """
    Houdini UI Class
    """
    def __init__(self, title, version, parent=hou_main_window()):
        """
        Houdini UI Init
        :param title: Tool Name
        :param version: Tool Version
        :param parent: Parent Window
        """
        super(HoudiniUI, self).__init__(parent)

        self.title = title
        self.version = version

        self.setWindowTitle("{0} v{1}".format(self.title, self.version))

        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint | QtCore.Qt.Window)
        self.setFixedSize(600, 160)

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        """
        Create UI Widgets
        :return: None
        """
        self.header = QtWidgets.QLabel(self.title)
        self.header.setAlignment(QtCore.Qt.AlignHCenter)
        self.header.setFont(QtGui.QFont("Arial", 16))

        self.import_label = QtWidgets.QLabel("Json File:")
        self.import_label.setAlignment(QtCore.Qt.AlignRight)

        self.import_line = QtWidgets.QLineEdit()

        self.import_open = QtWidgets.QPushButton("Browse")

        self.renderer_label = QtWidgets.QLabel("Renderer:")
        self.renderer_label.setAlignment(QtCore.Qt.AlignRight)

        self.mantra_check = QtWidgets.QCheckBox("Mantra")

        self.arnold_check = QtWidgets.QCheckBox("Arnold")

        self.scale_label = QtWidgets.QLabel("Scale:")
        self.scale_label.setAlignment(QtCore.Qt.AlignRight)

        self.scale_double_spin = QtWidgets.QDoubleSpinBox()
        self.scale_double_spin.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.scale_double_spin.setValue(0.1)
        self.scale_double_spin.setDecimals(3)
        self.scale_double_spin.setRange(0.001, 1000)

        self.import_btn = QtWidgets.QPushButton("Import Lights")

        self.vertical_spacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum,
                                                     QtWidgets.QSizePolicy.Expanding)

        self.author_label = QtWidgets.QLabel("Bhavesh Budhkar")
        self.author_label.setDisabled(True)
        self.author_label.setAlignment(QtCore.Qt.AlignLeft)

        self.email_label = QtWidgets.QLabel("bhaveshbudhkar@yahoo.com")
        self.email_label.setDisabled(True)
        self.email_label.setAlignment(QtCore.Qt.AlignRight)

    def create_layouts(self):
        """
        Create UI Layouts
        :return: None
        """
        self.grid_layout = QtWidgets.QGridLayout()
        self.grid_layout.addWidget(self.import_label, 0, 0)
        self.grid_layout.addWidget(self.import_line, 0, 1)
        self.grid_layout.addWidget(self.import_open, 0, 2)

        self.scale_layout = QtWidgets.QHBoxLayout()
        self.scale_layout.addWidget(self.mantra_check, 1)
        self.scale_layout.addWidget(self.arnold_check, 1)
        self.scale_layout.addWidget(self.scale_label, 1)
        self.scale_layout.addWidget(self.scale_double_spin, 1)

        self.grid_layout.addWidget(self.renderer_label, 1, 0)
        self.grid_layout.addLayout(self.scale_layout, 1, 1)
        self.grid_layout.addWidget(self.import_btn, 1, 2)

        self.grid_layout.setColumnStretch(0, 1)
        self.grid_layout.setColumnStretch(1, 6)
        self.grid_layout.setColumnStretch(2, 1)

        self.info_layout = QtWidgets.QHBoxLayout()
        self.info_layout.addWidget(self.author_label)
        self.info_layout.addWidget(self.email_label)

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.addWidget(self.header)
        self.main_layout.addLayout(self.grid_layout)
        self.main_layout.addSpacerItem(self.vertical_spacer)
        self.main_layout.addLayout(self.info_layout)

        self.setLayout(self.main_layout)

    def create_connections(self):
        """
        Signals and Slots
        :return: None
        """
        self.import_open.clicked.connect(self.import_json_file_path)
        self.import_btn.clicked.connect(self.import_lights)

    def import_json_file_path(self):
        """
        Open File Browser and Open Json file
        :return: None
        """
        current_directory = hou.homeHoudiniDirectory()
        save_file, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open", current_directory, "JSON Files (*.json)")
        self.import_line.setText(save_file)

    def import_lights(self):
        """
        Import Lights from Json file
        :return: None
        """
        import_json_file(self.import_line.text(), self.scale_double_spin.value(),
                         self.mantra_check.isChecked(), self.arnold_check.isChecked())
        self.close()
        self.deleteLater()
