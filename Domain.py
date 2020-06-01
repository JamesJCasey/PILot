# -*- coding: utf-8 -*-
"""
Created on Fri May 29 11:34:08 2020

@author: james
"""

class Domain():
    def __init__(self, xmin, ymin, xmax, ymax):
        self.xmin = int(xmin)
        self.ymin = int(ymin)
        self.xmax = int(xmax)
        self.ymax = int(ymax)
        
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
    
    def getDrawBounds(self):
        return self.xmin, self.ymin, self.xmax - self.xmin, self.ymax - self.ymin
    
    def getSize(self):
        return self.xmax - self.xmin, self.ymax - self.ymin

    def getPosition(self):
        return self.xmin, self.ymin

    def draw_domain(self, data):
        for dom in self.subdomains:
            dom.draw_domain(self.data)
        
        width, height = self.getSize()
        
        for x in range(width):
            for y in range(height):
                data[self.xmin + x, self.ymin + y, 2] += 0.4
        
        for x in range(width):
            data[self.xmin + x, self.ymin, :] += 1
            data[self.xmin + x, self.ymax - 1, :] = 1 
            
        for y in range(height):
            data[self.xmin, self.ymin + y, :] += 1
            data[self.xmax - 1, self.ymin + y, :] += 1
