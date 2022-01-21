"""

maya_to_houdini_light_parms_py3.py

Only works in Python 3, due to Ordered Dictionary.

Generates Json file "maya_to_houdini_light_data.json"

"""

import json

# Translate Parameters Dictionary
translate_parms = {"translateX": "tx",
                   "translateY": "ty",
                   "translateZ": "tz"}

# Rotate  Parameters Dictionary
rotate_parms = {"rotateX": "rx",
                "rotateY": "ry",
                "rotateZ": "rz"}

# Color  Parameters Dictionary
color_light_params = {"colorR": "light_colorr",
                      "colorG": "light_colorg",
                      "colorB": "light_colorb"}

# Mantra Light Contribution Parameters Dictionary
mantra_light_contrib_parms = {"diffuse": "light_contribenable1",
                              "reflect": "light_contribenable2",
                              "coat": "light_contribenable3",
                              "sss": "light_contribenable4",
                              "indirect": "light_contribenable5",
                              "volume": "light_contribenable6",
                              "refract": "light_contribenable7",
                              "camera": "light_contribprimary"}

# Mantra Common Light Parameters Dictionary
mantra_common_light_parms = {"visibility": "light_enable",
                             "intensity": "light_intensity",
                             "aiSamples": "vm_samplingquality",
                             "aiCastShadows": "shadow_type",
                             "aiShadowDensity": "shadow_intensity",
                             "aiAov": "vm_lpetag",
                             "aiDiffuse": mantra_light_contrib_parms["diffuse"],
                             "aiSpecular": [mantra_light_contrib_parms["reflect"], mantra_light_contrib_parms["coat"]],
                             "aiSss": mantra_light_contrib_parms["sss"],
                             "aiIndirect": mantra_light_contrib_parms["indirect"],
                             "aiVolume": mantra_light_contrib_parms["volume"]}

# Mantra Repeating Parameters Dictionary
mantra_repeating_parms = {"exposure": "light_exposure",
                          "shadColorR": "shadow_colorr",
                          "shadColorG": "shadow_colorg",
                          "shadColorB": "shadow_colorb",
                          "normalize": "normalizearea"}

# Mantra Per Light Parameters Dictionary
mantra_per_light_parms = {"aiRadius": ["areasize1", "areasize2"],
                          "aiAngle": "vm_envangle",
                          "coneAngle": "coneangle",
                          "penumbraAngle": "conedelta",
                          "dropoff": "coneroll",
                          "aiSpread": ["coneangle", "conedelta", "coneroll"],
                          "aiSoftEdge": "edgewidth"}

# Mantra Point Light Parameters Dictionary
mantra_pointP_light_parms = {"aiExposure": mantra_repeating_parms["exposure"],
                             "shadColorR": mantra_repeating_parms["shadColorR"],
                             "shadColorG": mantra_repeating_parms["shadColorG"],
                             "shadColorB": mantra_repeating_parms["shadColorB"]}

# Mantra Sphere Light Parameters Dictionary
mantra_pointS_light_parms = {"aiExposure": mantra_repeating_parms["exposure"],
                             "aiRadius": mantra_per_light_parms["aiRadius"],
                             "aiNormalize": mantra_repeating_parms["normalize"],
                             "shadColorR": mantra_repeating_parms["shadColorR"],
                             "shadColorG": mantra_repeating_parms["shadColorG"],
                             "shadColorB": mantra_repeating_parms["shadColorB"],
                             "aiCamera": mantra_light_contrib_parms["camera"],
                             "aiTransmission": mantra_light_contrib_parms["refract"]}

# Mantra Distant Light Parameters Dictionary
mantra_directionalD_light_parms = {"aiExposure": mantra_repeating_parms["exposure"],
                                   "shadColorR": mantra_repeating_parms["shadColorR"],
                                   "shadColorG": mantra_repeating_parms["shadColorG"],
                                   "shadColorB": mantra_repeating_parms["shadColorB"]}

