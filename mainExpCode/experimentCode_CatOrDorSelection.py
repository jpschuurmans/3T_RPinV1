#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Block design
Created on Tue Jan 28 14:22:20 2020
@author: jschuurmans
"""
#%% =============================================================================
# imports

from psychopy import visual, event, core, gui
import numpy as np


#%% =============================================================================

maskPathCAT = 'C:\\Users\\jolien\\Documents\\CAT.txt'
maskPathDOG = 'C:\\Users\\jolien\\Documents\\DOG.txt'

#%% =============================================================================
expName = 'Cats... or dogs?'
expInfo = {
        'Prefer cats or dogs?': ('cats','dogs')
        }

animal = expInfo['Prefer cats or dogs?']

if animal == 'cats':
    filename = maskPathCAT
else:
    filename = maskPathDOG
    

dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)

# If 'Cancel' is pressed, quit
if dlg.OK == False:
    core.quit()
        
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


win = visual.Window([800,600], color='grey', units='pix')
bitmap = visual.ImageStim(win, size=[800,600])



dotRL = visual.GratingStim(win, mask=myMask, color="green",texRes=256, 
           size=[150, 100], sf=[10, 0], ori = 0,pos=(0,0),units="pix",
           name='gabor1')
dotRU = visual.GratingStim(win, mask=myMask, color="red",texRes=256, 
           size=[150, 100], sf=[10, 0], ori = 0,pos=(0,0),units="pix",
           name='gabor1')
dotLU = visual.GratingStim(win, mask=myMask, color="blue",texRes=256, 
           size=[150, 100], sf=[10, 0], ori = 0,pos=(0,0),units="pix",
           name='gabor1')
dotLL = visual.GratingStim(win, mask=myMask, color="orange",texRes=256, 
           size=[150, 100], sf=[10, 0], ori = 0,pos=(0,0),units="pix",
           name='gabor1')

dotRL.draw()
win.flip()
while not '1' in event.getKeys():
    core.wait(0.1)

dotRU.draw()
win.flip()
while not '1' in event.getKeys():
    core.wait(0.1)

dotLL.draw()
win.flip()
while not '1' in event.getKeys():
    core.wait(0.1)

dotLU.draw()
win.flip()
while not '1' in event.getKeys():
    core.wait(0.1)    

win.close()
core.quit
