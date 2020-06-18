#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 10:15:49 2020

@author: jschuurmans
"""
from psychopy import visual, event

win = visual.Window()
patch = visual.GratingStim(
    win,
    size=(1, 1),
    colorSpace='rgb255',
    units='norm',
    sf=0)
text = visual.TextStim(win, pos=(0, -0.6))

for intensity in range(0, 255, 10):
    patch.color = (intensity, intensity, intensity)
    text.text = f'x={intensity}'
    patch.draw()
    text.draw()
    win.flip()
    event.waitKeys()
#%% =============================================================================
import numpy as np
from scipy.optimize import fmin


def error_func(abgamma, x, L):
    a, b, gamma = abgamma
    Lexpect = b + a*x**gamma
    return np.sum((Lexpect - L)**2)


def estimate_gamma(x, L):
    return fmin(error_func, [0, 1, 2], args=(x, L))[-1]


#x = [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200,210,220,230,240,250]
#L =[]
    
x=[0,100,200]
L=[0.2,0.5,0.9]
JA = estimate_gamma(x,L)
#https://fruendlab.github.io/understanding-gamma-calibration.html