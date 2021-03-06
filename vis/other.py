from utilz import *
from utilz.vis.matplotlib_ import *
#exec(identify_file_str)


        
from scipy.optimize import curve_fit





def inside_test(points , cube3d): 
    # https://stackoverflow.com/questions/21037241/how-to-determine-a-point-is-inside-or-outside-a-cube
    """
    cube3d  =  numpy array of the shape (8,3) with coordinates in the clockwise order. first the bottom plane is considered then the top one.
    points = array of points with shape (N, 3).

    Returns the indices of the points array which are outside the cube3d
    """
    b1,b2,b3,b4,t1,t2,t3,t4 = cube3d

    dir1 = (t1-b1)
    size1 = np.linalg.norm(dir1)
    dir1 = dir1 / size1

    dir2 = (b2-b1)
    size2 = np.linalg.norm(dir2)
    dir2 = dir2 / size2

    dir3 = (b4-b1)
    size3 = np.linalg.norm(dir3)
    dir3 = dir3 / size3

    cube3d_center = (b1 + t3)/2.0

    dir_vec = points - cube3d_center

    res1 = np.where( (np.absolute(np.dot(dir_vec, dir1)) * 2) > size1 )[0]
    res2 = np.where( (np.absolute(np.dot(dir_vec, dir2)) * 2) > size2 )[0]
    res3 = np.where( (np.absolute(np.dot(dir_vec, dir3)) * 2) > size3 )[0]

    return list( set().union(res1, res2, res3) )

def inside_test_with_in_out_return(points,cube3d):
    outpoints_indicies = inside_test(points,cube3d)
    outpoints = list(map(points.__getitem__, outpoints_indicies))
    inpoints = []
    inpoints_indicies = []
    for i in rlen(points):
        if i not in outpoints_indicies:
            inpoints_indicies.append(i)
    inpoints = list(map(points.__getitem__, inpoints_indicies))
    return outpoints,inpoints




def _open_imgs_with_Preview(l):
    if type(l) is str:
        l = [l]
    for f in l:
        os_system('open',qtd(f))

def _quit_Preview():
    os_system(""" osascript -e 'quit app "Preview"' """)
    return


try:
    r = txt_file_to_list_of_strings(opjh('.screen_resolution'))
    SCREEN_RESOLUTION = (int(r[0]),int(r[1]))
except:
    #clp("Didn't find or get data from",opjh('.screen_resolution'),'`wrb')
    try:
    #if using_osx:
        def screen_size():
            from Quartz import CGDisplayBounds
            from Quartz import CGMainDisplayID
            mainMonitor = CGDisplayBounds(CGMainDisplayID())
            return (mainMonitor.size.width, mainMonitor.size.height) 
        SCREEN_RESOLUTION = screen_size()
    #else:
    except:
        SCREEN_RESOLUTION = (800,800)


def rndrect(x=200,y=100):
    return z55(rndn(y,x,3))

    
###########
'''
e.g.
from k3.vis import *; kzpy_vis_test()
'''
################








def iadd(src,dst,xy,neg=False):
    try:
        src_size = []
        upper_corner = []
        lower_corner = []
        for i in [0,1]:
            src_size.append(shape(src)[i])
            upper_corner.append(int(xy[i]-src_size[i]/2.0))
            lower_corner.append(int(xy[i]+src_size[i]/2.0))
        if neg:
            dst[upper_corner[0]:lower_corner[0],upper_corner[1]:lower_corner[1]] -= src
        else:
            dst[upper_corner[0]:lower_corner[0],upper_corner[1]:lower_corner[1]] += src
    except Exception as e:
        print("********** iadd(src,dst,xy,neg=False) Exception ***********************")
        print(e.message, e.args)
        print(time_str(mode='Pretty'))

def isub(src,dst,xy):
    iadd(src,dst,xy,neg=True)



        





def xylim(a,b,c,d):
    plt.xlim(a,b)
    plt.ylim(c,d)
def xyliml(lst):
    xlim(lst[0],lst[1])
    ylim(lst[2],lst[3])
    
def xysqlim(a):
    xylim(-a,a,-a,a)
















def length(xy):
    return sqrt(xy[0]**2+xy[1]**2)




def gaussian(x, mu, sig):
    return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))

