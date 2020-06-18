#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 19:15:29 2020

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
    
datapath = 'data'                   # directory to save data in
impathmen = 'imagesmen'
impathwom = 'imageswom'    
eyepathmen= 'eyesmen'
eyepathwom= 'eyeswom'             
pracpath = 'pracims'
praceyepath = 'praceyes'
instpath= 'InstScr'
exppath= 'expims'  # directory where images can be found

#This should be a multiplier of 48
explength = 1536 #This should be a multiplier of 96, preferably 384, 768 or 1536
explength2 = explength/2 #This is necessary later to create trials

sesslength = explength/3
praclength = 96
tottri= praclength/2
tilt =[0,1]
imside=[0,1]

mencxts1 = ['123','100','26','125','9','145','66','143','45','24','2','8','53','49','146','7']
mencxts2 = ['44','90','38','17','148','52','57','140','76','160','46','93','87','151','147','25']
meneyes=['100_125','123_44','90_17','38_9','52_145','148_66','140_143','57_45',
             '160_24','76_2','93_8','46_53','151_49','87_146','25_7','147_55']

womcxts1 = ['77','152','126','33','213','142','139','135','192','220','129','94','41','20','13','128']
womcxts2 = ['215','153','150','217','222','58','103','197','111','216','131','37','65','208','96','225']
womeyes = ['153_152','215_126','217_33','150_213','58_142','222_139','197_135','103_192',
           '216_220','111_129','37_94','131_41','208_20','65_13','225_128','96_30']
    
praccxt1= ['223','209','78','203','224','226']
praccxt2= ['21','154','214','37','31','106']
praceyes=['154_209','21_78','37_203','214_224','106_226','31_163']
morphs=['5','20','35','65','95']
   
praclist=[]
       
imlistwom = [] 
imlistmen = []                       # image names without the suffixes
asfx = '.png'                      # suffix for the first image
bsfx = '.png'                      # suffix for the second image
scrsize = (1920,1200)                # screen size in pixels
timelimit = 3           # image freezing time in seconds
IBW=0 #the wait between the blocks
#ISI = [.7, .8, .9, 1, 1.1, 1.2]
ISI=[.01, .02]

#========================================
# Store info about the experiment session
#========================================
    
# Get subject name, gender, age, handedness through a dialog box
exp_name = 'Discriminability and Congruency'
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
for cxt1, cxt2, eyes in zip(mencxts1, mencxts2,meneyes):
    for morph in morphs:
        if (not os.path.exists(os.path.join(impathmen, cxt1+'-'+eyes+'-'+morph+asfx)) or
            not os.path.exists(os.path.join(impathmen, cxt2+'-'+eyes+'-'+morph+asfx))):
            raise Exception('Image files not found in image folder: ' + str(cxt1+'-'+eyes+'-'+morph+asfx) + ' or ' + str(cxt2+'-'+eyes+'-'+morph+asfx))
        if not os.path.exists(os.path.join(eyepathmen, eyes+'-'+morph+asfx)):
            raise Exception('Image files not found in image folder: ' + str(eyes+'-'+morph+asfx))           
    
for cxt1, cxt2, eyes in zip(womcxts1, womcxts2,womeyes):
    for morph in morphs:
        if (not os.path.exists(os.path.join(impathwom, cxt1+'-'+eyes+'-'+morph+asfx)) or
            not os.path.exists(os.path.join(impathwom, cxt2+'-'+eyes+'-'+morph+asfx))):
            raise Exception('Image files not found in image folder: ' + str(cxt1+'-'+eyes+'-'+morph+asfx) + ' or ' + str(cxt2+'-'+eyes+'-'+morph+asfx))
        if not os.path.exists(os.path.join(eyepathwom, eyes+'-'+morph+asfx)):
            raise Exception('Image files not found in image folder: ' + str(eyes+'-'+morph+asfx))
            
for cxt1, cxt2, eyes in zip(praccxt1,praccxt2,praceyes):
    for morph in morphs:
        if (not os.path.exists(os.path.join(pracpath, cxt1+'-'+eyes+'-'+morph+asfx)) or
            not os.path.exists(os.path.join(pracpath, cxt2+'-'+eyes+'-'+morph+asfx)) or
            not os.path.exists(os.path.join(pracpath, eyes+'-'+morph+asfx))):
            raise Exception('Image file not found in image folder:' + str(cxt1+'-'+eyes+'-'+morph+asfx))
                
    
    
    # Randomize the image order
rnd.shuffle(imlistmen)
    
    
    # Open a window
win = visual.Window(size=scrsize, color='grey', units='pix', fullscr=True)

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
    
    
morph11=npm.repmat([20, 35, 65, 5],1,int(len(praceyes)/2))
morph12=npm.repmat([5, 65, 35, 95],1,int(len(praceyes)/2))
morph1=np.append(morph11,morph12)

