"""
Mo Shams <MShamsCBR@gmail.com>
June 2023
---

The subject's task is to decide which of the two peripheral images appeared
first.

repetition per condition: 48
number of SOA conditions: 7
max SOA: 150 ms (9 frames)

"""

import os
import warnings
import numpy as np
import pandas as pd
from psychopy import visual, event, core
from lib import config_visual as cvis, timestamp, keymouse
from lib import stimulus_flow_control as sfc


# ----------------------------------------------------------------------------


def deg2rad(angle):
    return angle / 360 * 2 * np.pi


def rad2deg(angle):
    return angle / (2 * np.pi) * 360


def pol2cart(rho, phi):
    phi = deg2rad(phi)
    x_cart = rho * np.cos(phi)
    y_cart = rho * np.sin(phi)
    return x_cart, y_cart


def cart2pol(x_cart, y_cart):
    rho = np.sqrt(x_cart ** 2 + y_cart ** 2)
    phi = np.arctan2(y_cart, x_cart)
    phi = rad2deg(phi)
    return rho, phi


# ----------------------------------------------------------------------------
# turn off Numpy's FutureWarning
warnings.simplefilter(action='ignore', category=FutureWarning)
# ----------------------------------------------------------------------------

# /// GENERAL SETTINGS ///

subID = 'MS01_rep24_log_accuracy'
soa_corr_factor = 0
# n_soa = 7
n_soa = 8
# abs_soa_dt = 9  # frames
abs_soa_dt = 8  # frames
# rep_per_cnd = 48  # repetition per condition (factor of 4)
rep_per_cnd = 24  # repetition per condition (factor of 4)
n_blocks = 8
full_screen = True
running_device = 'linux'  # 'linux' or 'mac'

n_soa_trials = rep_per_cnd * n_soa
n_all_trials = round(n_soa_trials * 1)  # training SOA task
# n_all_trials = round(n_soa_trials * 1000)  # training Attention task
# n_all_trials = n_soa_trials + 88  # dual task (75% SOA; 25% att)
n_att_trials = n_all_trials - n_soa_trials
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
fixdot_size = .5
fixdot_pos = (0, 0)
fixdot_color = 'black'
fixdot_dur = 1 * frame_rate  # sec x Hz = frames

# /// image
im_size = 2
im_ecc = 6
im_opac = .5
im_dur = int(.1 * frame_rate)
im1_frames = np.round(np.arange(1, 1.5, .1) * frame_rate)
im1_frames = im1_frames.astype(int)
tilt_dur = int(.25 * frame_rate)

soa_response_grace_time = 300  # ms
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

n_cue_blocks = 4

ind_shuffle = np.arange(int(round(n_all_trials / n_cue_blocks)))

tail = np.full(int(n_att_trials / n_cue_blocks), np.nan)

# soa array
# soa_array_base = np.linspace(-abs_soa_dt, abs_soa_dt, n_soa) + soa_corr_factor
soa_array_base = np.array([-8, -4, -2, -1, 1, 2, 4, 8]) + soa_corr_factor
soa_array_quad = np.repeat(soa_array_base, int(rep_per_cnd / n_cue_blocks))

# congurency array
cong_array_base = [-1, 1]
cong_array_quad = np.tile(np.repeat(cong_array_base,
                                    int(rep_per_cnd / n_cue_blocks / 2)),
                          n_soa)

np.random.shuffle(ind_shuffle)
soa_array_quad1 = np.concatenate((soa_array_quad, tail))[ind_shuffle]
cong_array_quad1 = np.concatenate((cong_array_quad, tail))[ind_shuffle]
np.random.shuffle(ind_shuffle)
soa_array_quad2 = np.concatenate((soa_array_quad, tail))[ind_shuffle]
cong_array_quad2 = np.concatenate((cong_array_quad, tail))[ind_shuffle]
np.random.shuffle(ind_shuffle)
soa_array_quad3 = np.concatenate((soa_array_quad, tail))[ind_shuffle]
cong_array_quad3 = np.concatenate((cong_array_quad, tail))[ind_shuffle]
np.random.shuffle(ind_shuffle)
soa_array_quad4 = np.concatenate((soa_array_quad, tail))[ind_shuffle]
cong_array_quad4 = np.concatenate((cong_array_quad, tail))[ind_shuffle]
soa_array = np.concatenate((soa_array_quad1,
                            soa_array_quad2,
                            soa_array_quad3,
                            soa_array_quad4))
cong_array = np.concatenate((cong_array_quad1,
                             cong_array_quad2,
                             cong_array_quad3,
                             cong_array_quad4))

# indicate which task should be shown at each trial
att_task = np.isnan(soa_array)
soa_task = ~att_task

# cue array (1: face, 2: house)
image_block_choice = np.random.choice([0, 1])
if image_block_choice:
    cue_array = np.repeat(np.tile(['f', 'h'], 2),
                          int(n_all_trials / n_cue_blocks))