def makeGaussian(size, fwhm = 3, center=None):
    """ Make a square gaussian kernel.

    size is the length of a side of the square
    fwhm is full-width-half-maximum, which
    can be thought of as an effective radius.
    http://stackoverflow.com/questions/7687679/how-to-generate-2d-gaussian-with-python

    """

    x = np.arange(0, size, 1, float)
    y = x[:,np.newaxis]

    if center is None:
        x0 = y0 = size // 2
    else:
        x0 = center[0]
        y0 = center[1]

    return np.exp(-4*np.log(2) * ((x-x0)**2 + (y-y0)**2) / fwhm**2)

def Gaussian_2D(width):
    return makeGaussian(width,width/3.0)





def normalized(a, axis=-1, order=2):
    l2 = np.atleast_1d(np.linalg.norm(a, order, axis))
    l2[l2==0] = 1
    return a / np.expand_dims(l2, axis)



def f___(x,A,B):
    return A*x+B
def normalized_vector_from_pts(pts):
    pts = array(pts)
    x = pts[:,0]
    y = pts[:,1]
    m,b = curve_fit(f___,x,y)[0]
    heading = normalized([1,m])[0]
    len_heading = length(heading)
    #print len_heading
    #if np.abs(len_heading-1.0)>0.1:
    #    print('here')
    #    print((heading,len_heading,pts))
    #    assert(False)
    return heading



def Image_to_Folder_Saver(d):
    D = {}
    D['path'] = d['path']

    D['type'] = 'Image_to_Folder_Saver'
    D['Purpose'] = d2s(inspect.stack()[0][3],':','Save images to folder with counter for name.')
    D['save_img_ctr'] = 0
    def _save(d):
        img = d['img']
        if 'ext' not in d:
            ext = 'png'
        imsave(opj(D['path'],str(D['save_img_ctr'])+'.'+ext),img)
        D['save_img_ctr'] += 1
    D['save'] = _save
    return D






def plot_line(a_,b,c):
    plot([a_[0],b[0]],[a_[1],b[1]],c)







def Click_Data(**Args):
    """
    e.g.,
        CA()
        fig = figure(1)
        plot([1,2,1,3,4],'b')
        Cdat = Click_Data(FIG=fig)
        xy_list = Cdat['CLICK'](NUM_PTS=6)
        pts_plot(na(xy_list),'r')
    """
    _ = {}
    _['X'],_['Y'] = 0,0
    _['X_PREV'],_['Y_PREV'] = _['X'],_['Y']
    fig = Args['FIG']
    
    def _callback(event):
        _['X'],_['Y'] = event.xdata, event.ydata
    def _click(**Args):
        num_pts = Args['NUM_PTS']
        if num_pts == 1:
            pt_str = 'point'
        else:
            pt_str = 'points'
        if 'STR' in Args:
            print(Args['STR'])
        else:
            pd2s('click',num_pts,pt_str)
        fig.canvas.callbacks.connect('button_press_event', _callback)
        xy_list = []
        while len(xy_list) < num_pts:
            while _['X_PREV'] == _['X'] and _['Y_PREV'] == _['Y']:
                plt.pause(0.1)#;print '.'
                if not (_['X_PREV'] == _['X'] and _['Y_PREV'] == _['Y']):
                    print(_['X'],_['Y'])
                    xy_list.append([_['X'],_['Y']])
                    _['X_PREV'],_['Y_PREV'] = _['X'],_['Y']
                    break
        return xy_list
    _['CLICK'] = _click
    return _





