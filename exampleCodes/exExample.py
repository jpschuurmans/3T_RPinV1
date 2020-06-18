#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 11:26:58 2020

@author: jschuurmans
"""
from psychopy import visual, core, event
import datetime # Used to register the date of the experiment
import pandas as pd # Used to save the data as csv easily

# Colours
gray = '#969696'
black = '#000000'
white = '#FFFFFF'

# Window parameters
resolution = [300, 300]

def window(resolution):
    fullScreen = True
    win = visual.Window(resolution,units="pix",  color=gray, colorSpace='hex', fullscr=fullScreen, monitor = "testMonitor")
    win.setMouseVisible(False)
    return win


def loadInstructionsAndFlip(win):
    background = visual.Rect(win, width=resolution[0]+10, height=resolution[1]+10, fillColor=black, fillColorSpace='hex')
    msg1 = visual.TextStim(win, text="press [ q ] to exit", pos=(0.0,(-resolution[1]*0.10)), color=white, colorSpace='hex')
    msg2 = visual.TextStim(win, text="press [ n ] to continue", color=white, colorSpace='hex',alignHoriz='center', alignVert='center')
    background.draw()
    msg1.draw()
    msg2.draw()

    # Elements are only displayed after the flip command is executed
    win.flip()

def loadStartScreenAndFlip(win):
    background = visual.Rect(win, width=resolution[0]+10, height=resolution[1]+10, fillColor=gray, fillColorSpace='hex')
    msg1 = visual.TextStim(win, text="press any key to start", color=white, colorSpace='hex')
    background.draw()
    msg1.draw()

    # Elements are only displayed after the flip command is executed
    win.flip()
 
def startScreensAndRecordData(win):
    clock = core.Clock()
    win.clearBuffer()

    data = []
    loadStartScreenAndFlip(win)
    event.waitKeys()

    while True:
        loadInstructionsAndFlip(win)
        clock.reset()
        keys = event.waitKeys(keyList=["n","q"])
        for key in keys:
            time = clock.getTime()
            print("You pressed the {} key on {} seconds".format(key,round(time,3)))
            data.append([key,time])
            if key == "q":
                win.close()
                return data
            else:
                loadStartScreenAndFlip(win)
                event.waitKeys()
                

def main():
    win = window(resolution)
    data = startScreensAndRecordData(win)

    pd.DataFrame(data,columns=["Key","Time"]).to_csv('experiment_' + str(datetime.date.today()) + '.csv')
    print("Experiment saved as:",'experiment_' + str(datetime.date.today()) + '.csv')







if __name__ == "__main__":
    main()




