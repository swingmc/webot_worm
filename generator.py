# Define appearance properties
def create_appearance(base_color, roughness=1, metalness=0, transparency=0):
    return {
        "PBRAppearance": {
            "baseColor": base_color,
            "roughness": roughness,
            "metalness": metalness,
            "transparency": transparency
        }
    }

# Define shape properties
def create_shape(geometry_type, geometry_props, appearance):
    return {
        "Shape": {
            "appearance": appearance,
            "geometry": {
                geometry_type: geometry_props
            }
        }
    }

# Define physics properties
def create_physics(density, mass, center_of_mass=None):
    return {
        "Physics": {
            "density": density,
            "mass": mass,
            "centerOfMass": center_of_mass
        }
    }


def serialize_vrml(node, indent=0):
    """
    Recursively serializes a nested dictionary structure into VRML format.
    
    Args:
        node (dict): The nested dictionary representing the VRML nodes and properties.
        indent (int): Current indentation level for formatting the output.
    
    Returns:
        str: A string containing the serialized VRML code.
    """
    vrml_str = ""
    # Determine the indentation level
    space = "  " * indent

    square_brackets_list = ["muscles", "centerOfMass", "color", "device", "children"]
    
    if isinstance(node, dict):
        # Process dictionary type nodes
        for key, value in node.items():
            if isinstance(value, dict):
                vrml_str += f"{{{space}\n"
                if key in square_brackets_list:
                    vrml_str += f"{space}{key} [\n"
                # If the value is a dictionary, it represents a complex node
                #if 'type' in value:
                #    vrml_str += f"{space}{key} {value['type']} {{\n"
                # Recursively serialize child nodes
                #if 'children' in value:
                #    vrml_str += serialize_vrml(value['children'], indent + 1)
                vrml_str += serialize_vrml(value, indent + 1)
                vrml_str += f"{space}}}\n"
            else:
                # Handle simple attributes
                vrml_str += f"{space}{key} {value}\n"
    else:
        # Handle base type nodes
        vrml_str += f"{space}{node}\n"
    
    return vrml_str

# Example dictionary representing a VRML structure
vrml_dict = {
    "WorldInfo": {
        "type": "WorldInfo",
        "children": {
            "info": ["\"Example world demonstrating the use of the Muscle node\""],
            "title": "\"Muscle\"",
            "basicTimeStep": 16
        }
    },
    "Viewpoint": {
        "type": "Viewpoint",
        "children": {
            "orientation": "-0.5223578251770465 0.09301806886713386 0.8476378597847877 2.7753819314893793",
            "position": "0.26745501991810305 -0.05987278174127601 0.44031085296688044"
        }
    },
    "TexturedBackground": {
        "type": "TexturedBackground",
        "children": {}
    },
    
}



