import math

ChildrenNode = "children"
EmbededFlag = "is_embeded"

worm_length = 8
ring_muscle_number = 6

side_length = 0.2
angle_increment = math.pi / 3  # 60 degrees in radians for each step

# Coordinates storage
coordinates = []
rela_coordinates = []

# Starting point
coordinates.append((0.0, 0.0))

# Compute the remaining points
for i in range(1, 6):
    angle = angle_increment * i
    x = round(side_length * math.cos(angle), 7)
    y = round(side_length * math.sin(angle), 7)
    coordinates.append((x, y))

for i in range(0, 6):
    x1, y1 = coordinates[i]
    x2, y2 = coordinates[(i + 1) % 6]
    rela_coordinates.append((x2 - x1, y2 - y1))



# Compute the rotated vectors
for i in range(1, 6):
    # Initialize the original unit vector
    x, y = 1, 0

    # Initialize a list to hold the rotated vectors
    rotated_vectors = [(x, y)]

    # Angle of rotation in radians (60 degrees)
    rotation_angle = math.radians(60)

    # Apply the rotation matrix for 2D vectors
    x_rotated = x * math.cos(rotation_angle * i) - y * math.sin(rotation_angle * i)
    y_rotated = x * math.sin(rotation_angle * i) + y * math.cos(rotation_angle * i)
    # Append the rotated vector to the list
    rotated_vectors.append((round(x_rotated, 7), round(y_rotated, 7)))

# Print the rotated vectors
for vector in rotated_vectors:
    print(vector)

# Define appearance properties
def create_appearance(base_color = "0.337255 0.337255 0.337255", roughness=1, metalness=0, transparency=0.009999999776482582):
    return {
            "baseColor": base_color,
            "roughness": roughness,
            "metalness": metalness,
            "transparency": transparency
    }

