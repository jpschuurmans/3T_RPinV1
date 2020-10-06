# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 20:39:11 2020

@author: jolien
"""

#http://whatismyscreenresolution.net/
scrsize = (int(expInfo['4. Screen width in px']),int(expInfo['3. Screen hight in px']))
r = scrsize[1] # Vertical resolution of the monitor
h = int(expInfo['5. Screen hight in cm']) # Monitor height in cm
d = int(expInfo['6. distance to screen']) # Distance between monitor and participant in cm

degreesStim = int(expInfo['7. Size of the stimulus in vis degrees'])



pxlDensY = r/(h*10)
mmPerDeg = math.atan(1)/45 * (d*10)  # number of pixels per degree
mmPerStim = mmPerDeg*degreesStim # how big stim should be in mm
stimSize = mmPerStim*pxlDensY # nr of pixels the face should be
#HIGHT since the face itself is 400 out of 550 pixels.. stim size should be magnified by 1.375
#WIDTH since the face itself is 364 out of 550 pixels.. stim size should be magnified by ~1.511
stimSize = 550