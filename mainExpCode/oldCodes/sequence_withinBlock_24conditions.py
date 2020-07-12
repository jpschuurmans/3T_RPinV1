#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 14:22:48 2020

@author: jschuurmans

creates sequence within blocks

"""
import numpy as np 
from math import ceil
import copy

#% =============================================================================

durBlock = 10000 # in ms


# a block contains 20 unique images + their mask
durCond = [50, 83.33, 100, 150] #in ms
imagType = 3 #number of image types (face/negated/scrambled)
maskType = 2 #masks in 2 SFs
maskDur = 166.66

nCond = len(durCond)*imagType*maskType
nStim = 24 # stimuli per block


nBlocksCond = 20 #20 blocks per condition
nUniBlocks = nBlocksCond/2 #nr of unique blocks per condition = 10 (10 sequences to make)
nBlocks = nCond*nBlocksCond

nRuns = 20 # runs for whole exp
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


nFramesStimMask = nFramesCond[-1] + nFramesMask + 6 #plus 6 blank frames (100ms at least)
#nr of possible positions in the sequence 
nPositions = round(nFramesBlock/nFramesStimMask)
stimPosi = list(range(nPositions)) #24 possible positions in a block

# every block has 24 stimuli, and there will be 10 unique blocks.
totalPos = round(nStim*nUniBlocks)
# all positions of stimuli in the whole experiment (for all 10 blocks)
posReps = ceil(totalPos/nPositions)
allPosi = stimPosi*posReps

# every stimulus has 10 different spots 
#all 24 positions in a block should be equally filled over the 10 blocks
#
theMean = (nPositions-1)/2
DoIt = True

while DoIt:
    blockSeq = []
    allPosi = stimPosi*posReps
    for block in range(int(nUniBlocks)):#for every unique block (10 blocks)
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
    for bla in range(blockSeq.shape[1]): #get an array of mean block for all 24 positions
        x= np.mean(blockSeq[:,bla])
        means.append(x)
    

    checkMean = np.mean(means) #mean over all positions
    checkSTD = np.std(means)
    checkMin = checkMean - np.amin(means) #get smallest mean
    checkMax = np.amax(means) - checkMean #get biggest mean
    if checkMin > 2.7 or checkMax > 2.7 or checkMean > (theMean + 0.2) or checkMean < (theMean - 0.2):
        print('min: ' + str(checkMin) + ' ...... max: ' + str(checkMax))
        DoIt = True
        
    else:
        DoIt = False



logLocation = 'C:\\Users\\jolien\\Documents\\3T_RPinV1\\recurrentSF_3T_CodeRepo\\mainExpCode\\sequence_exp.txt'

np.savetxt(logLocation,blockSeq.astype(int),fmt='%i',delimiter=',')

#logfile = open(logLocation, 'w')
#logfile.write(blockSeq)
#logfile.close()





