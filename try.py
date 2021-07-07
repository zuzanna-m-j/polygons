#!/usr/bin/env python3
import numpy as np

ox = 2
oy = 1

x = 3
y = 1

theta = np.radians(90)
M = np.array([[np.cos(theta), -1 * np.sin(theta)], [np.sin(theta), np.cos(theta)]])
v = np.array([x - ox, y - oy])
nv = np.dot(M, v)
nv[0] += ox
nv[1] += oy

print(nv[0],nv[1])

a = np.array([[1,[1,5,3]],[3,4]],dtype=object)
print(a)
b = a[0,1].pop(1)
print(a,b)


grid = np.empty((5,5), dtype= object)
for i in range(5):
    for j in range(5):
        grid[i,j] = []

x = 55
y = 15
i = (x//10)%5
j = (y//10)%5
print(i,j)
q = len(grid[i, j])

x_dim = 6
y_dim = 6
i, j, = 0,2
neighs = [

    ((i + 1) % x_dim, (j - 1) % y_dim), ((i + 1) % x_dim, j), ((i + 1) % x_dim, (j + 1) % y_dim),
    (i, (j - 1) % y_dim), (i, (j + 1) % y_dim),
    ((i - 1) % x_dim, (j - 1) % y_dim), ((i - 1) % x_dim, j), ((i - 1) % x_dim, (j + 1) % y_dim)
]
print(neighs)