# Mantra Sun Light Parameters Dictionary
mantra_directionalS_light_parms = {"aiExposure": mantra_repeating_parms["exposure"],
                                   "aiAngle": mantra_per_light_parms["aiAngle"],
                                   "shadColorR": mantra_repeating_parms["shadColorR"],
                                   "shadColorG": mantra_repeating_parms["shadColorG"],
                                   "shadColorB": mantra_repeating_parms["shadColorB"]}

# Mantra Spot Light Point Light Parameters Dictionary
mantra_spotP_light_parms = {"coneAngle": mantra_per_light_parms["coneAngle"],
                            "penumbraAngle": mantra_per_light_parms["penumbraAngle"],
                            "dropoff": mantra_per_light_parms["dropoff"],
                            "aiExposure": mantra_repeating_parms["exposure"],
                            "shadColorR": mantra_repeating_parms["shadColorR"],
                            "shadColorG": mantra_repeating_parms["shadColorG"],
                            "shadColorB": mantra_repeating_parms["shadColorB"]}

# Mantra Spot Light Sphere Light Parameters Dictionary
mantra_spotS_light_parms = {"coneAngle": mantra_per_light_parms["coneAngle"],
                            "penumbraAngle": mantra_per_light_parms["penumbraAngle"],
                            "dropoff": mantra_per_light_parms["dropoff"],
                            "aiExposure": mantra_repeating_parms["exposure"],
                            "aiRadius": mantra_per_light_parms["aiRadius"],
                            "aiNormalize": mantra_repeating_parms["normalize"],
                            "shadColorR": mantra_repeating_parms["shadColorR"],
                            "shadColorG": mantra_repeating_parms["shadColorG"],
                            "shadColorB": mantra_repeating_parms["shadColorB"]}

# Mantra Grid Light Parameters Dictionary
mantra_area_light_parms = {"aiExposure": mantra_repeating_parms["exposure"],
                           "scaleX": "areasize1",
                           "scaleY": "areasize2",
                           "aiNormalize": mantra_repeating_parms["normalize"],
                           "aiSpread": ["coneangle", "conedelta", "coneroll"],
                           "aiSoftEdge": "edgewidth",
                           "aiRoundness": "",
                           "aiShadowColorR": mantra_repeating_parms["shadColorR"],
                           "aiShadowColorG": mantra_repeating_parms["shadColorG"],
                           "aiShadowColorB": mantra_repeating_parms["shadColorB"],
                           "aiCamera": mantra_light_contrib_parms["camera"],
                           "aiTransmission": mantra_light_contrib_parms["refract"]}

# Mantra Grid Light Parameters Dictionary
mantra_quad_light_parms = {"exposure": mantra_repeating_parms["exposure"],
                           "scaleX": "areasize1",
                           "scaleY": "areasize2",
                           "normalize": mantra_repeating_parms["normalize"],
                           "aiSpread": mantra_per_light_parms["aiSpread"],
                           "aiSoftEdge": mantra_per_light_parms["aiSoftEdge"],
                           "aiRoundness": "",
                           "aiShadowColorR": mantra_repeating_parms["shadColorR"],
                           "aiShadowColorG": mantra_repeating_parms["shadColorG"],
                           "aiShadowColorB": mantra_repeating_parms["shadColorB"],
                           "aiCamera": mantra_light_contrib_parms["camera"],
                           "aiTransmission": mantra_light_contrib_parms["refract"]}

# Mantra Disk Light Parameters Dictionary
mantra_disk_light_parms = {"exposure": mantra_repeating_parms["exposure"],
                           "scaleX": "areasize1",
                           "scaleY": "areasize2",
                           "normalize": mantra_repeating_parms["normalize"],
                           "aiSpread": mantra_per_light_parms["aiSpread"],
                           "aiShadowColorR": mantra_repeating_parms["shadColorR"],
                           "aiShadowColorG": mantra_repeating_parms["shadColorG"],
                           "aiShadowColorB": mantra_repeating_parms["shadColorB"],
                           "aiCamera": mantra_light_contrib_parms["camera"],
                           "aiTransmission": mantra_light_contrib_parms["refract"]}

