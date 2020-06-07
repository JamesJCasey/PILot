# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 14:07:58 2020

@author: james
"""

import numpy as np
from SlitSource import SlitSource

class Barrier():
    
    def __init__(self, domain):
        self.domain = domain
        
        self.slits = []
    
    def setSlits(self, numSlits, slit_width, separation, diffraction_domain, wavelength = 6, amplitude = 1, numSources = 1):
        x0, y0, width, height = self.domain.getDrawBounds()
        
        mid = np.array([x0 + width/2, y0 + height/2])
        
        start_pos = mid - np.array([0, (0.5 * (numSlits - 1) * separation)])
        
        ## TODO: Make a config/global timestepping of the wave with wavedata
        
        for i in range(numSlits):
            pos = start_pos + [0, separation * i]
            self.slits.append(SlitSource(pos, slit_width, numSources, wavelength, amplitude / numSources, diffraction_domain))
    
    def get_wave_data(self):
        res = []
        
        for slit in self.slits:
            res.append(slit.get_wave_data())
        
        data = res[0]
        
        for d in res[1:]:
            data += d
        
        return data
    
    def drawBarrier(self, canvas):
        yStart = self.domain.y0
        
        for slit in self.slits:
            
        return None