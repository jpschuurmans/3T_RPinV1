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
nUniBlocks = nBlockPerCond/2 #nr of unique blocks per condition = 11 (11 sequences to make)
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
#logfile.write('Trial_Number, Stimulus, StimCode, StimOnset, StimOffset, Response, ResponseTime \n') #################################edit what to log
# In allTrialOrder I have this info: 'blockNr, posInRun, posInBlock, trialNr, condName, stimFrames, imageName, maskName, noiseFrame1, noiseFrame2, noiseFrame3, noiseFrame4'

#%% =============================================================================
#make or load block order for participant
logLocationBlockSeq = os.path.join(dataPath, expInfo['Participant ID'] + 'blockSeq.txt')
logLocationblockCount = os.path.join(dataPath, expInfo['Participant ID'] + 'blockCount.txt')
logLocationStimSeq = os.path.join(dataPath, expInfo['Participant ID'] + 'StimSeq.txt')

runNr = int(expInfo['Run number'])

if runNr == 1: #make new block/stim sequences for first run
    
    sequenceAllCond = (list(range(nCond)))*2
    blockSeq = []

    for run in range(nRuns):
       random.shuffle(sequenceAllCond)
       toAdd = copy.deepcopy(sequenceAllCond)
       blockSeq.append(toAdd)

    with open(logLocationBlockSeq, 'wb') as fp:
        pickle.dump(blockSeq, fp)
        
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
    with open(logLocationblockCount, 'rb') as fp:
        blockCount = pickle.load(fp)
    with open(logLocationStimSeq, 'rb') as fp:
        stimSeq = pickle.load(fp)
    


#%% =============================================================================
#stim settings
runSeq =  blockSeq[runNr-1] #sequence of blocks within the current run


faceNames = glob.glob(os.path.join(stimPath, '*Stim*.bmp'))
maskNames = glob.glob(os.path.join(stimPath, '*Mask*.bmp'))
noiseNames = glob.glob(os.path.join(noisePath, '*.bmp'))
faceNames.sort()
maskNames.sort()
noiseNames.sort()


if not len(faceNames)+len(maskNames) == (nStim*len(typCond)*2):
    raise Exception('Images not complete')


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
    noise = 0 #noiseTrials start with 0 every block
    trialNumber = 0
    for position in stimPos: #if the position contains no stimulus, image/mask/trailnr dont exist
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
            image = faceNames[index[0][0]+trType][-13:]
            mask = maskNames[index[0][0]+trType][-13:]
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
                               'noiseFrame1': noiseNames[noise][-19:],
                               'noiseFrame2': noiseNames[noise+1][-19:],
                               'noiseFrame3': noiseNames[noise+2][-19:],
                               'noiseFrame4': noiseNames[noise+3][-19:]})
        noise += 4
    blockPos += 1
    blockCount[blockNr] += 1

# pickle the blockCount file
with open(logLocationblockCount, 'wb') as fp:
    pickle.dump(blockCount, fp)
with open(logLocationStimSeq, 'wb') as fp:
    pickle.dump(stimSeq, fp)


trialsReady = data.TrialHandler(allTrialsOrder, nReps=1, method='sequential',
                                originPath=stimPath)

#%% =============================================================================
#window setup
scrsize = (1920,1080)

win = visual.Window(size=scrsize, color='grey', units='pix', fullscr=True)
bitmap = visual.ImageStim(win, size=[400,400])
#win.close()

frameRate = win.getActualFrameRate()
print(frameRate)

instruc01 = 'These are instructions\n\nPress a button to continue (1 -> buttonbox key)'
instruc01 = visual.TextStim(win, text=instruc01)
instruc02 = 'The experiment is about to start!\n\n(press 5)'
instruc02 = visual.TextStim(win, text=instruc02)

fix1=visual.Line(win,start=(-scrsize[0],-scrsize[1]),end=(scrsize[0],scrsize[1]),pos=(0.0, 0.0),
                lineWidth=1.0,lineColor='blue',units='pix')
fix2=visual.Line(win,start=(-scrsize[0],scrsize[1]),end=(scrsize[0],-scrsize[1]),pos=(0.0, 0.0),
                lineWidth=1.0,lineColor='blue',units='pix')

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


#for nFrames in range(720): #12sec
fix1.setAutoDraw(True)
fix2.setAutoDraw(True)
for nFrames in range(60): # 1 sec
    win.flip()
#logfile.write(f'Start, beginFixation, 0, {expt_time_elapsed}, {clock.getTime()}, NA, NA, NA\n')

