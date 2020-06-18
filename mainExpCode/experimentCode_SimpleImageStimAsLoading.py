#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 17:06:24 2020

@author: jschuurmans
"""
#%% =============================================================================
# imports

from psychopy import visual, event, core, gui, data
import os
import numpy as np
import glob
from PIL import Image
import pickle
import random
import copy

#%% =============================================================================
# a block contains 20 unique images + their mask
durCond = [50, 83.33, 100, 150] #
typCond = ['Int', 'Neg', 'Scr']
nCond = len(durCond)*len(typCond) #nr of conditions = 12

nBlockPerCond = 22 #nr of blocks per condition (in total)
nUniBlocks = int(nBlockPerCond/2) #nr of unique blocks per condition = 11 (11 sequences to make)
nBlocks = nCond*nBlockPerCond # 264 blocks in total

nRuns = 11 # runs for whole exp
nBlocksRun = nBlocks/nRuns # so... 24 blocks per run --> PICKLE IT :)

durBlock = 10 # seconds
nStim = 20 # stimuli per block
nPositions = 30 # 30 positions in a block (for stim distribution)

fixStEn = 12 # Duration of fixation at begin/end of run in ms

#%% =============================================================================
#paths
dataPath = (r'C:\\Users\\jolien\\Documents\\3T_RPinV1\\recurrentSF_3T_CodeRepo\\testData\\')

logLocation = 'C:\\Users\\jolien\\Documents\\3T_RPinV1\\recurrentSF_3T_CodeRepo\\'

stimPath = (r'C:\\Users\\jolien\\Documents\\3T_RPinV1\\Stim_Main\\stimuli\\')
noisePath = (r'C:\\Users\\jolien\\Documents\\3T_RPinV1\\Stim_Main\\noiseFrames\\')
#%% =============================================================================
# in case we need to shut down the expt

def esc():
    if 'escape' in last_response:
#        logfile.close()
        win.close()
        core.quit

#%% =============================================================================
# Store info about the experiment session
# Get subject participant ID and run nr through a dialog box
expName = 'Recurrent face processing in V1'
expInfo = {
        'Participant ID': '',
        'Run number': '',
        }

dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)

# If 'Cancel' is pressed, quit
if dlg.OK == False:
    core.quit()
        
# Get date and time
expInfo['date'] = data.getDateStr()
expInfo['expName'] = expName

# Make sure there is a path to write away the data
if not os.path.isdir(dataPath):
    os.makedirs(dataPath)

# make a text file to save data with 'comma-separated-values'
dataName = expInfo['Participant ID'] + '_run' + expInfo['Run number'] + '_' + expInfo['date']
dataFname = os.path.join(dataPath, dataName)

#logfile = open(dataFname, 'w')
#logfile.write('Trial_Number, Stimulus, StimCode, StimOnset, StimOffset, Response, ###################################333
#       ResponseTime \n') 
#In allTrialOrder I have this info: 'blockNr, posInRun, posInBlock, trialNr, 
#       condName, stimFrames, imageName, maskName, noiseFrame1, noiseFrame2,
#       noiseFrame3, noiseFrame4'

#%% =============================================================================
#make or load block order for participant
logLocationBlockSeq = os.path.join(dataPath, expInfo['Participant ID'] + 'blockSeq.txt')
logLocationNoiseSeq = os.path.join(dataPath, expInfo['Participant ID'] + 'noiseSeq.txt')
logLocationBlockCount = os.path.join(dataPath, expInfo['Participant ID'] + 'blockCount.txt')
logLocationStimSeq = os.path.join(dataPath, expInfo['Participant ID'] + 'stimSeq.txt')

runNr = int(expInfo['Run number'])

if runNr == 1: #make new block/stim/noise sequences for first run
    
    sequenceAllCond = (list(range(nCond)))*2
    blockSeq = []

    for run in range(nRuns):
       random.shuffle(sequenceAllCond)
       toAdd = copy.deepcopy(sequenceAllCond)
       blockSeq.append(toAdd)

    with open(logLocationBlockSeq, 'wb') as fp:
        pickle.dump(blockSeq, fp)
    
    #22 blocks per condition (11 unique ones times 2)
    #sequence for noise background:
    noiseSeq = []
    noiseList = (list(range(nUniBlocks)))*2
    k=0
    while k < 12:
        random.shuffle(noiseList)
        toAdd = copy.deepcopy(noiseList)
        noiseSeq.append(toAdd)
        k +=1
    
    blockCount = list(np.zeros(nCond)) #there are 12 conditions.
    # one condition can be shown 22 timesthroughout the whole experiment    

    # blockSeq is the order of blocks within a run..
    #stimSeq is the order of stimuli within each block
    seqLocation = os.path.join(logLocation, 'sequence_withinBlock.txt')
    stimSeq = np.genfromtxt(seqLocation,dtype='int',delimiter=',') #seq within blocks
    stimSeq = np.append(stimSeq,stimSeq,axis=0)
    np.random.shuffle(stimSeq)

else: #get the old pickled stuff for the other runs
    with open(logLocationBlockSeq, 'rb') as fp:
        blockSeq = pickle.load(fp)
    with open(logLocationBlockSeq, 'wb') as fp:
        pickle.dump(blockSeq, fp)
    with open(logLocationNoiseSeq, 'rb') as fp:
        noiseSeq = pickle.load(fp)
    with open(logLocationBlockCount, 'rb') as fp:
        blockCount = pickle.load(fp)
    with open(logLocationStimSeq, 'rb') as fp:
        stimSeq = pickle.load(fp)



#%% =============================================================================
#stim settings
runSeq =  blockSeq[runNr-1] #sequence of blocks within the current run


faceNames = []
maskNames = []
for times in range(nUniBlocks):
    if times < 9:
        name = 'nf0' + str(times+1)
    else:
        name = 'nf' + str(times+1)
    
    stimSpecNoise = glob.glob(os.path.join(stimPath ,name + '*Stim*.bmp'))
    maskSpecNoise = glob.glob(os.path.join(stimPath, name + '*Mask*.bmp'))
    faceNames.append(stimSpecNoise)
    maskNames.append(maskSpecNoise)

noiseNames = glob.glob(os.path.join(noisePath, '*.bmp'))

#condition/block numbers, to make it more clear:
#			50		83.3	100	    150
#int		1		4		7		10
#neg		2		5		8		11
#scr		3		6		9		12

allTrialsOrder = []
stimPos = list(range(nPositions)) #possible positions within a block
blockPos = 1

#creating a trials order for all 

for blockNr in runSeq: #loop through blocks in specific run
    trials = stimSeq[blockNr] #get specific stim order for this block
    trialNumber = 0
    #select the correct noise frame
    noiseType = noiseSeq[blockNr][int(blockCount[blockNr])]
    if noiseType < 9:
        noiseName = 'nf0' + str(noiseType+1)
    else:
        noiseName = 'nf' + str(noiseType+1)
    noise = [i for i in noiseNames if (noiseName + '.bmp') in i]
    blockFaceNames = faceNames[noiseType]
    blockMaskNames = maskNames[noiseType]
    
    for position in stimPos: #if position contains no stims, no im/mask/trailnr 
        image = None 
        mask = None
        trialNr = None
        condiName = None
        #if there is a trial for the specific position, give it correct timing info
        if any(map((lambda value: value == blockNr), (0,1,2))):
            stimFr = 3
            duration = '50ms'
        elif any(map((lambda value: value == blockNr), (3,4,5))):
            stimFr = 5
            duration = '83.33ms'
        elif any(map((lambda value: value == blockNr), (6,7,8))):
            stimFr = 6
            duration = '100ms'
        else:
            stimFr = 9
            duration = '150ms'
        if any(map((lambda value: value == blockNr), (0,3,6,9))): #intact stim
            trType = 0
        elif any(map((lambda value: value == blockNr), (1,4,7,10))): #neg stim
            trType = 20
        else:
            trType = 40    
        if position in trials:
            index = np.where(trials == position)
            image = blockFaceNames[index[0][0]+trType][-18:]
            mask = blockMaskNames[index[0][0]+trType][-18:]
            trialNumber += 1
            trialNr  = trialNumber
            condiName = image[0:3] + '_' + duration
        allTrialsOrder.append({'blockNr' : blockNr+1,
                               'posInRun': blockPos,
                               'posInBlock' : position+1,
                               'trialNr': trialNr,
                               'condName': condiName,
                               'stimFrames': stimFr,
                               'imageName': image,
                               'maskName': mask,
                               'noiseFrame': noise[0][-8:],
                               'nrOfBlockOccurenceInExp': blockCount[blockNr]})
    blockPos += 1
    blockCount[blockNr] += 1

# pickle the noise sequence and stim sequence file
with open(logLocationNoiseSeq, 'wb') as fp:
    pickle.dump(noiseSeq, fp)
with open(logLocationBlockCount, 'wb') as fp:
    pickle.dump(blockCount, fp)    
with open(logLocationStimSeq, 'wb') as fp:
    pickle.dump(stimSeq, fp)


trialsReady = data.TrialHandler(allTrialsOrder, nReps=1, method='sequential',
                                originPath=stimPath)

#%% =============================================================================
#window setup
scrsize = (1920,1080)

win = visual.Window(size=scrsize, color='grey', units='pix', fullscr=True)
#win.close()

frameRate = win.getActualFrameRate(nIdentical=60, nMaxFrames=100,
    nWarmUpFrames=10, threshold=1)
print(frameRate)

#cra
instruc01 = 'These are instructions\n\nPress a button to continue (1 -> buttonbox key)'
instruc01 = visual.TextStim(win, text=instruc01)
instruc02 = 'The experiment is about to start!\n\n(press 5)'
instruc02 = visual.TextStim(win, text=instruc02)

fix1=visual.Line(win,start=(-scrsize[0],-scrsize[1]),end=(scrsize[0],
                scrsize[1]),pos=(0.0, 0.0),lineWidth=1.0,lineColor='blue',
                units='pix')
fix2=visual.Line(win,start=(-scrsize[0],scrsize[1]),end=(scrsize[0],
                -scrsize[1]),pos=(0.0, 0.0),lineWidth=1.0,lineColor='blue',
                units='pix')

instruc01.draw()
win.flip()
while not '1' in event.getKeys():
    core.wait(0.1)

instruc02.draw()
win.flip()
while not '5' in event.getKeys():
    core.wait(0.1)
    
# =============================================================================

# start stopwatch clock
clock = core.Clock()
clock.reset()

expt_time_elapsed = clock.getTime()
calc_baseline = fixStEn - expt_time_elapsed


# =============================================================================
# clear any previous presses/escapes
last_response = ''; response_time = ''

esc() # in case we need to shut down the expt

# =============================================================================
trialCount = 1
fr2 = 10
trNum = 0
#for nFrames in range(720): #12sec
fix1.setAutoDraw(True)
fix2.setAutoDraw(True)
#logfile.write(f'Start, beginFixation, 0, {expt_time_elapsed}, {clock.getTime()}, NA, NA, NA\n')



#win.close()
for trial in trialsReady:
    startTrial = clock.getTime()
    if trialCount == 1 or trialCount % 30 == 1: #beginning fixation 
        win.flip()
        fixStart  = clock.getTime() #start tracking time trialCount =30
        stim1=[]
        stim2=[]
        stim3=[]
        fr1=[]
        fr3=[]
        check =[]
        #load images for the next block    
        for ii in range(nPositions):
            if allTrialsOrder[trNum]['trialNr'] == None: #if the trial doesnt contain a stimulus
                stim1.append([Image.open(os.path.join(noisePath, allTrialsOrder[trNum]['noiseFrame']))])
                stim2.append([Image.open(os.path.join(noisePath, allTrialsOrder[trNum]['noiseFrame']))])
                stim3.append([Image.open(os.path.join(noisePath, allTrialsOrder[trNum]['noiseFrame']))])
                fr1.append([5])
                fr3.append([5])
                check.append([allTrialsOrder[trNum]['trialNr']])
            else:
                stim1.append([Image.open(os.path.join(stimPath, allTrialsOrder[trNum]['imageName']))])
                stim2.append([Image.open(os.path.join(stimPath, allTrialsOrder[trNum]['maskName']))])
                stim3.append([Image.open(os.path.join(noisePath, allTrialsOrder[trNum]['noiseFrame']))])
                check.append([trial['trialNr']])
                if allTrialsOrder[trNum]['stimFrames'] == 3: #it can be 3, 5, 6 or 9
                    fr1.append([3])
                    fr3.append([7])
                elif allTrialsOrder[trNum]['stimFrames'] == 5: #it can be 3, 5, 6 or 9
                    fr1.append([5])
                    fr3.append([5])
                elif allTrialsOrder[trNum]['stimFrames'] == 6: #it can be 3, 5, 6 or 9
                    fr1.append([6])
                    fr3.append([4])
                else: # frames = 9
                    fr1.append([9])
                    fr3.append([1])
            trNum += 1
        #if clock hits the fixation time for start/end in seconds, end the fixation
        loadEnd = clock.getTime()
        loadTime = loadEnd-fixStart
        x=1
        if trialCount == 1:
            while x==1: 
                fixNow = clock.getTime()
                timeFix = fixNow-fixStart
                if timeFix > (fixStEn-5): # time to fixate more then 7 seconds? end
                    x=2
                    print('fixtime=',timeFix)
                    print('loadtime=',loadTime)
        else:
            while x==1: 
                fixNow = clock.getTime()   
                timeFix = fixNow-fixStart
                if timeFix > 5: # time to fixate more then 5 seconds? end
                    x=2
                    print('fixtime=',timeFix)
                    print('loadtime=',loadTime)
#        for nFrames in range(300): # 5
#            win.flip()

    #loading the actual image (using SimpleImageStim to save a lot of loading time)
    bitmap1 = visual.SimpleImageStim(win=win, image=stim1[trial['posInBlock']-1][0])
    bitmap2 = visual.SimpleImageStim(win=win, image=stim2[trial['posInBlock']-1][0])
    bitmap3 = visual.SimpleImageStim(win=win, image=stim3[trial['posInBlock']-1][0])
    
    doneLoading = clock.getTime()
    for nFrames in range(fr1[trial['posInBlock']-1][0]):
        bitmap1.draw()
        win.flip()
    for nFrames in range(fr2):
        bitmap2.draw() 
        win.flip()        
    for nFrames in range(fr3[trial['posInBlock']-1][0]):
        bitmap3.draw()
        win.flip()

    esc() # in case we need to shut down the expt
    endTrial = clock.getTime()
    print('block:', int(trial['blockNr']),', trial', int(trialCount),
          ', load time: ', int((doneLoading-startTrial)*1000),
          'ms, trial itself:', int((endTrial-doneLoading)*1000), 'ms')
        
    trialCount  += 1

for nFrames in range(60*fixStEn): # 12 sec --> end fixation*refreshrate
    win.flip()
# =============================================================================

esc() # in case we need to shut down the expt

# =============================================================================




