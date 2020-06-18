#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 14:22:48 2020

@author: jschuurmans
"""
import numpy as np 
from math import ceil
import copy

#% =============================================================================

durBlock = 10000 # in ms


# a block contains 20 unique images + their mask
durCond = [50, 83.33, 100, 150] #in ms
imagType = 3 #number of image types (face/negated/scrambled)
maskDur = 166.66

nCond = len(durCond)*imagType
nStim = 20 # stimuli per block


nBlocksCond = 22 #22 blocks per condition
nUniBlocks = nBlocksCond/2 #nr of unique blocks per condition = 11 (11 sequences to make)
nBlocks = nCond*nBlocksCond

nRuns = 11 # runs for whole exp
nBlocksRun = nBlocks/nRuns # so... 24 blocks per run --> PICKLE IT :)


#% =============================================================================
# in frames

refRate = 60 #refreshrate of stimulus screen
oneFrame = 1000/60 #inms

# a block contains 600 frames
nFramesBlock = round(durBlock/oneFrame)

nFramesCond = []
for number in durCond:
    nFramesCond.append(round(number/oneFrame))
nFramesMask = round(maskDur/oneFrame)


nFramesStimMask = nFramesCond[-1] + nFramesMask + 1 #plus one blank frame
#nr of possible positions in the sequence
nPositions = round(nFramesBlock/nFramesStimMask)
stimPosi = list(range(nPositions)) #30 possible positions in a block

# every block has 20 stimuli, and there will be 11 unique blocks.
totalPos = round(nStim*nUniBlocks)
# all positions of stimuli in the whole experiment (for all 11 blocks)
posReps = ceil(totalPos/nPositions)
allPosi = stimPosi*posReps

# every stimulus has 11 different spots 
#all 30 positions in a block should be equally filled over the 11 blocks
#
blockSeq = []

for block in range(int(nUniBlocks)):
    row = []
    tmp = copy.deepcopy(allPosi)
    for trial in range(nStim):
        pick = np.random.choice(tmp)
        if pick in row:
            pick = np.random.choice(tmp)
        row.append(pick)
        allPosi.remove(pick)

        for elem in tmp:
            if elem == pick:
                tmp.remove(elem)

    if block == 0:
        blockSeq = row
    else:
        blockSeq = np.vstack([blockSeq, row])

#blockSeq.shape[1]
#check = np.matrix(blockSeq)
#check.mean()
means = []
for bla in range(blockSeq.shape[1]):
    x= np.mean(blockSeq[:,bla])
    means.append(x)
    
#1 trial contains 1 stim, 1 mask, 2 noiseframes. 1 block contains 20 trials.
# so for 1 block there must be 80 screens loaded

logLocation = '/home/jschuurmans/Documents/02_recurrentSF_3T/recurrentSF_3T_CodeRepo/sequence_exp.txt'
np.savetxt(logLocation,blockSeq.astype(int),fmt='%i',delimiter=',')

logfile = open(logLocation, 'w')
logfile.write(blockSeq)
logfile.close()





