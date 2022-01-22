"""

ui_launcher.py

Software Requirement:
Maya 2018+
Houdini 16+
Python 2 or 3

Tested on:
Windows, Maya 2018 Python 2
Windows, Maya 2022 Python 3
Windows, Houdini 18.5.499 Python 2
Windows, Houdini 18.5.596 Python 3

Installation
    1. Open "ui_launcher.py"
    2. Replace "Path" variable with your script folder path.
    3. Save script in Maya and Houdini Shelf.

How to use
    Maya
        Drag and select all the lights from the viewport.
        Run the script.
        Click "Browse" button, and save it to desired location. (Default path is current Maya workspace "data" folder.)
        Click "Export Lights" button.
    Houdini
        Run the script.
        Click "Browse" button, and load the exported Json file. (Default path is current Houdini workspace folder.)
        Tick desired Renderer.
        Set "Scene Scale" if required. It will adjust Translate, Scale, Exposure and Radius. (Default value is 0.1)
        Click "Import Lights" button.

Author:
Bhavesh Budhkar
bhaveshbudhkar@yahoo.com

"""

import sys

path = r"system_directory_path\maya_to_houdini_light_transfer"

if path not in sys.path:
    sys.path.append(path)

title = "Maya to Houdini Light Transfer"
version = str(1.0)


def main():
    if sys.version[0] == "3":
        import importlib
        try:
            from ui import maya_ui
            importlib.reload(maya_ui)
            maya_main_ui = maya_ui.MayaUI(title, version)
            maya_main_ui.show()
        except ModuleNotFoundError:
            from ui import houdini_ui
            importlib.reload(houdini_ui)
            houdini_main_ui = houdini_ui.HoudiniUI(title, version)
            houdini_main_ui.show()
        except ModuleNotFoundError:
            sys.stdout.write("Please run the script in Maya or Houdini!\n")
    else:
        try:
            from ui import maya_ui
            reload(maya_ui)
            maya_main_ui = maya_ui.MayaUI(title, version)
            maya_main_ui.show()
        except ImportError:
            from ui import houdini_ui
            reload(houdini_ui)
            houdini_main_ui = houdini_ui.HoudiniUI(title, version)
            houdini_main_ui.show()
        except ImportError:
            sys.stdout.write("Please run the script in Maya or Houdini!\n")


main()
