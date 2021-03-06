"""

maya_ui.py

Loads UI inside Maya

"""

from PySide2 import QtWidgets, QtCore, QtGui
from shiboken2 import wrapInstance
import maya.OpenMayaUI as omui

from logic.maya_logic import *


def maya_main_window():
    """
    Maya Main Window Pointer
    :return: QtWidgets.QWidget Object
    """
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)


class MayaUI(QtWidgets.QWidget):
    """
    Maya UI Class
    """
    def __init__(self, title, version, parent=maya_main_window()):
        """
        Maya UI Init
        :param title: Tool Name
        :param version: Tool Version
        :param parent: Parent Window
        """
        super(MayaUI, self).__init__(parent)

        self.title = title
        self.version = version

        self.setWindowTitle("{0} v{1}".format(self.title, self.version))

        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint | QtCore.Qt.Window)
        self.setFixedSize(550, 110)

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

        self.export_label = QtWidgets.QLabel("Json File:")

        self.export_line = QtWidgets.QLineEdit()

        self.export_open = QtWidgets.QPushButton("Browse")

        self.export_btn = QtWidgets.QPushButton("Export Lights")

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
        self.export_layout = QtWidgets.QHBoxLayout()
        self.export_layout.addWidget(self.export_label)
        self.export_layout.addWidget(self.export_line)
        self.export_layout.addWidget(self.export_open)
        self.export_layout.addWidget(self.export_btn)

        self.info_layout = QtWidgets.QHBoxLayout()
        self.info_layout.addWidget(self.author_label)
        self.info_layout.addWidget(self.email_label)

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.addWidget(self.header)
        self.main_layout.addLayout(self.export_layout)
        self.main_layout.addSpacerItem(self.vertical_spacer)
        self.main_layout.addLayout(self.info_layout)

        self.setLayout(self.main_layout)

    def create_connections(self):
        """
        Signals and Slots
        :return: None
        """
        self.export_open.clicked.connect(self.get_json_file_path)
        self.export_btn.clicked.connect(self.export_json_file)

    def get_json_file_path(self):
        """
        Open File Browser and Save Json file path
        :return: None
        """
        current_directory = cmds.workspace(q=True, rd=True)
        data_folder = os.path.join(current_directory, "data")
        if os.path.exists(data_folder):
            current_directory = data_folder
        save_file, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save", current_directory, "JSON Files (*.json)")
        self.export_line.setText(save_file)

    def export_json_file(self):
        """
        Export Lights to Json file
        :return: None
        """
        export_json_file(self.export_line.text())
        self.close()
        self.deleteLater()
