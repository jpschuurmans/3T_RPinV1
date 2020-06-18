from psychopy import visual, core, event, monitors, gui, logging, parallel
import math
import numpy as np
import csv
import datetime
import time

class settings(object):
    def setup(self, distanceToMonitor=40,
                    monitorWidthCM=16, widthPix=1920,heightPix=1080, frequency=0, duration = 0,
                    trialdur = 5.0, port='/dev/ttyACM0',visualAngle = 5,
                    fname='Sequence.csv', waitdur=1, parallelx="" ):

        self.mon = monitors.Monitor('testmonitor')
        self.mon.setDistance(distanceToMonitor)
        self.mon.setWidth(monitorWidthCM)
        self.mon.setSizePix([widthPix, heightPix])
        self.mywin = visual.Window([widthPix, heightPix], fullscr=True, monitor=self.mon, units='deg',waitBlanking=False, color=0.001) #you might want to remove waitblanking
        self.mywin.mouseVisible = False
        #self.pattern1 = visual.GratingStim(win=self.mywin, name='pattern1',units='cm',
        #               tex=None, mask=None,
          #              ori=0, pos=[0, 0], size=10, sf=1, phase=0.0,
           #             color=[1,1,1], colorSpace='rgb', opacity=1,
            #            texRes=256, interpolate=True, depth=-1.0)
        self.stimSequenceArray= []
        self.timingArray= []
        self.nextStimulus = visual.ImageStim(win=self.mywin, image='faces/eq_f01_a.bmp',mask = None, interpolate=False, ori=0,size=visualAngle, pos=[0, 0],units='deg')
        self.fixation = visual.GratingStim(win=self.mywin, mask='gauss',size = 0.3, pos=[0,0], sf=0, rgb=-1)
        self.pauseText = visual.TextStim(self.mywin,text= 'Break. Say GO ON to continue', color='black', height=0.5)
        self.blackSquare = visual.Rect(self.mywin, width=0.35, height =0.35,fillColor='white',lineColor='Black',pos=(9,-5))
        self.isiwindows = np.linspace(1800,2000,num=50)
        #print  self.isiwindows
        self.framerate = self.mywin.getActualFrameRate()
        self.frequency = frequency
        self.duration = duration
        self.trialdur = trialdur
        self.fname = fname
        self.waitdur = waitdur
        self.port = port
        self.stimcounter = 0
        self.maxframes = 0
        self.monitor = ""

        """Triggerport preparation """
        self.port = parallel.ParallelPort(address=0xDFF8)
        self.port.setData(0)

