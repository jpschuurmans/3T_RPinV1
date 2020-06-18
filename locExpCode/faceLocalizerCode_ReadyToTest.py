#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Block design
Created on Tue Jan 28 14:22:20 2020
@author: jschuurmans
"""
#%% =============================================================================
# imports

from psychopy import visual, event, core, gui, data
import os  
import numpy.random as rnd          # for random number generators
import glob
import numpy as np
import random
import copy

#%% =============================================================================
# Experimental settings for 1 run

nStim = 20 #number of unique stimuli per condition

nCond = 6 # nr of total conditions
conditions = list(range(1,nCond+1))
nBlocks = 6 # nr of blocks per condition

blockDur = 10 # Duration of block in sec
fixDur = 10 # Duration of fixation in sec (fix after every block)
fixStEn = 12 # Duration of fixation at begin/end of run in ms

trPerBlock = 10 #nr of trials per block

trialDur = 0.5 # Durations of trials defined in ms
isi = 0.5 #duration of inter stimulus 

#%% =============================================================================
# paths
stimPath = 'stimuli'
dataPath = 'data' # Where to write away the log file

#commented out, this is just for testing in Spyder
#stimPath = 'C:\\Users\\jolien\\Documents\\3T_RPinV1\\LocExp_ToTest\\stimuli'
#dataPath = 'C:\\Users\\jolien\\Documents\\3T_RPinV1\\LocExp_ToTest\\data'



#%% =============================================================================
# in case we need to shut down the expt

def esc():
    if 'escape' in last_response:
        logfile.close()
        win.close()
        core.quit


#%% =============================================================================
# Store info about the experiment session
        
# Get subject name, gender, age, handedness through a dialog box
expName = 'Recurrent face processing in V1'
expInfo = {
        'Participant ID': '',
        'Run number': ('1','2'),
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

logfile = open(dataFname, 'w')
logfile.write('BlockNumber, TrialNumber, StimulusType, ImageName, StimOnset, StimOffset, CatchTrial, Response, ResponseTime \n')


#%% =============================================================================
# create stimuli

#get all stimuli from the folder
stimPathList = glob.glob(os.path.join(stimPath,'*.bmp'))

#Check if all images exist
if not len(stimPathList) == (nStim*nCond):
    raise Exception('Images not complete')

#the extention of the used images is:
item01 =stimPathList[1]
imExt = item01[-4:]
lenStimName = len(item01[len(stimPath)+1:])

#create a list with the stimulus names
stimName=[]
for image in stimPathList:
    stimName.append(image[-lenStimName:])
stimName.sort()

#split list for all conditions
w=0
v=0
condList=[]
for unit in conditions:
    sliceStimList = slice(w,w+nStim,1) 
    stimListThisCon = stimName[sliceStimList]
    w += nStim
        
    #shuffle +append shuffeled. softcoded, but should be now: 3 times
    #(6 blocks per cond, 10 trials per block, and 20 unique stimuli in total --> 20*3)
    repTimes = int((nBlocks*trPerBlock)/nStim)
    shufStimList = []
    for shuff in range(repTimes):
        rnd.shuffle(stimListThisCon)
        toAdd = list(stimListThisCon)
        shufStimList.extend(toAdd)
    
    #splitting the 60 trials (nBlocks*trPerBlock) in 6 blocks (nBlock),
    u=0
    for num in list(range(1,nBlocks+1)):
        sliceTrials = slice(u,u+10,1)
        trialsCurrCon = shufStimList[sliceTrials]
        condList.append(trialsCurrCon)
        u += 10
        v += 1


#make a list for the nr of blocks
blockList = conditions*nBlocks
#shuffle this list
rnd.shuffle(blockList)
# list of block order
x=0
i=1
for times in conditions:
    for num in list(range(0,nBlocks)):
        t = blockList.index(i)
        blockList[t] = x
        x += 1
    i += 1


#make 1 big dictionary list
#append10 trials per condition in the order of the shuffled conditon list.
#et voila, un list des trials

r=0
s=1
allTrialsOrder = []
for blocks in blockList:
    blockNr = blockList[r]
    trials = condList[blockNr]
    q=0
    
    # decide which trials will be catch trials
    # 2 per block, one in first half other in second half
    catchList = list(np.zeros(int(trPerBlock/2)))
    catchList[0]=1
    random.shuffle(catchList)
    toAdd = copy.deepcopy(catchList)
    random.shuffle(toAdd)
    catchList.extend(toAdd)
    
    for amoun in trials:
        currTrial = trials[q]
        allTrialsOrder.append({'blockNr' : r+1,
                               'trialNr': s,
                               'condName': currTrial[0:8],
                               'imageName': currTrial,
                               'catchTrial': catchList[q]})
        q += 1
        s += 1
    r += 1
        

trialsReady = data.TrialHandler(allTrialsOrder, nReps=1, method='sequential',
                                originPath=stimPath)

#%% =============================================================================

scrsize = (1920,1080)

win = visual.Window(size=scrsize, color='grey', units='pix', fullscr=True) 
frameRate = win.getActualFrameRate()
print('framerate is' , frameRate)
bitmap = visual.ImageStim(win, size=[800,600])
#win.close()

instruct1 = 'During the experiment you\'ll see images appearing on the screen. \nPress a button as soon as you see the colour of the image change.\n\nIt is important to fixate on the fixation dot in the middle of the screen.\n\nPress a button to continue.. (buttonbox key = 1)'
instruct1 = visual.TextStim(win, height=32, text=instruct1)
instruct2 = 'The experiment is about to start!\nWaiting for scanner..\n(trigger = 5)'
instruct2 = visual.TextStim(win, height=32, text=instruct2)
   
fix = visual.TextStim(win, text='+', font='Arial', pos=(0, 0), height=50, color='black')

instruct1.draw()
win.flip()
while not '1' in event.getKeys():
    core.wait(0.1)

instruct2.draw()
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

fix.setAutoDraw(True)

for nFrames in range(720): #12sec
    win.flip()
logfile.write(f'StartFix, NA, StartFix, fix, {expt_time_elapsed}, {clock.getTime()}, NA, NA, NA\n')

trialCount = 1
trialInBlock = 0
totCaught = 0

for trial in trialsReady:
    trialOnsetTime = clock.getTime()
    stimFrame = os.path.join(stimPath, trial['imageName'])
    bitmap.setImage(stimFrame)
    if trial['catchTrial'] == True:
        bitmap.color = (0, 1.0, 1.0)
    else:
        bitmap.color = (1.0, 1.0, 1.0)   
    bitmap.size=(500,500)
# =============================================================================

    esc() # in case we need to shut down the expt

# =============================================================================
    for nFrames in range(30): #500ms trail
        bitmap.draw()
        win.flip()            
    
    # get response and it's associated timestamp as a list of tuples: (keypress, time)
    response = event.getKeys(timeStamped=clock)
    caught = 1
    
    if not response:
        response = [('No_Response', -1)]
        caught = 0
        
    if trial['catchTrial'] == True and caught == True:
        totCaught += 1
        print('click!')
        
    last_response = response[-1][0] # most recent response, first in tuple
    response_time = response[-1][1] # most recent response, second in tuple

    condition = trial['condName']; whichBlock = trial['blockNr']; imName = trial['imageName']; catTrial = trial['catchTrial']
    logfile.write(f'{whichBlock},{trialCount},{condition},{imName},{trialOnsetTime}, {clock.getTime()},{catTrial}, {last_response}, {response_time}\n')
    print('trial: ', trialCount, ', trial type: ', condition)
    if trialCount % 10 == 0:
        trialOnsetTime = clock.getTime()

        for nFrames in range(600): #2/5/8sec
            win.flip()

        condition = trial['condName']
        whichBlock = trial['blockNr']
        logfile.write(f'Fixation, NA, Fixation, fix, {trialOnsetTime}, {clock.getTime()}, {last_response}, {response_time}\n')

    else:
        trialInBlock += 1
        
    trialCount  += 1

endExpTime = clock.getTime()
for nFrames in range(720): #12sec
    fix.draw()
    win.flip()
logfile.write(f'EndFixation, NA, EndFixation, fix, {endExpTime}, {clock.getTime()}, {last_response}, {response_time}\n')
fix.setAutoDraw(False)

maxCat = (len(allTrialsOrder)/trPerBlock)*2
endScore = (100/maxCat)*maxCat
logfile.write(f'{endScore} percent of colour changes detected')


instruct3 = 'Done, you\'ve detected ' + str(endScore) +'% of the colour changes, thanks!\n'
instruct3 = visual.TextStim(win, text=instruct2)

instruct3.draw()
win.flip()
while not '1' in event.getKeys():
    core.wait(0.1)
# Quit the experiment (closing the window)
logfile.close()
win.close()
core.quit
