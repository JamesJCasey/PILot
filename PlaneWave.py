# -*- coding: utf-8 -*-
"""
Created on Thu May 28 11:46:37 2020

@author: james
"""

import numpy as np

class PlaneWave():
    def __init__(self, wavelength, amplitude, domain, direction):
        self.wavelength = wavelength
        self.domain = domain
        
        self.amplitude = amplitude
        
        self.direction = direction / np.sqrt(np.sum(direction**2))
        
        x_min, y_min, x_max, y_max = self.domain
        
        x = np.arange(x_min, x_max)
        y = np.arange(y_min, y_max)
        
        self.x_mesh, self.y_mesh = np.meshgrid(x, y)

    def get_wave_data(self):
        data = self.amplitude * np.cos(2 * np.pi/self.wavelength * (self.direction[0]*self.y_mesh + self.direction[1]*self.x_mesh))
        return data