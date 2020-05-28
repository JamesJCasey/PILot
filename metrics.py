# -*- coding: utf-8 -*-
"""
Created on Thu May 28 11:19:48 2020

@author: james
"""

import numpy as np

def lebesgue_metric(array, n):
    return (np.sum(array**n))**(1/n)

def euclid_metric(array):
    return lebesgue_metric(array, 2)