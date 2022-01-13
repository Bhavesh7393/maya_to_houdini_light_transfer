import json

translate_parms = {"translateX": "tx",
                   "translateY": "ty",
                   "translateZ": "tz"}

rotate_parms = {"rotateX": "rx",
                "rotateY": "ry",
                "rotateZ": "rz"}

color_light_params = {"colorR": "light_colorr",
                      "colorG": "light_colorg",
                      "colorB": "light_colorb"}

light_contribution_parms = {"diffuse": "light_contribenable1",
                            "reflect": "light_contribenable2",
                            "coat": "light_contribenable3",
                            "sss": "light_contribenable4",
                            "indirect": "light_contribenable5",
                            "volume": "light_contribenable6",
                            "refract": "light_contribenable7",
                            "camera": "light_contribprimary"}

common_light_parms = {"visibility": "light_enable",
                      "intensity": "light_intensity",
                      "aiSamples": "vm_samplingquality",
                      "aiCastShadows": "shadow_type",
                      "aiShadowDensity": "shadow_intensity",
                      "aiAov": "vm_lpetag",
                      "aiDiffuse": light_contribution_parms["diffuse"],
                      "aiSpecular": [light_contribution_parms["reflect"], light_contribution_parms["coat"]],
                      "aiSss": light_contribution_parms["sss"],
                      "aiIndirect": light_contribution_parms["indirect"],
                      "aiVolume": light_contribution_parms["volume"]}

repeating_parms = {"exposure": "light_exposure",
                   "shadColorR": "shadow_colorr",
                   "shadColorG": "shadow_colorg",
                   "shadColorB": "shadow_colorb",
                   "normalize": "normalizearea"}

per_light_parms = {"aiRadius": ["areasize1", "areasize2"],
                   "aiAngle": "vm_envangle",
                   "coneAngle": "coneangle",
                   "penumbraAngle": "conedelta",
                   "dropoff": "coneroll",
                   "aiSpread": ["coneangle", "conedelta", "coneroll"],
                   "aiSoftEdge": "edgewidth"}

pointP_light_parms = {"aiExposure": repeating_parms["exposure"],
                      "shadColorR": repeating_parms["shadColorR"],
                      "shadColorG": repeating_parms["shadColorG"],
                      "shadColorB": repeating_parms["shadColorB"]}

pointS_light_parms = {"aiExposure": repeating_parms["exposure"],
                      "aiRadius": per_light_parms["aiRadius"],
                      "aiNormalize": repeating_parms["normalize"],
                      "shadColorR": repeating_parms["shadColorR"],
                      "shadColorG": repeating_parms["shadColorG"],
                      "shadColorB": repeating_parms["shadColorB"],
                      "aiCamera": light_contribution_parms["camera"],
                      "aiTransmission": light_contribution_parms["refract"]}

directionalD_light_parms = {"aiExposure": repeating_parms["exposure"],
                            "shadColorR": repeating_parms["shadColorR"],
                            "shadColorG": repeating_parms["shadColorG"],
                            "shadColorB": repeating_parms["shadColorB"]}

directionalS_light_parms = {"aiExposure": repeating_parms["exposure"],
                            "aiAngle": per_light_parms["aiAngle"],
                            "shadColorR": repeating_parms["shadColorR"],
                            "shadColorG": repeating_parms["shadColorG"],
                            "shadColorB": repeating_parms["shadColorB"]}

spotP_light_parms = {"coneAngle": per_light_parms["coneAngle"],
                     "penumbraAngle": per_light_parms["penumbraAngle"],
                     "dropoff": per_light_parms["dropoff"],
                     "aiExposure": repeating_parms["exposure"],
                     "shadColorR": repeating_parms["shadColorR"],
                     "shadColorG": repeating_parms["shadColorG"],
                     "shadColorB": repeating_parms["shadColorB"]}

spotS_light_parms = {"coneAngle": per_light_parms["coneAngle"],
                     "penumbraAngle": per_light_parms["penumbraAngle"],
                     "dropoff": per_light_parms["dropoff"],
                     "aiExposure": repeating_parms["exposure"],
                     "aiRadius": per_light_parms["aiRadius"],
                     "aiNormalize": repeating_parms["normalize"],
                     "shadColorR": repeating_parms["shadColorR"],
                     "shadColorG": repeating_parms["shadColorG"],
                     "shadColorB": repeating_parms["shadColorB"]}

area_light_parms = {"aiExposure": repeating_parms["exposure"],
                    "scaleX": "areasize1",
                    "scaleY": "areasize2",
                    "aiNormalize": repeating_parms["normalize"],
                    "aiSpread": ["coneangle", "conedelta", "coneroll"],
                    "aiSoftEdge": "edgewidth",
                    "aiRoundness": "",
                    "aiShadowColorR": repeating_parms["shadColorR"],
                    "aiShadowColorG": repeating_parms["shadColorG"],
                    "aiShadowColorB": repeating_parms["shadColorB"],
                    "aiCamera": light_contribution_parms["camera"],
                    "aiTransmission": light_contribution_parms["refract"]}

