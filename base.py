#!/usr/bin/env python3

# base.py
# Description:

# Imports
import copy
import numpy as np
import matplotlib.pyplot as plt

# Classes:
# - Structure

# - Shape --:
#           |- Triangle
#           |- Qadrilateral

# Structure - stores configuration of the running script



class Structure():

    """
    Attributes:
        - x: x dimension
        - y: y dimension
        - types: number of types
        - shapes: shapes corresponding to given type
        - vertices: vertices for base of each shape
        - areas: area occupied by each type

    Methods:
        -

    """

    def CAPTURED(self,a,b,c):

        #c an c be on the line a---b
        x1, y1 = a
        x2, y2 = b
        x3, y3 = c

        if x3 >= min(x1,x2) and x3 <= max(x1,x2) and y3 >= min(y1,y2) and y3 <= max(y1,y2):
            return True
        else:
            return False

    def ORIENTATION(self,a,b,c):

        x1, y1 = a
        x2, y2 = b
        x3, y3 = c

        expr = (y2 - y1)*(x3 - x2) - (y3 - y2)*(x2 - x1)
        if expr > 0:
            return 1
        if expr < 0:
            return -1
        if expr == 0:
            return 0

    def CROSS(self,p1,p2,q1,q2):

        o1 = self.ORIENTATION(p1, p2, q1)
        o2 = self.ORIENTATION(p1, p2, q2)
        o3 = self.ORIENTATION(q1, q2, p1)
        o4 = self.ORIENTATION(q1, q2, p2)

        if ((o1 != o2) and (o3 != o4)):
            return True

        if ((o1 == 0) and self.CAPTURED(p1, p2, q1)):
            return True

        if (o2 == 0) and self.CAPTURED(p1, p2, q2):
            return True

        if (o3 == 0) and self.CAPTURED(q1, q2, p1):
            return True

        if (o4 == 0) and self.CAPTURED(q1, q2, p2):
            return True
        else:
            return False






    def VLEN(self,x1,y1,x2,y2):
        return np.sqrt((x2 - x1)*(x2 - x1) + (y2 - y1)*(y2 - y1))

    def TRI_AREA(self,type):

        v_list = np.array(self.vertices[type])
        print(v_list)
        AB = self.VLEN(*v_list[:4])
        BC = self.VLEN(*v_list[2:6])
        CA = self.VLEN(*v_list[np.array([4,5,0,1])])

        # calculate the area using Heron's formula
        s = 0.5 * (AB + BC + CA)
        help(np.sqrt(s * (s - AB) * (s - BC) * (s - CA)))
        return np.sqrt(s * (s - AB) * (s - BC) * (s - CA))

    def QUAD_AREA(self,type):

        v_list = np.array(self.vertices[type])
        AB = self.VLEN(*v_list[:4])
        BC = self.VLEN(*v_list[2:6])
        CD = self.VLEN(*v_list[4:8])
        DA = self.VLEN(*v_list[np.array([6,7,0,1])])

        s = 0.5 * (AB + BC + CD + DA)
        help(np.sqrt((s - AB) * (s - BC) * (s - CD)*(s - DA)))
        return np.sqrt((s - AB) * (s - BC) * (s - CD)*(s - DA))

    def AREA(self,type):

        vnum = self.shapes[type]
        if vnum == 3:
            return self.TRI_AREA(type)
        elif vnum == 4:
            return self.QUAD_AREA(type)
        else:
            print("Nope!")



    def __init__(self,file_name):

        self.global_id_list = []

        self.input_file = file_name
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
                    offset = 1

                    for n in range(self.types):
                        shape_vertices = []
                        for i in range(offset, self.shapes[n]*2 + offset):

                            if list(input[i])[-1] == ',':
                                 nums = list((input[i]))[:-1]
                                 inp = nums[0]
                                 for num in nums[1:]:
                                     inp += num
                                 shape_vertices.append(float(inp))
                            else:
                                shape_vertices.append(float(input[i]))

                        offset += self.shapes[n]*2
                        self.vertices.append(copy.deepcopy(shape_vertices))

        #number of polygon of each type
        self.type_numbers = np.zeros(self.types)

        #area of each polygon
        self.type_areas = np.zeros(self.types)
        for i in range(len(self.type_areas)):
            self.type_areas[i] = self.AREA(i)

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
        - MOVE - attempts to move the shape

    Attributes:
        - circle_center - center of the circumcirle
        - area - stores the area of the polygon
        - vertices - stores positions of the vertices of the polygon
    """
    # Methods
    # Update the simulation environment


    def APPEND_GLOBAL_ID_LIST(self):
        self.box.global_id_list.append(self)

    def GET_NEIGHBOURS(self):
        """Returns the list of particles neighbours"""
        pass

    def GET_GRID_POSITION(self):
        pass

    def ATTEMPT_MOVE(self):

        p = self.box.p
        D = self.box.D[self.type]
        moves = self.box.moves
        move_type = random.choices(moves, weights = D, k = 1)

        # choose the kind of move to attempt

        if move_type == 0:

            # make a displacement move
            # generate random displacement vector
            # move all indices
            # update circle coordinates

        if move_type == 1:
            # make SWAP move

        # 0 - DISPLACE
        # 1 - SWAP

        if ACCEPT_MOVE() == True:

            self.vertices = copy.deepcopy(self.temp_vertices)
            self.x, self.y = self.temp_x, self.temp_y
            self.

    def EDGES(self):

        shape = self.shape

        if shape == 3:

            AB = self.vertices[0,1,2,3]
            BC = self.vertices[2,3,4,5]
            CA = self.vertices[4,5,0,1]

            return (AB,BC,CA)


        elif shape == 4:

            AB = self.vertices[0,1,2,3]
            BC = self.vertices[2,3,4,5]
            CD = self.vertices[4,5,6,7]
            DA = self.vertices[6,7,0,1]

            return (AB,BC,CD,DA)

    def ACCEPT_MOVE(self):

        # generate neighbour list
        # from the position on the grid find the proximal squares
        # from each square get the global id of shapes there
        # append the pointers to the neighbour list
        # check if crosses with any neighbour

        # iterate all neighbours

        for n in self.neighbours:

            # for each edge in the original shape
            for edge1 in self.edges:
                p1 = edge1[:2]
                p2 = edge1[2:4]

                # for each edge in the neighbour
                for edge2 in n.edges:
                    q1 = edge2[:2]
                    q2 = edge2[2:4]

                    if self.box.CROSS(p1, p2, q1, q2) == True:
                        # do not approve move
                        return False

        # approve move if no overlap found
        return True

    def __init__(self,box,type):

        self.box = box

        self.global_id = len(box.global_id_list)
        self.APPEND_GLOBAL_ID_LIST(self)

        self.type = type
        self.shape = box.shapes[type]

        self.vertices = self.CREATE(box,type)
        self.temp_vertices = copy.deepcopy(self.vertices)

        self.edges = self.EDGES(self.shape)
        self.temp_edges = copy.deepcopy(self.edges)

        self.x, self.y, self.r = self.CIRCLE()
        self.grid_position = self.GET_GRID_POSITION()
        self.temp_grid_position = copy.deepcopy(self.grid_position)




