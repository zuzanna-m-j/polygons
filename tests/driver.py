import sys
sys.path.append('/Users/zuzannajedlinska/Documents/Projects_UPenn/Polygons/polygons/modules')

from code_base import *

box = Box()
ConfigFile = Settings(D = 2.0,seed = 11442)

t1 = Triangle([(3,3),(4,3),(3.5,4)],0,box)
t2 = Triangle([(0,0),(1,0),(0.5,1)],0,box)
print(t1.gridpoint)
print(t1.neighs)
for p in t1.vertices:
    plt.plot(p[0],p[1],'bo')
for p in t2.vertices:
    plt.plot(p[0],p[1],'ro')
plt.show()
t1.MakeMove(ConfigFile)
for p in t1.vertices:
    plt.plot(p[0],p[1],'bo')
for p in t2.vertices:
    plt.plot(p[0],p[1],'ro')
plt.show()
print(OverlapFound(t1,t2))
print(t1.gridpoint)
print(t1.neighs)