morph21=npm.repmat([35, 65, 5, 95],1,int(len(praceyes)/2))
morph22=npm.repmat([20, 35, 95, 5],1,int(len(praceyes)/2))
morph2=np.append(morph21,morph22)
    
morph31=npm.repmat([20, 95, 65, 5],1,int(len(praceyes)/2))
morph32=npm.repmat([5, 65, 35, 20],1,int(len(praceyes)/2))
morph3=np.append(morph31,morph32)
    
morph41=[20, 95, 35, 5, 20, 95, 35, 65]
morph42=npm.repmat([95, 65, 35, 20],1,int(len(praceyes)-2))
morph4=np.append(morph41,morph42)
    
morph51=[20, 35, 65, 5, 20, 95, 65, 5]
morph52=npm.repmat([20, 5, 35, 95],1,int(len(praceyes)-2))
morph5=np.append(morph51,morph52)
    
i=0
pracdiffdiff = []
pracdiffsame=[]
pracsamediff=[]
pracsamesame=[]
pracisodiff=[]
pracisosame=[]
ori= [0,180]
for cxt1, cxt2, eyes in zip(praccxt1, praccxt2, praceyes):
    for itr in np.arange(4):
        pracdiffdiff.append({'cxt1': cxt1, 'cxt2': cxt2, 'eyes': eyes, 'cond': 'DD', 'im1': str(cxt1+'-'+eyes+'-'+str(morph1[i])+asfx), 'im2': str(cxt2+'-'+eyes+'-'+str(morph2[i])+asfx), 'dissim': abs(morph1[i]-morph2[i])})
        pracdiffsame.append({'cxt1': cxt1, 'cxt2': cxt2, 'eyes': eyes, 'cond': 'DS', 'im1': str(cxt1+'-'+eyes+'-'+str(morph3[i])+asfx), 'im2': str(cxt2+'-'+eyes+'-'+str(morph3[i])+asfx), 'dissim': abs(morph3[i]-morph3[i])})
        pracsamediff.append({'cxt1': cxt1, 'cxt2': cxt1, 'eyes': eyes, 'cond': 'SD', 'im1': str(cxt1+'-'+eyes+'-'+str(morph1[i])+asfx), 'im2': str(cxt1+'-'+eyes+'-'+str(morph2[i])+asfx), 'dissim': abs(morph1[i]-morph2[i])})
        pracsamesame.append({'cxt1': cxt1, 'cxt2': cxt1, 'eyes': eyes, 'cond': 'SS', 'im1': str(cxt1+'-'+eyes+'-'+str(morph4[i])+asfx), 'im2': str(cxt2+'-'+eyes+'-'+str(morph4[i])+asfx), 'dissim': abs(morph4[i]-morph4[i])})
        pracisodiff.append({'cxt1': '0', 'cxt2': '0', 'eyes': eyes, 'cond': 'ISOD', 'im1': str(eyes+'-'+str(morph1[i])+asfx), 'im2': str(eyes+'-'+str(morph2[i])+asfx), 'dissim': abs(morph1[i]-morph2[i])})
        pracisosame.append({'cxt1': '0', 'cxt2': '0', 'eyes': eyes, 'cond': 'ISOS', 'im1': str(eyes+'-'+str(morph5[i])+asfx), 'im2': str(eyes+'-'+str(morph5[i])+asfx), 'dissim': abs(morph5[i]-morph5[i])})
        i=i+1
    
pddmat15=[]
pddmat30=[]
pddmat60=[]
pddmat90=[]
psdmat15=[]
psdmat30=[]
psdmat60=[]
psdmat90=[]
pisodmat15=[]
pisodmat30=[]
pisodmat60=[]
pisodmat90=[]
    
for j in np.arange(len(pracdiffdiff)):
    if pracdiffdiff[j]['dissim'] == 15:
        pddmat15.append(pracdiffdiff[j])
    elif pracdiffdiff[j]['dissim'] == 30:
        pddmat30.append(pracdiffdiff[j])
    elif pracdiffdiff[j]['dissim'] == 60:
        pddmat60.append(pracdiffdiff[j])
    elif pracdiffdiff[j]['dissim'] == 90:
        pddmat90.append(pracdiffdiff[j])
            
for j in np.arange(len(pracsamediff)):
    if pracsamediff[j]['dissim'] == 15:
        psdmat15.append(pracsamediff[j])
    elif pracsamediff[j]['dissim'] == 30:
        psdmat30.append(pracsamediff[j])
    elif pracsamediff[j]['dissim'] == 60:
        psdmat60.append(pracsamediff[j])
    elif pracsamediff[j]['dissim'] == 90:
        psdmat90.append(pracsamediff[j])
            
for j in np.arange(len(pracisodiff)):
    if pracisodiff[j]['dissim'] == 15:
        pisodmat15.append(pracisodiff[j])
    elif pracisodiff[j]['dissim'] == 30:
        pisodmat30.append(pracisodiff[j])
    elif pracisodiff[j]['dissim'] == 60:
        pisodmat60.append(pracisodiff[j])
    elif pracisodiff[j]['dissim'] == 90:
        pisodmat90.append(pracisodiff[j])
            
