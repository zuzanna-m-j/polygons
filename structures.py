import numpy as np
import matplotlib.pyplot as plt

def onSegment(p, q, r):
    if ((q[0] <= max(p[0], r[0])) and (q[0] >= min(p[0], r[0])) and
            (q[1] <= max(p[1], r[1])) and (q[1] >= min(p[1], r[1]))):
        return True
    return False
def orientation(p, q, r):
    # to find the orientation of an ordered triplet (p,q,r)
    # function returns the following values:
    # 0 : Colinear points
    # 1 : Clockwise points
    # 2 : Counterclockwise

    val = (float(q[1] - p[1]) * (r[0] - q[0])) - (float(q[0] - p[0]) * (r[1] - q[1]))
    if (val > 0):

        # Clockwise orientation
        return 1
    elif (val < 0):

        # Counterclockwise orientation
        return 2
    else:

        # Colinear orientation
        return 0
# The main function that returns true if
# the line segment 'p1q1' and 'p2q2' intersect.
def Intersection(p1, q1, p2, q2):
    # Find the 4 orientations required for
    # the general and special cases
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    # General case
    if ((o1 != o2) and (o3 != o4)):
        return True

    # Special Cases

    # p1 , q1 and p2 are colinear and p2 lies on segment p1q1
    if ((o1 == 0) and onSegment(p1, p2, q1)):
        return True

    # p1 , q1 and q2 are colinear and q2 lies on segment p1q1
    if ((o2 == 0) and onSegment(p1, q2, q1)):
        return True

    # p2 , q2 and p1 are colinear and p1 lies on segment p2q2
    if ((o3 == 0) and onSegment(p2, p1, q2)):
        return True

    # p2 , q2 and q1 are colinear and q1 lies on segment p2q2
    if ((o4 == 0) and onSegment(p2, q1, q2)):
        return True

    # If none of the cases
    return False
def OverlapFound(obj1,obj2):

    #FLAG = False -- no overlap found
    FLAG = False
    for m in obj1.endpoints:
        if FLAG == True:
            break
        else:
            for n in obj2.endpoints:
                FLAG = Intersection(m[0],m[1],n[0],n[1])
                if FLAG == True:
                    break
    return FLAG


class Settings():

    def __init__(self,dt = 1,steps = 1,num_species = 1,D = 0.5,seed = 12345):

        self.num_species = num_species
        self.dt = dt
        self.steps = steps
        self.seed = seed

        if type(D) == float:
            self.D = num_species * [D]
        else:
            self.D = D
    pass

class Box():

    def __init__(self,m,n,bc):

        self.m = m
        self.n = n
        self.bc = bc

class Shapes():

    id_list = []

    def VLen(self,v1,v2):
        return np.sqrt((v2[0] - v1[0])**2 + (v2[1] - v1[1])**2)

    def Vector(self,v1,v2):
        return (v2[0] - v1[0],v2[1] - v1[1])

    def OverlapCheck(self,o1,o2):

        """Checks if there is an overlap between the two shapes.
        Checks if any two edges intersect.
        """
        s1 = o1.vectors
        s2 = o2.vectors

    def AddToList(self):
        Shapes.id_list.append(self)
    def GlobalId(self):
        return len(Shapes.id_list)

class Triangle(Shapes):

    count = 0
    total_area = 0
    v_num = 3

    def Update_Count(self):
        Triangle.count += 1

    def Update_Area(self):
        Triangle.total_area += self.area

    def Sides(self):

        a = self.VLen(self.v1,self.v2)
        b = self.VLen(self.v2, self.v3)
        c = self.VLen(self.v3, self.v1)
        return a,b,c

    def Area(self):
        """
        Uses Heron's formula to calculate the area of the triangle given its vertex set
        ---
        Arguments:
            - none
        Returns:
            - area (scalar): area of the triangle
        """


        s1,s2,s3 = self.a,self.b,self.c
        s = 0.5 * (s1 + s2 +s3)
        return np.sqrt(s * (s - s1) * (s - s2) * (s - s3))

    def EndPoints(self):

        v1 = self.temp_v1
        v2 = self.temp_v2
        v3 = self.temp_v3

        a = (v1,v2)
        b = (v2,v3)
        c = (v3,v1)

        return a,b,c


    def Circumcircle(self):
        """
        https://mathworld.wolfram.com/Circumcircle.html
        """

        v1 = self.v1
        v2 = self.v2
        v3 = self.v3

        a = np.linalg.det(np.array([[v1[0],v1[1],1],
                                    [v2[0],v2[1],1],
                                    [v3[0],v3[1],1]]))

        bx = np.linalg.det(-1.0 * np.array([[v1[0]**2 + v1[1]**2, v1[1], 1],
                    [v2[0]**2 + v2[1]**2, v2[1], 1],
                    [v3[0]**2 + v3[1]**2, v3[1], 1]]))

        by = np.linalg.det(np.array([[v1[0]**2 + v1[1]**2, v1[0], 1],
                    [v2[0]**2 + v2[1]**2, v2[0], 1],
                    [v3[0]**2 + v3[1]**2, v3[0], 1]]))

        c = np.linalg.det(-1.0 * np.array([[v1[0]**2 + v1[1]**2,v1[0], v1[1]],
                    [v2[0]**2 + v2[1]**2, v2[0], v2[1]],
                    [v3[0]**2 + v3[1]**2, v3[0], v3[1]]]))

        x = -1.0 * (bx/(2*a))

        y = -1.0 * (by/(2*a))

        r = np.sqrt(bx**2 + by**2 - 4*a*c)/(2*abs(a))

        return x,y,r
    def MakeMove(self,config):

        D = config.D[self.species]
        #neighbours = self.neighbours

        rng = np.random.default_rng(config.seed)
        x,y = (rng.random(2) * 2 - 1)*D

        self.temp_v1 = self.temp_v1[0] + x, self.temp_v1[1] + y
        self.temp_v2 = self.temp_v2[0] + x, self.temp_v2[1] + y
        self.temp_v3 = self.temp_v3[0] + x, self.temp_v3[1] + y

        self.endpoints = self.EndPoints()

        reject = OverlapFound(self,Shapes.id_list[1])
        if reject  == True:

            #reverse the temporary coordinates
            self.temp_v1 = self.v1
            self.temp_v2 = self.v2
            self.temp_v3 = self.v3

        else:

            #update coordinates
            #shift the circle center
            #build neighbour list

            self.v1 = self.temp_v1
            self.v2 = self.temp_v2
            self.v3 = self.temp_v3

            self.x, self.y, self.r  = self.Circumcircle()
            self.vertices = self.v1,self.v2,self.v3

    def __init__(self,vertices,species):

        self.species = species
        self.vertices = vertices
        self.v1 = vertices[0]
        self.v2 = vertices[1]
        self.v3 = vertices[2]

        self.temp_v1 = vertices[0]
        self.temp_v2 = vertices[1]
        self.temp_v3 = vertices[2]

        self.a, self.b, self.c = self.Sides()
        self.x, self.y, self.r = self.Circumcircle()
        self.endpoints = self.EndPoints()

        #Increase total counters
        self.global_id = self.GlobalId()
        self.AddToList()
        self.area = self.Area()
        self.Update_Area()