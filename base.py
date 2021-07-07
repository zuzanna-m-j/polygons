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

    def PACKING_FRACTION(self):
        return (self.type_areas * self.type_numbers)/self.box_area

    def CIRCLE(self,shape,type):

        # https://mathworld.wolfram.com/Circumcircle.html

        if shape == 3:
            v1 = self.vertices[type][0:2]
            v2 = self.vertices[type][2:4]
            v3 = self.vertices[type][4:6]

            a = np.linalg.det(np.array([[v1[0], v1[1], 1],
                                        [v2[0], v2[1], 1],
                                        [v3[0], v3[1], 1]]))

            bx = np.linalg.det(-1.0 * np.array([[v1[0] ** 2 + v1[1] ** 2, v1[1], 1],
                                                [v2[0] ** 2 + v2[1] ** 2, v2[1], 1],
                                                [v3[0] ** 2 + v3[1] ** 2, v3[1], 1]]))

            by = np.linalg.det(np.array([[v1[0] ** 2 + v1[1] ** 2, v1[0], 1],
                                         [v2[0] ** 2 + v2[1] ** 2, v2[0], 1],
                                         [v3[0] ** 2 + v3[1] ** 2, v3[0], 1]]))

            c = np.linalg.det(-1.0 * np.array([[v1[0] ** 2 + v1[1] ** 2, v1[0], v1[1]],
                                               [v2[0] ** 2 + v2[1] ** 2, v2[0], v2[1]],
                                               [v3[0] ** 2 + v3[1] ** 2, v3[0], v3[1]]]))

            x = -1.0 * (bx / (2 * a))
            y = -1.0 * (by / (2 * a))
            r = np.sqrt(bx ** 2 + by ** 2 - 4 * a * c) / (2 * abs(a))

            return r

    def MAKE_GRID(self):

        grid = np.zeros((x_dim, y_dim), dtype=object)

        x_dim = self.x_dim
        y_dim = self.y_dim

        for i in range(x_dim):
            for j in range(y_dim):
                grid[i,j] = []
        return grid



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

        return np.sqrt(s * (s - AB) * (s - BC) * (s - CA))

    def QUAD_AREA(self,type):

        v_list = np.array(self.vertices[type])
        AB = self.VLEN(*v_list[:4])
        BC = self.VLEN(*v_list[2:6])
        CD = self.VLEN(*v_list[4:8])
        DA = self.VLEN(*v_list[np.array([6,7,0,1])])

        s = 0.5 * (AB + BC + CD + DA)
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

        self.input_file = file_name
        with open(file_name,"r") as file:
            lines = file.readlines()

            for line in lines:
                input = line.split()

                if input[0] == "#":
                    pass

                elif input[0] == 'x':
                    self.x_dim = int(input[1])

                elif input[0] == 'y':
                    self.y_dim = int(input[1])

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

        self.global_id_list = []
        self.R = []
        self.total_area = 0
        self.packing_fraction = 0

        #area of each polygon
        self.type_areas = np.zeros(self.types)
        for i in range(len(self.type_areas)):
            self.type_areas[i] = self.AREA(i)
            r = self.CIRCLE(self.shapes[i],i)
            self.R.append(r)

        #packing fraction
        self.grid = self.MAKE_GRID()
        self.spacing = 2 * max(self.R)
        self.box_area = (self.x_dim * self.spacing) * (self.y_dim * self.spacing)


