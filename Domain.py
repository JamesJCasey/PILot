# -*- coding: utf-8 -*-
"""
Created on Fri May 29 11:34:08 2020

@author: james
"""

class Domain():
    def __init__(self, xmin, ymin, xmax, ymax):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
        
        self.shape = (self.xmax - self.xmin, self.ymax - self.ymin)
        
        self.subdomains = []
        
    def split_vertical(self, xpos):
        left = self.create_subdomain(self.xmin, self.ymin, xpos, self.ymax)
        right = self.create_subdomain(xpos, self.ymin, self.xmax, self.ymax)
        
        return left, right

    def create_subdomain(self, xmin, ymin, xmax, ymax):
        dom = Domain(xmin, ymin, xmax, ymax)
        self.subdomains.append(dom)
        return dom
    
    def getBounds(self):
        return self.xmin, self.ymin, self.xmax, self.ymax
    
    def draw_domain(self, data):
        for dom in self.subdomains:
            dom.draw_domain(self.data)
        
        width = self.xmax - self.xmin
        height = self.ymax - self.ymin
        
        print(width, height)
        
        for x in range(width):
            for y in range(height):
                data[self.ymin + y, self.xmin + x, 2] += 0.4
        
        for x in range(width):
            data[self.ymin, self.xmin + x, :] += 1
            data[self.ymax - 1, self.xmin + x, :] = 1 
            
        for y in range(height):
            data[self.ymin + y, self.xmin, :] += 1
            data[self.ymin + y, self.xmax - 1, :] += 1
