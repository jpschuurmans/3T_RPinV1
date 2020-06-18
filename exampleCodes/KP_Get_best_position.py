# -*- coding: utf-8 -*-
"""
Created on Mon Sept 30 2019
Script to find the optimal position to display images


@author: KP
"""
from psychopy import visual, core, data, event, logging, sound, gui, info
from psychopy.constants import *  # things like STARTED, FINISHED
import os  # handy system and path functions
import time

## ================ Boring admin stuff ===============================
''' check paths, creates data folder and files, creates logfiles and
guis for participant descriptives and block codes. '''
## ===================================================================
# Ensure that relative paths start from the same directory as this script
#_thisDir = os.path.dirname(os.path.abspath(__file__))
_thisDir = "/home/jschuurmans/Documents/02_recurrentSF_3T/Kirstens_Code"  #remove before running script
os.chdir(_thisDir)

#Checks for data directory, if not, creates it. 
directory = 'data'
if not os.path.exists(directory):
    os.makedirs(directory)

# Store info about the experiment session
expName = 'iCOARSE_position'  
expInfo = {'ID': u''}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False: core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['exp'] = 'Position'
# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + 'data/%s_%s_%s' %(expInfo['ID'],expName,expInfo['exp'])


# Setup the Window
win = visual.Window(size=(1024, 758), fullscr=True, screen=0, units='deg', allowGUI=True, allowStencil=True, 
    waitBlanking=False,monitor='testMonitor', color=[165,165,165], colorSpace='rgb255',blendMode='avg')#, useFBO=True )


blankScr = visual.TextStim(win=win,text='')

instr = visual.TextStim(win=win, ori=0, name='block_instr',
    text='Tell me where to move to image so you can see it comfortably at the center of your visual field', #press space to continue
    font='Calibri', units='deg',
    pos=[0, 0], height=0.9, wrapWidth=25,
    color='black', colorSpace='rgb', opacity=1,
    depth=0.0)


## ================ Begin the experiment ===============================
'''All the code that makes run the experiments starts here'''
## ============================================================================

instr.draw()
win.flip()
event.waitKeys(keyList = ['space'])

x = 0 # initial positions
y = 0

#change this for changing stimulus size
stimsize = [400,400]


# create just once, no need to specify a position yet:
square = visual.Rect(win, size=[stimsize[0]*2,stimsize[1]*2], units="pix", fillColor= 'blue')
Fixation = visual.GratingStim(win, mask="gauss", color="red",texRes=256, 
           size=[40, 40], sf=[10, 0], ori = 0,pos=(x,y),units="pix", name='gabor1')
while True: # draw stimulus
    
    k = event.getKeys()
    if k: # if there was an actual key pressed:
        if k[0] == 'left':
            x = x-10
            event.clearEvents()
        elif k[0] == 'right':
            x = x+10
            event.clearEvents()
        elif k[0] == 'up':
            y = y+10
            event.clearEvents()
        elif k[0] == 'down':
            y = y-10
            event.clearEvents()
        elif k[0] == 'q':
            break
    event.clearEvents()
    square.pos = [x, y] # directly update both x *and* y
    Fixation.pos =[x,y] 
    square.draw()
    Fixation.draw()

    win.flip() # make the drawn things visible

dataFile =  open(filename+'.csv', 'w')
dataFile.write('{},{}\n'.format(str(x), str(y)))
dataFile.close()
win.close()

core.quit()
