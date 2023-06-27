import numpy as np
from psychopy import monitors, visual, event, core


def configmon_imac():
    monitor = monitors.Monitor('prim_mon', width=54.7, distance=57)
    monitor.setSizePix([2240, 1260])
    return monitor


def configmon_macair():
    monitor = monitors.Monitor('prim_mon', width=33.78, distance=57)
    monitor.setSizePix([1440, 900])
    return monitor


def configmon_dell():
    monitor = monitors.Monitor('prim_mon', width=52, distance=70)
    monitor.setSizePix([1920, 1080])
    return monitor


def configwin(mon, fullscr, color, screen=0):
    if fullscr:
        win = visual.Window(monitor=mon, screen=screen, units='deg',
                            pos=[0, 0], fullscr=fullscr, color=color)
    else:
        win = visual.Window(monitor=mon, units='deg',
                            size=[1920, 700], pos=[0, 0],
                            color=color)
    win.mouseVisible = False
    return win


def configwin_macair(mon, fullscr, color, screen=0):
    if fullscr:
        win = visual.Window(monitor=mon, screen=screen, units='deg',
                            pos=[0, 0], fullscr=fullscr, color=color)
    else:
        win = visual.Window(monitor=mon, units='deg',
                            size=[1440, 450], pos=[0, 0],
                            color=color)
    win.mouseVisible = False
    return win


def test_framerate(win, nominal_fr):
    actual_fr = win.getActualFrameRate(nIdentical=10, nMaxFrames=100,
                                       nWarmUpFrames=10, threshold=1)
    # if actual_fr is not None:
    #     actual_fr = round(actual_fr, 2)
    # print('\n=======================================================')
    # print(f"Nominal frame rate:  {nominal_fr} Hz")
    # print(f"Measured frame rate: {actual_fr} Hz\n")


def addfixdot(win, size=1, pos=(0, 0), color='black'):
    fixdot = visual.TextStim(win=win, text='+', height=size, pos=pos,
                             color=color)
    fixdot.draw()


def addprobe(win, radius, color, pos):
    probe = visual.Circle(win, radius=radius, fillColor=color, pos=pos)
    probe.draw()


def addprobe2(win, radius, color, pos):
    probe_ring = visual.Circle(win, radius=radius*1.2, fillColor='black',
                               pos=pos)
    probe = visual.Circle(win, radius=radius, fillColor=color, pos=pos)
    probe_ring.draw()
    probe.draw()


def addbar(win, size, color, theta, radius):
    # convert degree to radian
    theta_rad = (theta / 360) * 2 * np.pi
    # calculate the bar position
    posx = radius * np.cos(theta_rad)
    posy = radius * np.sin(theta_rad)
    # convert theta to the orientation convention of Pcyhopy
    orientation = (360 - theta) + 90
    bar = visual.Rect(win=win, size=size, fillColor=color,
                      ori=orientation, pos=(posx, posy),
                      lineWidth=.3)
    # cover = visual.Rect(win=win, size=width, fillColor=color, pos=pos,
    #                     width=line_width, ori=45)
    # inner_frame = visual.Rect(win=win, size=[width[0] - line_width,
    #                                          width[1] - line_width],
    #                           fillColor=fillcolor, pos=pos)
    # outer_frame.draw()
    bar.draw()


def addsquare(win, width, color, fillcolor, pos, line_width=0.2):
    outer_frame = visual.Rect(win=win, size=width, fillColor=color, pos=pos)
    inner_frame = visual.Rect(win=win, size=width - line_width,
                              fillColor=fillcolor, pos=pos)
    outer_frame.draw()
    inner_frame.draw()


def addline(win, size, color, pos, ori=0):
    line = visual.Rect(win=win, size=size, fillColor=color,
                       pos=pos, ori=ori)
    line.draw()


def gengrid(width, n, movpos1, movpos2):
    x = np.linspace(-width / 2, width / 2, n[0])
    y = np.linspace(-width / 2, width / 2, n[1])
    # move to moving object's starting position
    y = y + movpos1[1]
    # move horizontally to moving object's midway then push it back to the
    # trailing edge to give more room to the
    # more important leading edge (offset)
    offset = 1.5
    midwayx = (movpos1[0] + movpos2[0]) / 2
    x = x + midwayx + offset
    xv, yv = np.meshgrid(x, y)
    return xv, yv