class StimulusSequence(object):
    def __init__(self):
        self.currentProtocol = ""
        self.currentSequence = ""
        self.currentSettings = ""

    def loadStimArray(self, inputarray):
        counter = 0
        self.stimSequenceArray = []
        for filename in inputarray:
            if (counter >2): #skips first three columns of csv-file
                self.stimSequenceArray.append('./SweepStim/' + filename)
            counter+=1
        self.maxframes = len(self.stimSequenceArray) -1

    def loadTimingArray(self, inputarray):
        counter = 0
        self.timingArray = []
        for timing in inputarray:
            if (counter >2): #skips first three columns of csv-file
                self.timingArray.append(int(timing))
            counter+=1



    def epoch(self, mark):
        self.collector.tag(mark)

    def stop(self):
        self.mywin.close()
        core.quit()

    def runSweepSequence(self, frequency):
        self.framerate = self.currentSettings.mywin.getActualFrameRate()
        self.frame_on = int(math.floor((1000/frequency)/(1000/self.framerate)))
        self.frequency = frequency
        presentBlackSquare = True
        ###Testing framerate grabber###
        print(self.currentSettings.mywin.getActualFrameRate())

        print("frames on: "+ str(self.frame_on) +" stimulus duration: " + str(self.frame_on*(1000/self.framerate)) + " Actual frequency: " + str(1000/(self.frame_on*(1000/self.framerate))))
        self.currentSettings.mywin.logOnFlip(level=logging.DATA, msg='trial onset/stimulus offset')
        for frameN in range(200):
            self.currentSettings.mywin.flip()
        self.currentSettings.fixation.setAutoDraw(True)
        self.currentSettings.mywin.logOnFlip(level=logging.DATA, msg='fixation onset')
        for frameN in range(200):
            self.currentSettings.mywin.flip()
        self.currentSettings.fixation.setAutoDraw(False)
        self.stimcounter = 0
        
        while self.stimcounter<=self.maxframes:
            print(self.stimSequenceArray[self.stimcounter])
            self.currentSettings.nextStimulus.setImage(self.stimSequenceArray[self.stimcounter])
            self.currentSettings.nextStimulus.setAutoDraw(True)
            self.currentSettings.fixation.setAutoDraw(True)
            self.currentSettings.blackSquare.setAutoDraw(False)
            self.currentSettings.mywin.logOnFlip(level=logging.DATA, msg='stimulus onset: ' + self.currentSettings.nextStimulus.image)
            if self.stimSequenceArray[self.stimcounter][-6:-4] == 'nk':
                trigger = 99
            else:
                trigger = int(self.stimSequenceArray[self.stimcounter][-6:-4])
            self.currentSettings.port.setData(trigger)
            print(trigger)
            for frameN in range(self.frame_on):
                self.currentSettings.mywin.flip()
            trigger = 99
            self.currentSettings.port.setData(trigger)
            self.currentSettings.nextStimulus.setImage("./SweepStim/blank.bmp") #might need to change to match folder
            #self.currentSettings.nextStimulus.setAutoDraw(True)
            self.currentSettings.blackSquare.setAutoDraw(True)
            for frameN in range(self.frame_on):
                self.currentSettings.mywin.flip()
            self.currentSettings.port.setData(0)
            self.stimcounter +=1
            self.currentSettings.fixation.setAutoDraw(False)
            if event.getKeys(keyList=["escape"]):
                self.currentSettings.mywin.close()
                core.quit()
        self.currentSettings.nextStimulus.setAutoDraw(False)

    def makePause(self):
        self.currentSettings.pauseText.setAutoDraw(True)
        pressed = False
        while pressed==False:
            self.currentSettings.mywin.flip()
            if event.getKeys(keyList=["c"]):
                pressed = True
            if event.getKeys(keyList=["escape"]):
                self.currentSettings.mywin.close()
                core.quit()
        self.currentSettings.pauseText.setAutoDraw(False)

    
    def runSlowSequence(self, duration, isi):
        self.frame_on = int(round(duration/(1000/self.currentSettings.framerate)))
        print(self.currentSettings.mywin.getActualFrameRate())
        self.currentSettings.mywin.logOnFlip(level=logging.DATA, msg='trial onset/stimulus offset')
        for frameN in range(30):
            self.currentSettings.mywin.flip()
        self.currentSettings.fixation.setAutoDraw(True)
        self.currentSettings.mywin.logOnFlip(level=logging.DATA, msg='fixation onset')
        for frameN in range(60):
            self.currentSettings.mywin.flip()        
        self.stimcounter = 0
        while self.stimcounter<=self.maxframes:
            self.isi = round(self.currentSettings.isiwindows[np.random.randint(50)])
            isiFrames = int(round(self.isi/(1000/self.currentSettings.framerate)))
            self.currentSettings.nextStimulus.setImage(self.stimSequenceArray[self.stimcounter])
            self.currentSettings.nextStimulus.setAutoDraw(True)
            self.currentSettings.fixation.setAutoDraw(False)
            self.currentSettings.fixation.setAutoDraw(True)
            self.currentSettings.blackSquare.setAutoDraw(False)
            self.currentSettings.mywin.logOnFlip(level=logging.DATA, msg='stimulus onset: ' + self.currentSettings.nextStimulus.image)
            
            if self.currentSettings.nextStimulus.image[12:14] =='ca':
                paralleldata = 99
            else:
                paralleldata = int(self.currentSettings.nextStimulus.image[12:14])
            self.currentSettings.port.setData(paralleldata)
            for frameN in range(self.frame_on):
                self.currentSettings.mywin.flip()
            self.currentSettings.mywin.logOnFlip(level=logging.DATA, msg='frames isi: ' + str(isiFrames))
            print('trigger: ' + str(paralleldata))
            self.currentSettings.port.setData(0)
            self.stimcounter +=1
            self.currentSettings.mywin.logOnFlip(level=logging.DATA, msg='ITI onset')
            self.currentSettings.blackSquare.setAutoDraw(True)
            self.currentSettings.nextStimulus.setAutoDraw(False)
            for frameN in range(isiFrames):
                self.currentSettings.mywin.flip()
            if event.getKeys(keyList=["escape"]):
                    self.currentSettings.mywin.close()
                    core.quit()
        self.currentSettings.blackSquare.setAutoDraw(False)
        self.currentSettings.nextStimulus.setAutoDraw(False)

class Protocol(object):
    def __init__(self):
        self.text= ""
        self.singleBlock= []
        self.anglewidth = 0
        self.angleheight = 0
        self.maxBlocks = 0
    def LoadProtocol(self,file):
        self.maxBlocks = 0
        with open(file, 'rb') as csvFile:
            self.text = csv.reader(csvFile, delimiter =',',quotechar='|')
            
            self.singleBlock = []
            for row in self.text:
                #print row
                self.singleBlock.append(row)
                self.maxBlocks +=1