rnd.shuffle(pddmat15)
rnd.shuffle(pddmat30)
rnd.shuffle(pddmat60)
rnd.shuffle(pddmat90)
rnd.shuffle(psdmat15)
rnd.shuffle(psdmat30)
rnd.shuffle(psdmat60)
rnd.shuffle(psdmat90)
rnd.shuffle(pisodmat15)
rnd.shuffle(pisodmat30)
rnd.shuffle(pisodmat60)
rnd.shuffle(pisodmat90)
rnd.shuffle(pracdiffsame)
rnd.shuffle(pracsamesame)
rnd.shuffle(pracisosame)

    
adr=0
practrials=[]
for adder in np.arange(tottri/24):
    slcr=slice(adr*4,(adr*4)+4,1)
        
    practrials.append(pddmat15[adr])
    practrials.append(pddmat30[adr])
    practrials.append(pddmat60[adr])
    practrials.append(pddmat90[adr])
    practrials.extend(pracdiffsame[slcr])
        
    practrials.append(psdmat15[adr])
    practrials.append(psdmat30[adr])
    practrials.append(psdmat60[adr])
    practrials.append(psdmat90[adr])
    practrials.extend(pracsamesame[slcr])
        
    practrials.append(pisodmat15[adr])
    practrials.append(pisodmat30[adr])
    practrials.append(pisodmat60[adr])
    practrials.append(pisodmat90[adr])
    practrials.extend(pracisosame[slcr])
    adr=adr+1


import copy
p1 = copy.deepcopy(practrials)
    
for ind in range(0,int(len(practrials))):
        practrials[ind].update(ori=0)
for ind in range(0, int(len(p1))):
        p1[ind].update(ori=180)
        
p2 = practrials + p1
    

p2.sort(key=operator.itemgetter('dissim'))

pracordtrials1=[]
slcr=slice(0,int(len(p2)/2),1)
pracordtrials1.extend(p2[slcr])

pracordtrials2=[]
slcr2=slice(int(len(p2)/2),len(p2),1)
pracordtrials2.extend(p2[slcr2])

rnd.shuffle(pracordtrials1)
rnd.shuffle(pracordtrials2)

pracnewtrials=[]
# This is where we take equal number of same and diff trials and put them in a 
# new list.
for indx in np.arange(0,int(len(p2)/2),3):
    slcr=slice(indx,indx+3,1)
    pracnewtrials.extend(pracordtrials1[slcr])
    pracnewtrials.extend(pracordtrials2[slcr])

pracnewtrials2=[]
for indx in np.arange(0,len(p2),6):
    slcr=slice(indx,indx+6,1)
    pp=pracnewtrials[slcr]
    rnd.shuffle(pp)
    pracnewtrials2.extend(pp)
    

pp2= pracnewtrials2
prtrials = data.TrialHandler(pp2, nReps=1, method='sequential', originPath=datapath)




morph11=npm.repmat([20, 35, 65, 5],1,4)
morph12=npm.repmat([20, 95, 65, 5],1,4)
morph13=npm.repmat([5, 65, 35, 95],1,8)
morph1=np.append(morph11,morph12)
morph1=np.append(morph1, morph13)

morph21=npm.repmat([35, 65, 5, 95],1,8)
morph22=npm.repmat([20, 35, 95, 5],1,8)
morph2=np.append(morph21,morph22)
    
morph31=npm.repmat([20, 95, 65, 5],1,7)
morph32=[20, 95, 65, 20]
morph33=npm.repmat([5, 65, 35, 20],1,7)
morph34=[5, 65, 20, 20]
morph3=np.append(morph31,morph32)
morph3=np.append(morph3,morph33)
morph3=np.append(morph3,morph34)

morph41=npm.repmat([20, 95, 35, 5],1,3)
morph42=[20, 20, 35, 5]
morph43=npm.repmat([20, 95, 35, 65],1,4)
morph44=npm.repmat([95, 65, 35, 20],1,8)
morph4=np.append(morph41,morph42)
morph4=np.append(morph4,morph43)
morph4=np.append(morph4,morph44)

    
morph51=[20, 35, 65, 20]
morph52=npm.repmat([20, 35, 65, 5], 1, 3)
morph53=npm.repmat([20, 95, 65, 5], 1, 4)
morph54=npm.repmat([20, 5, 35, 95], 1, 3)
morph55=npm.repmat([20, 65, 35, 95],1, 5)
morph5=np.append(morph51,morph52)
morph5=np.append(morph5,morph53)
morph5=np.append(morph5,morph54)
morph5=np.append(morph5,morph55)
    
