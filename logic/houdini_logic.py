import os
import sys
import json
import hou
import math

package_path = os.path.dirname(os.path.realpath(__file__))
json_file_path = os.path.join(package_path, "maya_to_houdini_light_data.json")

if sys.version[0] == "3":
    with open(json_file_path, "r") as json_file:
        light_data = json.load(json_file)
else:
    from collections import OrderedDict
    with open(json_file_path, "r") as json_file:
        light_data = json.load(json_file, object_pairs_hook=OrderedDict)


def light_exposure_calculator(light_exposure, renderer_intensity_multiplier, old_scale, new_scale):
    # Exposure to Intensity conversion
    exposure_to_intensity = 2 ** light_exposure

    # Renderer Intensity conversion factor
    renderer_total_intensity = renderer_intensity_multiplier * exposure_to_intensity

    # Scale Factor
    scale_factor = new_scale / old_scale

    # New Intensity based on Scale Factor
    new_intensity = (scale_factor ** 2) * renderer_total_intensity

    # Intensity to Exposure conversion
    intensity_to_exposure = math.log(new_intensity, 2)
    return intensity_to_exposure


def soft_edge_exposure_calc(normalize, intensity, exposure, scale, value):
    current_exposure = light_exposure_calculator(exposure, 2 ** -2.65, 1, scale)
    exp_to_int = 2 ** exposure
    total_int = exp_to_int * intensity
    if normalize:
        mantra_total_int = 0.5 * total_int
        scale_factor = (scale ** 2) * mantra_total_int
        int_to_exp = scale_factor / intensity
        mantra_exp = math.log(int_to_exp, 2)
    else:
        mantra_total_int = 0.8 * total_int
        int_to_exp = mantra_total_int / intensity
        mantra_exp = math.log(int_to_exp, 2)

    old_range = [1, 0]
    new_range = [mantra_exp, current_exposure]

    old_percentage = (value - old_range[0]) / (old_range[1] - old_range[0])
    soft_edge_exposure = ((new_range[1] - new_range[0]) * old_percentage) + new_range[0]

    return soft_edge_exposure


obj = hou.node("obj")
mat = hou.node("mat")


