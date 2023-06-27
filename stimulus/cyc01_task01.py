"""
***** project: OBA-Psycho
***** Experiment pilot01

    Mo Shams <MShamsCBR@gmail.com>
    May 15, 2023


Task Procedure:

    There are two sets of image categories: im1, im2.
    A fixation mark appears and subject has to fixate on that.
    One image appears at the center--the relevant image.
    Subject is prompted to categorize the image by pressing a key.
    Eight irrelevant images will appear around the relevant image.
    There will be nine conditions:
        CND1: rel image #1 - congruent distractors
        CND2: rel image #1 - incongruent distractors
        CND3: rel image #2 - congruent distractors
        CND4: rel image #2 - incongruent distractors
"""
import os
import random
import numpy as np
import pandas as pd
from lib import stim_flow_control as sfc
from psychopy import event, visual, core


def pol2cart(rho, phi):
    x_cart = rho * np.cos(phi)
    y_cart = rho * np.sin(phi)
    return x_cart, y_cart


# disable Panda's false warning message
pd.options.mode.chained_assignment = None  # default='warn'

# ----------------------------------------------------------------------------

# /// INSERT SESSION'S META DATA ///

subID = "0006"
N_TRIALS = 400  # (400) must be a factor of four
n_trials_per_block = 40  # (40)
nblocks = int(N_TRIALS / n_trials_per_block)
full_screen = True  # (True/False)
keyboard = "numpad"  # numpad/mac
# ----------------------------------------------------------------------------

# /// CONFIGURE LOAD/SAVE FILES & DIRECTORIES ///

# create file name
date = sfc.get_date()
time = sfc.get_time()
file_name = f"{subID}_{date}_{time}_pilot01.json"
# set data directory
data_path = os.path.join("..", "data", "pilot01", "raw", file_name)
# ----------------------------------------------------------------------------

# /// CONFIGURE STIMULUS PARAMETERS AND INPUTS ///

# initialize the display and the keyboard
REF_RATE = 60

# configure the monitor and the stimulus window
mon = sfc.config_mon_dell()
win = sfc.config_win(mon=mon, fullscr=full_screen)
sfc.test_refresh_rate(win, REF_RATE)

# fixation cross
FIX_SIZE = .7
FIX_X = 0
FIX_Y = 0

INSTRUCT_DUR = REF_RATE  # duration of the instruction period [frames]

command_keys = {"quit_key": "escape", "response_key": ["left", "right"]}

# size [deg]
size_factor = 2.2
IMAGE_SIZE = np.array([size_factor, size_factor])

REL_IMAGE_POS0_X = FIX_X
REL_IMAGE_POS0_Y = FIX_Y

IRR_IMAGE_RHO = 3
IRR_IMAGE_THETA_deg = np.linspace(22.5, 360 + 22.5, 9)
IRR_IMAGE_THETA_deg = np.delete(IRR_IMAGE_THETA_deg, -1)
IRR_IMAGE_THETA = IRR_IMAGE_THETA_deg * (2 * np.pi) / 360
IRR_IMAGE_X, IRR_IMAGE_Y = pol2cart(IRR_IMAGE_RHO, IRR_IMAGE_THETA)

# potential gap durations (0.5 to 1 sec)
gap_dur_list = range(int(REF_RATE / 2), int(REF_RATE / 1) + 1, 1)

# define a timer to measure the change-detection reaction time
timer = core.Clock()

# # show a message before the block begins
# sfc.block_msg(win, iblock, N_BLOCKS, command_keys)

# hide the cursor
mouse = event.Mouse(win=win, visible=False)

# create an equal number of trials per condition in current block
n_trials_per_cnd = int(N_TRIALS / 4)
cnd_array = np.hstack([np.ones(n_trials_per_cnd, dtype=int) * 1,
                       np.ones(n_trials_per_cnd, dtype=int) * 2,
                       np.ones(n_trials_per_cnd, dtype=int) * 3,
                       np.ones(n_trials_per_cnd, dtype=int) * 4])
np.random.shuffle(cnd_array)
# ----------------------------------------------------------------------------

# /// TRIAL BEGINS ///

i_keypress = 0
iblock = 0