i=0
expdiffdiffmen = []
expdiffsamemen=[]
expsamediffmen=[]
expsamesamemen=[]
expisodiffmen=[]
expisosamemen=[]

for cxt1, cxt2, eyes in zip(mencxts1, mencxts2, meneyes):
    for itr in np.arange(4):
        expdiffdiffmen.append({'cxt1': cxt1, 'cxt2': cxt2, 'eyes': eyes, 'cond': 'DD', 'im1': str(cxt1+'-'+eyes+'-'+str(morph1[i])+asfx), 'im2': str(cxt2+'-'+eyes+'-'+str(morph2[i])+asfx), 'dissim': abs(morph1[i]-morph2[i])})
        expdiffsamemen.append({'cxt1': cxt1, 'cxt2': cxt2, 'eyes': eyes, 'cond': 'DS', 'im1': str(cxt1+'-'+eyes+'-'+str(morph3[i])+asfx), 'im2': str(cxt2+'-'+eyes+'-'+str(morph3[i])+asfx), 'dissim': abs(morph3[i]-morph3[i])})
        expsamediffmen.append({'cxt1': cxt1, 'cxt2': cxt1, 'eyes': eyes, 'cond': 'SD', 'im1': str(cxt1+'-'+eyes+'-'+str(morph1[i])+asfx), 'im2': str(cxt1+'-'+eyes+'-'+str(morph2[i])+asfx), 'dissim': abs(morph1[i]-morph2[i])})
        expsamesamemen.append({'cxt1': cxt1, 'cxt2': cxt1, 'eyes': eyes, 'cond': 'SS', 'im1': str(cxt1+'-'+eyes+'-'+str(morph4[i])+asfx), 'im2': str(cxt2+'-'+eyes+'-'+str(morph4[i])+asfx), 'dissim': abs(morph4[i]-morph4[i])})
        expisodiffmen.append({'cxt1': '0', 'cxt2': '0', 'eyes': eyes, 'cond': 'ISOD', 'im1': str(eyes+'-'+str(morph1[i])+asfx), 'im2': str(eyes+'-'+str(morph2[i])+asfx), 'dissim': abs(morph1[i]-morph2[i])})
        expisosamemen.append({'cxt1': '0', 'cxt2': '0', 'eyes': eyes, 'cond': 'ISOS', 'im1': str(eyes+'-'+str(morph5[i])+asfx), 'im2': str(eyes+'-'+str(morph5[i])+asfx), 'dissim': abs(morph5[i]-morph5[i])})
        i=i+1

expdiffdiffwom = []
expdiffsamewom=[]
expsamediffwom=[]
expsamesamewom=[]
expisodiffwom=[]
expisosamewom=[]

i=0
for cxt1, cxt2, eyes in zip(womcxts1, womcxts2, womeyes):
    for itr in np.arange(4):
        expdiffdiffwom.append({'cxt1': cxt1, 'cxt2': cxt2, 'eyes': eyes, 'cond': 'DD', 'im1': str(cxt1+'-'+eyes+'-'+str(morph1[i])+asfx), 'im2': str(cxt2+'-'+eyes+'-'+str(morph2[i])+asfx), 'dissim': abs(morph1[i]-morph2[i])})
        expdiffsamewom.append({'cxt1': cxt1, 'cxt2': cxt2, 'eyes': eyes, 'cond': 'DS', 'im1': str(cxt1+'-'+eyes+'-'+str(morph3[i])+asfx), 'im2': str(cxt2+'-'+eyes+'-'+str(morph3[i])+asfx), 'dissim': abs(morph3[i]-morph3[i])})
        expsamediffwom.append({'cxt1': cxt1, 'cxt2': cxt1, 'eyes': eyes, 'cond': 'SD', 'im1': str(cxt1+'-'+eyes+'-'+str(morph1[i])+asfx), 'im2': str(cxt1+'-'+eyes+'-'+str(morph2[i])+asfx), 'dissim': abs(morph1[i]-morph2[i])})
        expsamesamewom.append({'cxt1': cxt1, 'cxt2': cxt1, 'eyes': eyes, 'cond': 'SS', 'im1': str(cxt1+'-'+eyes+'-'+str(morph4[i])+asfx), 'im2': str(cxt2+'-'+eyes+'-'+str(morph4[i])+asfx), 'dissim': abs(morph4[i]-morph4[i])})
        expisodiffwom.append({'cxt1': '0', 'cxt2': '0', 'eyes': eyes, 'cond': 'ISOD', 'im1': str(eyes+'-'+str(morph1[i])+asfx), 'im2': str(eyes+'-'+str(morph2[i])+asfx), 'dissim': abs(morph1[i]-morph2[i])})
        expisosamewom.append({'cxt1': '0', 'cxt2': '0', 'eyes': eyes, 'cond': 'ISOS', 'im1': str(eyes+'-'+str(morph5[i])+asfx), 'im2': str(eyes+'-'+str(morph5[i])+asfx), 'dissim': abs(morph5[i]-morph5[i])})
        i=i+1
    
