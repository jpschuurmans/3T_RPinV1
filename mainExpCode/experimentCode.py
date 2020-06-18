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
import numpy as np
import glob
from PIL import Image

#%% =============================================================================
durBlock = 10 # seconds
nStim = 20 # stimuli per block
nCond = 12 #nr of conditions
nBlockPerCond = 22 #nr of blocks per condition (in total)
nBlocks = nCond*nBlockPerCond # blocks in total
nRuns = 11 # runs for whole exp
nBlocksRun = nBlocks/nRuns # so... 24 blocks per run --> PICKLE IT :)

# a block contains 20 unique images + their mask
durCond = [50, 83.33, 100, 150] #

#1 trial contains 1 stim, 1 mask, 2 noiseframes. 1 block contains 20 trials.
# so for 1 block there must be 80 screens loaded
#%% =============================================================================
#window setup
scrsize = (1920,1080)

win = visual.Window(size=[800, 800], color='grey', units='pix', fullscr=False)

fix = visual.GratingStim(win, mask="gauss", color="black",texRes=256, 
           size=[10, 10], sf=[10, 0], ori = 0,pos=(0,0),units="pix",
           name='gabor1')

#%% =============================================================================
#stim settings
stimPath = (r'/home/jschuurmans/Documents/02_recurrentSF_3T/Stimuli/testImages/')

#sequence
seqLocation = (r'/home/jschuurmans/Documents/02_recurrentSF_3T/recurrentSF_3T_CodeRepo/sequence_exp.txt')
wordset = np.genfromtxt(seqLocation,dtype='int',delimiter=',')

faceNames = glob.glob(os.path.join(stimPath, 'faces' ,'*.bmp'))
noiseNames = glob.glob(os.path.join(stimPath, 'noise' ,'*.bmp'))
faceNames.sort()
noiseNames.sort()


#img_face = Image.open(faceNames[1])
#img_noise = Image.open(noiseNames[4])
#check = Image.blend(img_face, img_noise, alpha=0.5)

#DoesItWork = visual.ImageStim(win=win, image=check, size=[800,800])
#DoesItWork.draw()
#blockOrder[1:0].draw()
#win.flip()

#checkITOUT.shape
#checkITOUT = np.matrix(blockOrder)
#checkITOUT.mean()


#blockOrder.shape
#checkIT = np.matrix(img_face)
#checkIT.mean()

seqLocation = (r'/home/jschuurmans/Documents/02_recurrentSF_3T/recurrentSF_3T_CodeRepo/sequence_exp.txt')
wordset = np.genfromtxt(seqLocation,dtype='int',delimiter=',')

blockOrder = []
yy = 0
for block in range(len(wordset)): #11 unique blocks
    #tempFaces = copy.deepcopy(faceNames)
    facesToUse = [x for _,x in sorted(zip(wordset[yy],faceNames))]    
    ii = 0
    uu = 0
    for locat in noiseNames: # 120 noiseframes
        trialOrder = []
        if ii in wordset[yy]:
            tempFace = Image.open(facesToUse[uu])
            tempNoise = Image.open(noiseNames[ii])
            NewIm = Image.blend(tempFace, tempNoise, alpha=0.5)
            trialOrder.append(visual.ImageStim(win=win, image=NewIm, size=[400,400]))
            uu += 1
        else:
            trialOrder.append(visual.ImageStim(win=win, image=locat, size=[400,400]))
        ii += 1
    blockOrder.append(trialOrder)
    yy +=1
    
# create an image stimulus from each file, and store in the list:
faces = []
for file in faceNames:
    faces.append(visual.ImageStim(win=win, image=file, size=[400,400]))

noise = []
for file in noiseNames:
    noise.append(visual.ImageStim(win=win, image=file, size=[800,800]))


#%% =============================================================================
# For the timing!
frameRate = win.getActualFrameRate(nIdentical=60, nMaxFrames=100,
    nWarmUpFrames=10, threshold=1)
clock = core.Clock()

clock.reset()

#%% =============================================================================
condNr = 2

noiseFr = 20 #noise will be 20 frames in total
maskFr = 10 #mask always has 10 frames

if condNr == 1: #50ms
    faceFr = 3
elif condNr == 2: #83ms
    faceFr = 5
elif condNr == 3: #100ms
    faceFr = 6
elif condNr == 4: #150ms
    faceFr = 9
else:
    faceFr = 0
    maskFr = 0

#doesnt work well for all conditions
noiseFr -= maskFr+faceFr


#try stuff out 
faces[0].draw()
win.flip()

noise[4].draw()
win.flip()




fix.setAutoDraw(True)

for nFrames in range(360): #6 sec fixation
    win.flip()
for ii in range(trPerBlock):
    startSTIM = clock.getTime()
    for nFrames in range(faceFr): #50ms
        faces[1].draw()
        win.flip()
    startMASK = clock.getTime()
    for nFrames in range(maskFr): #166ms
        faces[0].draw()
        win.flip()
    endMASK = clock.getTime()

    for nFrames in range(noiseFr): #166ms - stimulustime
        noise[1].draw()
        win.flip()
    
for nFrames in range(360): #6 sec fixation
    win.flip()   

fix.setAutoDraw(False)

stimTIME = (startMASK - startSTIM) *1000
MASK = (endMASK - startMASK) *1000
wholeTHING = (endMASK - startSTIM) *1000


print('----> the actual stimulus took', int(stimTIME), 'ms')
print('----> the actual mask took', int(MASK), 'ms')

print('frame rate is', frameRate)
#win.close()