##################################################################################


#this makes the question thing
info = {'Subject number':0,'experiment start':1, 'Trial counter':0}
infoDlg = gui.DlgFromDict(dictionary=info, title='Subject Info')
if infoDlg.OK:
    print(info)

else:
    print('User Cancelled')
Subnum = info.get('Subject number')
Trialstart = info.get('Trial counter')
ExpStart = info.get('experiment start')
print("Value : %s" %  Subnum)


dirname = "logfiles"
#logFile = logging.LogFile(dirname + '/' + str(Subnum)+'.log', level=logging.INFO, filemode='w')
#logging.log(level=logging.INFO, msg='starting experiment')




###########################################################################################################

whichBlockOrder = [28,7,4,4,53,3]

#setting up for the experiment
currentSettings = settings()
currentSettings.setup(distanceToMonitor=50, visualAngle = 9, parallelx=parallel)
currentProtocol = Protocol()
currentProtocol.LoadProtocol("sweep"+ str(whichBlockOrder[0]) + ".csv")

#First Block
Sequence =StimulusSequence()
Sequence.currentProtocol = currentProtocol
Sequence.currentSettings = currentSettings

#first experiment

if ExpStart < 2:
    counter = 0;
    while counter < currentProtocol.maxBlocks:
        Sequence.loadStimArray(currentProtocol.singleBlock[counter])
        Sequence.runSweepSequence(frequency=15)
        print("block: " + str(counter+1))
        #Sequence.makePause()
        counter += 1

Sequence.makePause()

#second experiment
currentProtocol.LoadProtocol("slow"+ str(whichBlockOrder[1]) + ".csv")
timingProtocol = Protocol()
#timingProtocol.LoadProtocol("timingprotocol2.csv")

if ExpStart < 3:
    counter = 0    
    while counter < currentProtocol.maxBlocks:
        Sequence.loadStimArray(currentProtocol.singleBlock[counter])
        #Sequence.loadTimingArray(timingProtocol.singleBlock[counter])
        Sequence.runSlowSequence(duration=250, isi=2000)
        print("block: " + str(counter+1))
        
        counter += 1
        
Sequence.makePause()
# second Block set up
currentProtocol = Protocol()
currentProtocol.LoadProtocol("sweep"+ str(whichBlockOrder[2]) + ".csv")

Sequence =StimulusSequence()
Sequence.currentProtocol = currentProtocol
Sequence.currentSettings = currentSettings

#first experiment

if ExpStart < 4:
    counter = 0;
    while counter < currentProtocol.maxBlocks:
        Sequence.loadStimArray(currentProtocol.singleBlock[counter])
        Sequence.runSweepSequence(frequency=15)
        print("block: " + str(counter+1))
        
        counter += 1

Sequence.makePause()
#second experiment
currentProtocol.LoadProtocol("slow"+ str(whichBlockOrder[3]) + ".csv")
timingProtocol = Protocol()

if ExpStart < 5:
    counter = 0    
    while counter < currentProtocol.maxBlocks:
        Sequence.loadStimArray(currentProtocol.singleBlock[counter])
        #Sequence.loadTimingArray(timingProtocol.singleBlock[counter])
        Sequence.runSlowSequence(duration=250, isi=2000)
        print("block: " + str(counter+1))
        
        counter += 1
        

Sequence.makePause()
# third Block set up
currentProtocol = Protocol()
currentProtocol.LoadProtocol("sweep"+ str(whichBlockOrder[4]) + ".csv")

Sequence =StimulusSequence()
Sequence.currentProtocol = currentProtocol
Sequence.currentSettings = currentSettings

#first experiment

if ExpStart < 4:
    counter = 0;
    while counter < currentProtocol.maxBlocks:
        Sequence.loadStimArray(currentProtocol.singleBlock[counter])
        Sequence.runSweepSequence(frequency=15)
        print("block: " + str(counter+1))
        
        counter += 1

Sequence.makePause()
#second experiment
currentProtocol.LoadProtocol("slow"+ str(whichBlockOrder[5]) + ".csv")
timingProtocol = Protocol()

if ExpStart < 5:
    counter = 0    
    while counter < currentProtocol.maxBlocks:
        Sequence.loadStimArray(currentProtocol.singleBlock[counter])
        #Sequence.loadTimingArray(timingProtocol.singleBlock[counter])
        Sequence.runSlowSequence(duration=250, isi=2000)
        print("block: " + str(counter+1))
        
        counter += 1        
Sequence.makePause()

# Close the window
Sequence.currentSettings.mywin.close()

# Close PsychoPy
core.quit()