eddmen15=[]
eddwom15=[]
eddmen30=[]
eddwom30=[]
eddmen60=[]
eddwom60=[]
eddmen90=[]
eddwom90=[]
esdmen15=[]
esdwom15=[]
esdmen30=[]
esdwom30=[]
esdmen60=[]
esdwom60=[]
esdmen90=[]
esdwom90=[]
eisodmen15=[]
eisodwom15=[]
eisodmen30=[]
eisodwom30=[]
eisodmen60=[]
eisodwom60=[]
eisodmen90=[]
eisodwom90=[]
    
for j in np.arange(len(expdiffdiffmen)):
    if expdiffdiffmen[j]['dissim'] == 15:
        eddmen15.append(expdiffdiffmen[j])
    elif expdiffdiffmen[j]['dissim'] == 30:
        eddmen30.append(expdiffdiffmen[j])
    elif expdiffdiffmen[j]['dissim'] == 60:
        eddmen60.append(expdiffdiffmen[j])
    elif expdiffdiffmen[j]['dissim'] == 90:
        eddmen90.append(expdiffdiffmen[j])
        
for j in np.arange(len(expdiffdiffwom)):
    if expdiffdiffwom[j]['dissim'] == 15:
        eddwom15.append(expdiffdiffwom[j])
    elif expdiffdiffwom[j]['dissim'] == 30:
        eddwom30.append(expdiffdiffwom[j])
    elif expdiffdiffwom[j]['dissim'] == 60:
        eddwom60.append(expdiffdiffwom[j])
    elif expdiffdiffwom[j]['dissim'] == 90:
        eddwom90.append(expdiffdiffwom[j])
            
for j in np.arange(len(expsamediffmen)):
    if expsamediffmen[j]['dissim'] == 15:
        esdmen15.append(expsamediffmen[j])
    elif expsamediffmen[j]['dissim'] == 30:
        esdmen30.append(expsamediffmen[j])
    elif expsamediffmen[j]['dissim'] == 60:
        esdmen60.append(expsamediffmen[j])
    elif expsamediffmen[j]['dissim'] == 90:
        esdmen90.append(expsamediffmen[j])
for j in np.arange(len(expsamediffwom)):
    if expsamediffwom[j]['dissim'] == 15:
        esdwom15.append(expsamediffwom[j])
    elif expsamediffwom[j]['dissim'] == 30:
        esdwom30.append(expsamediffwom[j])
    elif expsamediffwom[j]['dissim'] == 60:
        esdwom60.append(expsamediffwom[j])
    elif expsamediffwom[j]['dissim'] == 90:
        esdwom90.append(expsamediffwom[j])
for j in np.arange(len(expisodiffmen)):
    if expisodiffmen[j]['dissim'] == 15:
        eisodmen15.append(expisodiffmen[j])
    elif expisodiffmen[j]['dissim'] == 30:
        eisodmen30.append(expisodiffmen[j])
    elif expisodiffmen[j]['dissim'] == 60:
        eisodmen60.append(expisodiffmen[j])
    elif expisodiffmen[j]['dissim'] == 90:
        eisodmen90.append(expisodiffmen[j])
for j in np.arange(len(expisodiffwom)):
    if expisodiffwom[j]['dissim'] == 15:
        eisodwom15.append(expisodiffwom[j])
    elif expisodiffwom[j]['dissim'] == 30:
        eisodwom30.append(expisodiffwom[j])
    elif expisodiffwom[j]['dissim'] == 60:
        eisodwom60.append(expisodiffwom[j])
    elif expisodiffwom[j]['dissim'] == 90:
        eisodwom90.append(expisodiffwom[j])
            