else:
    cue_array = np.repeat(np.tile(['h', 'f'], 2),
                          int(n_all_trials / n_cue_blocks))

keypress_flag = False

timer = core.Clock()
delta_t = None

resp_eval_arr = []
run_perf = 80  # set expected accuracy as initial value
tilt_mag = 30  # set initial tilt

# set when to pause the task for rest
pause_trials = np.linspace(0, n_all_trials, n_blocks + 1)
pause_trials = pause_trials[:-1]
pause_counter = 0
# ----------------------------------------------------------------------------

# /// START TRIAL ///

for itrial in range(n_all_trials):

    if itrial == int(pause_trials[pause_counter]):
        sfc.run_pause_screen(win, pause_counter + 1, n_blocks)
        if pause_counter < n_blocks - 1:
            pause_counter += 1

    # -------------------------------
    # decide on when the tilt/flash should occur
    event_time_s = np.random.choice(np.arange(1, 2.1, .1))
    event_frame = int(event_time_s * frame_rate)

    # decide on tilt magnitude
    if len(resp_eval_arr) >= 10:
        tilt_change = sfc.cal_next_tilt(goal_perf=80, run_perf=run_perf)
        tilt_mag = int(tilt_mag + tilt_change)
    # take care of saturated scenarios
    if tilt_mag > 99:
        tilt_mag = 99
    elif tilt_mag < 7:
        tilt_mag = 7

    # load tilted image
    tilt_cat = np.random.choice(['f', 'h'])
    tilt_dir = np.random.choice(['CW', 'CCW'])
    im_directory = os.path.join(image_folder, 'cyc03_tilted',
                                f'{tilt_cat}1_tilt{tilt_mag}_{tilt_dir}.png')
    if tilt_cat == 'h':
        tilt_opacity = .7
    else:
        tilt_opacity = .5

    tilt = visual.ImageStim(win,
                            image=im_directory,
                            size=im_size,
                            opacity=tilt_opacity,
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
                             opacity=.7,
                             pos=(0, 0))

    # load cue/target image
    if cue_array[itrial] == 'f':
        cue = f_cnt
    else:
        cue = h_cnt

    im1_pos = np.nan
    im2_pos = np.nan

    im1_frame = np.nan
    im2_frame = np.nan

    im1_theta = np.nan
    im2_theta = np.nan

    tilt_frame = np.nan

    # if in soa task
    if soa_task[itrial]:
        # set image times
        im1_frame = event_frame
        im2_frame = im1_frame + int(soa_array[itrial])
        # set image positions
        im1_theta = np.random.choice(
            np.arange(180 - 30, 180 + 30 + 1))  # im1 left
        im2_theta = im1_theta + 180  # im2 right
        im1_pos = pol2cart(im_ecc, im1_theta)
        im2_pos = pol2cart(im_ecc, im2_theta)

        # load peripheral images
        if cong_array[itrial] == 1:
            per_im = cue_array[itrial]
        else:
            per_im = np.setdiff1d(['f', 'h'], cue_array[itrial])[0]

        im_directory = os.path.join(image_folder, 'cyc03_source',
                                    f'{per_im}1.png')
        im1_per = visual.ImageStim(win,
                                   image=im_directory,
                                   size=im_size,
                                   opacity=im_opac,
                                   pos=im1_pos)
        im2_per = visual.ImageStim(win,
                                   image=im_directory,
                                   size=im_size,
                                   opacity=im_opac,
                                   pos=im2_pos)

    # -------------------------------

    # /// run task

    tilt_seen = False
    pressed_key = []
    correct_resp = np.nan
    soa_rt = np.nan
    soa_resp = np.nan
    soa_resp_eval = np.nan

    # gap period
    for frame in range(int(.5 * frame_rate)):
        win.flip()

    # cue period
    # for frame in range(int(.5 * frame_rate)):
    for frame in range(int(.2 * frame_rate)):
        cvis.addprobe(win, radius=1.5, color=[-.5, -.5, -.5], pos=(0, 0))
        cue.draw()
        win.flip()

    # gap period
    # for frame in range(int(.5 * frame_rate)):
    for frame in range(int(0 * frame_rate)):
        win.flip()

    # overlap period
    # for frame in range(int(1 * frame_rate)):
    for frame in range(int(.5 * frame_rate)):
        # add central images
        h_cnt.draw()
        f_cnt.draw()
        # add fixation mark
        cvis.addfixdot(win=win, size=fixdot_size, pos=fixdot_pos,
                       color=fixdot_color)
        win.flip()

    # soa task
    if soa_task[itrial]:
        print('=================================')
        print(f'*** im1 frame: {im1_frame} ***')
        print(f'*** im2 frame: {im2_frame} ***')
        for iframe in range(max(im1_frame, im2_frame) + im_dur):
            # add central images
            h_cnt.draw()
            f_cnt.draw()
            # add fixation mark
            cvis.addfixdot(win=win, size=fixdot_size, pos=fixdot_pos,
                           color=fixdot_color)
            # flash peripheral images
            if (iframe >= im1_frame) and (iframe <= im1_frame + im_dur):
                im1_per.draw()
            if (iframe >= im2_frame) and (iframe <= im2_frame + im_dur):
                im2_per.draw()

            win.flip()

        # response period
        timer.reset()
        cvis.addfixdot(win=win, size=fixdot_size * 1.5, pos=fixdot_pos,
                       color=fixdot_color)
        win.flip()
        keymouse.escape_session()
        pressed_key = event.waitKeys(keyList=['left', 'right', 'escape'])

        # check input keys
        if 'escape' in pressed_key:
            core.quit()
        if ('left' in pressed_key) or ('right' in pressed_key):
            soa_rt = round(timer.getTime() * 1000)
            if 'left' in pressed_key:
                soa_resp = 'l'
            elif 'right' in pressed_key:
                soa_resp = 'r'
            else:
                soa_resp = np.nan
            print(f'*** Congruency: {cong_array[itrial]}')
            print(f'*** SOA response: {soa_resp} ***')
            print(f'*** SOA RT: {soa_rt} ms ***')
            if (im1_frame > im2_frame) & (soa_resp == 'r'):
                soa_resp_eval = True
                print('*** response eval: correct')
            if (im1_frame < im2_frame) & (soa_resp == 'l'):
                soa_resp_eval = True
                print('*** response eval: correct')
            if (im1_frame > im2_frame) & (soa_resp == 'l'):
                soa_resp_eval = False
                print('*** response eval: wrong')
            if (im1_frame < im2_frame) & (soa_resp == 'r'):
                soa_resp_eval = False
                print('*** response eval: wrong')
            if im1_frame == im2_frame:
                print('*** response eval: ---')

        # feedback period
        # if soa_rt <= soa_response_grace_time:
        #     soa_feedback_color = 'darkgreen'
        # else:
        #     soa_feedback_color = 'darkred'
        if soa_resp_eval:
            soa_feedback_color = 'darkgreen'
        else:
            soa_feedback_color = 'darkred'
        for frame in range(int(.3 * frame_rate)):
            cvis.addfixdot(win=win, size=fixdot_size * 1.5, pos=fixdot_pos,
                           color=soa_feedback_color)
            win.flip()

    if att_task[itrial]:
        tilt_frame = event_frame
        for iframe in range(tilt_frame + att_response_grace_time):
            pressed_key = event.getKeys(keyList=['space', 'escape'])
            if (iframe >= tilt_frame) and (iframe <= tilt_frame + tilt_dur):
                if tilt_cat == 'f':
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
            if 'escape' in pressed_key:
                core.quit()

        # evaluate response
        if (cue_array[itrial] == tilt_cat) and tilt_seen:
            correct_resp = True
            feedback_color = 'darkgreen'
        elif (cue_array[itrial] != tilt_cat) and not tilt_seen:
            correct_resp = True
            feedback_color = 'darkgreen'
        else:
            correct_resp = False
            feedback_color = 'darkred'

        # feedback period
        for frame in range(int(.3 * frame_rate)):
            cvis.addfixdot(win=win, size=fixdot_size * 1.5, pos=fixdot_pos,
                           color=feedback_color)
            win.flip()

        resp_eval_arr.append(correct_resp)
        run_perf = sum(resp_eval_arr[-10:]) / 10 * 100

        print('=================================')
        print(f'cued image: {cue_array[itrial]}')
        print(f'tilted image: {tilt_cat}')
        print(f'tilt magnitude: {tilt_mag}')
        print(f'current eval: {correct_resp}')
        print(f'running performance: {run_perf}')
        print(f'key pressed?: {tilt_seen}')
        # -------------------------------

    # /// SAVE DATA

    # create a dictionary
    trial_dict = {
        'trial_num': [itrial + 1],
        'frame_rate': [frame_rate],
        'cued_image': [cue_array[itrial]],
        'congruency': [cong_array[itrial]],
        'soa_cnd': [soa_array[itrial]],
        'im1_pos': [im1_pos],
        'im2_pos': [im2_pos],
        'im1_frame': [im1_frame],
        'im2_frame': [im2_frame],
        'flash_dur': [im_dur],
        'soa_rt': [soa_rt],
        'soa_response': [soa_resp],
        'soa_resp_eval': [soa_resp_eval],
        'tilt_image': [tilt_cat],
        'tilt_frame': [tilt_frame],
        'tilt_duration': [tilt_dur],
        'tilt_mag_deg': [tilt_mag / 10],
        'tilt_seen': [tilt_seen],
        'att_corr_resp_flag': [correct_resp]
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
