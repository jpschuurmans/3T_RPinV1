#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 17:33:27 2019

@author: petras
"""

from datetime import datetime
from psychopy import visual, core, data, event, logging, gui, info
from psychopy.constants import *  # things like STARTED, FINISHED
from scipy import io
import os  # handy system and path functions
import numpy as np
import time
import csv

## ================ Boring admin stuff ===============================
''' check paths, creates data folder and files, creates logfiles and
guis for participant descriptives and block codes. '''
## ===================================================================
# Ensure that relative paths start from the same directory as this script
#_thisDir = os.path.dirname(os.path.abspath(__file__))
_thisDir = "/home/jschuurmans/Documents/02_recurrentSF_3T/Kirstens_Code"  #remove before running script

os.chdir(_thisDir)

trialClock = core.Clock()
logging.setDefaultClock(trialClock)
logging.console.setLevel(logging.DATA)  #set back to debug, for the love of god plz

#Checks for data directory, if not, creates it. 
directory = 'data'
if not os.path.exists(directory):
    os.makedirs(directory)

# Store info about the experiment session
expName = 'iCOARSE_Main'  
expInfo = {'ID': u'', 'RunNr': u''}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False: core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp

logDat = logging.LogFile('ICoarse_' + expInfo['ID'] + "_" + expInfo['RunNr'] + "_" + data.getDateStr() + ".log",
    filemode='w',  # if you set this to 'a' it will append instead of overwriting
    level=logging.DEBUG)  # errors, data and warnings will be sent to this logfile


# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + 'data/%s_%s_%s' %(expInfo['ID'],expName,expInfo['RunNr'])


## ================General set up ===============================
''' finds the prepared positions, sets up the window and prepares the stim sequence'''
## ===================================================================
Posfilename = _thisDir + os.sep + 'data/%s' %(expInfo['ID'] + '_iCOARSE_position_Position.csv')

#change this for changing stimulus size
stimsize = [400,400]

# read the positions from Get_best_position
posX =0
posY = 0

with open(Posfilename, newline='') as csvfile:
    Positionreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for ThisPosition in Positionreader:
        posX = ThisPosition[0]
        posY = ThisPosition[1]


# set up the sequence and write it to log

BlockMatrix = io.loadmat(_thisDir + os.sep + "Seq_1run"+expInfo['RunNr'] +"_IntWarp_Coh_cond_size.mat")
BlockMatrix = BlockMatrix["run" + expInfo['RunNr']]

# Setup the Window
win = visual.Window(fullscr=True, screen=0, units='pix', allowGUI=True, allowStencil=True, 
    waitBlanking=False,monitor='testMonitor', color=[165,165,165], colorSpace='rgb255',blendMode='avg')#, useFBO=True )

FrameRate = win.getActualFrameRate()
logging.data('FrameRate: ' + str(FrameRate)) 

blankScr = visual.TextStim(win=win,text='')

## ================Actually start ===============================
''' from here on, timing matters!'''
## ===================================================================



message = visual.TextStim(win, pos=(0.0, -0.9), text='Wait for Kirsten to press the thing')
Fixation = visual.GratingStim(win, mask="gauss", color="red",texRes=256, 
           size=[40, 40], sf=[10, 0], ori = 0,pos=(posX,posY),units="pix", name='gabor1')
BarWidth = 10; 
LeftSquare = visual.Rect(win, size=[BarWidth*2,stimsize[1]*2], units="pix", color= 'black',pos=[int(posX) - 15 - ((stimsize[0]/2) + (BarWidth/2)) ,posY])
RightSquare = visual.Rect(win, size=[BarWidth*2,stimsize[1]*2], units="pix", color= 'black',pos=[int(posX) + 15 + ((stimsize[0]/2) + (BarWidth/2)) ,posY])

ConditionCounters = [0,0,0,0,0,0]
TaskBlocks = [np.random.randint(1,6),np.random.randint(1,6),np.random.randint(1,6),np.random.randint(1,6),np.random.randint(1,6),np.random.randint(1,6)];
CatchBlocks = [0,0,0,0,0,0]

for i in range(len(CatchBlocks)):
    while True:
        CatchBlocks[i] = np.random.randint(1,6)
        if CatchBlocks[i] != TaskBlocks[i]:
            break; 
print(TaskBlocks)
print(CatchBlocks)
TRCounter = 0; 
#scannercountdown

while True:
    message.draw()
    keys = event.getKeys(keyList = ['space'])
    if 'space' in keys:
        break
    win.flip()

while True:
    Fixation.draw()
    LeftSquare.draw()
    RightSquare.draw()
    win.flip()
    keys = event.getKeys(keyList = ['5'])
    if '5' in keys:
        TRCounter = TRCounter +1
        if TRCounter == 12:
            break

for Block in BlockMatrix:
    ImageSequence = []
    IntWarp = Block[0][0][0]
    Coherency = Block[1][0][0]
    Condition = Block[2][0][0]
    Size = Block[3][0][0]
    TRCounter = 0; 
    

    for x in range(4,len(Block)):
        FileString = Block[x][0][7:len(Block[x][0])]
        if IntWarp == 0:
            string1 = "W0"
        else:
            string1 = "W1"
        
        if Coherency==0:
            string2="D100"
        elif Coherency ==1:
            string2="D060"
        else:
            string2 = "D000"
        
        FileString = _thisDir + os.sep + "stim/"+ string1 +"_"+ string2 + FileString
        ImageSequence.append(FileString)

    StimCounter = 0
    TaskStim = np.random.randint(1,8)
    #actual Experiment
    for image in ImageSequence:
        LeftSquare.color = 'black'
        RightSquare.color = 'black'

        NextStimulus = visual.ImageStim(win=win, size=stimsize[1], image= image, mask = None, interpolate=True, ori=0,units="pix", pos=[posX, posY])
        #print(image)
        if (ConditionCounters[Condition-1] == TaskBlocks[Condition-1] and StimCounter ==TaskStim):
            LeftSquare.color = 'white'
            RightSquare.color = 'white'
            logging.data('####TargetTrial####')  #set back to logging.data DANGER!

        if (ConditionCounters[Condition-1] == CatchBlocks[Condition-1] and StimCounter==TaskStim):
            leftright = np.random.randint(1,2)
            if leftright == 1:
                LeftSquare.color = 'white'
            if leftright == 2:
                RightSquare.color= 'white'
            logging.data('####CatchTrial####')

        for nframes in range(12):
            LeftSquare.draw()
            RightSquare.draw()
            NextStimulus.draw()
            Fixation.draw()
            win.flip()
            if nframes ==1:
                logging.data("stimulus onset")
            keys = event.getKeys(keyList = ['space', 'escape'])
            if 'escape' in keys:
                win.close()

        for nframes in range(12):
            keys = event.getKeys(keyList = ['space', 'escape'])
            if 'escape' in keys:
                win.close()
            LeftSquare.draw()
            RightSquare.draw()
            Fixation.draw()
            win.flip()
        StimCounter = StimCounter +1
    ConditionCounters[Condition-1] = ConditionCounters[Condition-1] +1
    
    #ITI:
    for nFrames in range(690): #11.5 sec
        Fixation.draw()
        LeftSquare.draw()
        RightSquare.draw()
        win.flip()
    keys = []
   # while true:  #waits for next scanner rigger to make ITI a full 12 sec
   #     Fixation.draw()
   #     LeftSquare.draw()
   #     RightSquare.draw()
   #     win.flip()
   #     keys = event.getKeys(keyList = ['5'])
   #     if '5' in keys:
   #         break

for nFrames in range(720): #12 sec
    Fixation.draw()
    LeftSquare.draw()
    RightSquare.draw()
    win.flip()

print(ConditionCounters)
#write the log file
dataFile =  open(filename+'.csv', 'w')
dataFile.write('{},{},{},{}\n'.format(expName,expInfo,str(posX), str(posY)))
dataFile.write('test')

# close all the stuff and clean up
dataFile.close()
win.close()

core.quit()