for trial in trialsReady:
    esc() # in case we need to shut down the expt
    if trial['trialNr'] == None:
        stim1 = Image.open(os.path.join(noisePath, trial['noiseFrame1']))
        fr1 = 3
        stim2 = Image.open(os.path.join(noisePath, trial['noiseFrame1']))
        fr2 = 2
        stim3 = Image.open(os.path.join(noisePath, trial['noiseFrame2']))
        fr3 = 3
        stim4 = Image.open(os.path.join(noisePath, trial['noiseFrame2']))
        fr4 = 2
        stim5 = Image.open(os.path.join(noisePath, trial['noiseFrame3']))
        fr5 =5
        stim6 = Image.open(os.path.join(noisePath, trial['noiseFrame4']))
        fr6 = 5
    else:
        facestim = Image.open(os.path.join(stimPath, trial['imageName']))
        maskstim = Image.open(os.path.join(stimPath, trial['maskName']))
        noisestim1 = Image.open(os.path.join(noisePath, trial['noiseFrame1']))
        noisestim2 = Image.open(os.path.join(noisePath, trial['noiseFrame2']))
        noisestim3 = Image.open(os.path.join(noisePath, trial['noiseFrame3']))
        noisestim4 = Image.open(os.path.join(noisePath, trial['noiseFrame4']))
        
        if trial['stimFrames'] == 3: #it can be 3, 5, 6 or 9
            stim1 = Image.blend(facestim, noisestim1, alpha=0.5)
            fr1 = 3
            stim2 = Image.blend(maskstim, noisestim1, alpha=0.5)
            fr2 = 2
            stim3 = Image.blend(maskstim, noisestim2, alpha=0.5)
            fr3 = 5
            stim4 = Image.blend(maskstim, noisestim3, alpha=0.5)
            fr4 = 3
            stim5 = noisestim3
            fr5 = 2
            stim6 = noisestim4
            fr6 = 5
        elif trial['stimFrames'] == 5: #it can be 3, 5, 6 or 9
            stim1 = Image.blend(facestim, noisestim1, alpha=0.5)
            fr1 = 3
            stim2 = stim1
            fr2 = 2
            stim3 = Image.blend(maskstim, noisestim2, alpha=0.5)
            fr3 = 5
            stim4 = Image.blend(maskstim, noisestim3, alpha=0.5)
            fr4 = 5
            stim5 = noisestim4
            fr5 = 2
            stim6 = noisestim4
            fr6 = 3
        elif trial['stimFrames'] == 6: #it can be 3, 5, 6 or 9
            stim1 = Image.blend(facestim, noisestim1, alpha=0.5)
            fr1 = 5
            stim2 = Image.blend(facestim, noisestim2, alpha=0.5)
            fr2 = 1
            stim3 = Image.blend(maskstim, noisestim2, alpha=0.5)
            fr3 = 4
            stim4 = Image.blend(maskstim, noisestim3, alpha=0.5)
            fr4 = 5
            stim5 = Image.blend(maskstim, noisestim4, alpha=0.5)
            fr5 = 1
            stim6 = noisestim4
            fr6 = 4
        else: # frames = 9
            stim1 = Image.blend(facestim, noisestim1, alpha=0.5)
            fr1 = 5
            stim2 = Image.blend(facestim, noisestim2, alpha=0.5)
            fr2 = 4
            stim3 = Image.blend(maskstim, noisestim2, alpha=0.5)
            fr3 = 1
            stim4 = Image.blend(maskstim, noisestim3, alpha=0.5)
            fr4 = 5
            stim5 = Image.blend(maskstim, noisestim4, alpha=0.5)
            fr5 = 4
            stim6 = noisestim4
            fr6 = 1            

    for nFrames in range(fr1):
        bitmap.setImage(stim1)
        bitmap.draw()
        win.flip()
    for nFrames in range(fr2):
        bitmap.setImage(stim2)
        bitmap.draw() 
        win.flip()        
    for nFrames in range(fr3):
        bitmap.setImage(stim3)
        bitmap.draw()
        win.flip()    
    for nFrames in range(fr4):
        bitmap.setImage(stim4)
        bitmap.draw()
        win.flip()
    for nFrames in range(fr5):
        bitmap.setImage(stim5)
        bitmap.draw()
        win.flip()
    for nFrames in range(fr6):
        bitmap.setImage(stim6)
        bitmap.draw()
        win.flip()
    esc() # in case we need to shut down the expt
        
        
#    trialOnsetTime = clock.getTime()
#    stimFrame = os.path.join(stimPath, trial['imageName'])
#    bitmap.setImage(stimFrame)
#    bitmap.size=(400,400)
# =============================================================================

esc() # in case we need to shut down the expt

# =============================================================================






################################################################################### untill here is works :)
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