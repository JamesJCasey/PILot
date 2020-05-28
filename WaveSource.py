# -*- coding: utf-8 -*-
"""
Created on Thu May 28 11:00:23 2020

@author: james
"""

import numpy as np

class WaveSource():
    
    def __init__(self, source_pos, wavelength, domain, amplitude):
        self.pos  = source_pos
        self.wavelength = wavelength
        self.domain = domain
        self.amplitude = amplitude
        
        x_min, y_min, x_max, y_max = self.domain
        
        x = np.arange(x_min, x_max, dtype=np.float64)
        y = np.arange(y_min, y_max, dtype=np.float64)

        x -= self.pos[0]
        y -= self.pos[1]
        
        self.x_mesh, self.y_mesh = np.meshgrid(x, y)

    def get_wave_data(self):
        data = self.amplitude * np.cos(2 * np.pi/self.wavelength * np.sqrt(self.x_mesh**2 + self.y_mesh**2))
        return data