class Shape():

    """General class defining shared shape methods.

    Methods:
        - CREATE - initializes the shape
        - INTERSECTION - checks if the two shapes intersect
        - ENDPOINTS
        - ADD_NUMBER - increases the count for the given shape
        - ADD_AREA - adds total area
        - MOVE - attempts to move the shape
    """

    # updater functions
    def ADD_NUMBER(self):
        self.box.type_numbers[self.type] += 1
    def ADD_AREA(self):
        self.box.total_area += self.box.type_areas[self.type]


    def ROTATE(self, x, y):

        ox = self.temp_x
        oy = self.temp_y
        rnd = np.random()
        theta = np.radians(rnd*360)
        M = np.array([[np.cos(theta), -1 * np.sin(theta)],[np.sin(theta), np.cos(theta)]])
        v = np.array([x - ox,y - oy])
        nv= np.dot(M,v)
        nv[0] += ox
        nv[1] += oy

        return nv[0],nv[1]

    def CIRCLE(self):

        # https://mathworld.wolfram.com/Circumcircle.html

        if self.shape == 3:

            v1 = self.vertices[0]
            v2 = self.vertices[1]
            v3 = self.vertices[2]

            a = np.linalg.det(np.array([[v1[0], v1[1], 1],
                                        [v2[0], v2[1], 1],
                                        [v3[0], v3[1], 1]]))

            bx = np.linalg.det(-1.0 * np.array([[v1[0] ** 2 + v1[1] ** 2, v1[1], 1],
                                                [v2[0] ** 2 + v2[1] ** 2, v2[1], 1],
                                                [v3[0] ** 2 + v3[1] ** 2, v3[1], 1]]))

            by = np.linalg.det(np.array([[v1[0] ** 2 + v1[1] ** 2, v1[0], 1],
                                         [v2[0] ** 2 + v2[1] ** 2, v2[0], 1],
                                         [v3[0] ** 2 + v3[1] ** 2, v3[0], 1]]))

            c = np.linalg.det(-1.0 * np.array([[v1[0] ** 2 + v1[1] ** 2, v1[0], v1[1]],
                                               [v2[0] ** 2 + v2[1] ** 2, v2[0], v2[1]],
                                               [v3[0] ** 2 + v3[1] ** 2, v3[0], v3[1]]]))

            x = -1.0 * (bx / (2 * a))
            y = -1.0 * (by / (2 * a))
            r = np.sqrt(bx ** 2 + by ** 2 - 4 * a * c) / (2 * abs(a))

            return x,y,r

    def UPDATE_GRID(self):

        i,j,q = self.grid_position
        m,n,_ = self.temp_grid_position
        self.box.grid[i,j].pop(q)
        self.box.grid[m,n].append(self.global_id)

    def GET_GRID_POSITION(self,x,y):

        i = (x//(self.grid.spacing))%self.grid.x_dim
        j = (y//(self.grid.spacing))%self.grid.y_dim
        q = len(self.grid[i,j])
        return i, j, q

    def APPEND_GLOBAL_ID_LIST(self):
        self.box.global_id_list.append(self)

    def GET_NEIGHBOURS(self):
        """Returns the list of particles neighbours"""
        pass

    def ATTEMPT_MOVE(self):

        p = self.box.p
        d = self.box.D[self.type]
        moves = self.box.moves
        move_type = random.choices(moves, weights = p, k = 1)

        # choose the kind of move to attempt

        if move_type == 0:

            r = self.r
            rnd1 = d * r * np.random()
            rnd2 = d * r * np.random()

            self.temp_vertices = copy.deepcopy(self.vertices)

            for i in range(len(self.vertices)-1):
                self.temp_vertices[i] += rnd1
                self.temp_vertices[i+1] += rnd2

            self.temp_x, self.temp_y, _ = self.CIRCLE()
            self.temp_grid_position = self.GET_GRID_POSITION(self.temp_x,self.temp_y)
            self.neighbours = self.GET_NEIGHBOURS()
            self.temp_edges = self.GET_EDGES()

            # make a displacement move
            # generate random displacement vector
            # move all indices
            # update circle coordinates



        if move_type == 1:
            # make SWAP move
            pass

        # 0 - DISPLACE
        # 1 - SWAP

        if move_type == 2:
            # rotate each vertex about the center of the circle
            for i in range(int(len(self.temp_vertices)/2)):
                x = self.temp_vertices[i]
                y = self.temp_vertices[i+1]
                self.temp_vertices[i], self.temp_vertices[i+1] = copy.deepcopy(self.ROTATE(x,y))



        if self.ACCEPT_MOVE() == True:

            self.vertices = copy.deepcopy(self.temp_vertices)
            self.x, self.y = copy.deepcopy(self.temp_x, self.temp_y)
            self.UPDATE_GRID() # i, j, q
            self.grid_position = copy.deepcopy(self.temp_grid_position)
            self.edges = copy.deepcopy(self.temp_edges)


    def GET_EDGES(self):

        shape = self.shape
        if shape == 3:

            AB = self.temp_vertices[0,1,2,3]
            BC = self.temp_vertices[2,3,4,5]
            CA = self.temp_vertices[4,5,0,1]

            return (AB,BC,CA)
        elif shape == 4:

            AB = self.temp_vertices[0,1,2,3]
            BC = self.temp_vertices[2,3,4,5]
            CD = self.temp_vertices[4,5,6,7]
            DA = self.temp_vertices[6,7,0,1]

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
            for edge1 in self.temp_edges:
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