def import_json_file(path, scale, mantra_check, arnold_check):
    if sys.version[0] == "3":
        with open(path, "r") as file:
            json_load = json.load(file)
    else:
        with open(path, "r") as file:
            json_load = json.load(file, object_pairs_hook=OrderedDict)

    light_nodes = []
    hou.Node.setSelected(obj, False, clear_all_selected=True)
    for light in json_load:
        for renderer in json_load[light].keys():
            if renderer == "Mantra" and mantra_check:
                if bool(obj.node("mantra_{0}".format(light))):
                    light_obj = obj.node("mantra_{0}".format(light))
                    light_obj.destroy()

                light_obj = obj.createNode(light_data[renderer][json_load[light][renderer]["nodeType"]]["light_node_type"], "mantra_{0}".format(light))
                light_nodes.append(light_obj)
                hou.Node.setSelected(light_obj, True)

                if json_load[light][renderer]["nodeType"] != "aiSkyDomeLight":
                    light_obj.parm("iconscale").set(scale)

                for parm, value in json_load[light][renderer].items():
                    if parm == "nodeType":
                        if json_load[light][renderer][parm] != "aiSkyDomeLight":
                            light_obj.parm("light_type").set(light_data[renderer][json_load[light][renderer][parm]]["light_node_sub_type"])

                        if json_load[light][renderer][parm] == "spotLightP" or json_load[light][renderer][parm] == "spotLightS":
                            light_obj.parm("coneenable").set(True)
                        elif json_load[light][renderer][parm] == "areaLight":
                            light_obj.parm("coneenable").set(True)
                            light_obj.parm("singlesided").set(True)
                            light_obj.parm("edgeenable").set(True)
                        elif json_load[light][renderer][parm] == "quad":
                            light_obj.parm("coneenable").set(True)
                            light_obj.parm("singlesided").set(True)
                            light_obj.parm("edgeenable").set(True)
                        elif json_load[light][renderer][parm] == "disk":
                            light_obj.parm("coneenable").set(True)
                            light_obj.parm("singlesided").set(True)
                        elif json_load[light][renderer][parm] == "cylinderC":
                            light_obj.parm("rOrd").set(2)
                            light_obj.parm("singlesided").set(True)
                        elif json_load[light][renderer][parm] == "cylinderL":
                            light_obj.parm("rOrd").set(2)
                            light_obj.parm("singlesided").set(True)

                        light_obj.parm("light_contrib").set(light_data[renderer][json_load[light][renderer][parm]]["num_of_light_contrib"])
                        for contrib in range(1, light_data[renderer][json_load[light][renderer][parm]]["num_of_light_contrib"] + 1):
                            light_obj.parm("light_contribname{0}".format(contrib)).set(
                                list(light_data["light_contribution_parms"])[contrib - 1])

                    elif parm == "translateX":
                        light_obj.parm(
                            light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"][parm]).set(value * scale)

                    elif parm == "translateY":
                        light_obj.parm(
                            light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"][parm]).set(value * scale)

                    elif parm == "translateZ":
                        light_obj.parm(
                            light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"][parm]).set(value * scale)

                    elif parm == "rotateX":
                        if json_load[light][renderer]["nodeType"] == "cylinderC" or json_load[light][renderer]["nodeType"] == "cylinderL":
                            light_obj.parm(
                                light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"][parm]).set(value * -1)
                        else:
                            light_obj.parm(
                                light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"][parm]).set(value)

                    elif parm == "rotateY":
                        if json_load[light][renderer]["nodeType"] == "aiSkyDomeLight":
                            light_obj.parm(
                                light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"][parm]).set(value + 180)
                        else:
                            light_obj.parm(
                                light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"][parm]).set(value)

                    elif parm == "rotateZ":
                        if json_load[light][renderer]["nodeType"] == "cylinderC" or json_load[light][renderer]["nodeType"] == "cylinderL":
                            light_obj.parm(
                                light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"][parm]).set(value + 90)
                        else:
                            light_obj.parm(
                                light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"][parm]).set(value)

                    elif parm == "scaleX":
                        light_obj.parm(
                            light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"][parm]).set(
                            value * 2 * scale)

                    elif parm == "scaleY":
                        light_obj.parm(
                            light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"][parm]).set(
                            value * 2 * scale)

                    elif parm == "scaleZ":
                        if json_load[light][renderer]["nodeType"] == "cylinderC":
                            scale_x = json_load[light][renderer].get("scaleX")
                            light_obj.parm(
                                light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"][parm]).set(
                                ((value + scale_x) / 2) * (40 / 3) * scale)
                        else:
                            light_obj.parm(
                                light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"][parm]).set(
                                value * scale)

                    elif parm == "aiExposure":
                        if json_load[light][renderer]["nodeType"] == "aiSkyDomeLight":
                            light_obj.parm(
                                light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"][parm]).set(value)
                        elif json_load[light][renderer]["nodeType"] == "directionalLightD"\
                                or json_load[light][renderer]["nodeType"] == "directionalLightS":
                            exposure = light_exposure_calculator(json_load[light][renderer][parm],
                                                                 2 ** -2.65, 1, 1)
                            light_obj.parm(
                                light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"][parm]).set(
                                exposure)
                        else:
                            if json_load[light][renderer].get("aiNormalize") is None or json_load[light][renderer]["aiNormalize"]:
                                exposure = light_exposure_calculator(json_load[light][renderer][parm],
                                                                     2 ** -2.65, 1, scale)
                            else:
                                exposure = value
                            light_obj.parm(
                                light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"][parm]).set(exposure)

                    elif parm == "exposure":
                        if json_load[light][renderer]["nodeType"] == "aiSkyDomeLight":
                            light_obj.parm(
                                light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"][parm]).set(value)
                        elif json_load[light][renderer]["nodeType"] == "cylinderL":
                            exposure = light_exposure_calculator(json_load[light][renderer][parm],
                                                                 0.05, 1, scale)
                            light_obj.parm(
                                light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"][parm]).set(
                                exposure)
                        else:
                            if json_load[light][renderer].get("normalize") is None or json_load[light][renderer]["normalize"]:
                                exposure = light_exposure_calculator(json_load[light][renderer][parm],
                                                                     2 ** -2.65, 1, scale)
                            else:
                                exposure = value
                            light_obj.parm(
                                light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"][parm]).set(exposure)

                    elif parm == "aiRadius":
                        light_obj.parm(
                            light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"][parm][0]).set(
                            value * 2 * scale)
                        light_obj.parm(
                            light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"][parm][1]).set(
                            value * 2 * scale)

                    elif parm == "aiAngle":
                        light_obj.parm(
                            light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"][parm]).set(
                            value / 2)

                    elif parm == "coneAngle" or parm == "penumbraAngle":
                        pass

                    elif parm == "dropoff":
                        if value == 0 or value == 1:
                            light_obj.parm(
                                light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"][parm]).set(1)
                            if json_load[light][renderer]["penumbraAngle"] >= 90 and json_load[light][renderer]["coneAngle"] >= 90:
                                light_obj.parm(
                                    light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"]["coneAngle"]).set(0)
                                light_obj.parm(
                                    light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"]["penumbraAngle"]).set(90)
                            elif json_load[light][renderer]["penumbraAngle"] >= 90 and json_load[light][renderer]["coneAngle"] < 90:
                                light_obj.parm(
                                    light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"]["penumbraAngle"]).set(90)
                            else:
                                light_obj.parm(light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"]["coneAngle"]).set(
                                    json_load[light][renderer]["coneAngle"])
                                light_obj.parm(
                                    light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"]["penumbraAngle"]).set(
                                    json_load[light][renderer]["penumbraAngle"])

                        elif 1 > value > 0:
                            dropoff = 1 - (math.log(100 - (value * 100), 100))
                            light_obj.parm(light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"][parm]).set(dropoff)

                        elif value > 1:
                            if json_load[light][renderer]["nodeType"] == "spotLightP":
                                light_obj.parm("sharpspot").set(False)
                                if json_load[light][renderer]["penumbraAngle"] > json_load[light][renderer]["coneAngle"]:
                                    coneangle = json_load[light][renderer]["coneAngle"] / 2
                                    light_obj.parm(
                                        light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"]["coneAngle"]).set(0)
                                    light_obj.parm(light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"][parm]).set(
                                        value)
                                    if json_load[light][renderer]["penumbraAngle"] >= 90:
                                        light_obj.parm(light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"][
                                                           "penumbraAngle"]).set(90)
                                    else:
                                        light_obj.parm(light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"][
                                                           "penumbraAngle"]).set(
                                            json_load[light][renderer]["penumbraAngle"] + coneangle)
                                else:
                                    coneangle = json_load[light][renderer]["coneAngle"] / 2
                                    penumbra = json_load[light][renderer]["penumbraAngle"] / 2
                                    light_obj.parm(
                                        light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"]["coneAngle"]).set(0)
                                    light_obj.parm(light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"][parm]).set(
                                        value)
                                    if coneangle + penumbra > 90:
                                        light_obj.parm(light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"][
                                                           "penumbraAngle"]).set(90)
                                    else:
                                        light_obj.parm(light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"][
                                                           "penumbraAngle"]).set(coneangle + penumbra)
                            else:
                                light_obj.parm("sharpspot").set(True)
                                light_obj.parm(light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"][parm]).set(value)
                                if json_load[light][renderer]["penumbraAngle"] >= 90:
                                    light_obj.parm(
                                        light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"]["coneAngle"]).set(0)
                                    light_obj.parm(
                                        light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"]["penumbraAngle"]).set(90)
                                else:
                                    light_obj.parm(
                                        light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"]["coneAngle"]).set(
                                        json_load[light][renderer]["coneAngle"])
                                    light_obj.parm(
                                        light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"]["penumbraAngle"]).set(
                                        json_load[light][renderer]["penumbraAngle"])

                    elif parm == "aiSpread":
                        if value >= 0.4:
                            old_range = [0.4, 1]
                            new_range = [1, 50]
                            exposure_range = [0.9, 0]
                            old_percentage = (value - old_range[0]) / (old_range[1] - old_range[0])
                            new_num = ((new_range[1] - new_range[0]) * old_percentage) + new_range[0]
                            cone_value = math.log(new_num, new_range[1])
                            new_exposure_num = ((exposure_range[1] - exposure_range[0]) * cone_value) + exposure_range[0]
                            spread_values = [cone_value * 180, 180, 10]
                            for num in range(len(light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"][parm])):
                                light_obj.parm(light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"][parm][num]).set(
                                    spread_values[num])

                            if new_exposure_num != 0:
                                try:
                                    exposure_value = light_obj.parm(
                                        light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"][
                                            "aiExposure"]).eval() + new_exposure_num
                                except KeyError:
                                    exposure_value = light_obj.parm(
                                        light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"][
                                            "exposure"]).eval() + new_exposure_num

                                old_exp_value = light_exposure_calculator(exposure_value, 1, 1, 1 / scale)
                                exp_scale_value = light_exposure_calculator(old_exp_value, 1, 1, scale)

                                try:
                                    light_obj.parm(
                                        light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"]["aiExposure"]).set(
                                        exp_scale_value)
                                except KeyError:
                                    light_obj.parm(
                                        light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"]["exposure"]).set(
                                        exp_scale_value)

                        elif 0.4 > value >= 0.02:
                            old_range = [0.02, 0.4]
                            new_range = [0, 1]
                            exposure_range = [7, 0]
                            old_percentage = (value - old_range[0]) / (old_range[1] - old_range[0])
                            new_num = ((new_range[1] - new_range[0]) * old_percentage) + new_range[0]
                            cone_value = (2 ** new_num) - 1
                            exp_value = math.log(1 + new_num, 1 + new_range[1])
                            new_exposure_num = ((exposure_range[1] - exposure_range[0]) * exp_value) + exposure_range[0]
                            spread_values = [0, cone_value * 180, 10]

                            for num in range(len(light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"][parm])):
                                light_obj.parm(light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"][parm][num]).set(
                                    spread_values[num])

                            try:
                                exposure_value = light_obj.parm(
                                    light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"]["aiExposure"]).eval()
                                light_obj.parm(
                                    light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"]["aiExposure"]).set(
                                    exposure_value + new_exposure_num)
                            except KeyError:
                                exposure_value = light_obj.parm(
                                    light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"]["exposure"]).eval()
                                light_obj.parm(light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"]["exposure"]).set(
                                    exposure_value + new_exposure_num)
                        else:
                            spread_values = [4.5, 0, 0]
                            for num in range(len(light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"][parm])):
                                light_obj.parm(light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"][parm][num]).set(
                                    spread_values[num])
                            try:
                                exposure_value = light_obj.parm(
                                    light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"]["aiExposure"]).eval() + 8
                            except KeyError:
                                exposure_value = light_obj.parm(
                                    light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"]["exposure"]).eval() + 8

                            exp_scale_value = light_exposure_calculator(exposure_value, 1, scale)

                            try:
                                light_obj.parm(
                                    light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"]["aiExposure"]).set(
                                    exp_scale_value)
                            except KeyError:
                                light_obj.parm(light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"]["exposure"]).set(
                                    exp_scale_value)

                    elif parm == "aiRoundness":
                        if value > 0.5:
                            light_obj.parm("light_type").set(light_data[renderer]["disk"]["light_node_sub_type"])

                    elif parm == "aiSoftEdge":
                        light_obj.parm(light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"][parm]).set(value)
                        if value != 0:
                            try:
                                normalize = json_load[light][renderer]["aiNormalize"]
                            except KeyError:
                                normalize = json_load[light][renderer]["normalize"]
                            try:
                                exposure = soft_edge_exposure_calc(normalize, json_load[light][renderer]["intensity"],
                                                                   json_load[light][renderer]["aiExposure"], scale, value)
                            except KeyError:
                                exposure = soft_edge_exposure_calc(normalize, json_load[light][renderer]["intensity"],
                                                                   json_load[light][renderer]["exposure"], scale, value)
                            light_obj.parm("light_exposure").set(exposure)

                    elif parm == "texture_node":
                        pass

                    elif parm == "texture_map":
                        if json_load[light][renderer]["nodeType"] == "aiSkyDomeLight":
                            light_obj.parm("env_map").set(value)
                        elif json_load[light][renderer]["nodeType"] == "areaLight" or json_load[light][renderer]["nodeType"] == "quad":
                            if bool(mat.node(json_load[light][renderer]["texture_node"])):
                                tex_node = mat.node(json_load[light][renderer]["texture_node"])
                            else:
                                tex_node = mat.createNode("texture::2.0", json_load[light][renderer]["texture_node"])
                                tex_node.parm("orient").set(1)
                                tex_node.parm("map").set(value)
                            light_obj.parm("shop_materialpath").set(tex_node.path())

                    elif parm == "aiCamera":
                        if 0.5 <= value <= 1:
                            light_obj.parm(light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"][parm]).set(True)
                        else:
                            light_obj.parm(light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"][parm]).set(False)

                    elif parm == "aiDiffuse":
                        if 0.5 <= value <= 1:
                            light_obj.parm(light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"][parm]).set(True)
                        else:
                            light_obj.parm(light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"][parm]).set(False)

                    elif parm == "aiSpecular":
                        for spec in light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"][parm]:
                            if 0.5 <= value <= 1:
                                light_obj.parm(spec).set(True)
                            else:
                                light_obj.parm(spec).set(False)

                    elif parm == "aiSss":
                        if 0.5 <= value <= 1:
                            light_obj.parm(light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"][parm]).set(True)
                        else:
                            light_obj.parm(light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"][parm]).set(False)

                    elif parm == "aiIndirect":
                        if 0.5 <= value <= 1:
                            light_obj.parm(light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"][parm]).set(True)
                        else:
                            light_obj.parm(light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"][parm]).set(False)

                    elif parm == "aiVolume":
                        if 0.5 <= value <= 1:
                            light_obj.parm(light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"][parm]).set(True)
                        else:
                            light_obj.parm(light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"][parm]).set(False)

                    elif parm == "aiTransmission":
                        if 0.5 <= value <= 1:
                            light_obj.parm(light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"][parm]).set(True)
                        else:
                            light_obj.parm(light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"][parm]).set(False)
                    else:
                        light_obj.parm(light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"][parm]).set(value)

            elif renderer == "Arnold" and arnold_check:
                if bool(obj.node("arnold_{0}".format(light))):
                    light_obj = obj.node("arnold_{0}".format(light))
                    light_obj.destroy()

                light_obj = obj.createNode("arnold_light", "arnold_{0}".format(light))
                light_nodes.append(light_obj)
                hou.Node.setSelected(light_obj, True)

                if json_load[light][renderer]["nodeType"] != "aiSkyDomeLight":
                    light_obj.parm("l_iconscale").set(scale)

                for parm, value in json_load[light][renderer].items():
                    if parm == "nodeType":
                        light_obj.parm("ar_light_type").set(light_data[renderer][json_load[light][renderer][parm]]["light_node_sub_type"])

                    elif parm == "translateX":
                        light_obj.parm(
                            light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"][parm]).set(value * scale)

                    elif parm == "translateY":
                        light_obj.parm(
                            light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"][parm]).set(value * scale)

                    elif parm == "translateZ":
                        light_obj.parm(
                            light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"][parm]).set(value * scale)

                    elif parm == "scaleX":
                        light_obj.parm(
                            light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"][parm]).set(
                            value * 2 * scale)

                    elif parm == "scaleY":
                        if json_load[light][renderer]["nodeType"] == "disk":
                            scale_x = json_load[light][renderer].get("scaleX")
                            light_obj.parm(
                                light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"][parm]).set(
                                ((value + scale_x) / 2) * scale)
                        elif json_load[light][renderer]["nodeType"] == "areaLight" or json_load[light][renderer]["nodeType"] == "quad":
                            light_obj.parm(
                                light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"][parm]).set(
                                value * 2 * scale)
                        elif json_load[light][renderer]["nodeType"] == "cylinder":
                            light_obj.parm(
                                light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"][parm]).set(
                                (value * 2) * scale)
                        else:
                            light_obj.parm(
                                light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"][parm]).set(
                                value * scale)

                    elif parm == "scaleZ":
                        if json_load[light][renderer]["nodeType"] == "cylinder":
                            scale_x = json_load[light][renderer].get("scaleX")
                            light_obj.parm(
                                light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"][parm]).set(
                                ((value + scale_x) / 2) * scale)
                        else:
                            light_obj.parm(
                                light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"][parm]).set(
                                value * scale)

                    elif parm == "aiExposure":
                        if json_load[light][renderer]["nodeType"] != "directionalLight":
                            if json_load[light][renderer].get("aiNormalize"):
                                exposure = light_exposure_calculator(value, 1, 1, scale)

                                light_obj.parm(
                                    light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"][parm]).set(
                                    exposure)
                            else:
                                light_obj.parm(
                                    light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"][parm]).set(
                                    value)

                    elif parm == "exposure":
                        if json_load[light][renderer]["nodeType"] != "directionalLight":
                            if json_load[light][renderer].get("normalize"):
                                exposure = light_exposure_calculator(value, 1, 1, scale)

                                light_obj.parm(
                                    light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"][parm]).set(
                                    exposure)
                            else:
                                light_obj.parm(
                                    light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"][parm]).set(
                                    value)

                    elif parm == "aiRadius":
                        light_obj.parm(
                            light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"][parm]).set(
                            value * scale)

                    elif parm == "coneAngle":
                        if json_load[light][renderer]["penumbraAngle"] < 0:
                            light_obj.parm(light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"][parm]).set(value)
                        else:
                            cone_angle = value + (json_load[light][renderer]["penumbraAngle"] * 2)
                            light_obj.parm(
                                light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"][parm]).set(
                                cone_angle)

                    elif parm == "penumbraAngle":
                        light_obj.parm(light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"][parm]).set(abs(value))

                    elif parm == "texture_map":
                        light_obj.parm("ar_light_color_type").set(1)
                        light_obj.parm("ar_light_color_texture").set(value)

                    else:
                        light_obj.parm(light_data[renderer][json_load[light][renderer]["nodeType"]]["light_parms"][parm]).set(value)

    if len(light_nodes) != 0:
        obj.layoutChildren(items=light_nodes)
    hou.ui.setStatusMessage("Lights Imported.")
