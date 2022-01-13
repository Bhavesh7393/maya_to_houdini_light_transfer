light_type = {"pointLight": 0,
              "directionalLight": 1,
              "spotLight": 2,
              "areaLight": 3,
              "quad": 3,
              "disk": 4,
              "cylinder": 5,
              "aiSkyDomeLight": 6}

translate_parms = {"translateX": "tx",
                   "translateY": "ty",
                   "translateZ": "tz"}

rotate_parms = {"rotateX": "rx",
                "rotateY": "ry",
                "rotateZ": "rz"}

common_light_parms = {"visibility": "light_enable",
                      "intensity": "ar_intensity",
                      "aiSamples": "ar_samples",
                      "aiVolumeSamples": "ar_volume_samples",
                      "aiShadowDensity": "ar_shadow_density",
                      "aiCastShadows": "ar_cast_shadows",
                      "aiCastVolumetricShadows": "ar_cast_volumetric_shadows",
                      "aiDiffuse": "ar_diffuse",
                      "aiSpecular": "ar_specular",
                      "aiSss": "ar_sss",
                      "aiIndirect": "ar_indirect",
                      "aiVolume": "ar_volume",
                      "aiMaxBounces": "ar_max_bounces",
                      "aiAov": "ar_aov"}

color_light_params = {"colorR": "ar_colorr",
                      "colorG": "ar_colorg",
                      "colorB": "ar_colorb", }

point_light_parms = {"aiExposure": "ar_exposure",
                     "aiRadius": "ar_point_radius",
                     "aiNormalize": "ar_normalize",
                     "shadColorR": "ar_shadow_colorr",
                     "shadColorG": "ar_shadow_colorg",
                     "shadColorB": "ar_shadow_colorb",
                     "aiCamera": "ar_camera",
                     "aiTransmission": "ar_transmission"}

directional_light_parms = {"aiExposure": "ar_exposure",
                           "aiAngle": "ar_angle",
                           "aiNormalize": "ar_normalize",
                           "shadColorR": "ar_shadow_colorr",
                           "shadColorG": "ar_shadow_colorg",
                           "shadColorB": "ar_shadow_colorb"}

spot_light_parms = {"aiExposure": "ar_exposure",
                    "aiRoundness": "ar_spot_roundness",
                    "aiRadius": "ar_spot_radius",
                    "aiLensRadius": "ar_lens_radius",
                    "aiAspectRatio": "ar_aspect_ratio",
                    "aiNormalize": "ar_normalize",
                    "shadColorR": "ar_shadow_colorr",
                    "shadColorG": "ar_shadow_colorg",
                    "shadColorB": "ar_shadow_colorb"}