# Mantra Tube Light Parameters Dictionary
mantra_cylinderC_light_parms = {"rotateX": "ry",
                                "rotateY": "rx",
                                "rotateZ": "rz",
                                "exposure": mantra_repeating_parms["exposure"],
                                "scaleX": "areasize2",
                                "scaleY": "areasize1",
                                "scaleZ": "areasize2",
                                "normalize": mantra_repeating_parms["normalize"],
                                "aiShadowColorR": mantra_repeating_parms["shadColorR"],
                                "aiShadowColorG": mantra_repeating_parms["shadColorG"],
                                "aiShadowColorB": mantra_repeating_parms["shadColorB"],
                                "aiCamera": mantra_light_contrib_parms["camera"],
                                "aiTransmission": mantra_light_contrib_parms["refract"]}

# Mantra Line Light Parameters Dictionary
mantra_cylinderL_light_parms = {"rotateX": "ry",
                                "rotateY": "rx",
                                "rotateZ": "rz",
                                "exposure": mantra_repeating_parms["exposure"],
                                "scaleY": "areasize1",
                                "normalize": mantra_repeating_parms["normalize"],
                                "aiShadowColorR": mantra_repeating_parms["shadColorR"],
                                "aiShadowColorG": mantra_repeating_parms["shadColorG"],
                                "aiShadowColorB": mantra_repeating_parms["shadColorB"]}

# Mantra Environment Light Parameters Dictionary
mantra_skydome_light_parms = {"exposure": mantra_repeating_parms["exposure"],
                              "camera": mantra_light_contrib_parms["camera"],
                              "transmission": mantra_light_contrib_parms["refract"]}

# Mantra Light Types Dictionary
mantra_light_type = ["pointLightP", "pointLightS", "directionalLightD", "directionalLightS", "spotLightP", "spotLightS",
                     "areaLight", "quad", "disk", "cylinderC", "cylinderL", "aiSkyDomeLight"]

# Mantra Light Node Type Dictionary
mantra_light_node_type = ["hlight::2.0", "hlight::2.0", "hlight::2.0", "hlight::2.0", "hlight::2.0", "hlight::2.0",
                          "hlight::2.0", "hlight::2.0", "hlight::2.0", "hlight::2.0", "hlight::2.0", "envlight"]

# Mantra Light Node Sub-Type Dictionary e.g. Point, Spot
mantra_light_node_sub_type = [0, 4, 7, 8, 0, 4, 2, 2, 3, 5, 1, ""]

# Mantra Light Number of Contributions Dictionary e.g. Diffuse, Specular
mantra_num_of_light_contrib = [6, 7, 6, 6, 6, 6, 7, 7, 7, 7, 6, 7]

# Mantra Light Parameters Combine Dictionary
mantra_light_parms = [
    {**translate_parms, **rotate_parms, **mantra_common_light_parms, **color_light_params, **mantra_pointP_light_parms},
    {**translate_parms, **rotate_parms, **mantra_common_light_parms, **color_light_params, **mantra_pointS_light_parms},
    {**translate_parms, **rotate_parms, **mantra_common_light_parms, **color_light_params,
     **mantra_directionalD_light_parms},
    {**translate_parms, **rotate_parms, **mantra_common_light_parms, **color_light_params,
     **mantra_directionalS_light_parms},
    {**translate_parms, **rotate_parms, **mantra_common_light_parms, **color_light_params, **mantra_spotP_light_parms},
    {**translate_parms, **rotate_parms, **mantra_common_light_parms, **color_light_params, **mantra_spotS_light_parms},
    {**translate_parms, **rotate_parms, **mantra_common_light_parms, **color_light_params, **mantra_area_light_parms},
    {**translate_parms, **rotate_parms, **mantra_common_light_parms, **color_light_params, **mantra_quad_light_parms},
    {**translate_parms, **rotate_parms, **mantra_common_light_parms, **color_light_params, **mantra_disk_light_parms},
    {**translate_parms, **mantra_common_light_parms, **color_light_params, **mantra_cylinderC_light_parms},
    {**translate_parms, **mantra_common_light_parms, **color_light_params, **mantra_cylinderL_light_parms},
    {**translate_parms, **rotate_parms, **mantra_common_light_parms, **color_light_params,
     **mantra_skydome_light_parms}]

