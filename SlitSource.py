# -*- coding: utf-8 -*-
"""
Created on Thu May 28 13:39:32 2020

@author: james
"""

import numpy as np

from WaveSource import WaveSource

class SlitSource():
    def __init__(self, pos, width, num_sources, wavelength, amplitude, domain):
        self.sources = []
        self.amplitude = amplitude
        
        start_pos = pos - np.array([0, width / 2])
        
        sep = width / (num_sources + 1)
        
        for i in range(num_sources):
            self.sources.append(WaveSource(start_pos + [0, sep * i], wavelength, domain, amplitude / num_sources))
        
    def get_wave_data(self):
        res = []
        
        for source in self.sources:
            res.append(source.get_wave_data())
        
        data = res[0]
        
        for d in res[1:]:
            data += d
        
        return data