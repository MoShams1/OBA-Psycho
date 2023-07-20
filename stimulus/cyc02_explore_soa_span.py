"""
Mo Shams <MShamsCBR@gmail.com>
June 2023
---

The subject's task is to decide which of the two peripheral images appeared
first.

20 repetitions
9 SOAs

"""

import os
import warnings
import numpy as np
import pandas as pd
from psychopy import visual, event, core
from lib import config_visual as cvis, timestamp, keymouse

# ----------------------------------------------------------------------------
# turn off Numpy's FutureWarning
warnings.simplefilter(action='ignore', category=FutureWarning)
# ----------------------------------------------------------------------------

# /// GENERAL SETTINGS ///

subID = '0012'
rep_per_cnd = 20  # repetition per condition
full_screen = True
running_device = 'linux'  # 'linux' or 'mac'

n_cnds = 13
n_trials = rep_per_cnd * n_cnds
frame_rate = 60
# ----------------------------------------------------------------------------

# /// SET UP DIRECTORY PATHS ///

save_folder = os.path.join('..', 'data', 'cyc02')
image_folder = os.path.join('image', 'source_cyc02')

save_path = \
    os.path.join(save_folder,
                 f"{subID}_soa_{timestamp.getdate()}_"
                 f"{timestamp.gettime()}.json")
# ----------------------------------------------------------------------------

# /// CONFIGURE VISUAL OBJECTS ///

# /// frame rate downsampling
# division by 60 to obtain 60 Hz (16.67 ms per frame) regardless of actual
# frame rate
frame_rate_rep = int(frame_rate / 60)
practical_fr = int(frame_rate / frame_rate_rep)

# /// background
bg_color = [0, 0, 0]

# /// temporal gap
# sec x Hz = frames
gap_dur_arr = np.round(np.arange(1, 1.5, .1) * practical_fr)
gap_dur_arr = gap_dur_arr.astype(int)

# /// fixation dot
fixdot_size = .7
fixdot_pos = (0, 0)
fixdot_color = 'black'
fixdot_dur = 1 * practical_fr  # sec x Hz = frames

# /// image
im_size = 2
im_ecc = 8
im_opac = .2
im_dur = int(.2 * practical_fr)  # in frames
im1_frames = np.round(np.arange(1, 1.5, .1) * practical_fr)
im1_frames = im1_frames.astype(int)
# ----------------------------------------------------------------------------

# # /// CONFIGURE MONITOR AND SCREEN ///

if running_device == 'linux':
    mon = cvis.configmon_dell()
    win = cvis.configwin(mon=mon, fullscr=full_screen, color=bg_color)
else:
    mon = cvis.configmon_macair()
    win = cvis.configwin_macair(mon=mon, fullscr=full_screen, color=bg_color)
cvis.test_framerate(win=win, nominal_fr=frame_rate)
# ----------------------------------------------------------------------------

# /// CONDITIONING ///

ind_cnd = np.arange(n_trials)
np.random.shuffle(ind_cnd)

# soa array
soa_array = np.repeat(np.arange(-(n_cnds-1)/2, (n_cnds-1)/2+1, 1),
                      rep_per_cnd)[ind_cnd]

keypress_flag = False

timer = core.Clock()
delta_t = None
# ----------------------------------------------------------------------------

# /// START TRIAL ///

for itrial in range(n_trials):

    # -------------------------------

    # /// set up trial variables

    im1_frame = np.random.choice(im1_frames)
    im2_frame = im1_frame + int(np.absolute(soa_array[itrial]))

    im1_pos = im_ecc if soa_array[itrial] > 0 else -im_ecc
    im2_pos = -im1_pos

    # decide on annulus type
    im_directory = os.path.join(image_folder, 'ring_noise.png')
    im1 = visual.ImageStim(win,
                           image=im_directory,
                           size=im_size,
                           opacity=im_opac,
                           pos=(im1_pos, 0))

    im2 = visual.ImageStim(win,
                           image=im_directory,
                           size=im_size,
                           opacity=im_opac,
                           pos=(im2_pos, 0))

    # decide on gap durations
    firstgap_dur = np.random.choice(gap_dur_arr)
    # -------------------------------

    # /// run task

    # gap period
    for frame in range(firstgap_dur):
        win.flip()

    # stimulus onsets period
    for iframe in range(im2_frame + im_dur):
        cvis.addfixdot(win=win, size=fixdot_size, pos=fixdot_pos,
                       color=fixdot_color)
        if iframe >= im1_frame:
            im1.draw()
            if iframe == im1_frame:
                timer.reset()
        if iframe >= im2_frame:
            im2.draw()
            if iframe == im2_frame:
                delta_t = np.round(timer.getTime() * 1000)

        win.flip()

    win.flip()
    cvis.addfixdot(win=win, size=fixdot_size, pos=fixdot_pos,
                   color=fixdot_color)
    win.flip()
    keymouse.escape_session()
    pressed_key = event.waitKeys(keyList=['left', 'right', 'escape'])

    # check input keys
    if 'escape' in pressed_key:
        core.quit()

    # gap period
    for frame in range(int(.5 * practical_fr)):
        cvis.addfixdot(win=win, size=fixdot_size, pos=fixdot_pos,
                       color='darkgreen')
        win.flip()

    # -------------------------------

    # /// save data
    # create a dictionary
    trial_dict = {
        'trial_num': [itrial + 1],
        'frame_rate': [frame_rate],
        'im1_pos': [im1_pos],
        'response': [pressed_key],
        'soa_cnd': [soa_array[itrial]],
        'soa_ms': [delta_t]
    }

    # convert to data frame
    dfnew = pd.DataFrame(trial_dict)

    # if first trial create a file, else load and add the new data frame
    if itrial == 0:
        dfnew.to_json(save_path)
    else:
        df = pd.read_json(save_path)
        dfnew = pd.concat([df, dfnew], ignore_index=True)
        dfnew.to_json(save_path)

win.close()