# Arnold Light Types Dictionary
arnold_light_type = ["pointLight", "directionalLight", "spotLight", "areaLight", "quad", "disk", "cylinder",
                     "aiSkyDomeLight"]

# Arnold Light Node Sub-Type Dictionary e.g. Point, Spot
arnold_light_node_sub_type = [0, 1, 2, 3, 3, 4, 5, 6]

# Arnold Light Contribution Parameters Dictionary
arnold_light_contrib_parms = {"aiDiffuse": "ar_diffuse",
                              "aiSpecular": "ar_specular",
                              "aiSss": "ar_sss",
                              "aiIndirect": "ar_indirect",
                              "aiVolume": "ar_volume",
                              "aiTransmission": "ar_transmission",
                              "aiCamera": "ar_camera"}

# Arnold Common Light Parameters Dictionary
arnold_common_light_parms = {"visibility": "light_enable",
                             "intensity": "ar_intensity",
                             "aiSamples": "ar_samples",
                             "aiVolumeSamples": "ar_volume_samples",
                             "aiShadowDensity": "ar_shadow_density",
                             "aiCastShadows": "ar_cast_shadows",
                             "aiCastVolumetricShadows": "ar_cast_volumetric_shadows",
                             "aiDiffuse": arnold_light_contrib_parms["aiDiffuse"],
                             "aiSpecular": arnold_light_contrib_parms["aiSpecular"],
                             "aiSss": arnold_light_contrib_parms["aiSss"],
                             "aiIndirect": arnold_light_contrib_parms["aiIndirect"],
                             "aiVolume": arnold_light_contrib_parms["aiVolume"],
                             "aiMaxBounces": "ar_max_bounces",
                             "aiAov": "ar_aov"}

# Arnold Repeating Parameters Dictionary
arnold_repeating_parms = {"exposure": "ar_exposure",
                          "shadColorR": "ar_shadow_colorr",
                          "shadColorG": "ar_shadow_colorg",
                          "shadColorB": "ar_shadow_colorb",
                          "normalize": "ar_normalize"}

# Arnold Per Light Parameters Dictionary
arnold_per_light_parms = {"aiAngle": "ar_angle",
                          "coneAngle": "ar_cone_angle",
                          "penumbraAngle": "ar_penumbra_angle",
                          "aiRoundness": "ar_quad_roundness",
                          "aiSoftEdge": "ar_soft_edge",
                          "aiSpread": "ar_spread",
                          "scaleX": "ar_quad_sizex",
                          "scaleY": "ar_quad_sizey"}

# Arnold Point Light Parameters Dictionary
arnold_point_light_parms = {"aiExposure": arnold_repeating_parms["exposure"],
                            "aiRadius": "ar_point_radius",
                            "aiNormalize": arnold_repeating_parms["normalize"],
                            "shadColorR": arnold_repeating_parms["shadColorR"],
                            "shadColorG": arnold_repeating_parms["shadColorG"],
                            "shadColorB": arnold_repeating_parms["shadColorB"],
                            "aiCamera": arnold_light_contrib_parms["aiCamera"],
                            "aiTransmission": arnold_light_contrib_parms["aiTransmission"]}

# Arnold Directional Light Parameters Dictionary
arnold_directional_light_parms = {"aiExposure": arnold_repeating_parms["exposure"],
                                  "aiAngle": arnold_per_light_parms["aiAngle"],
                                  "aiNormalize": arnold_repeating_parms["normalize"],
                                  "shadColorR": arnold_repeating_parms["shadColorR"],
                                  "shadColorG": arnold_repeating_parms["shadColorG"],
                                  "shadColorB": arnold_repeating_parms["shadColorB"]}

