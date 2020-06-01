# -*- coding: utf-8 -*-
"""
Created on Fri May 29 16:34:00 2020

@author: james
"""

from PIL import Image
import numpy as np

from Domain import Domain

class Canvas():
    
    def __init__(self, canv_width, canv_height):
        self.width = canv_width
        self.height = canv_height
        
        self.canv_data = np.zeros((self.width, self.height, 3))
        
        self.image_domain = Domain(0, 0, self.width, self.height)
    
    def getData(self):
        return self.canv_data
    
    def getDomain(self):
        return self.image_domain

    def drawData(self, data, domain):
        x0, y0, width, height = domain.getDrawBounds()
        
        for x in range(width):
            for y in range(height):
                self.canv_data[x0 + x, y0 + y] = data[x, y]
                
        self.clip()
    
    def clip(self):
        self.canv_data = np.clip(self.canv_data, a_min = 0, a_max = 255)
        
    def getImage(self):
        return Image.fromarray(np.transpose(self.canv_data.astype(np.uint8), (1, 0, 2)))

    def __add__(self, other):
        assert other.canv_data.shape == self.canv_data.shape
        
        self.canv_data += other.canv_data
        self.clip()