from structures import *

ConfigFile = Settings(D = 5.0,seed = 11112)

t1 = Triangle([(-1,0),(2,0),(0,3)],0)
t2 = Triangle([(0,0),(4,0),(2,3)],0)
t1.MakeMove(ConfigFile)
for p in t1.vertices:
    plt.plot(p[0],p[1],'bo')
for p in t2.vertices:
    plt.plot(p[0],p[1],'ro')
plt.show()
print(OverlapFound(t1,t2))