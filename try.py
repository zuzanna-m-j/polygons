#!/usr/bin/env python3
import numpy as np
from base import*

box = Structure("input.txt")

particles = []
for _ in range(5):
    particles.append(Shape(box,random.choice(list(range(box.types)))))

color = ["dodgerblue","red",'green','gold','violet']
for i in range(len(particles)):
    v = np.array(box.vertex_positions[i])
    st = 0
    s = particles[i].shape
    for n in range(s):
        x, y = v[st:st + 2]
        p, q = v[st - 2], v[st - 1]
        st += 2
        plt.plot(x, y, 'o', label=n)
        plt.plot((x, p), (y, q), '--', color=color[i])
    plt.legend()
plt.show()

# print positions before and after

# ox = 2
# oy = 1
#
# x = 3
# y = 1
#
# theta = np.radians(90)
# M = np.array([[np.cos(theta), -1 * np.sin(theta)], [np.sin(theta), np.cos(theta)]])
# v = np.array([x - ox, y - oy])
# nv = np.dot(M, v)
# nv[0] += ox
# nv[1] += oy
#
# print(nv[0],nv[1])
#
# a = np.array([[1,[1,5,3]],[3,4]],dtype=object)
# print(a)
# b = a[0,1].pop(1)
# print(a,b)
#
#
# grid = np.empty((5,5), dtype= object)
# for i in range(5):
#     for j in range(5):
#         grid[i,j] = []
#
# x = 55
# y = 15
# i = (x//10)%5
# j = (y//10)%5
# print(i,j)
# q = len(grid[i, j])
#
# x_dim = 6
# y_dim = 6
# i, j, = 0,2
# neighs = [
#
#     ((i + 1) % x_dim, (j - 1) % y_dim), ((i + 1) % x_dim, j), ((i + 1) % x_dim, (j + 1) % y_dim),
#     (i, (j - 1) % y_dim), (i, (j + 1) % y_dim),
#     ((i - 1) % x_dim, (j - 1) % y_dim), ((i - 1) % x_dim, j), ((i - 1) % x_dim, (j + 1) % y_dim)
# ]
# print(neighs)

