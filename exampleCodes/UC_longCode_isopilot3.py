
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 13:21:27 2020

@author: umut
"""

#===============
# Import modules
#===============
import os                    
import numpy as np
import numpy.matlib as npm          # for file/folder operations
import numpy.random as rnd          # for random number generators
import operator
from psychopy import visual, event, core, gui, data

# lower than 50 change color check
# 3 sessions check
# training is equal number of same and different within each block. check
# remind them the keys at the end of every block check

#==============================================
# Settings that we might want to tweak later on
#==============================================
    
datapath = 'Pilotdata'                   # directory to save data in
piloteyepath = 'Eyes_pilot'
instpath= 'InstScr'


# Each spectrum has either 5 different pairs:
# 15-30, 30-45, 45-60, 60-75, 75-90

# or 15 different pairs:
# 15-30, 30-45, 45-60, 60-75, 75-90
# 15-45, 30-60, 45-75, 60-90
# 15-60, 30,75, 45-90
# 15-75, 30,90
# 15-90

# Or different pairs, each crossing boundary
# 45-60
# 35-65
# 30-75
# 35-95, 05-65
# 20-95, 05-80
# 05-95


pairs1=['15-30','30-45','45-60','60-75','75-90']
pairs2=['15-30','30-45','40-55','45-60','60-75','75-90']

pairs = pairs1 # pairs2 isn't ready yet.

piloteyes = ['153_152' ,'215_126','217_33','150_213','58_142','222_139','197_135','103_192',
           '216_220','111_129','37_94','131_41','208_20','65_13','225_128','96_30', '100_125','123_44','90_17','38_9','52_145','148_66','140_143','57_45',
             '160_24','76_2','93_8','46_53','151_49','87_146','25_7','147_55']
repetition=1

explength=len(pairs)*len(piloteyes)*repetition*2 # 2 in the end is for the same amount of "same response" trials


tilt =[0,1]
imside=[0,1]
pilotlist=[]
pilotmorphs = ['15','30','45','60','75','90']
pilotmorphs2= ['15','30','40','45','55','60','75','90']
imlistwom = []
imlistmen = []                       # image names without the suffixes
asfx = '.png'                      # suffix for the first image 
scrsize = (800,800)                # screen size in pixels
timelimit = 3           # image freezing time in seconds
IBW=0 #the wait between the blocks
#ISI = [.7, .8, .9, 1, 1.1, 1.2]
ISI=[.01, .02]
blocksize=10

#========================================
# Store info about the experiment session
#========================================
    
# Get subject name, gender, age, handedness through a dialog box
exp_name = 'Isolated Eyes Pilot'
exp_info = {
        'participant': '',
        'gender': ('male', 'female'),
        'age':'',
        'left-handed':False,
        'session': ('1','2','3','all')
        }

session = exp_info['session']
dlg = gui.DlgFromDict(dictionary=exp_info, title=exp_name)
    
# If 'Cancel' is pressed, quit
if dlg.OK == False:
    core.quit()
        
# Get date and time
exp_info['date'] = data.getDateStr()
exp_info['exp_name'] = exp_name
    
# Create a unique filename for the experiment data
if not os.path.isdir(datapath):
    os.makedirs(datapath)
data_fname = exp_info['participant'] + '_' + exp_info['date']
data_fname = os.path.join(datapath, data_fname)
    
    #========================
    # Prepare condition lists
    #========================
    
#Check if all images exist
for eyes in piloteyes:
    for morph in pilotmorphs:
        if not os.path.exists(os.path.join(piloteyepath, eyes+'-'+morph+asfx)):
            raise Exception('Image files not found in image folder: ' + str(eyes+'-'+morph+asfx))           
    
   
    
    # Open a window
win = visual.Window(size=scrsize, color='grey', units='pix', fullscr=False)

bitmapinst = visual.ImageStim(win, size=scrsize)
    # Define trial start text

empty_scr = visual.TextStim(win,
                            text="Por.",
                                    color='black', height=20)
    # Define bitmap stimulus (contents can still change)
bitmap1 = visual.ImageStim(win, size=[284,332])
bitmap2 = visual.ImageStim(win, size=[284,332])
bitmap3 = visual.ImageStim(win, size=[284,332])
bitmap4 = visual.ImageStim(win, size=[284,332])
bitmap5 = visual.ImageStim(win, size=[284,332])
bitmap6 = visual.ImageStim(win, size=[284,332])
bitmap7 = visual.ImageStim(win, size=[284,332])
bitmap8 = visual.ImageStim(win, size=[284,332])
bitmap9 = visual.ImageStim(win, size=[284,332])
bitmap10 = visual.ImageStim(win, size=[284,332])
bitmap11 = visual.ImageStim(win, size=[284,332])
bitmap12 = visual.ImageStim(win, size=[284,332])
bitmap13 = visual.ImageStim(win, size=[284,332])
bitmap14 = visual.ImageStim(win, size=[284,332])
bitmap15 = visual.ImageStim(win, size=[284,332])
bitmap16 = visual.ImageStim(win, size=[284,332])

    
    #==========================
    # Define the trial sequence
    #==========================
    
    # Define a list of trials with their properties:
    #   - Which image (without the suffix)
    #   - Which orientation
stim_order = []
    
i=0
pilotdiff=[]
pilotsame=[]    

if len(pairs) <=5:
    morph1=npm.repmat((15, 30, 45, 60, 75),1,len(piloteyes))
    morph2=npm.repmat((30, 45, 60, 75, 90),1,len(piloteyes))
    morph3=npm.repmat((15, 45, 60, 75, 90),1,len(piloteyes))
    rnd.shuffle(morph3)
    
    morph1=morph1[0][:]
    morph2=morph2[0][:]
    morph3=morph3[0][:]

    for eyes in piloteyes:
        for itr in np.arange(5):
            pilotdiff.append({'eyes': eyes, 'cond': 'diff', 'im1': str(eyes+'-'+str(morph1[i])+asfx), 'im2': str(eyes+'-'+str(morph2[i])+asfx), 'dissim': abs(morph1[i]-morph2[i])})
            pilotsame.append({'eyes': eyes, 'cond': 'same', 'im1': str(eyes+'-'+str(morph3[i])+asfx), 'im2': str(eyes+'-'+str(morph3[i])+asfx), 'dissim': abs(morph3[i]-morph3[i])})
            i=i+1
    
else:
    morph1=npm.repmat((15,30,40,45,60,75),1,len(piloteyes))
    morph2=npm.repmat((30,45,55,60,75,90),1,len(piloteyes))
    morph3=npm.repmat((15,30,40,45,55,60,75,90),1,int(len(piloteyes)*len(pairs)/len(pilotmorphs2)))
    rnd.shuffle(morph3)
    
    morph1=morph1[0][:]
    morph2=morph2[0][:]
    morph3=morph3[0][:]


    for eyes in piloteyes:
        for itr in np.arange(15):
            pilotdiff.append({'eyes': eyes, 'cond': 'diff', 'im1': str(eyes+'-'+str(morph1[i])+asfx), 'im2': str(eyes+'-'+str(morph2[i])+asfx), 'dissim': abs(morph1[i]-morph2[i])})
            pilotsame.append({'eyes': eyes, 'cond': 'same', 'im1': str(eyes+'-'+str(morph3[i])+asfx), 'im2': str(eyes+'-'+str(morph3[i])+asfx), 'dissim': abs(morph3[i]-morph3[i])})
            i=i+1

        #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
if len(pairs) >5:
    pilotdiff15=[]
    pilotdiff30=[]
    pilotdiff45=[]
    pilotdiff60=[]
    pilotdiff75=[]
    
    for j in np.arange(len(pilotdiff)):
        if pilotdiff[j]['dissim'] == 15:
            pilotdiff15.append(pilotdiff[j])
        elif pilotdiff[j]['dissim'] == 30:
            pilotdiff30.append(pilotdiff[j])
        elif pilotdiff[j]['dissim'] == 45:
            pilotdiff45.append(pilotdiff[j])
        elif pilotdiff[j]['dissim'] == 60:
            pilotdiff60.append(pilotdiff[j])
        elif pilotdiff[j]['dissim'] == 75:
            pilotdiff75.append(pilotdiff[j])

    rnd.shuffle(pilotdiff15)
    rnd.shuffle(pilotdiff30)
    rnd.shuffle(pilotdiff45)
    rnd.shuffle(pilotdiff60)
    rnd.shuffle(pilotdiff75)
    
rnd.shuffle(pilotdiff)
rnd.shuffle(pilotsame)

    
adr=0
pilottrials=[]

for itr in np.arange(repetition):
    for adder in np.arange(explength/10):
        if len(pairs) > 5:
            slcr=slice(adr*5,(adr*5)+5,1)
            
            pilottrials.append(pilotdiff15[adr])
            pilottrials.append(pilotdiff30[adr])
            pilottrials.append(pilotdiff45[adr])
            pilottrials.append(pilotdiff60[adr])
            pilottrials.append(pilotdiff75[adr])
            pilottrials.extend(pilotsame[slcr])
            
            adr=adr+1
        else:
            slcr=slice(adr*5,(adr*5)+5,1)
            pilottrials.extend(pilotdiff[slcr])
            pilottrials.extend(pilotsame[slcr])
        
            adr=adr+1


pilottrials.sort(key=operator.itemgetter('dissim'))

pilottrials1=[]
slcr=slice(0,int(len(pilottrials)/2),1)
pilottrials1.extend(pilottrials[slcr])

pilottrials2=[]
slcr2=slice(int(len(pilottrials)/2),len(pilottrials),1)
pilottrials2.extend(pilottrials[slcr2])

rnd.shuffle(pilottrials1)
rnd.shuffle(pilottrials2)

pilottrialsfin=[]
# This is where we take equal number of same and diff trials and put them in a 
# new list.

#taking 20 from each response (or half the blocksize)
for indx in np.arange(0,int(len(pilottrials)/2),int(blocksize/2)):
    slcr=slice(indx,indx+(int(blocksize/2)),1)
    pilottrialsfin.extend(pilottrials1[slcr])
    pilottrialsfin.extend(pilottrials2[slcr])

# shuffling the 40 within itself
pilottrialsfin2=[]
for indx in np.arange(0,len(pilottrialsfin),blocksize):
    slcr=slice(indx,indx+blocksize,1)
    pp=pilottrialsfin[slcr]
    rnd.shuffle(pp)
    pilottrialsfin2.extend(pp)
    

fintrials = pilottrialsfin2
pilotlast = data.TrialHandler(fintrials, nReps=1, method='sequential', originPath=datapath)



#=====================
# Start the experiment
#=====================

# Initialize two clocks:
#   - for image change time
#   - for response time
change_clock = core.Clock()
rt_clock = core.Clock()

trialCount=0
expAccTot=0
expAccBlock=0


for trial in pilotlast:
    trialCount=trialCount+1
    if trialCount == 1:
                ##Instruction Screen 1: Before starting, make sure to find ...
        expscrbgn_imname=os.path.join(instpath, 'expscrbgn.png')
        bitmapinst.setImage(expscrbgn_imname)
        bitmapinst.draw()
        
        win.flip()
        # Wait for a spacebar press to start the trial, or escape to quit
        keys = event.waitKeys()
        if 'escape' in keys:
            break
        keys = []
        event.clearEvents()
        
                
            # Set the images
    im1_fname = os.path.join(piloteyepath, trial['im1'])
    im2_fname = os.path.join(piloteyepath, trial['im2'])
                
    rnd.shuffle(imside)
    if imside[1] == 0:
        bitmap1.setImage(im1_fname)
        bitmap2.setImage(im2_fname)
    else:
        bitmap1.setImage(im2_fname)
        bitmap2.setImage(im1_fname)
                        
    rnd.shuffle(tilt)
    if tilt[1] == 0:
        bitmap1.pos=(-284,10) #142+284/2
        bitmap2.pos=(284,0)
    else:
        bitmap1.pos=(-284,0) #142+284/2
        bitmap2.pos=(284,10)
                                
    bitmap1.size=(284,332)
    bitmap2.size=(284,332)  
                                
    bitmap1.draw()
    bitmap2.draw()
    win.flip()
    change_clock.reset()
    rt_clock.reset()
                                
    # Wait until a response, or until time limit.
    keys = event.waitKeys(maxWait=timelimit, keyList=['s','l', 'escape'])
              
    # If a key is pressed, take the reaction time. If not, just remove the images from the screen    
    if keys:
        rt = rt_clock.getTime()
    bitmap1.clearTextures()
    bitmap2.clearTextures()
    win.flip()
                                    
        #At this point, there are still no keys pressed. So "if not keys" is definitely 
        #going to be processed.
        #After removing the images from the screen, still listening for a keypress. 
        #Record the reaction time if a key is pressed.
                                    
    if not keys:
        keys = event.waitKeys(keyList=['s','l','escape'])
        rt = rt_clock.getTime()
                                        
        #If the key is pressed analyze the keypress.
    acc = 0
    if keys:
        if 'escape' in keys:
            break
        elif 's' in keys and trial['dissim'] == 0: # is same
            acc = 1
        elif 'l' in keys and not trial['dissim'] == 0: # is different
            acc = 1
    
    #samecount=0
    #if trial['dissim'] == 0:
        #print('same')
        #samecount=samecount+1
        #print(samecount)
                                                    
    expAccTot=expAccTot+acc
    expAccBlock=expAccBlock+acc
    #print(expAccBlock)
    #print(trialCount)
    blockPerc=expAccBlock/blocksize*100                     
    #print(blockPerc)                   
    if trialCount%blocksize == 0 and blockPerc >=75:
        win.setColor('darkgreen')
        win.flip()
        expAcc_message1 = visual.TextStim(win,
                                              text="Your accuracy for this block was: %d%%. \n Press Space to continue. \n\n\n\n\n Press ""S"" for SAME, ""L"" for DIFFERENT." %blockPerc,
                                              color='black', height=20)
        expAcc_message1.draw()
        win.flip()
        expAccBlock=0
        blockPerc=0
        keys = event.waitKeys(keyList=['space', 'escape'])
        if 'escape' in keys:
            win.setColor(color = 'gray')
            win.flip()
            break
        elif 'space' in keys:
            keys = []
            event.clearEvents()
            win.setColor(color = 'gray')
            win.flip()
        core.wait(IBW)
    elif trialCount%blocksize == 0 and (blockPerc <75 and blockPerc >=50):
        win.setColor('darkblue')
        win.flip()
        expAcc_message2 = visual.TextStim(win,
                                              text="Your accuracy for this block was: %d%%. \n Please, take a rest and concentrate to be more accurate. \n\n Press Space to continue. \n\n\n\n\n Press ""S"" for SAME, ""L"" for DIFFERENT." %blockPerc,
                                              color='white', height=20)
        expAcc_message2.draw()
        win.flip()
        expAccBlock=0
        blockPerc=0
        keys = event.waitKeys(keyList=['space', 'escape'])
        if 'escape' in keys:
            win.setColor(color = 'gray')
            win.flip()
            break
        elif 'space' in keys:
            keys = []
            event.clearEvents()
            win.setColor(color = 'gray')
            win.flip()
        core.wait(IBW)
    elif trialCount%blocksize == 0 and (blockPerc <50) and not trialCount == explength:
        win.setColor('darkred')
        win.flip()
        expAcc_message2 = visual.TextStim(win,
                                              text="Your accuracy for this block was: %d%%. \n Please, take a rest and concentrate to be more accurate. \n\n Press Space to continue. \n\n\n\n\n Press ""S"" for SAME, ""L"" for DIFFERENT." %blockPerc,
                                              color='white', height=20)
        expAcc_message2.draw()
        win.flip()
        expAccBlock=0
        blockPerc=0
        keys = event.waitKeys(keyList=['space', 'escape'])
        if 'escape' in keys:
            win.setColor(color = 'gray')
            win.flip()
            break
        elif 'space' in keys:
            keys = []
            event.clearEvents()
            win.setColor(color = 'gray')
            win.flip()
        core.wait(IBW)
    elif trialCount == explength:
        totPerc=expAccTot/explength*100
        
        win.setColor(color = 'darkgreen')
        win.flip()
        expAcc_message3 = visual.TextStim(win,
                                                  text="Your accuracy for the experiment was: %d%%. \n Thank you for your participation!. \n\n Please call the experimenter." %totPerc,
                                                  color='black', height=20)
        expAcc_message3.draw()
        keys = event.waitKeys(keyList=['space','escape'])
        win.setColor(color = 'gray')
        win.flip()
                                                                                    
        if 'escape' in keys:
            win.setColor(color = 'gray')
            win.flip()
            break
        elif 'space' in keys:
            win.setColor(color = 'gray')
            win.flip()
            keys = []
            event.clearEvents()
        core.wait(IBW)
                # Add the current trial's data to the TrialHandler
    pilotlast.addData('rt', rt)
    pilotlast.addData('acc', acc)
    rnd.shuffle(ISI)
    core.wait(ISI[1])
    
                # Advance to the next trial

pilotlast.saveAsWideText(data_fname + 'Exp' + '.csv', delim=',')
# Quit the experiment
win.close()