rnd.shuffle(eddmen15)
rnd.shuffle(eddwom15)
rnd.shuffle(eddmen30)
rnd.shuffle(eddwom30)
rnd.shuffle(eddmen60)
rnd.shuffle(eddwom60)
rnd.shuffle(eddmen90)
rnd.shuffle(eddwom90)
rnd.shuffle(esdmen15)
rnd.shuffle(esdwom15)
rnd.shuffle(esdmen30)
rnd.shuffle(esdwom30)
rnd.shuffle(esdmen60)
rnd.shuffle(esdwom60)
rnd.shuffle(esdmen90)
rnd.shuffle(esdwom90)
rnd.shuffle(eisodmen15)
rnd.shuffle(eisodwom15)
rnd.shuffle(eisodmen30)
rnd.shuffle(eisodwom30)
rnd.shuffle(eisodmen60)
rnd.shuffle(eisodwom60)
rnd.shuffle(eisodmen90)
rnd.shuffle(eisodwom90)
rnd.shuffle(expdiffsamemen)
rnd.shuffle(expdiffsamewom)
rnd.shuffle(expsamesamemen)
rnd.shuffle(expsamesamewom)
rnd.shuffle(expisosamemen)
rnd.shuffle(expisosamewom)

    
adr=0
exptrials=[]
for adder in np.arange(explength2/48):
    slcr=slice(adr*4,(adr*4)+4,1)
        
    exptrials.append(eddmen15[adr])
    exptrials.append(eddmen30[adr])
    exptrials.append(eddmen60[adr])
    exptrials.append(eddmen90[adr])
    exptrials.extend(expdiffsamemen[slcr])
    exptrials.append(eddwom15[adr])
    exptrials.append(eddwom30[adr])
    exptrials.append(eddwom60[adr])
    exptrials.append(eddwom90[adr])
    exptrials.extend(expdiffsamewom[slcr])
        
    exptrials.append(esdmen15[adr])
    exptrials.append(esdmen30[adr])
    exptrials.append(esdmen60[adr])
    exptrials.append(esdmen90[adr])
    exptrials.extend(expsamesamemen[slcr])
    exptrials.append(esdwom15[adr])
    exptrials.append(esdwom30[adr])
    exptrials.append(esdwom60[adr])
    exptrials.append(esdwom90[adr])
    exptrials.extend(expsamesamewom[slcr])
        
    exptrials.append(eisodmen15[adr])
    exptrials.append(eisodmen30[adr])
    exptrials.append(eisodmen60[adr])
    exptrials.append(eisodmen90[adr])
    exptrials.extend(expisosamemen[slcr])
    exptrials.append(eisodwom15[adr])
    exptrials.append(eisodwom30[adr])
    exptrials.append(eisodwom60[adr])
    exptrials.append(eisodwom90[adr])
    exptrials.extend(expisosamewom[slcr])
    adr=adr+1


e1 = copy.deepcopy(exptrials)
    
for ind in range(0,int(len(exptrials))):
        exptrials[ind].update(ori=0)
for ind in range(0, int(len(e1))):
        e1[ind].update(ori=180)
        
e2 = exptrials + e1


e2.sort(key=operator.itemgetter('dissim'))

ordtrials1=[]
slcr=slice(0,int(len(e2)/2),1)
ordtrials1.extend(e2[slcr])

ordtrials2=[]
slcr2=slice(int(len(e2)/2),len(e2),1)
ordtrials2.extend(e2[slcr2])

rnd.shuffle(ordtrials1)
rnd.shuffle(ordtrials2)

newtrials=[]
# This is where we take equal number of same and diff trials and put them in a 
# new list.
for indx in np.arange(0,int(len(e2)/2),24):
    slcr=slice(indx,indx+24,1)
    newtrials.extend(ordtrials1[slcr])
    newtrials.extend(ordtrials2[slcr])

# This part shuffles every 48 within itself.
newtrials2=[]
for indx in np.arange(0,len(e2),48):
    slcr=slice(indx,indx+48,1)
    a=newtrials[slcr]
    rnd.shuffle(a)
    newtrials2.extend(a)

# creating two sessions.
newtrials3=[]
slcr3=slice(0,int(len(newtrials2)/3),1)
newtrials3.extend(newtrials2[slcr3])

newtrials4=[]
slcr4=slice(int(len(newtrials2)/3),int(len(newtrials2)/3*2),1)
newtrials4.extend(newtrials2[slcr4])

newtrials5=[]
slcr5=slice(int(len(newtrials2)/3*2),len(newtrials2),1)
newtrials5.extend(newtrials2[slcr4])
print('potato')

import pickle

trials_fname = exp_info['participant'] + '_' + 'trials'
trials_fname = os.path.join(datapath, trials_fname)
pickle_fname = exp_info['participant'] + '-' + 'pickle'
pickle_fname = os.path.join(datapath, pickle_fname)
pickled=False

if os.path.exists(pickle_fname):
    pickled=True
    print('pickled')


if not pickled: 
    print('unpickled, pickling now')
    with open(trials_fname, 'wb') as pickle_file:
        pickle.dump([newtrials2], pickle_file)
    with open(pickle_fname, 'wb') as pickle_file2:
        pickle.dump([pickled], pickle_file2)
        
else:    
    with open(trials_fname, 'rb') as pickle_file:
        newtrials2=pickle.load(pickle_file)
        newtrials2=newtrials2[0][:]
    with open(pickle_fname, 'rb') as pickle_file2:
        pickled=pickle.load(pickle_file2)
        

if exp_info['session'] == '1':
    newtrials3=[]
    slcr3=slice(0,int(len(newtrials2)/3),1)
    newtrials3.extend(newtrials2[slcr3])
    exTrials = data.TrialHandler(newtrials3, nReps=1, method='sequential', originPath=datapath)
    print('ses1')
elif exp_info['session'] == '2':
    newtrials4=[]
    slcr4=slice(int(len(newtrials2)/3),int(len(newtrials2)/3*2),1)
    newtrials4.extend(newtrials2[slcr4])
    exTrials = data.TrialHandler(newtrials4, nReps=1, method='sequential', originPath=datapath)
    print('kartoffel')
