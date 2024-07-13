import math

from worm_generator import serialize_vrml



        
if __name__ == "__main__":
    # Call the function and print the result
    #print(vrml_robot)
    vrml_code = serialize_vrml(create_worm_ring("1 1 0.5"))
    #print(vrml_code)
    #print(vrml_code)
    #print(coordinates)
    with open("generator2.proto", "w") as file:
        file.write(vrml_code)