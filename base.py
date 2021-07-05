#!/usr/bin/env python3

# base.py
# Description:

# Imports
import numpy as np
import matplotlib.pyplot as plt

# Classes:
# - Structure
# - Shapes

# Structure - stores configuration of the running script

class Structure():

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

        print(self.vertices)
        print(self.types)

box = Structure("input.txt")