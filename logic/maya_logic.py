import os
import sys
import json
import maya.cmds as cmds

package_path = os.path.dirname(os.path.realpath(__file__))
json_file_path = os.path.join(package_path, "maya_to_houdini_light_data.json")

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
    lights_transform_name = []
    for slash in lights_transform:
        lights_transform_name.append(slash.replace("|", "_")[1:])

    return lights_transform, all_lights, lights_transform_name


def export_json_file(path):
    lights = lights_list()
    light_list = lights[0]
    light_shape_list = lights[1]
    light_list_name = lights[2]

    if sys.version[0] == "3":
        light_export_data = {}
    else:
        light_export_data = OrderedDict()
    for light in range(len(light_list)):
        if sys.version[0] == "3":
            mantra_parms_dict = {}
            arnold_parms_dict = {}
            mantra_dict = {}
            arnold_dict = {}
        else:
            mantra_parms_dict = OrderedDict()
            arnold_parms_dict = OrderedDict()
            mantra_dict = OrderedDict()
            arnold_dict = OrderedDict()

        node_type = cmds.nodeType(light_shape_list[light])

        for renderer in light_data:
            if renderer == "Arnold":
                arnold_parms_dict["nodeType"] = node_type

                if node_type == "aiAreaLight":
                    light_type = cmds.getAttr("{0}.aiTranslator".format(light_shape_list[light]))
                    if light_type == "quad":
                        arnold_parms_dict["nodeType"] = "{0}".format(light_type)
                    elif light_type == "disk":
                        arnold_parms_dict["nodeType"] = "{0}".format(light_type)
                    elif light_type == "cylinder":
                        arnold_parms_dict["nodeType"] = "{0}".format(light_type)

                for parm in light_data[renderer][arnold_parms_dict["nodeType"]]["light_parms"]:
                    value = cmds.getAttr("{0}.{1}".format(light_list[light], parm))
                    translate = cmds.xform(light_list[light], q=True, translation=True, worldSpace=True)
                    if parm == "aiAov" and value == "default":
                        arnold_parms_dict[parm] = ""
                    elif parm == "aiAov" and value != "default":
                        arnold_parms_dict[parm] = value
                    elif parm == "translateX":
                        arnold_parms_dict[parm] = translate[0]
                    elif parm == "translateY":
                        arnold_parms_dict[parm] = translate[1]
                    elif parm == "translateZ":
                        arnold_parms_dict[parm] = translate[2]
                    else:
                        arnold_parms_dict[parm] = value

            elif renderer == "Mantra":
                if node_type == "pointLight":
                    if not cmds.getAttr("{0}.aiRadius".format(light_shape_list[light])):
                        mantra_parms_dict["nodeType"] = "{0}P".format(node_type)
                    else:
                        mantra_parms_dict["nodeType"] = "{0}S".format(node_type)
                elif node_type == "directionalLight":
                    if not cmds.getAttr("{0}.aiAngle".format(light_shape_list[light])):
                        mantra_parms_dict["nodeType"] = "{0}D".format(node_type)
                    else:
                        mantra_parms_dict["nodeType"] = "{0}S".format(node_type)
                elif node_type == "spotLight":
                    if not cmds.getAttr("{0}.aiRadius".format(light_shape_list[light])):
                        mantra_parms_dict["nodeType"] = "{0}P".format(node_type)
                    else:
                        mantra_parms_dict["nodeType"] = "{0}S".format(node_type)
                elif node_type == "areaLight":
                    mantra_parms_dict["nodeType"] = "{0}".format(node_type)
                elif node_type == "aiAreaLight":
                    light_type = cmds.getAttr("{0}.aiTranslator".format(light_shape_list[light]))
                    if light_type == "quad":
                        mantra_parms_dict["nodeType"] = "{0}".format(light_type)
                    elif light_type == "disk":
                        mantra_parms_dict["nodeType"] = "{0}".format(light_type)
                    elif light_type == "cylinder":
                        if cmds.getAttr("{0}.scaleX".format(light_list[light])) == 0 and cmds.getAttr("{0}.scaleZ".format(light_list[light])) == 0:
                            mantra_parms_dict["nodeType"] = "{0}L".format(light_type)
                        else:
                            mantra_parms_dict["nodeType"] = "{0}C".format(light_type)
                elif node_type == "aiSkyDomeLight":
                    mantra_parms_dict["nodeType"] = "{0}".format(node_type)

                for parm in light_data[renderer][mantra_parms_dict["nodeType"]]["light_parms"]:
                    value = cmds.getAttr("{0}.{1}".format(light_list[light], parm))
                    translate = cmds.xform(light_list[light], q=True, translation=True, worldSpace=True)
                    if parm == "aiAov" and value == "default":
                        mantra_parms_dict[parm] = ""
                    elif parm == "aiAov" and value != "default":
                        mantra_parms_dict[parm] = value
                    elif parm == "translateX":
                        mantra_parms_dict[parm] = translate[0]
                    elif parm == "translateY":
                        mantra_parms_dict[parm] = translate[1]
                    elif parm == "translateZ":
                        mantra_parms_dict[parm] = translate[2]
                    else:
                        mantra_parms_dict[parm] = value

        if bool(cmds.connectionInfo("{0}.color".format(light_list[light]), sourceFromDestination=True)):
            if cmds.getAttr("{0}.aiUseColorTemperature".format(light_list[light])):
                kelvin_temp = cmds.getAttr("{0}.aiColorTemperature".format(light_list[light]))
                color_temp = cmds.arnoldTemperatureToColor(kelvin_temp)
                for parm, value in zip(light_data["color_light_params"], color_temp):
                    mantra_parms_dict[parm] = value
                    arnold_parms_dict[parm] = value
                mantra_parms_dict["texture_map"] = ""
                arnold_parms_dict["texture_map"] = ""

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
                mantra_parms_dict[color] = 1
                arnold_parms_dict[color] = 1
            mantra_parms_dict["texture_node"] = split[0]
            mantra_parms_dict["texture_map"] = texture_path
            arnold_parms_dict["texture_map"] = texture_path
        else:
            if cmds.getAttr("{0}.aiUseColorTemperature".format(light_list[light])):
                kelvin_temp = cmds.getAttr("{0}.aiColorTemperature".format(light_list[light]))
                color_temp = cmds.arnoldTemperatureToColor(kelvin_temp)
                for parm, value in zip(light_data["color_light_params"], color_temp):
                    mantra_parms_dict[parm] = value
                    arnold_parms_dict[parm] = value
            else:
                for color in light_data["color_light_params"]:
                    value = cmds.getAttr("{0}.{1}".format(light_list[light], color))
                    mantra_parms_dict[color] = value
                    arnold_parms_dict[color] = value

        mantra_dict["Mantra"] = mantra_parms_dict
        arnold_dict["Arnold"] = arnold_parms_dict

        light_export_data[light_list_name[light]] = mantra_dict
        light_export_data[light_list_name[light]].update(arnold_dict)

    with open(path, "w") as json_maya_file:
        json.dump(light_export_data, json_maya_file, indent=4, ensure_ascii=False)

    sys.stdout.write("Lights exported.\n")
