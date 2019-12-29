#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 28 21:53:04 2019

@author: yash
"""

# recursively build a compressed quadtree for a given set of points

import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class Point():
    
    def __init__(self, x, y):
        
        self.x = x
        self.y = y
        
class Node():
    
    def __init__(self, low_x, high_x, low_y, high_y):
        
        self.low_x = low_x
        self.high_x = high_x
        self.low_y = low_y
        self.high_y = high_y
        self.children = []
        self.isLeaf = False
    
    def draw(self, ax):
        width = self.high_x - self.low_x
        height = self.high_y - self.low_y
        rect = patches.Rectangle((self.low_x, self.low_y), width, height, linestyle='-.',linewidth=1, edgecolor='r', facecolor='None')
        ax.add_patch(rect)
        
    def make_children(self, points):
        
        mid_x = (self.low_x + self.high_x)/2
        mid_y = (self.low_y + self.high_y)/2
        
        c1 = Node(self.low_x, mid_x, self.low_y, mid_y)
        if(c1.check_points(points)>0):
            self.children.append(c1)
        
        c2 = Node(mid_x, self.high_x, self.low_y, mid_y)
        if(c2.check_points(points)>0):
            self.children.append(c2)
            
        c3 = Node(self.low_x, mid_x, mid_y, self.high_y)
        if(c3.check_points(points)>0):
            self.children.append(c3)
            
        c4 = Node(mid_x, self.high_x, mid_y, self.high_y)
        if(c4.check_points(points)>0):
            self.children.append(c4)
        
    def check_points(self, points):
        
        count_points = 0
        
        for p in points:
            if((self.low_x <= p.x < self.high_x) & (self.low_y <= p.y < self.high_y)):
                count_points += 1
                
        if(count_points==1):
            self.isLeaf = True
                
        return count_points

def compressed_quadtree(node, ax, points):
    node.make_children(points)
    nodepoints = node.check_points(points)
    for child in node.children:
        if(nodepoints != child.check_points(points)):
            child.draw(ax)
        if(child.isLeaf==False):
            compressed_quadtree(child, ax, points)
    
        

s = 1/math.sqrt(2)
root = Node(0,s,0,s)

points = [(0.05,0.01), (0.3,0.3), (0.68,0.68), (0.07,0.01), (0.12,0.15), (0.63,0.68)]
list_of_points = []

fig, ax = plt.subplots(1)

for i in range(len(points)):
    p = Point(points[i][0], points[i][1])
    ax.plot(p.x, p.y,'.b')
    list_of_points.append(p)

compressed_quadtree(root, ax, list_of_points)

plt.xlim(-0.01,0.72)
plt.ylim(-0.01,0.72)
plt.show()