quad_light_parms = {"exposure": repeating_parms["exposure"],
                    "scaleX": "areasize1",
                    "scaleY": "areasize2",
                    "normalize": repeating_parms["normalize"],
                    "aiSpread": per_light_parms["aiSpread"],
                    "aiSoftEdge": per_light_parms["aiSoftEdge"],
                    "aiRoundness": "",
                    "aiShadowColorR": repeating_parms["shadColorR"],
                    "aiShadowColorG": repeating_parms["shadColorG"],
                    "aiShadowColorB": repeating_parms["shadColorB"],
                    "aiCamera": light_contribution_parms["camera"],
                    "aiTransmission": light_contribution_parms["refract"]}

disk_light_parms = {"exposure": repeating_parms["exposure"],
                    "scaleX": "areasize1",
                    "scaleY": "areasize2",
                    "normalize": repeating_parms["normalize"],
                    "aiSpread": per_light_parms["aiSpread"],
                    "aiShadowColorR": repeating_parms["shadColorR"],
                    "aiShadowColorG": repeating_parms["shadColorG"],
                    "aiShadowColorB": repeating_parms["shadColorB"],
                    "aiCamera": light_contribution_parms["camera"],
                    "aiTransmission": light_contribution_parms["refract"]}

cylinderC_light_parms = {"rotateX": "ry",
                         "rotateY": "rx",
                         "rotateZ": "rz",
                         "exposure": repeating_parms["exposure"],
                         "scaleX": "areasize2",
                         "scaleY": "areasize1",
                         "scaleZ": "areasize2",
                         "normalize": repeating_parms["normalize"],
                         "aiShadowColorR": repeating_parms["shadColorR"],
                         "aiShadowColorG": repeating_parms["shadColorG"],
                         "aiShadowColorB": repeating_parms["shadColorB"],
                         "aiCamera": light_contribution_parms["camera"],
                         "aiTransmission": light_contribution_parms["refract"]}

cylinderL_light_parms = {"rotateX": "ry",
                         "rotateY": "rx",
                         "rotateZ": "rz",
                         "exposure": repeating_parms["exposure"],
                         "scaleY": "areasize1",
                         "normalize": repeating_parms["normalize"],
                         "aiShadowColorR": repeating_parms["shadColorR"],
                         "aiShadowColorG": repeating_parms["shadColorG"],
                         "aiShadowColorB": repeating_parms["shadColorB"]}

skydome_light_parms = {"exposure": repeating_parms["exposure"],
                       "camera": light_contribution_parms["camera"],
                       "transmission": light_contribution_parms["refract"]}

maya_light_type = ["pointLightP", "pointLightS", "directionalLightD", "directionalLightS", "spotLightP", "spotLightS",
                   "areaLight", "quad", "disk", "cylinderC", "cylinderL", "aiSkyDomeLight"]

mantra_light_node_type = ["hlight::2.0", "hlight::2.0", "hlight::2.0", "hlight::2.0", "hlight::2.0", "hlight::2.0",
                          "hlight::2.0", "hlight::2.0", "hlight::2.0", "hlight::2.0", "hlight::2.0", "envlight"]

mantra_light_type = [0, 4, 7, 8, 0, 4, 2, 2, 3, 5, 1, ""]

num_of_light_contributions = [6, 7, 6, 6, 6, 6, 7, 7, 7, 7, 6, 7]

mantra_light_parms = [
    {**translate_parms, **rotate_parms, **common_light_parms, **color_light_params, **pointP_light_parms},
    {**translate_parms, **rotate_parms, **common_light_parms, **color_light_params, **pointS_light_parms},
    {**translate_parms, **rotate_parms, **common_light_parms, **color_light_params, **directionalD_light_parms},
    {**translate_parms, **rotate_parms, **common_light_parms, **color_light_params, **directionalS_light_parms},
    {**translate_parms, **rotate_parms, **common_light_parms, **color_light_params, **spotP_light_parms},
    {**translate_parms, **rotate_parms, **common_light_parms, **color_light_params, **spotS_light_parms},
    {**translate_parms, **rotate_parms, **common_light_parms, **color_light_params, **area_light_parms},
    {**translate_parms, **rotate_parms, **common_light_parms, **color_light_params, **quad_light_parms},
    {**translate_parms, **rotate_parms, **common_light_parms, **color_light_params, **disk_light_parms},
    {**translate_parms, **common_light_parms, **color_light_params, **cylinderC_light_parms},
    {**translate_parms, **common_light_parms, **color_light_params, **cylinderL_light_parms},
    {**translate_parms, **rotate_parms, **common_light_parms, **color_light_params, **skydome_light_parms}]

light_data_dict = {}

for a, b, c, d, e in zip(maya_light_type, mantra_light_node_type, mantra_light_type, num_of_light_contributions,
                         mantra_light_parms):
    light_data_dict.setdefault(a, {})["mantra_light_node_type"] = b
    light_data_dict.setdefault(a, {})["mantra_light_type"] = c
    light_data_dict.setdefault(a, {})["num_of_light_contributions"] = d
    light_data_dict.setdefault(a, {})["mantra_light_parms"] = e

light_data_dict["light_contribution_parms"] = light_contribution_parms
light_data_dict["color_light_params"] = color_light_params

path = r"C:\Users\bhave\PycharmProjects\arnold_to_mantra_light_transfer\logic\arnold_to_mantra_light_data.json"

with open(path, "w") as json_file:
    json.dump(light_data_dict, json_file, indent=4, ensure_ascii=False)
