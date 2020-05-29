# -*- coding: utf-8 -*-
"""
Created on Fri May 29 16:34:00 2020

@author: james
"""

import numpy as np

class Canvas():
    
    def __init__(self, canv_width, canv_height):
        self.width = canv_width
        self.height = canv_height
        
        self.canv_data = np.zeros((self.width, self.height, 3))
    
    def getData(self):
        return self.canvas_data
    
    def drawData(self, data, x0, y0):
        width, height = data.shape
        
        for x in range(height):
            for y in range(width):
                data[y0 + y, x0 + x, :] = data[x, y]
    
    def __add__(self, other):
        self.canv_data + other.canv_data