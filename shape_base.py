import numpy as np
from copy import deepcopy
import random

class SHAPE():

    def __init__(self,box,type):

        # initialize frm the box

        self.box = box
        self.type = type
        self.shape = self.box.shape_list[self.type]
        self.area = self.box.area_list[self.type]

        # set position
        temp_vertices = []
        rx = np.random.rand() * self.box.x_dim * self.box_spacing
        ry = np.random.rand() * self.box.y_dim * self.box_spacing
        base = self.box.base_list[self.type] # --> [()()()]

        for i in range(self.shape):
            x = base[i][0]
            y = base[i][1]
            temp_vertices.append((x,y))
        self.temp_vertices = np.array(temp_vertices)
        self.WRAP()
        self.temp_circle = self.GET_CIRCLE()
        self.temp_edges = self.GET_EDGES()
        self.temp_neighbours = self.GET_NEIGHBOURS()

        while self.ACCEPT_POSITION() == False:



        # update global information