# Define shape properties
def create_shape():
    return {
        
            "appearance PBRAppearance": create_appearance(),
            "geometry Sphere": {
                "radius":0.008
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

    ignore_list = [EmbededFlag]
    
    if isinstance(node, dict):
        # Process dictionary type nodes
        for key, value in node.items():
            if isinstance(value, dict):
                
                if key in square_brackets_list:
                    vrml_str += f"{space}{key} [\n"
                    vrml_str += serialize_vrml(value, indent + 2)
                    vrml_str += f"{space}  ]\n"
                else:
                    vrml_str += f"{space}{key} {{\n"
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




"""
# Example usage
appearance = create_appearance("0.8 0.8 0.8")
shape = create_shape()
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
"""







"""
def create_joint(row, column):
    return {f"DEF JOINT_{row}_{column} Shape": 
            create_shape(),
            "SliderJoint": create_slider_joint(f"JOINT_{row}_{column}", f"JOINT_{row}_{column+1}", "{row} {} 0")
         }
"""

def create_worm_ring(translation):
    return {
        "DEF WORM Robot":
        {
        "translation": translation,
        ChildrenNode: {
            f"DEF JOINT_{0}_{0} Shape": create_shape(),
            "SliderJoint": create_slider_joint(0,0),
            "SliderJoint": create_slider_joint(0,1),
            },
        "name": "\"worm\"",
        "boundingObject": "USE JOINT_0_0",
        "controller": "\"ring_muscle\"",
        }
    }


"""
def create_joint_string(row, column):
    return serialize_vrml(
        {f"DEF JOINT_{row}_{column} Shape": 
            create_shape()
         }
    )
    """

def create_joint_parameters():
    return {
        "axis": "0 1 0",
    }

"""
def create_endpoint(translation, rotation, children, boundingObject, physics):
    return {
            "translation": translation,
            "rotation": rotation,
            "children": children,
            "boundingObject": boundingObject,
            "physics": physics
    }
    """

#link joint_row_column to joint_row_column+1
def create_slider_joint(row, column):
    return {
        "jointParameters JointParameters": create_joint_parameters(),
        "device": create_linear_muscle_device(f"muscle_{row}_{column}"),
        "endPoint Solid": create_linked_slider_joint_endpoint(row, column+1)
    }


def create_linked_slider_joint_endpoint(row, column):
    global coordinates
    global ring_muscle_number
    #print(coordinates)
    x, y = coordinates[column%ring_muscle_number]
    if column == ring_muscle_number:
        return {
            "translation": f"{row} {x} {y}",
            "rotation": "1 0 0 1.0472",
            "children": {
                "USE": f"JOINT_{row}_{0}"
            },
            "boundingObject": f"USE JOINT_{row}_{0}",
            "physics Physics": {   
                "density": "1",
                "mass": "2"
            }
        }

    return {
        "translation": f"{row} {x} {y}",
        "children": {
            f"DEF JOINT_{row}_{column} Shape": create_shape(),
            "SliderJoint": create_slider_joint(row, column),
            
        },
        "boundingObject": f"USE JOINT_{row}_{column}",
        "physics Physics": {   
            "density": "1",
            "mass": "2"
        }
    }

"""
def create_linked_slider_joint_endpoint_with_children(translation, endpoint_children):

    return {
        "translation": translation,
        "children": {
            ""
        },
        "boundingObject": {
            "USE": endpoint_children
        },
        "physics Physics": {   
            "density": "1",
            "mass": "2"
        }
    }
"""


def create_linear_muscle_device(name):
    return {
        "LinearMotor": create_linear_motor(name),
        "PositionSensor": {
            "name": f"\"{name}_sensor\"",
        }
    }

def create_linear_motor(name):
    return {        
        "name": f"\"{name}\"",
        "controlPID": "0.4 0.6 0",
        "minPosition": "0",
        "maxPosition": "1",
        "maxForce": "0.3",
        "muscles": create_muscle(),
    }

def create_muscle():
    return {
        "Muscle": {
            "volume": "0.0001",
            #"startOffset": "0.01 0 0",
            #"endOffset": "0 0.05 0",
            "color": "[1 0 0 1 1 0 1 0 1]"
        }
    }


def calculate_hexagon_vertices(a, cx=0.5, cy=0.5):
    
    vertices = []
    for i in range(6):
        angle_rad = math.radians(60 * i)  
        x = cx + a * math.cos(angle_rad)
        y = cy + a * math.sin(angle_rad)
        vertices.append((x, y))
    return vertices


a = 1
vertices = calculate_hexagon_vertices(a)
for vertex in vertices:
    print(vertex)

def construct_worm():
    worm_length = 8
    worm_ring_muscle_number = 6
    worm_joints = [[0 for _ in range(worm_ring_muscle_number)] for _ in range(worm_length)]

    for i in range(worm_length):
        for j in range(worm_ring_muscle_number):
            worm_joints[i][j] = create_joint(i,j)

    robot = {
        "DEF WORM Robot": {
            "translation": "0 0 1",
            "children": {
                 worm_joints[0][0]:""
            },
            "name": "\"worm\"",
            "controller": "\"muscle\""
        }
    }

    return robot


def construct_worm_ring():
    worm_ring_muscle_number = 4

    points = calculate_hexagon_vertices(1)
   
    worm_joints = [0 for _ in range(worm_ring_muscle_number)]
    for j in range(worm_ring_muscle_number):
        worm_joints[j] = create_joint(0,j)

    robot = {
        "DEF WORM Robot": {
            "translation": "0 0 1",
            "children": {
                 worm_joints[0][0]:""
                 
            },
            "name": "\"worm\"",
            "controller": "\"muscle\""
        }
    }


    return robot




     


        
if __name__ == "__main__":
    # Call the function and print the result
    #print(vrml_robot)
    vrml_code = serialize_vrml(create_worm_ring("1 1 0.5"))
    #print(vrml_code)
    #print(vrml_code)
    #print(coordinates)
    with open("generator.proto", "w") as file:
        file.write(vrml_code)