elif exp_info['session'] == '3':
    newtrials5=[]
    slcr5=slice(int(len(newtrials2)/3*2),len(newtrials2),1)
    newtrials5.extend(newtrials2[slcr5])
    exTrials = data.TrialHandler(newtrials5, nReps=1, method='sequential', originPath=datapath)
    print('pommes')
else:
    exTrials = data.TrialHandler(newtrials2, nReps=1, method='sequential', originPath=datapath)
    
    



#pickle.load(trials_fname)




#=====================
# Start the experiment
#=====================

# Initialize two clocks:
#   - for image change time
#   - for response time
change_clock = core.Clock()
rt_clock = core.Clock()

trialCount=0
training=0
trainingAccTot=0
trainingAccBlock=0


pracCount=0
pracDone=0
# Run through the trials PRACTICE


for trial in prtrials:
    pracCount=pracCount+1
    # Display trial start text
    if pracCount == 1:
        
        ##Instruction Screen 1: Before starting, make sure to find ...
        inst1_imname=os.path.join(instpath, 'instscr1.png')
        bitmapinst.setImage(inst1_imname)
        bitmapinst.draw()

        win.flip()
        # Wait for a spacebar press to start the trial, or escape to quit
        keys = event.waitKeys()
        if 'escape' in keys:
            break
        keys = []
        event.clearEvents()
        
        ##Instruction Screen 2: In this experiment, pictures of faces ...
        inst2_imname=os.path.join(instpath, 'instscr2.png')
        bitmapinst.setImage(inst2_imname)
        bitmapinst.draw()
        win.flip()
        # Wait for a spacebar press to start the trial, or escape to quit
        keys = event.waitKeys()
        if 'escape' in keys:
            break
        keys = []
        event.clearEvents()
        
        ##Instruction Screen 3: Different eyes...
        inst3_imname=os.path.join(instpath, 'instscr3.png')
        bitmapinst.setImage(inst3_imname)
        bitmapinst.draw()
        win.flip()
        # Wait for a spacebar press to start the trial, or escape to quit
        keys = event.waitKeys()
        if 'escape' in keys:
            break
        keys = []
        event.clearEvents()
        
        ##Instruction Screen 4: Same eyes...
        inst4_imname=os.path.join(instpath, 'instscr4.png')
        bitmapinst.setImage(inst4_imname)
        bitmapinst.draw()
        win.flip()
        # Wait for a spacebar press to start the trial, or escape to quit
        keys = event.waitKeys()
        if 'escape' in keys:
            break
        keys = []
        event.clearEvents()
        
        ##Instruction Screen 5: Only eyes...
        insteyes_imname=os.path.join(instpath, 'instscreyes.png')
        bitmapinst.setImage(insteyes_imname)
        bitmapinst.draw()
        win.flip()
        # Wait for a spacebar press to start the trial, or escape to quit
        keys = event.waitKeys()
        if 'escape' in keys:
            break
        keys = []
        event.clearEvents()
        
        ##Instruction Screen 6: The task is difficult since...
        inst5_imname=os.path.join(instpath, 'instscr5.png')
        bitmapinst.setImage(inst5_imname)
        bitmapinst.draw()
        win.flip()
        # Wait for a spacebar press to start the trial, or escape to quit
        keys = event.waitKeys()
        if 'escape' in keys:
            break
        keys = []
        event.clearEvents()
        
        ##Instruction Screen 7: IDENTICAL eyes = "S", DIFFERENT...
        inst6_imname=os.path.join(instpath, 'instscr6.png')
        bitmapinst.setImage(inst6_imname)
        bitmapinst.draw()
        win.flip()
        # Wait for a spacebar press to start the trial, or escape to quit
        keys = event.waitKeys()
        if 'escape' in keys:
            break
        keys = []
        event.clearEvents()
        
        
     
        
            # Set the images
    im1_fname = os.path.join(pracpath, trial['im1'])
    im2_fname = os.path.join(pracpath, trial['im2'])
                
    rnd.shuffle(imside)
    if imside[1] == 0:
        bitmap1.setImage(im1_fname)
        bitmap2.setImage(im2_fname)
    else:
        bitmap1.setImage(im2_fname)
        bitmap2.setImage(im1_fname)
    bitmap1.setOri(trial['ori'])
    bitmap2.setOri(trial['ori'])
                        
    rnd.shuffle(tilt)
    if tilt[1] == 0:
        bitmap1.pos=(-284,10) #142+284/2
        bitmap2.pos=(284,0)
    else:
        bitmap1.pos=(-284,0) #142+284/2 (Because .pos puts the center of the image on the defined location)
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
    if keys:
        if 'escape' in keys:
            break
        elif 's' in keys and trial['dissim'] == 0: #left is same
            acc = 1
        elif 'l' in keys and not trial['dissim'] == 0: #right is different
            acc = 1
        else:
            acc = 0
                                                        
    trainingAccTot=trainingAccTot+acc
    trainingAccBlock=trainingAccBlock+acc
                                                        
                                                        
    if pracCount <=50 and pracCount%6 == 0:
        blockPerc=trainingAccBlock/6*100
        if blockPerc >= 75:
            win.setColor(color = 'darkgreen')
        elif blockPerc <75 and blockPerc >=50:
            win.setColor(color = 'gray')
        elif blockPerc < 50:
            win.setColor(color = 'darkred')
        win.flip()
        pracAcc_message = visual.TextStim(win,
                                              text="Your accuracy for this block was: %d%%. \n Press Space to continue. \n\n\n\n\n Press ""S"" for SAME, ""L"" for DIFFERENT." %blockPerc,
                                              color='black', height=20)
        pracAcc_message.draw()
        win.flip()
        trainingAccBlock=0
        keys = event.waitKeys(keyList=['space', 'escape'])
        win.setColor(color = 'gray')
        win.flip()
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
    elif pracCount >50 and pracCount%12==0 and not pracCount == len(pp2):
        blockPerc=trainingAccBlock/12*100
        if blockPerc >= 75:
            win.setColor(color = 'darkgreen')
        elif blockPerc <75 and blockPerc >=50:
            win.setColor(color = 'gray')
        elif blockPerc < 50:
            win.setColor(color = 'darkred')
        win.flip()
        pracAcc_message = visual.TextStim(win,
                                              text="Your accuracy for this block was: %d%%. \n Press Space to continue. \n\n\n\n\n Press ""S"" for SAME, ""L"" for DIFFERENT." %blockPerc,
                                              color='black', height=20)
        pracAcc_message.draw()
        win.flip()
        trainingAccBlock=0
        keys = event.waitKeys(keyList=['space', 'escape'])
        win.setColor(color = 'gray')
        win.flip()
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
    elif pracCount == len(pp2):
        totPerc=trainingAccTot/len(p2)*100;
        if totPerc >= 65:
            win.setColor(color = 'darkgreen')
            win.flip()
            pracAcc_message = visual.TextStim(win,
                                                  text="Your accuracy for the training was: %d%%. \n Press T to continue. \n\n\n\n\n Press ""S"" for SAME, ""L"" for DIFFERENT." %totPerc,
                                                  color='black', height=25, bold = True )
            pracAcc_message.draw()
            win.flip()
            keys = event.waitKeys(keyList=['t','escape'])
            if 'escape' in keys:
                win.setColor(color = 'gray')
                win.flip()
                break
            elif 'space' in keys:
                keys = []
                event.clearEvents()
                win.setColor(color = 'gray')
                win.flip()                   
            pracDone=1
            core.wait(IBW)
        elif totPerc < 65:
            win.setColor(color = 'darkred')
            win.flip()
            pracAcc_message = visual.TextStim(win,
                                                  text="Your accuracy for the training was too low: %d%%. \n Please call the experimenter to start training again." %totPerc,
                                                  color='white', height=25, bold = True)        
            pracAcc_message.draw()
            win.flip()
            keys = event.waitKeys(keyList=['escape'])                                                      
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
    win.setColor(color = 'gray')
    win.flip()  
    prtrials.addData('rt', rt)
    prtrials.addData('acc', acc)
    rnd.shuffle(ISI)
    core.wait(ISI[1])
                # Advance to the next trial
                                                                                        

