#!/usr/bin/env python3

# base.py
# Description:

# Imports
import numpy as np
import matplotlib.pyplot as plt

# Classes:
# - Structure

# - Shape --:
#           |- Triangle
#           |- Qadrilateral

# Structure - stores configuration of the running script

class Structure():

    def AREA(self,type):
        vnum = self.shapes(type)

        if vnum == 3:
            return self.TRIANGLE_AREA(type)

        elif vnum == 4:
            return self.QUADR_AREA(type)

    def __init__(self,file_name):

        with open(file_name,"r") as file:
            lines = file.readlines()

            for line in lines:
                input = line.split()

                if input[0] == "#":
                    pass

                elif input[0] == 'x':
                    self.x = float(input[1])

                elif input[0] == 'y':
                    self.y = float(input[1])

                elif input[0] == 'types':
                    self.types = int(input[1])

                elif input[0] == 'shapes':
                    self.shapes = []
                    for i in range(self.types):
                        self.shapes.append(int(input[i+1]))

                elif input[0] == 'vertices':
                    self.vertices = []
                    shape_vertices = []
                    offset = 1

                    for t in range(self.types):

                        for i in range(offset, self.shapes[t]*2 + offset):
                            if list(input[i])[-1] == ',':
                                 nums = list((input[i]))[:-1]
                                 inp = nums[0]
                                 for num in nums[1:]:
                                     inp += num
                                 shape_vertices.append(float(inp))
                            else:
                                shape_vertices.append(float(input[i]))
                        offset += self.shapes[t]*2
                        self.vertices.append(shape_vertices)



        #number of polygon of each type
        self.type_numbers = np.zeros(self.types)

        #area of each polygon
        self.type_areas = np.zeros(self.types)
        for i in range(len(self.type_areas)):
            self.type_areas[i] = self.AREA()

        #packing fraction
        self.packing_fraction = 0


class Shape():
    """General class defining shared shape methods.

    Methods:
        - CREATE - initializes the shape
        - INTERSECTION - checks if the two shapes intersect
        - ENDPOINTS
        - ADD_NUMBER - increases the count for the given shape
        - INCREASE_AREA - adds to the occupied area

    Variables:
        - circle_center - center of the circumcirle
        - area - stores the area of the polygon
        - vertices - stores positions of the vertices of the polygon
    """
    # Methods
    # Update the simulation environment

    self.

box = Structure("input.txt")