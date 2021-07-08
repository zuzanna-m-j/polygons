#!/usr/bin/env python3

import copy
import numpy as np
import random

class Structure():

    def CONDITION(self):
        self.PACKING_FRACTION()
        print(f'Packing fraction is: {self.packing_fraction}')
        print(f'Move: {self.iter_counter}')
        if self.stop == 0:
            condition = self.packing_fraction < self.max_packing_fraction
        elif self.stop == 1:
            condition = self.iter_counter < self.max_iter
        return condition

    def PACKING_FRACTION(self):
        self.packing_fraction = self.total_area/self.box_area

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

        grid = np.zeros((self.x_dim, self.y_dim), dtype=object)

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

                elif input[0] == 'masses':
                    self.M = list(map(float,input[1:]))

                elif input[0] == 'moves':
                    self.moves = list(map(float,input[1:]))

                elif input[0] == "prob":
                    self.p = list(map(float,input[1:]))

                elif input[0] == 'stop':
                    if input[1] == 'pack_frac':
                        self.stop = 0
                        self.max_packing_fraction = float(input[2])

                    elif input[1] == 'max_iter':
                        self.stop = 1
                        self.max_iter = float(input[2])
                        condition = self.iter_counter >= self.max_iter

                elif input[0] == "initial_num":
                    self.initial_num = int(input[1])

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

        self.vertices = np.array(self.vertices)
        self.type_numbers = np.zeros(self.types)
        self.vertex_positions = []
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
        self.spacing = max(self.R)
        self.box_area = (self.x_dim * self.spacing) * (self.y_dim * self.spacing)

        #simulation
        self.move_pattern = []
        self.move_acceptance = []
        self.iter_counter = 0


