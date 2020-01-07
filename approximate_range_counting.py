#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 12:11:28 2020

@author: yash
"""

## approx range counting

import math
import matplotlib.pyplot as plt
from compressed_quadtree import Node, Point, compressed_quadtree

def approx_range(root, radius, query, e, points):
    
    range_points = []
    stack = [root]
    
    while(len(stack) > 0):
        u = stack.pop()
        u.cal_cpd_fpd_key(query, e)
        if (u.fpd <= (1+e)*radius):
            for p in u.check_points(points): 
                range_points.append()
        elif (u.cpd < (1+e)*radius):
            if(u.isLeaf):
                leaf_point = u.check_points(points)
                if(leaf_point[0].distance_from_point(query) <= (1+e)*radius):
                    range_points.append(leaf_point[0])
            else:
                for v in u.children:
                    stack.append(v)
                
    return range_points
    
s = 1/math.sqrt(2)
root = Node(0,s,0,s)

# initial point list
points = [(0.05,0.01), (0.3,0.3), (0.68,0.68), (0.07,0.01), (0.12,0.15), (0.63,0.68)]
list_of_points = []

# range counting circle parameters
q_point = Point(0.4, 0.4)
radius = 0.2
e = 0.05

fig, ax = plt.subplots(1)
ax.plot(q_point.x, q_point.y, '*m')

# plotting the given points
for i in range(len(points)):
    p = Point(points[i][0], points[i][1])
    ax.plot(p.x, p.y,'.b')
    list_of_points.append(p)

compressed_quadtree(root, ax, list_of_points)

range_points = approx_range(root, radius, q_point, e, list_of_points)

# plotting the range circle
# r - circle
r_circ = plt.Circle((q_point.x, q_point.y), radius, ls = '--', fill=False)
ax.add_artist(r_circ)
# (1+e)r - circle
er_circ = plt.Circle((q_point.x, q_point.y), (1+e)*radius, ls = '-.', fill=False)
ax.add_artist(er_circ)

# plotting the points in circle
for r_p in range_points:
    circ = plt.Circle((r_p.x, r_p.y), 0.01, color='k', fill=False)
    ax.add_artist(circ)
    
#plt.xlim(-0.01,0.72)
#plt.ylim(-0.01,0.72)
plt.show()
