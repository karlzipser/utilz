from utilz.vis.cv2_ import *
from utilz.core.arrays import *

Mouse = {
    'x' : 0,
    'y' : 0,
    'x_prev' : 0,
    'y_prev' : 0,
    'x_max' : 0,
    'y_max' : 0,
    'x_proportion' : 0,
    'y_proportion' : 0,
    'dx' : 0,
    'dy' : 0,
    'x_temp_center' : 0,
    'y_temp_center' : 0,
    'x_temp_center_proportion' : 0,
    'y_temp_center_proportion' : 0,
    'change' : False,
    'gamma' : [1.,1.,1.],
    'gamma_lock' : [0,0,0],
    'y_gamma_mode' : 'gamma/g',
}

def _track_mouse_callback(event,x,y,flags,param):
    M = Mouse
    M['x_prev'] = M['x']
    M['y_prev'] = M['y']
    M['x'],M['y'] = x,y
    M['dx'] = M['x'] - M['x_prev']
    M['dy'] = M['y'] - M['y_prev']
    if M['dx'] != 0 or M['dy'] != 0:
        M['change'] = True
        if M['x_max'] > 1 and M['y_max'] > 1:
            M['x_proportion'] = M['x'] / (M['x_max']-1)
            M['y_proportion'] = M['y'] / (M['y_max']-1)
            if M['x_temp_center'] > 0:
                M['x_temp_center_proportion'] = (M['x']-M['x_temp_center']) / (M['x_max']-M['x_temp_center'])
            if M['y_temp_center'] > 0:
                M['y_temp_center_proportion'] = (M['y']-M['y_temp_center']) / (M['y_max']-M['y_temp_center'])
    else:
        M['change'] = False


def track_mouse_to_figure(fig_name,dims):
    mci(get_blank_rgb(dims[0],dims[1]),title=fig_name)
    cv2.setMouseCallback(fig_name,_track_mouse_callback)

#EOF