class Shape():

    # ============================
    # INITIALIZATION METHODS
    def WRAP(self):
        for i in range(len(self.vertices) // 2):
            if self.temp_vertices[2 * i] > self.box.x_dim * self.box.spacing or self.temp_vertices[2 * i] < 0:
                self.temp_vertices[2 * i] = copy.deepcopy(self.temp_vertices[2 * i] % (self.box.x_dim * self.box.spacing))

            if self.temp_vertices[2 * i + 1] > self.box.y_dim * self.box.spacing or self.temp_vertices[2 * i + 1] < 0:
                self.temp_vertices[2 * i + 1] = copy.deepcopy(self.temp_vertices[2 * i + 1] % (self.box.y_dim * self.box.spacing))

    def CREATE(self):

        # random offset from the origin
        rnd1 = np.random.rand() * self.box.spacing * self.box.x_dim
        rnd2 = np.random.rand() * self.box.spacing * self.box.y_dim
        self.vertices = copy.deepcopy(self.box.vertices[self.type])
        self.temp_vertices = copy.deepcopy(self.vertices)


        for i in range(len(self.vertices) // 2):
            self.temp_vertices[2 * i] = copy.deepcopy(self.temp_vertices[2 * i] + rnd1)
            self.temp_vertices[2 * i + 1] = copy.deepcopy(self.temp_vertices[2 * i + 1] + rnd2)
        self.WRAP()

        self.edges = self.GET_EDGES()
        self.temp_edges = copy.deepcopy(self.edges)

        self.x, self.y, self.r = self.CIRCLE()
        self.temp_x, self.temp_y = self.x, self.y
        self.grid_position = self.GET_GRID_POSITION()
        self.temp_grid_position = copy.deepcopy(self.grid_position)
        self.neighbours = self.GET_NEIGHBOURS()

        while (not self.ACCEPT_MOVE()):
            rnd1 = np.random.rand() * self.box.spacing * self.box.x_dim
            rnd2 = np.random.rand() * self.box.spacing * self.box.y_dim

            for i in range(len(self.vertices) // 2):
                self.temp_vertices[2 * i] = copy.deepcopy(self.temp_vertices[2 * i] + rnd1)
                self.temp_vertices[2 * i + 1] = copy.deepcopy(self.temp_vertices[2 * i + 1] + rnd2)
            self.WRAP()

        self.vertices = copy.deepcopy(self.temp_vertices)
        self.x, self.y, self.r = self.CIRCLE()
        self.temp_x, self.temp_y = self.x, self.y
        self.grid_position = self.GET_GRID_POSITION()
        self.temp_grid_position = copy.deepcopy(self.grid_position)
        self.neighbours = self.GET_NEIGHBOURS()

    def APPEND_GLOBAL_ID_LIST(self):
            self.box.global_id_list.append(self)

    def ADD_TO_GRID(self):
            i, j, q = self.GET_GRID_POSITION()
            self.box.grid[i, j].append(self.global_id)

    def ADD_VERTEX_POSITIONS(self):
            self.box.vertex_positions.append(self.vertices)

    def GET_EDGES(self):

            shape = self.shape
            if shape == 3:

                AB = self.temp_vertices[np.array([0, 1, 2, 3])]
                BC = self.temp_vertices[np.array([2, 3, 4, 5])]
                CA = self.temp_vertices[np.array([4, 5, 0, 1])]

                return (AB, BC, CA)
            elif shape == 4:

                AB = self.temp_vertices[0, 1, 2, 3]
                BC = self.temp_vertices[2, 3, 4, 5]
                CD = self.temp_vertices[4, 5, 6, 7]
                DA = self.temp_vertices[6, 7, 0, 1]

                return AB, BC, CD, DA

    # ========================================================
    # UPDATING METHODS
    def ADD_MOVE(self,move,acc):
        self.box.move_pattern.append(move)
        self.box.move_acceptance.append(acc)

    def ADD_NUMBER(self):
        self.box.type_numbers[self.type] += 1

    def ADD_AREA(self):
        self.box.total_area += self.box.type_areas[self.type]

    def UPDATE_GRID(self):

        i, j, q = self.grid_position
        m, n, _ = self.temp_grid_position
        self.box.grid[i, j].pop(q)
        self.box.grid[m, n].append(self.global_id)

    # ========================
    # MOVE METHODS
    def GET_GRID_POSITION(self):

        x = self.temp_x
        y = self.temp_y

        i = int((x // (self.box.spacing)) % self.box.x_dim)
        j = int((y // (self.box.spacing)) % self.box.y_dim)
        q = len(self.box.grid[i, j])
        return i, j, q

    def GET_NEIGHBOURS(self):

        neigh_id_list = []

        x_dim = self.box.x_dim
        y_dim = self.box.y_dim
        i, j, _ = self.temp_grid_position
        neigh_positions = [

            ((i+1)%x_dim,(j - 1) % y_dim),((i+1)%x_dim,j),((i+1)%x_dim,(j + 1) % y_dim),
            (i,(j - 1) % y_dim), (i,(j + 1) % y_dim),
            ((i-1)%x_dim,(j - 1) % y_dim),((i-1)%x_dim,j),((i-1)%x_dim,(j + 1) % y_dim)
        ]

        for pos in neigh_positions:
            a = pos[0]
            b = pos[1]
            for global_id in self.box.grid[a,b]:
                neigh_id_list.append(global_id)

        return neigh_id_list

    def ROTATE(self, x, y,angle):

        ox = self.temp_x
        oy = self.temp_y
        theta = np.radians(angle)
        M = np.array([[np.cos(theta), -1 * np.sin(theta)],[np.sin(theta), np.cos(theta)]])
        v = np.array([x - ox,y - oy])
        nv= np.dot(M,v)
        nv[0] += ox
        nv[1] += oy

        return nv[0],nv[1]

    def CIRCLE(self):

        # https://mathworld.wolfram.com/Circumcircle.html

        if self.shape == 3:

            v1 = self.temp_vertices[:2]
            v2 = self.temp_vertices[2:4]
            v3 = self.temp_vertices[4:6]

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

    def ATTEMPT_MOVE(self):
        self.box.iter_counter += 1
        moves = self.box.moves
        p = self.box.p
        move_type = random.choices(moves, weights = p)[0]
        # =================================================================================
        # DISPLACE
        if move_type == 0:
            r = self.r
            d = 1/self.box.M[self.type]
            rnd1 = d * r * np.random.rand()
            rnd2 = d * r * np.random.rand()

            for i in range(len(self.vertices)//2):
                self.temp_vertices[2*i] = copy.deepcopy(self.temp_vertices[2*i] + rnd1)
                self.temp_vertices[2*i+1] = copy.deepcopy(self.temp_vertices[2*i + 1] + rnd2)
            self.WRAP()

            if (self.ACCEPT_MOVE() == True):

                self.UPDATE_GRID()
                self.vertices = copy.deepcopy(self.temp_vertices)
                self.x, self.y = self.temp_x, self.temp_y
                self.grid_position = copy.deepcopy(self.temp_grid_position)
                self.edges = copy.deepcopy(self.temp_edges)
                self.box.vertex_positions[self.global_id] = copy.deepcopy(self.vertices)
                self.ADD_MOVE(move_type,1)

            else:

                self.temp_vertices = copy.deepcopy(self.vertices)
                self.temp_x, self.temp_y = self.x, self.y
                self.temp_grid_position = copy.deepcopy(self.grid_position)
                self.temp_edges = copy.deepcopy(self.edges)
                self.ADD_MOVE(move_type,0)
        # ==================================================================================
        # SWAP
        if move_type == 1:

            rand = random.randint(0, len(self.box.global_id_list) - 1)
            p2 = self.box.global_id_list[rand]
            ox,oy = p2.x - self.x, p2.y - self.y

            self.temp_vertices = copy.deepcopy(self.vertices)
            for i in range(len(self.vertices)//2):
                self.temp_vertices[2*i] = copy.deepcopy(self.temp_vertices[2*i] + ox)
                self.temp_vertices[2*i+1] = copy.deepcopy(self.temp_vertices[2*i + 1] + oy)
            self.WRAP()

            p2.temp_vertices = copy.deepcopy(p2.vertices)
            for i in range(len(p2.vertices)//2):
                p2.temp_vertices[2*i] = copy.deepcopy(p2.temp_vertices[2*i] - ox)
                p2.temp_vertices[2*i+1] = copy.deepcopy(p2.temp_vertices[2*i + 1] - oy)
            p2.WRAP()

            p2.temp_x, p2.temp_y, _ = p2.CIRCLE()
            self.temp_x, self.temp_y, _ = self.CIRCLE()

            r = self.r
            d = 1/self.box.M[self.type]
            rnd1 = d * r * np.random.rand()
            rnd2 = d * r * np.random.rand()

            for i in range(len(self.vertices)//2):
                self.temp_vertices[2*i] = copy.deepcopy(self.temp_vertices[2*i] + rnd1)
                self.temp_vertices[2*i+1] = copy.deepcopy(self.temp_vertices[2*i + 1] + rnd2)
            self.WRAP()

            # move p2
            r = p2.r
            d = 1/p2.box.M[p2.type]
            rnd1 = d * r * np.random.rand()
            rnd2 = d * r * np.random.rand()

            for i in range(len(p2.vertices)//2):
                p2.temp_vertices[2*i] = copy.deepcopy(p2.temp_vertices[2*i] - rnd1)
                p2.temp_vertices[2*i+1] = copy.deepcopy(p2.temp_vertices[2*i + 1] - rnd2)
            p2.WRAP()

            self.temp_x, self.temp_y, _ = self.CIRCLE()
            p2.temp_x, p2.temp_y, _ = p2.CIRCLE()

            # rotate self
            angle = np.random.randint(360)
            for i in range(int(len(self.temp_vertices)//2)):
                x = self.temp_vertices[2*i]
                y = self.temp_vertices[2*i+1]
                self.temp_vertices[2*i], self.temp_vertices[2*i+1] = copy.deepcopy(self.ROTATE(x,y,angle))
            self.WRAP()
            self.temp_x, self.temp_y, _ = self.CIRCLE()
            self.temp_grid_position = self.GET_GRID_POSITION()
            self.neighbours = self.GET_NEIGHBOURS()
            self.temp_edges = self.GET_EDGES()

            # rotate p2
            angle = np.random.randint(360)
            for i in range(int(len(p2.temp_vertices)//2)):
                x = p2.temp_vertices[2*i]
                y = p2.temp_vertices[2*i+1]
                p2.temp_vertices[2*i], p2.temp_vertices[2*i+1] = copy.deepcopy(p2.ROTATE(x,y,angle))
            p2.WRAP()
            p2.temp_x, p2.temp_y, _ = p2.CIRCLE()
            p2.temp_grid_position = p2.GET_GRID_POSITION()
            p2.neighbours = p2.GET_NEIGHBOURS()
            p2.temp_edges = p2.GET_EDGES()

            if (self.ACCEPT_MOVE() == True) and (p2.ACCEPT_MOVE() == True):

                self.UPDATE_GRID()
                self.vertices = copy.deepcopy(self.temp_vertices)
                self.x, self.y = self.temp_x, self.temp_y
                self.grid_position = copy.deepcopy(self.temp_grid_position)
                self.edges = copy.deepcopy(self.temp_edges)

                p2.UPDATE_GRID()
                p2.vertices = copy.deepcopy(p2.temp_vertices)
                p2.x, p2.y = p2.temp_x, p2.temp_y
                p2.grid_position = copy.deepcopy(p2.temp_grid_position)
                p2.edges = copy.deepcopy(p2.temp_edges)

                self.box.vertex_positions[self.global_id] = copy.deepcopy(self.vertices)
                p2.box.vertex_positions[p2.global_id] = copy.deepcopy(p2.vertices)

                self.ADD_MOVE(move_type,1)

            else:

                self.temp_vertices = copy.deepcopy(self.vertices)
                self.temp_x, self.temp_y = self.x, self.y
                self.temp_grid_position = copy.deepcopy(self.grid_position)
                self.temp_edges = copy.deepcopy(self.edges)

                p2.temp_vertices = copy.deepcopy(p2.vertices)
                p2.temp_x, p2.temp_y = p2.x, p2.y
                p2.temp_grid_position = copy.deepcopy(p2.grid_position)
                p2.temp_edges = copy.deepcopy(p2.edges)
                self.ADD_MOVE(move_type, 0)

        # =================================================
        # ADD NEW PARTICLE
        if move_type == 2:
            pick_type = random.choice(list(range(self.box.types)))
            Shape(self.box,pick_type)

            if (self.ACCEPT_MOVE() == True):

                self.UPDATE_GRID()
                self.vertices = copy.deepcopy(self.temp_vertices)
                self.x, self.y = self.temp_x, self.temp_y
                self.grid_position = copy.deepcopy(self.temp_grid_position)
                self.edges = copy.deepcopy(self.temp_edges)
                self.box.vertex_positions[self.global_id] = copy.deepcopy(self.vertices)
                self.ADD_MOVE(move_type,1)

            else:

                self.temp_vertices = copy.deepcopy(self.vertices)
                self.temp_x, self.temp_y = self.x, self.y
                self.temp_grid_position = copy.deepcopy(self.grid_position)
                self.temp_edges = copy.deepcopy(self.edges)

                self.ADD_MOVE(move_type,0)

    def ACCEPT_MOVE(self):

        for n_id in self.neighbours:
            n = self.box.global_id_list[n_id]
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
        self.APPEND_GLOBAL_ID_LIST()

        self.type = type
        self.shape = box.shapes[type]

        self.CREATE()
        self.box.total_area += self.box.type_areas[self.type]

        self.ADD_TO_GRID()
        self.ADD_VERTEX_POSITIONS()
