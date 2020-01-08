#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 16:13:41 2020

@author: yash
"""

## query k-approximate nearest neighbour

# heap data structure used to implement the priority queue

import heapq
import math
import matplotlib.pyplot as plt
from compressed_quadtree import Node, Point, compressed_quadtree

def approx_nn(root, k, query, e):
    near_points = []
    
    # initialize the priority queue
    root.cal_cpd_fpd_key(query,e)
    priority_queue = []
    heapq.heappush(priority_queue, root)
    
    while(k > len(near_points)):
        print(len(priority_queue))
        print('----')
        u = heapq.heappop(priority_queue)
        print(u.low_x)
        print(u.high_x)
        if(u.fpd <= (1 + e)*u.cpd):
            print(u.fpd)
            print(u.cpd)
            # greedy explore the subtree at u
            stack = [u]
            while(len(stack)>0):
                print(len(stack))
                u = stack.pop()
                if(u.isLeaf==True):
                    near_points.append(u)
                    if(len(near_points) == k):
                        return near_points
                else:
                    for v in u.children:
                        stack.append(u)
            
        else:
            for v in u.children:
                v.cal_cpd_fpd_key(query,e)
                heapq.heappush(priority_queue, v)

s = 1/math.sqrt(2)
root = Node(0,s,0,s,-1)

# initial point list
points = [(0.05,0.01), (0.3,0.3), (0.68,0.68), (0.07,0.01), (0.12,0.15), (0.63,0.68)]
list_of_points = []

# query nn parameters
q_point = Point(0.4, 0.4)
k = 2
e = 0.1

fig, ax = plt.subplots(1)
ax.plot(q_point.x, q_point.y, '*m')

# plotting the given points
for i in range(len(points)):
    p = Point(points[i][0], points[i][1])
    ax.plot(p.x, p.y,'.b')
    list_of_points.append(p)

compressed_quadtree(root, ax, list_of_points)

nn_nodes = approx_nn(root, k, q_point, e)

# plotting the nearest neighbour points
for nn in nn_nodes:
    nnp = nn.check_points(list_of_points)
    circ = plt.Circle((nnp[0].x, nnp[0].y), 0.01, color='k', fill=False)
    ax.add_artist(circ)
    
#plt.xlim(-0.01,0.72)
#plt.ylim(-0.01,0.72)
plt.show()