def gengrid2(width, n, movpos1, movpos2):
    x = np.linspace(-width[0] / 2, width[0] / 2, n[0])
    y = np.linspace(-width[1] / 2, width[1] / 2, n[1])
    # move to moving object's starting position
    y = y + movpos1[1]
    # move horizontally to moving object's midway then push it back to the
    # trailing edge to give more room to the
    # more important leading edge (offset)
    offset = 2.5
    midwayx = (movpos1[0] + movpos2[0]) / 2
    x = x + midwayx + offset
    xv, yv = np.meshgrid(x, y)
    return xv, yv


def gengrid3(width, n, pos, pos_offset=0):
    x = np.linspace(-width / 2, width / 2, n[0])
    y = np.linspace(-width / 2, width / 2, n[1])
    # move to desired position
    x = x + pos[0]
    y = y + pos[1]
    # generate meshgrid
    xv, yv = np.meshgrid(x, y)
    return xv, yv


def showgrid(win, grid_n, grid_x_tr, grid_y_tr):
    for i in range(grid_n[1]):
        for j in range(grid_n[0]):
            probe = \
                visual.Circle(win, radius=.05,
                              pos=(grid_x_tr[i, j],
                                   grid_y_tr[i, j]))
            probe.draw()


def showgrid_exp6(win, x, y):
    for i in range(len(x)):
        probe = visual.Circle(win, radius=.05, pos=(x[i], y))
        probe.draw()


def infoscreen_exp1(win, iblock, cmd, nblocks):
    msg = f"<<<   BLOCK {iblock}/{nblocks}   >>>" \
          f"\n\nReady to proceed?"
    message = visual.TextStim(win,
                              text=msg, color='white', height=.5,
                              alignText='center')
    message.pos = (0, 1)
    message.draw()

    commands = '[Escape]: Quit\t[Space]: OK'
    cmnd_text = visual.TextStim(win,
                                text=commands, color='white', height=.5,
                                alignText='center')
    cmnd_text.pos = (0, -2)
    cmnd_text.draw()

    win.flip()
    pressed_key = event.waitKeys(keyList=list(cmd.values()))
    if cmd['quit_key'] in pressed_key:
        core.quit()
    elif cmd['response_key'] in pressed_key:
        pass


def infoscreen_exp5(win, cmd):
    msg = f"<<<   Locate the probe!   >>>" \
          f"\n\n\nReady to proceed?"
    message = visual.TextStim(win,
                              text=msg, color='white', height=.5,
                              alignText='center')
    message.pos = (0, 1)
    message.draw()

    commands = '[Escape]: Quit\t[Space]: OK'
    cmnd_text = visual.TextStim(win,
                                text=commands, color='white', height=.5,
                                alignText='center')
    cmnd_text.pos = (0, -2)
    cmnd_text.draw()

    win.flip()
    pressed_key = event.waitKeys(keyList=list(cmd.values()))
    if cmd['quit_key'] in pressed_key:
        core.quit()
    elif cmd['response_key'] in pressed_key:
        pass


def run_pause_screen(win, current_block, cmd, nblocks, cnd=None,
                     cnd_order=None):
    if cnd_order == 'blocked':
        if cnd[0] == 1:
            dir1 = 'rightward'
        else:
            dir1 = 'leftward'
        if cnd[1] == 1:
            trj = 'passing'
        else:
            trj = 'reversive'
        msg = f"<<<   Block {current_block}/{nblocks}   >>>" \
              f"\n\nStarting motion direction: {dir1}" \
              f"\nTrajectory mode: {trj}" \
              f"\n\n\nReady to proceed?"
    else:
        msg = f"<<<   Block {current_block}/{nblocks}   >>>" \
              f"\n\n\nReady to proceed?"

    message = visual.TextStim(win,
                              text=msg, color='white', height=.5,
                              alignText='center')
    message.pos = (0, 1)
    message.draw()

    commands = '[Escape]: Quit\t[Space]: OK'
    cmnd_text = visual.TextStim(win,
                                text=commands, color='white', height=.5,
                                alignText='center')
    cmnd_text.pos = (0, -2)
    cmnd_text.draw()

    win.flip()
    pressed_key = event.waitKeys(keyList=list(cmd.values()))
    if cmd['quit_key'] in pressed_key:
        core.quit()
    elif cmd['response_key'] in pressed_key:
        pass


def rotate_point(origin, point, angle):
    """
    Rotate a point counterclockwise by a given angle around a given origin.
    The angle should be given in degrees.
    """
    ox, oy = origin
    px, py = point

    qx = ox + np.cos(angle) * (px - ox) - np.sin(angle) * (py - oy)
    qy = oy + np.sin(angle) * (px - ox) + np.cos(angle) * (py - oy)
    q = (qx, qy)
    return q
