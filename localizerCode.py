#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Block design
Created on Tue Jan 28 14:22:20 2020
@author: jschuurmans
"""
#%% =============================================================================
# imports

from psychopy import visual, event, core, gui, data, monitors
import os  
import numpy.matlib as npm          # for file/folder operations
import numpy.random as rnd          # for random number generators
import glob
import numpy as np
import random

#%% =============================================================================
# paths
stimPath =  (r'/home/jschuurmans/Documents/02_recurrentSF_3T/recurrentSF_3T_CodeRepo/exampleCodes/TestImages/')
#stimPath =  (r'C:\\Users\\jolien\\Documents\\3T_RPinV1\\TestImages\\')
exStimName = 'Con1_01_faInt.jpg' #an example of the stimulus name
lenStimName = len(exStimName)

maskPathCAT = '/home/jschuurmans/Documents/02_recurrentSF_3T/Stimuli/Cat'
maskPathDOG = '/home/jschuurmans/Documents/02_recurrentSF_3T/Stimuli/Dog'
# Where to write away the log file
dataPath = (r'/home/jschuurmans/Documents/02_recurrentSF_3T/recurrentSF_3T_CodeRepo/exampleCodes/TestData')
#dataPath = (r'C:\\Users\\jolien\\Documents\\3T_RPinV1\\TestData')
#%% =============================================================================
# Experimental settings for 1 run

nStim = 20 #number of unique stimuli per condition

nCond = 8 # nr of total conditions
conditions = list(range(1,nCond+1))
nBlocks = 4 # nr of blocks per condition


blockDur = 10 # Duration of block in sec
fixDur = 10 # Duration of fixation in sec (fix after every block)
fixStEn = 12 # Duration of fixation at begin/end of run in ms

trPerBlock = 10 #nr of trials per block

trialDur = 0.5 # Durations of trials defined in ms
isi = 0.5 #duration of inter stimulus 

scrsize = (1920,1080)

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
        'Run number': '',
        'Prefer cats or dogs?': ('cats','dogs')
        }

dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)

animal = expInfo['Prefer cats or dogs?']

if animal == 'cats':
    filename = maskPathCAT
else:
    filename = maskPathDOG
    

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
logfile.write('Trial_Number, Stimulus, StimCode, StimOnset, StimOffset, KittenPresent, Response, ResponseTime \n')



#%% =============================================================================
# create stimuli

#get all stimuli from the folder
stimPathList = glob.glob(str(stimPath +'*'))

#Check if all images exist
if not len(stimPathList) == (nStim*nCond):
    raise Exception('Images not complete')

#the extention of the used images is:
item01 =stimPathList[1]
imExt = item01[-4:]

#create a list with the stimulus names
z=0
stimName=[]
for image in stimPathList:
    y=stimPathList[z]
    stimName.append(y[-lenStimName:])
    z+=1
stimName.sort()

#split list for all conditions
w=0
v=0
condList=[]
for unit in conditions:
    sliceStimList = slice(w,w+20,1) 
    stimListThisCon = stimName[sliceStimList]
    w += 20
        
    #shuffle +append shuffeled double = 40 trials per condition in total
    rnd.shuffle(stimListThisCon)
    toAdd = list(stimListThisCon)
    rnd.shuffle(stimListThisCon)
    stimListThisCon.extend(toAdd)
    
    #splitting the 40 trials in 4, because 4 blocks of 10 trials per condition
    u=0
    for num in list(range(1,nBlocks+1)):
        sliceTrials = slice(u,u+10,1)
        trialsCurrCon = stimListThisCon[sliceTrials]
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
    for amoun in trials:
        currTrial = trials[q]
        allTrialsOrder.append({'blockNr' : r+1,
                               'trialNr': s,
                               'condNr' : currTrial[3:4],
                               'condName': currTrial[-9:-4],
                               'imageName': currTrial})
        q += 1
        s += 1
    r += 1
        

trialsReady = data.TrialHandler(allTrialsOrder, nReps=1, method='sequential',
                                originPath=stimPath)

#%% =============================================================================
#dot probe task preparation open the mask for the animals
text = []
with open(filename) as f:
    line = f.readline()
    cnt = 0
    while line:
        line = list(line)
        line = list(map(lambda x:-1 if x== '\n' else x,line))
        line = list(map(lambda x:-1 if x== '0' else x,line))
        line = list(map(lambda x:1 if x== '1' else x,line))
        

        text.append(line)

        line = f.readline()
        cnt += 1
myMask = np.array(text)


#win.close()
#there are 32 blocks, each block should show 4 stimlui (2 during block, 2 during fix)
#create list 
nrCatsPerBlock = [1]#how many cats per block?
nrCats = [1,2,3,4]
catTrials = list(np.zeros(trPerBlock-len(nrCatsPerBlock),dtype=int))
catTrials.extend(nrCatsPerBlock)
rnd.shuffle(catTrials)


win = visual.Window(size=scrsize, color='grey', units='pix', fullscr=True) 
#win = visual.Window([800,600], color='grey', units='pix')
frameRate = win.getActualFrameRate()
print(frameRate)
#bitmap = visual.ImageStim(win, size=scrsize) #fullscreen
bitmap = visual.ImageStim(win, size=[800,600])



insructions_to_subjects1 = 'During the experiment you\'ll see cats pop-up. \nPress a button as soon as you see a cat.\n\nIt is important to fixate on the fixation dot in the middle of the screen.\n\nPress a button to continue (1 -> buttonbox key)'
insructions_to_subjects1 = visual.TextStim(win, text=insructions_to_subjects1)
experimenter_message = 'The experiment is about to start!'
experimenter_message = visual.TextStim(win, text=experimenter_message)


   
fix = visual.GratingStim(win, mask="gauss", color="black",texRes=256, 
           size=[10, 10], sf=[10, 0], ori = 0,pos=(0,0),units="pix",
           name='gabor1')

dotRL = visual.GratingStim(win, mask=myMask, color="green",texRes=256, 
           size=[150, 100], sf=[10, 0], ori = 0,pos=(800,-400),units="pix",
           name='gabor1')
dotRU = visual.GratingStim(win, mask=myMask, color="red",texRes=256, 
           size=[150, 100], sf=[10, 0], ori = 0,pos=(800,400),units="pix",
           name='gabor1')
dotLU = visual.GratingStim(win, mask=myMask, color="blue",texRes=256, 
           size=[150, 100], sf=[10, 0], ori = 0,pos=(-800,400),units="pix",
           name='gabor1')
dotLL = visual.GratingStim(win, mask=myMask, color="orange",texRes=256, 
           size=[150, 100], sf=[10, 0], ori = 0,pos=(-800,-400),units="pix",
           name='gabor1')

#dotRL = visual.GratingStim(win, mask=myMask, color="green",texRes=256, 
#           size=[150, 100], sf=[10, 0], ori = 0,pos=(10,-10),units="pix",
#           name='gabor1')
#dotRU = visual.GratingStim(win, mask=myMask, color="red",texRes=256, 
#           size=[150, 100], sf=[10, 0], ori = 0,pos=(10,10),units="pix",
#           name='gabor1')
#dotLU = visual.GratingStim(win, mask=myMask, color="blue",texRes=256, 
#           size=[150, 100], sf=[10, 0], ori = 0,pos=(-10,-10),units="pix",
#           name='gabor1')
#dotLL = visual.GratingStim(win, mask=myMask, color="orange",texRes=256, 
#           size=[150, 100], sf=[10, 0], ori = 0,pos=(-10,10),units="pix",
#           name='gabor1')

Gone = visual.GratingStim(win, mask=myMask, color="orange",texRes=256, 
           size=[0, 0], sf=[10, 0], ori = 0,pos=(0,0),units="pix",
           name='gabor1')

insructions_to_subjects1.draw()
dotRL.draw()
dotRU.draw()
dotLL.draw()
dotLU.draw()
win.flip()
while not '1' in event.getKeys():
    core.wait(0.1)

experimenter_message.draw()
win.flip()
while not 'c' in event.getKeys():
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
for nFrames in range(60): # 1 sec
    fix.draw()
    win.flip()
logfile.write(f'Start, beginFixation, 0, {expt_time_elapsed}, {clock.getTime()}, NA, NA, NA\n')

trialCount = 1
trialInBlock = 0
kitty=0
totCaught = 0
catPosFix = [1,2,3]

for trial in trialsReady:
    trialOnsetTime = clock.getTime()
    stimFrame = os.path.join(stimPath, trial['imageName'])
    bitmap.setImage(stimFrame)
    bitmap.size=(400,400)
# =============================================================================

    esc() # in case we need to shut down the expt

# =============================================================================

    if catTrials[trialInBlock] == True:
        kitty = random.choice(nrCats)
    if kitty == 1:
        dot = dotRL
    elif kitty == 2:
        dot = dotRU
    elif kitty == 3:
        dot = dotLU
    elif kitty == 4:
        dot = dotLL
    else:
        dot = Gone
     
    for nFrames in range(15): #250ms with probe
        bitmap.draw()
        dot.draw()
        fix.draw()
        win.flip()            
    for nFrames in range(15): #250ms ms no probe
        bitmap.draw()
        fix.draw()
        win.flip()
    for nFrames in range(30): #500ms
        fix.draw()
        win.flip()
    
    # get response and it's associated timestamp as a list of tuples: (keypress, time)
    response = event.getKeys(timeStamped=True)
    caught = 1
    
    if not response:
        response = [('No_Response', -1)]
        caught = 0
        
    if catTrials[trialInBlock] == True and caught == True:
        totCaught += 1
        
    last_response = response[-1][0] # most recent response, first in tuple
    response_time = response[-1][1] # most recent response, second in tuple

    condition = trial['condName']
    whichBlock = trial['blockNr']
    logfile.write(f'{trialCount}, {condition}, {whichBlock}, {trialOnsetTime}, {clock.getTime()}, {kitty}, {last_response}, {response_time}\n')


    if trialCount % 10 == 0:
        trialOnsetTime = clock.getTime()
        kitty = random.choice(nrCats)
        if kitty == 1:
            dot = dotRL
        elif kitty == 2:
            dot = dotRU
        elif kitty == 3:
            dot = dotLU
        elif kitty == 4:
            dot = dotLL
        else:
            dot = Gone
        posOfCat = random.choice(catPosFix)
        if posOfCat == 1: #after 2seconds
            np1 = 120
            np2 = 465
        elif posOfCat == 2: #after 5 seconds
            np1 = 300
            np2 = 285
        else: # after 8 seconds
            np1 = 480
            np2 = 105

        for nFrames in range(np1): #2/5/8sec
            fix.draw()
            win.flip()
        for nFrames in range(15): #250ms probe
            dot.draw()
            fix.draw()
            win.flip()
        for nFrames in range(np2): #rest of fix
            fix.draw()
            win.flip() 

        response = event.getKeys(timeStamped=True)
        caught = 1
        
        if not response:
            response = [('No_Response', -1)]
            caught = 0

        last_response = response[-1][0] # most recent response, first in tuple
        response_time = response[-1][1] # most recent response, second in tuple

        condition = trial['condName']
        whichBlock = trial['blockNr']
        logfile.write(f'Fixation, NA, {whichBlock}, {trialOnsetTime}, {clock.getTime()}, {kitty}, {last_response}, {response_time},{posOfCat}\n')
    
        if caught == True:
            totCaught += 1
            
        trialInBlock = 0
        rnd.shuffle(catTrials)
    else:
        trialInBlock += 1
        
    trialCount  += 1
    kitty=0


endExpTime = clock.getTime()
#for nFrames in range(720): #12sec
for nFrames in range(60): # 1 sec
    fix.draw()
    win.flip()
logfile.write(f'End, EndFixation, 0, {endExpTime}, {clock.getTime()}, NA, NA, NA\n')

maxCat = 100/((len(allTrialsOrder)/trPerBlock)/2)
endScore = totCaught*maxCat
logfile.write(f'{endScore} percent of cats caught')
logfile.write(f'{frameRate} is the frame rate')



insructions_to_subjects2 = 'Done, you\'ve caught ' + str(endScore) +'% of the kitties, thanks!\n'
insructions_to_subjects2 = visual.TextStim(win, text=insructions_to_subjects2)

insructions_to_subjects2.draw()
dotRL.draw()
dotRU.draw()
dotLL.draw()
dotLU.draw()
win.flip()
while not '1' in event.getKeys():
    core.wait(0.1)
# Quit the experiment (closing the window)
logfile.close()
win.close()
core.quit


#%% =============================================================================

win = visual.Window(size=scrsize, color='grey', units='pix', fullscr=True)

fix = visual.GratingStim(win, mask="gauss", color="black",texRes=256, 
           size=[10, 10], sf=[10, 0], ori = 0,pos=(0,0),units="pix",
           name='gabor1')

frameRate = win.getActualFrameRate(nIdentical=60, nMaxFrames=100,
    nWarmUpFrames=10, threshold=1)
clock = core.Clock()
clock.reset()

#try stuff out 
stimDRAW = clock.getTime()
stimFrame1 = os.path.join(stimPath, 'con1_01_faInt.bmp')
bitmap1 = visual.ImageStim(win, size=[800,600])
bitmap1.setImage(stimFrame1)
bitmap1.size=(400,400)

startDRAW2 = clock.getTime()
stimFrame2 = os.path.join(stimPath, 'con2_01_faScr.bmp')
bitmap2 = visual.ImageStim(win, size=[800,600])
bitmap2.setImage(stimFrame2)
bitmap2.size=(400,400)


for nFrames in range(360): #6 sec
    fix.draw()
    win.flip()
    
startSTIM = clock.getTime()
for nFrames in range(3): #50ms
    bitmap1.draw()
    fix.draw()
    win.flip()

startMASK = clock.getTime()

for nFrames in range(10): #166ms
    bitmap2.draw()
    fix.draw()
    win.flip()
   
endMASK = clock.getTime()

for nFrames in range(30): #500ms
    fix.draw()
    win.flip()
    


makeSTIM = (startDRAW2 - stimDRAW) *1000
makeMASK = (startSTIM - startDRAW2) *1000
stimTIME = (startMASK - startSTIM) *1000
MASK = (endMASK - startMASK) *1000
wholeTHING = (endMASK - stimDRAW) *1000

print('drawing the stimulus took', int(makeSTIM), 'ms')
print('drawing the mask took', int(makeMASK), 'ms')

print('the actual stimulus took', int(stimTIME), 'ms')
print('the actual mask took', int(MASK), 'ms')


print('frame rate is', frameRate)
#msPerFrame = win.getMsPerFrame(nFrames=60)
#print(msPerFrame)