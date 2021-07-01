import numpy as np
import matplotlib.pyplot as plt


class Settings():

    def __init__(self,dt,steps,num_species,D):


        self.num_species = num_species
        self.dt = dt
        self.steps = steps

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

class Methods():

    def OverlapCheck(self,o1,o2):

        """Checks if there is an overlap between the two shapes.
        Checks if any two edges intersect.
        """
        s1 = o1.vectors
        s2 = o2.vectors

class Shapes():

    def VLen(self,v1,v2):
        return np.sqrt((v2[0] - v1[0])**2 + (v2[1] - v1[1])**2)

    def Vector(self,v1,v2):
        return (v2[0] - v1[0],v2[1] - v1[1])

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

    def Vectors(self):

        v1 = self.v1
        v2 = self.v2
        v3 = self.v3

        a = self.Vector(v1,v2)
        b = self.Vector(v2,v3)
        c = self.Vector(v3,v1)

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

    def __init__(self,vertices):

        self.vertices = vertices
        self.v1 = vertices[0]
        self.v2 = vertices[1]
        self.v3 = vertices[2]

        self.a, self.b, self.c = self.Sides()
        self.x, self.y, self.r = self.Circumcircle()
        self.vectors = self.Vectors()

        #Increase total counters
        self.area = self.Area()
        self.Update_Area()

t1 = Triangle([(0,0),(2,0),(0,3)])

plt.plot(0,0,'o')
plt.plot(2,0,'o')
plt.plot(0,3,'o')
plt.plot(t1.x,t1.y,'o',label = "center")
plt.legend()
plt.show()
print(t1.r)
r0 = np.sqrt(3**2 + 2**2)/2
print(r0)
