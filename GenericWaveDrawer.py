# -*- coding: utf-8 -*-
"""
Created on Sat Jun  6 16:13:31 2020

@author: james
"""

import numpy as np
from Domain import Domain
from Canvas import Canvas

class GenericWaveDrawer():
    
    def __getScaleFunc(self, low, high, left, right):
        return lambda x: left + (right - left) * ((x - low)/(high - low))

    def drawPlaneWaveData(self, waveData, domain, canvas):
        """
        Draws any generic planewave or interference over a 2D domain.
        """
        red = np.where(waveData > 0, waveData, 0)
        blue = np.where(waveData < 0, -waveData, 0)
        
        r_scale = self.__getScaleFunc(np.min(red), np.max(red), 0, 255)
        b_scale = self.__getScaleFunc(np.min(blue), np.max(blue), 0, 255)
        
        red = r_scale(red)
        blue = b_scale(blue)
        
        canvas.drawData(red, domain, 0)
        canvas.drawData(blue, domain, 2)
