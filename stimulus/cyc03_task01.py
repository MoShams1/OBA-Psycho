"""
Mo Shams <MShamsCBR@gmail.com>
June 2023
---

The subject's task is to decide which of the two peripheral images appeared
first.

20 repetitions
9 SOAs conditions

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

subID = 'test'
rep_per_cnd = 20  # repetition per condition
full_screen = False
running_device = 'mac'  # 'linux' or 'mac'

n_soa = 9
n_soa_trials = rep_per_cnd * n_soa  # 2/3 of all trials
n_all_trials = int(n_soa_trials * 1.5)
n_att_trials = n_all_trials - n_soa_trials  # 1/3 of all trials
frame_rate = 60
# ----------------------------------------------------------------------------

# /// SET UP DIRECTORY PATHS ///

save_folder = os.path.join('..', 'data', 'cyc03')
image_folder = os.path.join('image')

save_path = \
    os.path.join(save_folder,
                 f"{subID}_soa_{timestamp.getdate()}_"
                 f"{timestamp.gettime()}.json")
# ----------------------------------------------------------------------------

# /// CONFIGURE STIMULUS PARAMETERS ///

# /// background
bg_color = [0, 0, 0]

# /// temporal gap
# sec x Hz = frames
gap_dur_arr = np.round(np.arange(1, 1.5, .1) * frame_rate)
gap_dur_arr = gap_dur_arr.astype(int)

# /// fixation dot
fixdot_size = .7
fixdot_pos = (0, 0)
fixdot_color = 'black'
fixdot_dur = 1 * frame_rate  # sec x Hz = frames

# /// image
im_size = 2
im_ecc = 6
# im_opac = .2
im_opac = .5
im_dur_ms = 200
im_dur = int(im_dur_ms / 1000 * frame_rate)  # in frames
im1_frames = np.round(np.arange(1, 1.5, .1) * frame_rate)
im1_frames = im1_frames.astype(int)
tilt_dur = int(.5 * frame_rate)

att_response_grace_time = int(1 * frame_rate)
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

ind_shuffle = np.arange(n_all_trials)
np.random.shuffle(ind_shuffle)

# soa array
soa_array_base = np.linspace(-20, 20, n_soa)
soa_array = np.repeat(soa_array_base, rep_per_cnd)
tail = np.full(n_att_trials, np.nan)
soa_array = np.concatenate((soa_array, tail))[ind_shuffle]

# indicate which task should be shown at each trial
att_task = np.isnan(soa_array)
soa_task = ~att_task

# cue array (1: face, 2: house)
cue_array = np.repeat(['f', 'h'], int(n_soa_trials / 2))
tail = np.repeat(['f', 'h'], int(n_att_trials / 2))
cue_array = np.concatenate((cue_array, tail))[ind_shuffle]

keypress_flag = False

timer = core.Clock()
delta_t = None
# ----------------------------------------------------------------------------

# /// START TRIAL ///

for itrial in range(n_all_trials):

    # -------------------------------

    # decide on gap period durations
    firstgap_dur = np.random.choice(gap_dur_arr)

    # decide on when the tilt/flash should occur
    event_time_s = np.random.choice(np.arange(0, 1.1, .1))
    event_time = int(event_time_s * frame_rate)

    # load tilted image
    tilt_cat = np.random.choice(['f', 'h'])
    tilt_mag = np.random.choice(range(100))
    tilt_dir = np.random.choice(['CW', 'CCW'])
    im_directory = os.path.join(image_folder, 'cyc03_tilted',
                                f'{tilt_cat}1_tilt{tilt_mag}_{tilt_dir}.png')
    tilt = visual.ImageStim(win,
                            image=im_directory,
                            size=im_size,
                            opacity=.5,
                            pos=(0, 0))

    # load central images
    im_directory = os.path.join(image_folder, 'cyc03_source', 'f1.png')
    f_cnt = visual.ImageStim(win,
                             image=im_directory,
                             size=im_size,
                             opacity=.5,
                             pos=(0, 0))
    im_directory = os.path.join(image_folder, 'cyc03_source', 'h1.png')
    h_cnt = visual.ImageStim(win,
                             image=im_directory,
                             size=im_size,
                             opacity=.5,
                             pos=(0, 0))

    # load cue/target image
    if cue_array[itrial] == 'f':
        cue = f_cnt
    else:
        cue = h_cnt

    # if in soa task
    if soa_task[itrial]:
        # set image times
        im1_frame = event_time
        im2_frame = im1_frame + int(np.absolute(soa_array[itrial]))
        # set image positions
        im1_pos = im_ecc if soa_array[itrial] > 0 else -im_ecc
        im2_pos = -im1_pos

        # load peripheral images
        im_directory = os.path.join(image_folder,  'cyc03_source', 'f1.png')
        im1_per = visual.ImageStim(win,
                                   image=im_directory,
                                   size=im_size,
                                   opacity=im_opac,
                                   pos=(im1_pos, 0))
        im_directory = os.path.join(image_folder,  'cyc03_source', 'f1.png')
        im2_per = visual.ImageStim(win,
                                   image=im_directory,
                                   size=im_size,
                                   opacity=im_opac,
                                   pos=(im2_pos, 0))

    # -------------------------------

    # /// run task

    tilt_seen = False
    correct_resp = np.nan

    # gap period
    for frame in range(int(.5 * frame_rate)):
        win.flip()

    # cue period
    for frame in range(int(1 * frame_rate)):
        cue.draw()
        win.flip()

    # gap period
    for frame in range(int(.5 * frame_rate)):
        win.flip()

    # overlap period
    for frame in range(int(2 * frame_rate)):
        # add central images
        h_cnt.draw()
        f_cnt.draw()
        # add fixation mark
        cvis.addfixdot(win=win, size=fixdot_size, pos=fixdot_pos,
                       color=fixdot_color)
        win.flip()

    # soa task
    if soa_task[itrial]:
        for iframe in range(int(1 * frame_rate)):
            # add central images
            h_cnt.draw()
            f_cnt.draw()
            # add fixation mark
            cvis.addfixdot(win=win, size=fixdot_size, pos=fixdot_pos,
                           color=fixdot_color)
            # flash peripheral images
            if iframe >= im1_frame:
                im1_per.draw()
                # if iframe == im1_frame:
                # timer.reset()
            if iframe >= im2_frame:
                im2_per.draw()
                # if iframe == im2_frame:
                # delta_t = np.round(timer.getTime() * 1000)

            win.flip()

        # response period
        win.flip()
        cvis.addfixdot(win=win, size=fixdot_size, pos=fixdot_pos,
                       color=fixdot_color)
        win.flip()
        keymouse.escape_session()
        pressed_key = event.waitKeys(keyList=['left', 'right', 'escape'])

        # check input keys
        if 'escape' in pressed_key:
            core.quit()

        # feedback period
        for frame in range(int(.5 * frame_rate)):
            cvis.addfixdot(win=win, size=fixdot_size, pos=fixdot_pos,
                           color='darkgreen')
            win.flip()

    if att_task[itrial]:
        tilt_time = event_time
        for iframe in range(tilt_time + att_response_grace_time):
            pressed_key = event.getKeys(keyList=['space', 'escape'])
            if (iframe >= tilt_time) and (iframe <= tilt_time + tilt_dur):
                if cue_array[itrial] == 'f':
                    h_cnt.draw()
                    tilt.draw()
                else:
                    tilt.draw()
                    f_cnt.draw()
            else:
                h_cnt.draw()
                f_cnt.draw()
            cvis.addfixdot(win=win, size=fixdot_size, pos=fixdot_pos,
                           color=fixdot_color)
            win.flip()

            # check input keys
            if 'space' in pressed_key:
                tilt_seen = True
            # evaluate response
            if (cue_array[itrial] == tilt_cat) and tilt_seen:
                correct_resp = True
            else:
                correct_resp = False

            if 'escape' in pressed_key:
                core.quit()

    # -------------------------------

    # /// SAVE DATA

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