for itrial in range(N_TRIALS):

    # pre-allocate variables
    # pressed_key = [np.nan]
    response_time = [np.nan]

    # --------------------------------
    # /// set up the stimulus behavior in current trial

    # randomly decide on gap duration
    gap_dur = random.choice(gap_dur_list)
    # extract current condition
    cnd = cnd_array[itrial]

    # --------------------------------
    # set image properties and load

    if cnd == 1:
        i_image_rel = 1
        i_image_irr = 1
    elif cnd == 2:
        i_image_rel = 1
        i_image_irr = 2
    elif cnd == 3:
        i_image_rel = 2
        i_image_irr = 1
    elif cnd == 4:
        i_image_rel = 2
        i_image_irr = 2
    else:
        i_image_rel = None
        i_image_irr = None

    image_directory_rel = os.path.join("image", f"im{i_image_rel}.png")
    image_directory_irr = os.path.join("image", f"im{i_image_irr}.png")

    image_directory_cue1 = os.path.join("image", "im1.png")
    image_directory_cue2 = os.path.join("image", "im2.png")

    # load image
    rel_image = visual.ImageStim(win,
                                 image=image_directory_rel,
                                 size=IMAGE_SIZE,
                                 opacity=1,
                                 pos=(REL_IMAGE_POS0_X, REL_IMAGE_POS0_Y))

    # --------------------------------
    # /// load irrelevant image(s)

    irr_image11 = visual.ImageStim(win,
                                   image=image_directory_irr,
                                   pos=(IRR_IMAGE_X[0],
                                        IRR_IMAGE_Y[0]),
                                   size=IMAGE_SIZE)
    irr_image12 = visual.ImageStim(win,
                                   image=image_directory_irr,
                                   pos=(IRR_IMAGE_X[1],
                                        IRR_IMAGE_Y[1]),
                                   size=IMAGE_SIZE)
    irr_image13 = visual.ImageStim(win,
                                   image=image_directory_irr,
                                   pos=(IRR_IMAGE_X[2],
                                        IRR_IMAGE_Y[2]),
                                   size=IMAGE_SIZE)
    irr_image14 = visual.ImageStim(win,
                                   image=image_directory_irr,
                                   pos=(IRR_IMAGE_X[3],
                                        IRR_IMAGE_Y[3]),
                                   size=IMAGE_SIZE)

    irr_image15 = visual.ImageStim(win,
                                   image=image_directory_irr,
                                   pos=(IRR_IMAGE_X[4],
                                        IRR_IMAGE_Y[4]),
                                   size=IMAGE_SIZE)
    irr_image16 = visual.ImageStim(win,
                                   image=image_directory_irr,
                                   pos=(IRR_IMAGE_X[5],
                                        IRR_IMAGE_Y[5]),
                                   size=IMAGE_SIZE)
    irr_image17 = visual.ImageStim(win,
                                   image=image_directory_irr,
                                   pos=(IRR_IMAGE_X[6],
                                        IRR_IMAGE_Y[6]),
                                   size=IMAGE_SIZE)
    irr_image18 = visual.ImageStim(win,
                                   image=image_directory_irr,
                                   pos=(IRR_IMAGE_X[7],
                                        IRR_IMAGE_Y[7]),
                                   size=IMAGE_SIZE)
    # --------------------------------
    # /// load cue images
    cue_image1_xpos = (-20, -10)
    cue_image2_xpos = (+20, -10)
    cue_image1 = visual.ImageStim(win,
                                  image=image_directory_cue2,
                                  pos=cue_image1_xpos,
                                  size=IMAGE_SIZE)
    cue_image2 = visual.ImageStim(win,
                                  image=image_directory_cue1,
                                  pos=cue_image2_xpos,
                                  size=IMAGE_SIZE)

    # --------------------------------
    # /// run the stimulus

    if itrial % n_trials_per_block == 0:
        # message screen
        iblock += 1
        sfc.block_msg(win, iblock, nblocks, command_keys)

    # gap period
    for igap in range(gap_dur):
        win.flip()

    timer.reset()

    # draw relevant image
    rel_image.draw()
    # draw fixation mark
    sfc.draw_fixdot(win=win, size=FIX_SIZE,
                    pos=(FIX_X, FIX_Y))
    # draw irrelevant images
    irr_image11.draw()
    irr_image12.draw()
    irr_image13.draw()
    irr_image14.draw()
    irr_image15.draw()
    irr_image16.draw()
    irr_image17.draw()
    irr_image18.draw()
    # draw cue images
    # cue_image1.draw()
    # cue_image2.draw()

    win.flip()

    pressed_key = event.waitKeys(keyList=["escape", "left", "right"])

    i_keypress = i_keypress + 1

    # check input keys
    if pressed_key[0] in command_keys['quit_key']:
        core.quit()
    if pressed_key[0] in command_keys['response_key']:
        # calculate response time upon a valid key press
        response_time = timer.getTime()
        response_time = round(response_time * 1000)

    # --------------------------------
    # /// prepare data for saving

    # create a dictionary of variables to be saved
    trial_dict = {'trial_num': itrial+1,
                  'condition_num': cnd,
                  'rel_image': i_image_rel,
                  'irr_image': i_image_irr,
                  'rt': response_time,
                  'response': pressed_key}

    # convert to data frame
    dfnew = pd.DataFrame(trial_dict)
    # if not first trial, load the existing data frame and concatenate
    if i_keypress > 1:
        df = pd.read_json(data_path)
        dfnew = pd.concat([df, dfnew], ignore_index=True)
    # save the dataframe
    dfnew.to_json(data_path)
# --------------------------------

win.close()

# --------------------------------
# quick analysis
correct_blue = (dfnew.rel_image == 1) & (dfnew.response == 'right')
correct_red = (dfnew.rel_image == 2) & (dfnew.response == 'left')
correct_all = correct_blue | correct_red
error_rate = 1 - (np.sum(correct_all) / correct_all.shape)

print("=================================")
print(f"Average response time: {dfnew.rt.mean()} ms")
print(f"Error rate: {int(error_rate*100)} %")
print("=================================")
