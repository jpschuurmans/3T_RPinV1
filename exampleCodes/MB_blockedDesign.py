# -*- coding: utf-8 -*-
"""
Basic event-related/block design with/without flicker, records and logs trials and responses in .txt file
Created by Matthew A. Bennett (Thu May 9 16:07:28 2019)
Matthew.Bennett@glasgow.ac.uk
"""
#%% =============================================================================
# imports
from psychopy import core, visual, event, gui
import os  

#%% =============================================================================
# paths and definitions

stim_path = (r'/home/jschuurmans/Pictures/')

stimuli_names = ['JolienAtMRI.png',
                 'JolienInMRI.png']
dataPath = (r'/home/jschuurmans/Documents/02_recurrentSF_3T/recurrentSF_3T_CodeRepo/exampleCodes/TestData')

block_order= [0, 1]

# in seconds
trial_duration = 2;

# if flicker = 0, image persists throughout block
flicker_rate_hz = 4

baseline = 2

insructions_to_subjects = 'Do the experiment right Press 1 to continue'
#%% =============================================================================
# functions

def esc():
    if 'escape' in last_response:
        logfile.close()
        window.close()
        core.quit

#%% =============================================================================
# setup

# =============================================================================
dialog_info = gui.Dlg(title="Visual Experiment")
dialog_info.addField('Subject ID:')
dialog_info.addField('Run:')
dialog_info = dialog_info.show()  # show dialog and wait for OK or Cancel
# =============================================================================
#dialog_info = ['Test', '1']

dataName = dialog_info[0] + '_run' + dialog_info[1] + 'logfile.csv'
dataFname = os.path.join(dataPath, dataName)

logfile = open(dataFname, 'w')
logfile.write('Trial_Number, Stimulus, StimCode, StimOnset, StimOffset, Response, Response_Time\n')




#%% =============================================================================
# create stimuli

window = visual.Window([800,600],monitor="testMonitor", units="deg", screen=1) #, fullscr=True)
#window = visual.Window([800, 600], monitor="DELL U2415", units="pix", fullscr=True)

# create a list of image objects t obe shown in the expt
Stimuli = []
for name in stimuli_names:

    Stimuli.append(visual.ImageStim(window, image = stim_path + name))

#fixation = visual.Rect(window, width=10, height=10, fillColor='white', autoDraw=True)

experimenter_message1 = visual.TextStim(window, pos=[0,+100], text='Experiment Running...')
experimenter_message2 = visual.TextStim(window, pos=[0,+100], text='Waiting for Experimenter C Key Press...')
trigger_message = visual.TextStim(window, pos=[0,+100], text='Waiting for Scanner Trigger...')

insructions_to_subjects = visual.TextStim(window, pos=[0,+100], text=experimenter_message1)

#%% =============================================================================
# start experiment

insructions_to_subjects.draw()
window.flip()
while not '1' in event.getKeys():
    core.wait(0.1)

experimenter_message2.draw()
window.flip()
while not 'c' in event.getKeys():
    core.wait(0.1)

# =============================================================================
# trigger_message.draw()
# window.flip()
# while not trigger
#     core.wait(0.1)
# =============================================================================

# start stopwatch clock
clock = core.Clock()
clock.reset()

# clear any previous presses/escapes
last_response = ''; response_time = ''

for idx, trial in enumerate(block_order):

# =============================================================================
    # how much time has passes since we began the expt?
    expt_time_elapsed = clock.getTime()

    # Calculate baseline to keep us on time
    #               upcoming +      theortical time elapsed    - empirical time elapsed = corrected time for upcoming baseline
    calc_baseline = baseline + (baseline + trial_duration)*idx - expt_time_elapsed
# =============================================================================

# =============================================================================
    # show baseline
    window.flip()
    core.wait(calc_baseline)

    logfile.write(f'{idx+1}, Baseline, 0, {expt_time_elapsed}, {clock.getTime()}, NA, NA\n')
# =============================================================================

    esc() # in case we need to shut down the expt

# =============================================================================
    # show next trial
    trial_onset_time = clock.getTime()

    while clock.getTime() < trial_onset_time + trial_duration:
        # flash stim on
        Stimuli[trial].draw()
        experimenter_message1.draw()
        window.flip()
        if flicker_rate_hz:
            core.wait(1/flicker_rate_hz/2)
            # flash stim off
            window.flip()
            core.wait(1/flicker_rate_hz/2)

    # get response and it's associated timestamp as a list of tuples: (keypress, time)
    response = event.getKeys(timeStamped=True)

    if not response:
        response = [('No_Response', -1)]

    last_response = response[-1][0] # most recent response, first in tuple
    response_time = response[-1][1] # most recent response, second in tuple

    logfile.write(f'{idx+1}, {stimuli_names[block_order[idx]]}, {block_order[idx]+1}, {trial_onset_time}, {clock.getTime()}, {last_response}, {response_time}\n')
# =============================================================================

    esc() # in case we need to shut down the expt

#%% =============================================================================
# cleanup
logfile.close()
window.close()
core.quit()