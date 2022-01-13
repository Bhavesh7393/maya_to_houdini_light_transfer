import os
import sys
import json
import maya.cmds as cmds

package_path = os.path.dirname(os.path.realpath(__file__))
json_file_path = os.path.join(package_path, "arnold_to_mantra_light_data.json")

if sys.version[0] == "3":
    with open(json_file_path, "r") as json_file:
        light_data = json.load(json_file)
else:
    from collections import OrderedDict
    with open(json_file_path, "r") as json_file:
        light_data = json.load(json_file, object_pairs_hook=OrderedDict)


def lights_list():
    selection = cmds.ls(selection=True, long=True)
    lights = cmds.listRelatives(selection, fullPath=True,
                                type=["directionalLight", "pointLight", "spotLight", "areaLight", "aiAreaLight",
                                      "aiSkyDomeLight"])

    all_lights = []

    if lights:
        for light in lights:
            if cmds.nodeType(light) != "volumeLight":
                all_lights.append(light)

    lights_transform = cmds.listRelatives(all_lights, parent=True, fullPath=True)
    lights_transform_slash = []
    for slash in lights_transform:
        lights_transform_slash.append(slash.replace("|", "_")[1:])

    return lights_transform, all_lights, lights_transform_slash


def export_json_file(path):
    lights = lights_list()
    light_list = lights[0]
    light_shape_list = lights[1]
    light_list_slash = lights[2]

    if sys.version[0] == "3":
        light_export_data = {}
    else:
        light_export_data = OrderedDict()
    for light in range(len(light_list)):
        if sys.version[0] == "3":
            temp = {}
        else:
            temp = OrderedDict()
        node_type = cmds.nodeType(light_shape_list[light])
        if node_type == "pointLight":
            if not cmds.getAttr("{0}.aiRadius".format(light_shape_list[light])):
                temp["nodeType"] = "{0}P".format(node_type)
            else:
                temp["nodeType"] = "{0}S".format(node_type)
        elif node_type == "directionalLight":
            if not cmds.getAttr("{0}.aiAngle".format(light_shape_list[light])):
                temp["nodeType"] = "{0}D".format(node_type)
            else:
                temp["nodeType"] = "{0}S".format(node_type)
        elif node_type == "spotLight":
            if not cmds.getAttr("{0}.aiRadius".format(light_shape_list[light])):
                temp["nodeType"] = "{0}P".format(node_type)
            else:
                temp["nodeType"] = "{0}S".format(node_type)
        elif node_type == "areaLight":
            temp["nodeType"] = "{0}".format(node_type)
        elif node_type == "aiAreaLight":
            light_type = cmds.getAttr("{0}.aiTranslator".format(light_shape_list[light]))
            if light_type == "quad":
                temp["nodeType"] = "{0}".format(light_type)
            elif light_type == "disk":
                temp["nodeType"] = "{0}".format(light_type)
            elif light_type == "cylinder":
                if not cmds.getAttr("{0}.scaleX".format(light_list[light])) \
                        and not cmds.getAttr("{0}.scaleZ".format(light_list[light])):
                    temp["nodeType"] = "{0}L".format(light_type)
                else:
                    temp["nodeType"] = "{0}C".format(light_type)
        elif node_type == "aiSkyDomeLight":
            temp["nodeType"] = "{0}".format(node_type)

        for parm in light_data[temp["nodeType"]]["mantra_light_parms"]:
            value = cmds.getAttr("{0}.{1}".format(light_list[light], parm))
            translate = cmds.xform(light_list[light], q=True, translation=True, worldSpace=True)
            if parm == "aiAov" and value == "default":
                temp[parm] = ""
            elif parm == "aiAov" and value != "default":
                temp[parm] = value
            elif parm == "translateX":
                temp[parm] = translate[0]
            elif parm == "translateY":
                temp[parm] = translate[1]
            elif parm == "translateZ":
                temp[parm] = translate[2]
            else:
                temp[parm] = value

        if bool(cmds.connectionInfo("{0}.color".format(light_list[light]), sourceFromDestination=True)):
            if cmds.getAttr("{0}.aiUseColorTemperature".format(light_list[light])):
                kelvin_temp = cmds.getAttr("{0}.aiColorTemperature".format(light_list[light]))
                color_temp = cmds.arnoldTemperatureToColor(kelvin_temp)
                for parm, value in zip(light_data["color_light_params"], color_temp):
                    temp[parm] = value
                temp["texture_map"] = ""

            file_node = cmds.connectionInfo("{0}.color".format(light_list[light]), sourceFromDestination=True)
            split = file_node.split(".")
            node_type = cmds.nodeType(split[0])
            if node_type == "file":
                texture_path = cmds.getAttr("{0}.fileTextureName".format(split[0]))
            elif node_type == "aiImage":
                texture_path = cmds.getAttr("{0}.filename".format(split[0]))
            else:
                texture_path = ""
            for color in light_data["color_light_params"]:
                temp[color] = 1
            temp["texture_node"] = split[0]
            temp["texture_map"] = texture_path
        else:
            if cmds.getAttr("{0}.aiUseColorTemperature".format(light_list[light])):
                kelvin_temp = cmds.getAttr("{0}.aiColorTemperature".format(light_list[light]))
                color_temp = cmds.arnoldTemperatureToColor(kelvin_temp)
                for parm, value in zip(light_data["color_light_params"], color_temp):
                    temp[parm] = value
            else:
                for color in light_data["color_light_params"]:
                    value = cmds.getAttr("{0}.{1}".format(light_list[light], color))
                    temp[color] = value

        light_export_data[light_list_slash[light]] = temp

    with open(path, "w") as json_maya_file:
        json.dump(light_export_data, json_maya_file, indent=4, ensure_ascii=False)

    sys.stdout.write("Lights exported.\n")