vrml_robot = {
    "DEF HINGE": {
        "type": "Robot",
        "translation": "0 0 0.04",
        "children": {
                "DEF BOX": {
                    "type": "Pose",
                    "translation": "-0.025 0 -0.01",
                    "children": 
                        {
                            "Shape": {
                                "appearance": {
                                    "PBRAppearance": {
                                        "baseColor": "0.8 0.8 0.8",
                                        "roughness": 1,
                                        "metalness": 0
                                    }
                                },
                                "geometry": {
                                    "Box": {
                                        "size": "0.05 0.08 0.06"
                                    }
                                }
                            }
                        }
                    
                },
                "DEF JOINT Shape": {
                    "type": "Shape",
                    "appearance": {
                        "PBRAppearance": {
                            "baseColor": "0.337255 0.337255 0.337255",
                            "transparency": "0.009999999776482582",
                            "roughness": 1,
                            "metalness": 0
                        }
                    },
                    "geometry": {
                        "Sphere": {
                            "radius": "0.008"
                        }
                    }
                },
                "DEF BONE1 Pose": {
                    "type": "Pose",
                    "translation": "0.05 0 0",
                    "rotation": "0 1 0 -1.5707953071795862",
                    "children": [
                        {
                            "Shape": {
                                "appearance": {
                                    "PBRAppearance": {
                                        "baseColor": "0.8 0.8 0.8",
                                        "roughness": 1,
                                        "metalness": 0
                                    }
                                },
                                "geometry": {
                                    "Capsule": {
                                        "height": "0.1",
                                        "radius": "0.005"
                                    }
                                }
                            }
                        }
                    ]
                },
                "HingeJoint": {
                    "type": "HingeJoint",
                    "jointParameters": {
                        "HingeJointParameters": {
                            "axis": "0 -1 0",
                            "anchor": "0.1 0 0",
                            "dampingConstant": "0.4",
                            "suspensionAxis": "0 1 0"
                        }
                    },
                    "device": [
                        {
                            "RotationalMotor": {
                                "name": "muscle",
                                "controlPID": "1 0.1 0",
                                "minPosition": "-0.5",
                                "maxPosition": "3",
                                "maxTorque": "0.5",
                                "muscles": [
                                    {
                                        "Muscle": {
                                            "volume": "0.0001",
                                            "startOffset": "0.01 0 0",
                                            "endOffset": "0 0.05 0",
                                            "color": ["1 0 0", "1 1 0", "1 0 1"]
                                        }
                                    },
                                    {
                                        "Muscle": {
                                            "volume": "6e-05",
                                            "startOffset": "0.1 0 0",
                                            "endOffset": "0 0.05 0"
                                        }
                                    }
                                ]
                            }
                        },
                        {
                            "PositionSensor": {}
                        }
                    ],
                    "endPoint": {
                        "Solid": {
                            "translation": "0.1 0 0",
                            "rotation": "0 0 1 -1.5707996938995747",
                            "children": [
                                {
                                    "USE JOINT": {},
                                    "DEF BONE2 Pose": {
                                        "type": "Pose",
                                        "translation": "0 0.0225 0",
                                        "rotation": "1 0 0 1.5707996938995747",
                                        "children": [
                                            {
                                                "Shape": {
                                                    "appearance": {
                                                        "PBRAppearance": {
                                                            "baseColor": "0.8 0.8 0.8",
                                                            "roughness": 1,
                                                            "metalness": 0
                                                        }
                                                    },
                                                    "geometry": {
                                                        "Capsule": {
                                                            "height": "0.045",
                                                            "radius": "0.005"
                                                        }
                                                    }
                                                }
                                            }
                                        ]
                                    }
                                }
                            ],
                            "boundingObject": {
                                "Group": {
                                    "children": [
                                        {
                                            "USE JOINT": {}
                                        },
                                        {
                                            "USE BONE2": {}
                                        }
                                    ]
                                }
                            },
                            "physics": {
                                "Physics": {
                                    "density": "-1",
                                    "mass": "0.6"
                                }
                            }
                        }
                    }
                }
            
    },
        "name": "hinge",
        "boundingObject": {
            "Group": {
                "children": [
                    {
                        "USE BOX": {}
                    },
                    {
                        "USE JOINT": {}
                    },
                    {
                        "USE BONE1": {}
                    }
                ]
            }
        },
        "physics": {
            "Physics": {
                "density": "-1",
                "mass": "20",
                "centerOfMass": [
                    "-0.03 0 -0.015"
                ]
            }
        },
        "controller": "muscle"
    }
}

# Example usage
appearance = create_appearance("0.8 0.8 0.8")
shape = create_shape("Box", {"size": "0.05 0.08 0.06"}, appearance)
physics = create_physics(-1, 20, ["-0.03 0 -0.015"])

# Integrating into a VRML node
vrml_robot = {
    "DEF HINGE Robot": {
        "children": {
            "DEF BOX Pose": {
                "children": {
                    "Shape1": shape
                }
            }
        },
        "physics": physics
    }
}





if __name__ == "__main__":
    # Call the function and print the result
    #print(vrml_robot)
    vrml_code = serialize_vrml(vrml_robot)
    print(vrml_code)
    with open("generator.proto", "w") as file:
        file.write(vrml_code)

