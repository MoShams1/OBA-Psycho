import random
import numpy as np
from psychopy import event, core


def escape_session():
    exit_key = event.getKeys(keyList=['escape'])
    if 'escape' in exit_key:
        core.quit()


def get_mouseclick(win):
    ms_corrcoef = 2
    ms_posx = random.choice(range(-3, 3 + 1))
    ms_posy = random.choice(range(-1, 1 + 1))
    mouse = event.Mouse(win=win, visible=True,
                        newPos=[ms_posx * ms_corrcoef,
                                ms_posy * ms_corrcoef])
    while not mouse.getPressed()[0]:
        escape_session()  # force exit with 'escape' button
        win.flip()
    while mouse.getPressed()[0]:
        pass
    click_loc = mouse.getPos() / ms_corrcoef
    click_loc = [round(item, 2) for item in click_loc]
    mouse.setVisible(False)
    return click_loc


def get_mouseclick_exp5(win, pos):
    ms_corrcoef = 2
    pos = np.array(pos) * ms_corrcoef
    mouse = event.Mouse(win=win, visible=True, newPos=pos)
    while not mouse.getPressed()[0]:
        escape_session()  # force exit with 'escape' button
        win.flip()
    while mouse.getPressed()[0]:
        pass
    click_loc = mouse.getPos() / ms_corrcoef
    click_loc = [round(item, 2) for item in click_loc]
    mouse.setVisible(False)
    return click_loc


def get_mouseclick11(win, ms_corrcoef=1):
    ms_posx = random.choice(range(-3, 3 + 1))
    ms_posy = random.choice(range(-1, 1 + 1))
    mouse = event.Mouse(win=win, visible=True,
                        newPos=[ms_posx * ms_corrcoef,
                                ms_posy * ms_corrcoef])
    while not mouse.getPressed()[0]:
        escape_session()  # force exit with 'escape' button
        win.flip()
    while mouse.getPressed()[0]:
        pass
    click_loc = mouse.getPos() / ms_corrcoef
    click_loc = [round(item, 2) for item in click_loc]
    mouse.setVisible(False)
    return click_loc
