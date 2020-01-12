#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 12 13:41:40 2020

@author: yash
"""

# well separated pair decomposition for the given datas

import time
import math
import matplotlib.pyplot as plt
from compressed_quadtree import Node, Point, compressed_quadtree

def add_well_separated_pairs(u, v, s, pairs):
    
    if(u.dist_node(v) > 0.5*s*max(u.diam, v.diam)):
        print('--------------')
        print(u.low_x)
        print(u.high_x)
        print('~~~~~~~~~~~')
        print(v.low_x)
        print(v.high_x)
        print('--------------')
        print(len(pairs))
        pairs.append([u,v])
    else:
        if(u.diam > v.diam):
           t = u
           u = v
           v = t
        for child in v.true_child:
            add_well_separated_pairs(u, child, s, pairs)
            
    return pairs
            
    
def well_separated_pair_decomposition(root,s):
    
    pairs = []
    stack = [root];
    while(len(stack) > 0):
        u = stack.pop()
        for i in range(len(u.true_child)):
            stack.append(u.true_child[i])
            for child_j in u.true_child[i+1:]:
                pairs = add_well_separated_pairs(u.true_child[i], child_j, s, pairs)
        
    return pairs


# s param for wspd
s = 3
r = 1/math.sqrt(2)
root = Node(0,r,0,r,-1)

points = [(0.05,0.01), (0.3,0.3), (0.68,0.68), (0.07,0.01), (0.12,0.15), (0.63,0.68)]
list_of_points = []

fig, ax = plt.subplots()

for i in range(len(points)):
    p = Point(points[i][0], points[i][1])
    ax.plot(p.x, p.y,'.b')
    list_of_points.append(p)

# construct compressed quadtree
compressed_quadtree(root, ax, list_of_points)
well_sep_pairs = well_separated_pair_decomposition(root, s)

plt.xlim(-0.01,0.72)
plt.ylim(-0.01,0.72)
plt.show()