from psychopy import visual, core, event


def cal_next_tilt(goal_perf, run_perf):
    delta = goal_perf - run_perf
    delta_max = max([100 - goal_perf, goal_perf])
    step_max = 5
    step_change = round(delta / delta_max * step_max, 0)
    return step_change


def run_pause_screen(win, b):
    msg = f"Ready for block {b}/{4}?"
    message = visual.TextStim(win,
                              text=msg, color='black', height=.5,
                              alignText='center')
    message.pos = (0, 1)
    message.draw()

    commands = '[Escape]: Quit\t\t\t[Enter]: Go'
    cmnd_text = visual.TextStim(win,
                                text=commands, color='black', height=.5,
                                alignText='center')
    cmnd_text.pos = (0, -2)
    cmnd_text.draw()

    win.flip()
    pressed_key = event.waitKeys(keyList=['escape', 'return'])
    if 'escape' in pressed_key:
        core.quit()
    elif 'return' in pressed_key:
        pass