#======================
# End of the experiment
#======================

# Save all data to a file
prtrials.saveAsWideText(data_fname + 'prac' + '.csv', delim=',')


trialCount=0
expAccTot=0
expAccBlock=0

for trial in exTrials:
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
    im1_fname = os.path.join(exppath, trial['im1'])
    im2_fname = os.path.join(exppath, trial['im2'])
                
    rnd.shuffle(imside)
    if imside[1] == 0:
        bitmap1.setImage(im1_fname)
        bitmap2.setImage(im2_fname)
    else:
        bitmap1.setImage(im2_fname)
        bitmap2.setImage(im1_fname)
    bitmap1.setOri(trial['ori'])
    bitmap2.setOri(trial['ori'])
                        
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
    blockPerc=expAccBlock/48*100                     
    #print(blockPerc)                   
    if trialCount%48 == 0 and blockPerc >=75:
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
    elif trialCount%48 == 0 and (blockPerc <75 and blockPerc >=50):
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
    elif trialCount%48 == 0 and (blockPerc <50) and not trialCount == sesslength:
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
    elif trialCount == sesslength:
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
    exTrials.addData('rt', rt)
    exTrials.addData('acc', acc)
    rnd.shuffle(ISI)
    core.wait(ISI[1])
    
                # Advance to the next trial

exTrials.saveAsWideText(data_fname + 'Exp' + '.csv', delim=',')
# Quit the experiment
win.close()