# Arnold Spot Light Parameters Dictionary
arnold_spot_light_parms = {"aiExposure": arnold_repeating_parms["exposure"],
                           "aiRoundness": "ar_spot_roundness",
                           "coneAngle": arnold_per_light_parms["coneAngle"],
                           "penumbraAngle": arnold_per_light_parms["penumbraAngle"],
                           "aiRadius": "ar_spot_radius",
                           "aiLensRadius": "ar_lens_radius",
                           "aiAspectRatio": "ar_aspect_ratio",
                           "aiNormalize": arnold_repeating_parms["normalize"],
                           "shadColorR": arnold_repeating_parms["shadColorR"],
                           "shadColorG": arnold_repeating_parms["shadColorG"],
                           "shadColorB": arnold_repeating_parms["shadColorB"]}

# Arnold Area Light Parameters Dictionary
arnold_area_light_parms = {"aiExposure": arnold_repeating_parms["exposure"],
                           "aiRoundness": arnold_per_light_parms["aiRoundness"],
                           "aiSoftEdge": arnold_per_light_parms["aiSoftEdge"],
                           "aiSpread": arnold_per_light_parms["aiSpread"],
                           "scaleX": arnold_per_light_parms["scaleX"],
                           "scaleY": arnold_per_light_parms["scaleY"],
                           "aiNormalize": arnold_repeating_parms["normalize"],
                           "shadColorR": arnold_repeating_parms["shadColorR"],
                           "shadColorG": arnold_repeating_parms["shadColorG"],
                           "shadColorB": arnold_repeating_parms["shadColorB"],
                           "aiCamera": arnold_light_contrib_parms["aiCamera"],
                           "aiTransmission": arnold_light_contrib_parms["aiTransmission"]}

# Arnold Quad Light Parameters Dictionary
arnold_quad_light_parms = {"exposure": arnold_repeating_parms["exposure"],
                           "aiRoundness": arnold_per_light_parms["aiRoundness"],
                           "aiSoftEdge": arnold_per_light_parms["aiSoftEdge"],
                           "aiSpread": arnold_per_light_parms["aiSpread"],
                           "scaleX": arnold_per_light_parms["scaleX"],
                           "scaleY": arnold_per_light_parms["scaleY"],
                           "normalize": arnold_repeating_parms["normalize"],
                           "aiShadowColorR": arnold_repeating_parms["shadColorR"],
                           "aiShadowColorG": arnold_repeating_parms["shadColorG"],
                           "aiShadowColorB": arnold_repeating_parms["shadColorB"],
                           "aiCamera": arnold_light_contrib_parms["aiCamera"],
                           "aiTransmission": arnold_light_contrib_parms["aiTransmission"]}

# Arnold Disk Light Parameters Dictionary
arnold_disk_light_parms = {"exposure": arnold_repeating_parms["exposure"],
                           "aiRoundness": arnold_per_light_parms["aiRoundness"],
                           "aiSoftEdge": arnold_per_light_parms["aiSoftEdge"],
                           "aiSpread": arnold_per_light_parms["aiSpread"],
                           "scaleX": "ar_disk_radius",
                           "scaleY": "ar_disk_radius",
                           "normalize": arnold_repeating_parms["normalize"],
                           "aiShadowColorR": arnold_repeating_parms["shadColorR"],
                           "aiShadowColorG": arnold_repeating_parms["shadColorG"],
                           "aiShadowColorB": arnold_repeating_parms["shadColorB"],
                           "aiCamera": arnold_light_contrib_parms["aiCamera"],
                           "aiTransmission": arnold_light_contrib_parms["aiTransmission"]}