def show_color_net_inputs(camera_input,pre_metadata_features_metadata=None,channel=0):

    import torch

    camera_input = camera_input.data.cpu().numpy()
    for i in range(4):
        a = 3*i
        b = 3*(i+1)-1
        c = camera_input[channel,a:b+1,:,:]
        assert shape(c) == (3, 94,168)
        c = c.transpose(1,2,0) 
        assert shape(c) == (94,168,3)
        c = z55(c) # rgb
        mi(c,d2s(a,'to',b))

    if pre_metadata_features_metadata != None:
        p = pre_metadata_features_metadata.data.cpu().numpy()
        offset = 128+1+4

        for i in range(4):
            a = 3*(i)+offset
            b = 3*(i+1)-1+offset
            c = p[channel,a:b+1,:,:]
            assert shape(c) == (3, 23,41)
            c = c.transpose(1,2,0) 
            assert shape(c) == (23,41,3)
            c = z55(c) #rgb
            mi(c,d2s(a,'to',b))
    spause()



    if x1 > sg[1]:
        q = -x0_
    else:
        q = -x0d_
    if y1 > sg[0]:

        u = -y0_
    else:
        u = -y0d_

    g0[  int(y0_):int(y1_+y0d_-y0d_),  int(x0_):int(x1_+x0d_-x0d_),:3] = f.copy()[int(-y0d_):int(y1_+u),int(-x0d_):int(x1_+q),:3]

    return g0


"""
# HSV: Hue, Saturation, Value
# H: position in the spectrum
# S: color saturation ("purity")
# V: color brightness

# HLS: Hue, Luminance, Saturation
# H: position in the spectrum
# L: color lightness
# S: color saturation

def hsv_to_rgb(h, s, v):
    if s == 0.0:
        return v, v, v
    i = int(h*6.0) # XXX assume int() truncates!
    f = (h*6.0) - i
    p = v*(1.0 - s)
    q = v*(1.0 - s*f)
    t = v*(1.0 - s*(1.0-f))
    i = i%6
    if i == 0:
        return v, t, p
    if i == 1:
        return q, v, p
    if i == 2:
        return p, v, t
    if i == 3:
        return p, q, v
    if i == 4:
        return t, p, v
    if i == 5:
        return v, p, q
"""

def hsv_to_rgb__vectorized(h):

    s = zeros(len(h))+1.0
    v = zeros(len(h))+1.0
    rgb = zeros((len(h),3))


    i = (h*6.0).astype(int)
    f = (h*6.0) - i
    p = v*(1.0 - s)
    q = v*(1.0 - s*f)
    t = v*(1.0 - s*(1.0-f))

    a = np.where(i==0)
    if len(a[0]):
        rgb[a,:] = na((v[a],t[a],p[a])).T


    a = np.where(i==1)
    if len(a[0]):
        rgb[a,:] = na((q[a],v[a],p[a])).T


    a = np.where(i==2)
    if len(a[0]):
        rgb[a,:] = na((p[a],v[a],t[a])).T


    a = np.where(i==3)
    if len(a[0]):
        rgb[a,:] = na((p[a],q[a],v[a])).T


    a = np.where(i==4)
    if len(a[0]):
        rgb[a,:] = na((t[a],p[a],v[a])).T
    

    a = np.where(i==5)
    if len(a[0]):
        rgb[a,:] = na((v[a],p[a],q[a])).T    
    f = (h*6.0) - i
    p = v*(1.0 - s)
    q = v*(1.0 - s*f)
    t = v*(1.0 - s*(1.0-f))
    
    return (255*rgb).astype(np.uint8)




def pseudocolor(val, minval, maxval,max_angle=360):
    # https://stackoverflow.com/questions/10901085/range-values-to-pseudocolor
    """ Convert val in range minval..maxval to the range 0..120 degrees which
        correspond to the colors Red and Green in the HSV colorspace.
    """
    h = (float(val-minval) / (maxval-minval)) * max_angle

    # Convert hsv color (h,1,1) to its rgb equivalent.
    # Note: hsv_to_rgb() function expects h to be in the range 0..1 not 0..360
    r, g, b = hsv_to_rgb(h/360, 1., 1.)
    return r, g, b



def pseudocolors(vals, minval, maxval,max_angle=360):
    vals = vals.copy()
    vals[vals < minval] = minval
    vals[vals > maxval] = maxval
    # https://stackoverflow.com/questions/10901085/range-values-to-pseudocolor
    """ Convert val in range minval..maxval to the range 0..120 degrees which
        correspond to the colors Red and Green in the HSV colorspace.
    """
    h = (vals-minval) / (maxval-minval) * max_angle
    ones = zeros(len(vals))+1
    # Convert hsv color (h,1,1) to its rgb equivalent.
    # Note: hsv_to_rgb() function expects h to be in the range 0..1 not 0..360
    rgbs = hsv_to_rgb__vectorized(h/360)
    return rgbs



#EOF
