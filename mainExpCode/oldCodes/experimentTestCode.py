#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 17:06:24 2020

@author: jschuurmans
"""
#%% =============================================================================
# imports

from psychopy import visual, core
import os  


#%% =============================================================================
durBlock = 10 # seconds
nStim = 20 # stimuli per block
nBlocks = 264 # blocks in total
nRuns = 11 # runs for whole exp
nBlocksRun = nBlocks/nRuns # so... 24 blocks per run --> PICKLE IT :)

# a block contains 20 unique images + their mask
durCond = [50, 83.33, 100, 150] #

#1 trial contains 1 stim, 1 mask, 2 noiseframes. 1 block contains 20 trials.
# so for 1 block there must be 80 screens loaded
#%% =============================================================================
#window setup
scrsize = (1920,1080)

win = visual.Window(size=scrsize, color='grey', units='pix', fullscr=True)

fix = visual.GratingStim(win, mask="gauss", color="black",texRes=256, 
           size=[10, 10], sf=[10, 0], ori = 0,pos=(0,0),units="pix",
           name='gabor1')

#%% =============================================================================
#stim settings
stimPath = (r'/home/jschuurmans/Documents/02_recurrentSF_3T/Stimuli/Valerie/Stimuli_done/')

stim1 = 'bb_face.jpg'
stim2 = 'bb_mask.jpg'
noise1 = 'whitenoise1.bmp'
noise2 = 'whitenoise2.bmp'
noise3 = 'whitenoise3.bmp'

trPerBlock = 20 #nr of trials per block
#%% =============================================================================
# For the timing!
frameRate = win.getActualFrameRate(nIdentical=60, nMaxFrames=100,
    nWarmUpFrames=10, threshold=1)
clock = core.Clock()

clock.reset()

#%% =============================================================================
noiseFr = 10
stimDur = 3

if stimDur == 1: 
    stimFr = 3 #50ms
elif stimDur ==2:
    stimFr = 6 #100ms
else: 
    stimFr = 9 #150ms
noiseFr -= stimFr

#try stuff out 
stimDRAW = clock.getTime()

stimFrame1 = os.path.join(stimPath, stim1)
bitmap1 = visual.ImageStim(win, size=[800,600])
bitmap1.setImage(stimFrame1)
bitmap1.size=(400,400)

stimFrame2 = os.path.join(stimPath, stim2)
bitmap2 = visual.ImageStim(win, size=[800,600])
bitmap2.setImage(stimFrame2)
bitmap2.size=(400,400)

noiseFrame1 = os.path.join(stimPath, noise1)
bitmap3 = visual.ImageStim(win, size=[800,600])
bitmap3.setImage(noiseFrame1)
bitmap3.size=(400,400)

noiseFrame2 = os.path.join(stimPath, noise2)
bitmap4 = visual.ImageStim(win, size=[800,600])
bitmap4.setImage(noiseFrame2)
bitmap4.size=(400,400)

noiseFrame3 = os.path.join(stimPath, noise2)
bitmap5 = visual.ImageStim(win, size=[800,600])
bitmap5.setImage(noiseFrame3)
bitmap5.size=(400,400)
endDRAW = clock.getTime()


for nFrames in range(360): #6 sec fixation
    fix.draw()
    win.flip()
for ii in range(trPerBlock):
    startSTIM = clock.getTime()
    for nFrames in range(stimFr): #50ms
        bitmap1.draw()
        fix.draw()
        win.flip()
    startMASK = clock.getTime()
    for nFrames in range(10): #166ms
        bitmap2.draw()
        fix.draw()
        win.flip()
    endMASK = clock.getTime()

    for nFrames in range(noiseFr): #166ms - stimulustime
        bitmap3.draw()
        fix.draw()
        win.flip()
    
    for nFrames in range(10): #166ms
        bitmap4.draw()
        fix.draw()
        win.flip()
for nFrames in range(360): #6 sec fixation
    fix.draw()
    win.flip()   


drawALL = (endDRAW - stimDRAW) *1000
stimTIME = (startMASK - startSTIM) *1000
MASK = (endMASK - startMASK) *1000
wholeTHING = (endMASK - stimDRAW) *1000

print('drawing the stimuli took', int(drawALL), 'ms')

print('----> the actual stimulus took', int(stimTIME), 'ms')
print('----> the actual mask took', int(MASK), 'ms')

print('frame rate is', frameRate)
#win.close()