"""
Mo Shams <MShamsCBR@gmail.com>
October 2023
---

The subject should vary the tempral offset between the two flashes until
they perceive simultanity. This process repeats 10 times.

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


def show_delta_t(dt):
    msg = f'delta_t: {dt}'
    message = visual.TextStim(win,
                              text=msg, color='black', height=.3,
                              alignText='center', pos=(0, 5))
    message.draw()


def check_input(dt, itrial, delta_t_all, confirm_old_state):
    keymouse.escape_session()
    key = event.getKeys(keyList=['left', 'right', 'return'])
    if 'left' in key:
        dt -= 1
    if 'right' in key:
        dt += 1
    if 'return' in key:
        delta_t_all[itrial] = delta_t
        print(f'dt array: {delta_t_all}')
        confirmation = True
    else:
        confirmation = confirm_old_state
    return dt, confirmation


# ----------------------------------------------------------------------------
# turn off Numpy's FutureWarning
warnings.simplefilter(action='ignore', category=FutureWarning)
# ----------------------------------------------------------------------------

# /// GENERAL SETTINGS ///

subID = 'MS01'
n_soa = 9
abs_soa_dt = 9  # frames
rep_per_cnd = 12  # repetition per condition (factor of 4)
full_screen = False
running_device = 'linux'  # 'linux' or 'mac'

frame_rate = 60
# ----------------------------------------------------------------------------

# /// SET UP DIRECTORY PATHS ///

image_folder = os.path.join('image')

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
im_dur = int(.1 * frame_rate)
im1_frames = np.round(np.arange(1, 1.5, .1) * frame_rate)
im1_frames = im1_frames.astype(int)
tilt_dur = int(.25 * frame_rate)

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

ntrials = 10
delta_t_all = np.full(ntrials, np.nan)

for itrial in range(ntrials):

    print('=================================')
    print(f'Trial: {itrial + 1}')

    # gap period
    for frame in range(int(2 * frame_rate)):
        win.flip()

    # set image positions
    im1_theta = np.random.choice(np.arange(135, 135 + 90 + 1))  # im1 left
    im2_theta = im1_theta + 180  # im2 right
    im1_pos = pol2cart(im_ecc, im1_theta)
    im2_pos = pol2cart(im_ecc, im2_theta)

    # load peripheral images
    im_directory = os.path.join(image_folder, 'cyc03_source', 'f1.png')
    im1_per = visual.ImageStim(win,
                               image=im_directory,
                               size=im_size,
                               opacity=im_opac,
                               pos=im1_pos)
    im_directory = os.path.join(image_folder, 'cyc03_source', 'f1.png')
    im2_per = visual.ImageStim(win,
                               image=im_directory,
                               size=im_size,
                               opacity=im_opac,
                               pos=im2_pos)

    # -------------------------------

    # /// run task

    delta_t = np.random.choice(np.arange(-9, 9 + 1, 1))
    confirmed = False

    while True:

        # decide on when the tilt/flash should occur
        event_time_s = np.random.choice(np.arange(0, 1.1, .1))

        # set image times
        im1_frame = int(event_time_s * frame_rate)
        im2_frame = im1_frame + delta_t
        pressed_key = []

        # gap period
        for frame in range(int(1 * frame_rate)):
            cvis.addfixdot(win=win, size=fixdot_size, pos=fixdot_pos,
                           color=fixdot_color)
            delta_t, confirmed = check_input(delta_t, itrial, delta_t_all,
                                             confirmed)
            show_delta_t(delta_t)
            win.flip()
        if confirmed:
            print(f'{confirmed}')
            break

        for iframe in range(max(im1_frame, im2_frame) + im_dur):
            # add fixation mark
            cvis.addfixdot(win=win, size=fixdot_size, pos=fixdot_pos,
                           color=fixdot_color)
            # flash peripheral images
            if (iframe >= im1_frame) and (iframe <= im1_frame + im_dur):
                im1_per.draw()
            if (iframe >= im2_frame) and (iframe <= im2_frame + im_dur):
                im2_per.draw()
            delta_t, confirmed = check_input(delta_t, itrial, delta_t_all,
                                             confirmed)
            show_delta_t(delta_t)
            win.flip()
        if confirmed:
            print(f'{confirmed}')
            break

        # check input keys
        delta_t_old = delta_t
        delta_t, confirmed = check_input(delta_t, itrial, delta_t_all,
                                         confirmed)
        show_delta_t(delta_t)
        win.flip()
        if confirmed:
            print(f'{confirmed}')
            break

print('\n\n')
print('************************')
print(f'Avg. SOA offset: {np.round(np.mean(delta_t_all))}')
print('************************')
print('\n')