# Arnold Cylinder Light Parameters Dictionary
arnold_cylinder_light_parms = {"exposure": arnold_repeating_parms["exposure"],
                               "scaleX": "ar_cylinder_radius",
                               "scaleY": "ar_height",
                               "scaleZ": "ar_cylinder_radius",
                               "normalize": arnold_repeating_parms["normalize"],
                               "aiShadowColorR": arnold_repeating_parms["shadColorR"],
                               "aiShadowColorG": arnold_repeating_parms["shadColorG"],
                               "aiShadowColorB": arnold_repeating_parms["shadColorB"],
                               "aiCamera": arnold_light_contrib_parms["aiCamera"],
                               "aiTransmission": arnold_light_contrib_parms["aiTransmission"]}

# Arnold Skydome Light Parameters Dictionary
arnold_skydome_light_parms = {"resolution": "ar_resolution",
                              "format": "ar_format",
                              "exposure": arnold_repeating_parms["exposure"],
                              "aiShadowColorR": arnold_repeating_parms["shadColorR"],
                              "aiShadowColorG": arnold_repeating_parms["shadColorG"],
                              "aiShadowColorB": arnold_repeating_parms["shadColorB"],
                              "camera": arnold_light_contrib_parms["aiCamera"],
                              "transmission": arnold_light_contrib_parms["aiTransmission"],
                              "aiAovIndirect": "ar_aov_indirect"}

# Arnold Light Parameters Combine Dictionary
arnold_light_parms = [
    {**translate_parms, **rotate_parms, **arnold_common_light_parms, **color_light_params, **arnold_point_light_parms},
    {**translate_parms, **rotate_parms, **arnold_common_light_parms, **color_light_params,
     **arnold_directional_light_parms},
    {**translate_parms, **rotate_parms, **arnold_common_light_parms, **color_light_params, **arnold_spot_light_parms},
    {**translate_parms, **rotate_parms, **arnold_common_light_parms, **color_light_params, **arnold_area_light_parms},
    {**translate_parms, **rotate_parms, **arnold_common_light_parms, **color_light_params, **arnold_quad_light_parms},
    {**translate_parms, **rotate_parms, **arnold_common_light_parms, **color_light_params, **arnold_disk_light_parms},
    {**translate_parms, **rotate_parms, **arnold_common_light_parms, **color_light_params,
     **arnold_cylinder_light_parms},
    {**translate_parms, **rotate_parms, **arnold_common_light_parms, **color_light_params,
     **arnold_skydome_light_parms}]

# Main Light Data Dictionary
light_data_dict = {}

# Mantra Light Data Dictionary
mantra_light_data_dict = {}

# Arnold Light Data Dictionary
arnold_light_data_dict = {}

# Dictionary Generation
for a, b, c, d, e in zip(mantra_light_type, mantra_light_node_type, mantra_light_node_sub_type,
                         mantra_num_of_light_contrib, mantra_light_parms):
    mantra_light_data_dict.setdefault(a, {})["light_node_type"] = b
    mantra_light_data_dict.setdefault(a, {})["light_node_sub_type"] = c
    mantra_light_data_dict.setdefault(a, {})["num_of_light_contrib"] = d
    mantra_light_data_dict.setdefault(a, {})["light_parms"] = e

for a, b, c in zip(arnold_light_type, arnold_light_node_sub_type, arnold_light_parms):
    arnold_light_data_dict.setdefault(a, {})["light_node_sub_type"] = b
    arnold_light_data_dict.setdefault(a, {})["light_parms"] = c

light_data_dict["Mantra"] = mantra_light_data_dict
light_data_dict["Arnold"] = arnold_light_data_dict

light_data_dict["light_contribution_parms"] = mantra_light_contrib_parms
light_data_dict["color_light_params"] = color_light_params

# Json Export
path = r"C:\Users\bhave\PycharmProjects\maya_to_houdini_light_transfer\logic\maya_to_houdini_light_data.json"

with open(path, "w") as json_file:
    json.dump(light_data_dict, json_file, indent=4, ensure_ascii=False)
