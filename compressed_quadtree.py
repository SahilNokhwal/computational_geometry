#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 28 21:53:04 2019

@author: yash
"""

# recursively build a compressed quadtree for a given set of points

import time
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class Point():
    
    def __init__(self, x, y):
        
        self.id = 'point'
        self.x = x
        self.y = y
        
    def distance_from_point(self, point):
        dx = self.x - point.x
        dy = self.y - point.y
        return math.sqrt(dx**2 + dy**2)
        
class Node():
    
    def __init__(self, low_x, high_x, low_y, high_y, parent):
        
        self.low_x = low_x
        self.high_x = high_x
        self.low_y = low_y
        self.high_y = high_y
        self.children = []
        self.true_child = []
        self.parent = parent
        self.isLeaf = False
        self.cpd = 0.0
        self.fpd = 0.0
        self.key = 0.0
        self.add_to_parent = False
        
    def __lt__(self, other):
        return self.key < other.key
        
    def distance(self, u,v):
        return math.sqrt((u[0] - v[0])**2 + (u[1] - v[1])**2)
        
    def dist_2_node_vert(self, query_point):
        
        list_dist = []

        # distances from vertices
        list_dist.append(self.distance([self.low_x,self.low_y], [query_point.x,query_point.y]))
        list_dist.append(self.distance([self.high_x,self.high_y], [query_point.x,query_point.y]))
        list_dist.append(self.distance([self.high_x,self.low_y], [query_point.x,query_point.y]))
        list_dist.append(self.distance([self.low_x,self.high_y], [query_point.x,query_point.y]))
        
        return list_dist
    
    def cal_cpd_fpd_key(self, query_point,e):
        self.cal_cpd(query_point)
        self.cal_fpd(query_point)
        self.key = min(self.cpd, (self.fpd/(1+e)))
    
#    def cal_cpd(self, query_point):
#        
#        if(self.check_inside_node(query_point)):
#            self.cpd = 0.0
#        elif((query_point.x < self.low_x or query_point.x >= self.high_x) 
#                    & (self.low_y <= query_point.y < self.high_y)):
#            self.cpd = min(self.distance([self.low_x,0], [query_point.x,0]),
#                           self.distance([self.high_x,0], [query_point.x,0]))
#        elif((query_point.y < self.low_y or query_point.y >= self.high_y) 
#                    & (self.low_x <= query_point.x < self.high_x)):
#            self.cpd = min(self.distance([0, self.low_y], [0,query_point.y]),
#                           self.distance([0,self.high_y], [0,query_point.y]))
#        else:
#            self.cpd = min(self.dist_2_node_vert(query_point))
    
    def cal_cpd(self, query_point):
        
        dx = max(self.low_x - query_point.x, 0, query_point.x - self.high_x)
        dy = max(self.low_y - query_point.y, 0, query_point.y - self.high_y)
        
        self.cpd =  math.sqrt(dx**2 + dy**2)
    
#    def cal_fpd(self, query_point):
#        dx = max(- self.low_x + query_point.x, - query_point.x + self.high_x)
#        dy = max(- self.low_y + query_point.y, - query_point.y + self.high_y)
#        
#        self.fpd =  math.sqrt(dx**2 + dy**2)
    
    def cal_fpd(self, query_point):
        self.fpd = max(self.dist_2_node_vert(query_point))
    
    def draw(self, ax):
        width = self.high_x - self.low_x
        height = self.high_y - self.low_y
        rect = patches.Rectangle((self.low_x, self.low_y), width, height, linestyle='-.',linewidth=1, edgecolor='r', facecolor='None')
        ax.add_patch(rect)
        
    def make_children(self, points):
        
        mid_x = (self.low_x + self.high_x)/2
        mid_y = (self.low_y + self.high_y)/2
        
        c1 = Node(self.low_x, mid_x, self.low_y, mid_y, self)
        if(len(c1.check_points(points))>0):
            self.children.append(c1)
        
        c2 = Node(mid_x, self.high_x, self.low_y, mid_y, self)
        if(len(c2.check_points(points))>0):
            self.children.append(c2)
            
        c3 = Node(self.low_x, mid_x, mid_y, self.high_y, self)
        if(len(c3.check_points(points))>0):
            self.children.append(c3)
            
        c4 = Node(mid_x, self.high_x, mid_y, self.high_y, self)
        if(len(c4.check_points(points))>0):
            self.children.append(c4)
        
    def check_inside_node(self, p):
        return (self.low_x <= p.x < self.high_x) & (self.low_y <= p.y < self.high_y)
    
    def check_points(self, points):
        
        count_points = []
        
        for p in points:
            if(self.check_inside_node(p)):
                count_points.append(p)
                
        if(len(count_points)==1):
            self.isLeaf = True
                
        return count_points

def compressed_quadtree(node, ax, points):
    node.make_children(points)
    nodepoints = len(node.check_points(points))
    for child in node.children:
        
        if(nodepoints != len(child.check_points(points))):
            node.add_to_parent = True
        
        if(child.isLeaf==False):
            compressed_quadtree(child, ax, points)
        else:
            leaf_point = child.check_points(points)[0]
            leaf_node = Node(leaf_point.x-0.01, leaf_point.x+0.001, leaf_point.y-0.0001, leaf_point.y+0.001, node)
            node.true_child.append(leaf_node)
            leaf_node.draw(ax)
    
    if(node.add_to_parent):
        if(node.parent != -1): # node is not the root node itself
            points_in_node = len(node.check_points(points))
            par = node.parent
            while(len(par.check_points(points)) == points_in_node):
                par = par.parent
            par.true_child.append(node)
        node.draw(ax)
        

s = 1/math.sqrt(2)
root = Node(0,s,0,s,-1)

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