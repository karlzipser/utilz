
from utilz.misc import *
from utilz.core.arrays import *
import matplotlib
import matplotlib.pyplot as plt  # the Python plotting package
plt.ion()
plot = plt.plot
hist = plt.hist
xlim = plt.xlim
ylim = plt.ylim
clf = plt.clf
pause = plt.pause
figure = plt.figure
title = plt.title
plt.ion()
plt.show()
PP,FF = plt.rcParams,'figure.figsize'

MacOSX = False
if '/Users/' in home_path:
    MacOSX = True

if MacOSX:
    matplotlib.use(u'MacOSX')

if username == 'nvidia':
    matplotlib.use(u'TkAgg')


def get_blank_rgb(h,w):
    return zeros((h,w,3),np.uint8)


def xylim(a,b,c,d):
    xlim(a,b)
    ylim(c,d)
    
def xysqlim(a):
    xylim(-a,a,-a,a)

def spause():
    pause(0.0001)

def hist(data,bins=100):
    """
    default hist behavior
    """
    plt.clf()
    plt.hist(data,bins=bins)
    pass
plot = plt.plot
figure = plt.figure
clf=plt.clf


def toolbar():
    plt.rcParams['toolbar'] = 'toolbar2'
    
######################
#
def mi(
    image_matrix,
    figure_num = 1,
    subplot_array = [1,1,1],
    img_title = '',
    img_xlabel = 'x',
    img_ylabel = 'y',
    cmap = 'gray',
    toolBar = True,
    do_clf = True,
    do_axis = False ):
    """
    My Imagesc, displays a matrix as grayscale image if 2d, or color if 3d.
    Can take different inputs -- e.g.,

        from matrix:

            from k3.vis import *
            mi(np.random.rand(256,256),99,[1,1,1],'random matrix')

        from path:
            mi(opjh('Desktop','conv1'),1,[5,5,0])

        from list:
            l = load_img_folder_to_list(opjh('Desktop','conv5'))
            mi(l,2,[4,3,0])

        from dict:
            mi(load_img_folder_to_dict(opjh('Desktop','conv5')),1,[3,4,0])
    """
    if type(image_matrix) == str:
        l=load_img_folder_to_list(image_matrix)
        mi(l)
        return

    if type(image_matrix) == list:
        l=1.0*array(image_matrix)
        l/=l.max()
        mi(vis_square(l))
        return

    if type(image_matrix) == dict:
        img_keys = sorted(image_matrix.keys(),key=natural_keys)
        l = []
        for k in img_keys:
            l.append(image_matrix[k])
        mi(l)
        return        

    if toolBar == False:
        plt.rcParams['toolbar'] = 'None'
    else:
        plt.rcParams['toolbar'] = 'toolbar2'

    f = plt.figure(figure_num)
    if do_clf:
        #print('plt.clf()')
        plt.clf()

    if True:
        f.subplots_adjust(bottom=0.05)
        f.subplots_adjust(top=0.95)
        f.subplots_adjust(wspace=0.1)
        f.subplots_adjust(hspace=0.1)
        f.subplots_adjust(left=0.05)
        f.subplots_adjust(right=0.95)
    if False:
        f.subplots_adjust(bottom=0.0)
        f.subplots_adjust(top=0.95)
        f.subplots_adjust(wspace=0.0)
        f.subplots_adjust(hspace=0.1)
        f.subplots_adjust(left=0.0)
        f.subplots_adjust(right=1.0)
    f.add_subplot(subplot_array[0],subplot_array[1],subplot_array[2])
    imgplot = plt.imshow(image_matrix, cmap)
    imgplot.set_interpolation('nearest')
    if not do_axis:
        plt.axis('off')
    if len(img_title) > 0:# != 'no title':
        plt.title(img_title)
#
######################


def plt_square(half_width=0):
    plt.gca().set_aspect('equal',adjustable='box')
    plt.draw()
    if half_width > 0:
        xysqlim(half_width)





def pt_plot(xy,color='r'):
    plot(xy[0],xy[1],color+'.')

def pts_plot(xys,color='r',sym='.',ms=None):
    if type(xys) == list:
        xys = na(xys)
    if len(shape(xys)) == 1:
        xys = na([xys])
    assert(len(color)==1)
    x = xys[:,0]
    y = xys[:,1]
    if ms is None:
        plot(x,y,color+sym)
    else:
        plot(x,y,color+sym,ms=ms)






###########
#
def Image(xyz_sizes,origin,mult,data_type=np.uint8):
    D = {}
    D['origin'] = origin
    D['mult'] = mult
    D['Purpose'] = d2s(inspect.stack()[0][3],':','An image which translates from float coordinates.')
    D['name'] = 'Image'
    def _floats_to_pixels(xy):
        xy = array(xy)
        xyn = 0*xy
        if len(shape(xy)) == 1:
            xyn[0] = D['mult'] * xy[0]
            xyn[0] += D['origin']
            xyn[1] = D['mult'] * xy[1]
            xyn[1] += D['origin']
        else:
            xyn[:,0] = D['mult'] * xy[:,0]
            xyn[:,0] += D['origin']
            xyn[:,1] = D['mult'] * xy[:,1]
            xyn[:,1] += D['origin']
        return np.ndarray.astype(xyn,int)
    def _pixel_to_float(xy):
        xy = array(xy)
        xyn = 0.0*xy
        assert(len(shape(xy)) == 1)
        xyn[0] = xy[0] - D['origin']
        xyn[0] /= (1.0*D['mult'])
        xyn[1] = xy[1] - D['origin']
        xyn[1] /= (1.0*D['mult'])
        return np.ndarray.astype(xyn,float)
    D['floats_to_pixels'] = _floats_to_pixels
    D['pixel_to_float'] = _pixel_to_float
    def _pts_plot(xy,c='b'):
        if len(xy) < 1:
            #print('warning, asked to plot empty pts')
            return
        xy_pix = D['floats_to_pixels'](xy)
        if len(shape(xy)) == 1:
            plot(xy_pix[1],xy_pix[0],c+'.')
        else:
            plot(xy_pix[:,1],xy_pix[:,0],c+'.')
    D['pts_plot'] = _pts_plot
    def _apply_fun(f):
        for x in range(0,2*D['origin']):
            for y in range(0,2*D['origin']):
                xy_float = D['pixel_to_float']((x,y))
                D['img'][x][y] = f(xy_float[0],xy_float[1])      
    D['apply_fun'] = _apply_fun
    def _show(name=None):
        if name == None:
            name = D['name']
        mi(D['img'],name)
        #prin(t d2s('name =',name))
    D['show'] = _show
    def _clear():
        D['img'] *= 0.0
    if len(xyz_sizes) == 2:
        D['img'] = zeros((xyz_sizes[0],xyz_sizes[1]),data_type)
    elif len(xyz_sizes) == 3:
        D['img'] = zeros((xyz_sizes[0],xyz_sizes[1],xyz_sizes[2]),data_type)
    else:
        assert(False)
    return D


#
###############






###########
# https://stackoverflow.com/questions/35281427/fast-python-plotting-library-to-draw-plots-directly-on-2d-numpy-array-image-buff
def Plot(xy_pix_sizes,origin,xy_mults):
    D = {}
    D['origin'] = origin
    D['xy_mults'] = xy_mults
    D['Purpose'] = d2s(inspect.stack()[0][3],':','A cv2 ploter.')
    D['name'] = 'Image'
    def _floats_to_pixels(xy):
        xy = array(xy)
        xyn = 0*xy
        if len(shape(xy)) == 1:
            xyn[0] = D['mult'] * xy[0]
            xyn[0] += D['origin']
            xyn[1] = D['mult'] * xy[1]
            xyn[1] += D['origin']
        else:
            xyn[:,0] = D['mult'] * xy[:,0]
            xyn[:,0] += D['origin']
            xyn[:,1] = D['mult'] * xy[:,1]
            xyn[:,1] += D['origin']
        return np.ndarray.astype(xyn,int)
    def _pixel_to_float(xy):
        xy = array(xy)
        xyn = 0.0*xy
        assert(len(shape(xy)) == 1)
        xyn[0] = xy[0] - D['origin']
        xyn[0] /= (1.0*D['mult'])
        xyn[1] = xy[1] - D['origin']
        xyn[1] /= (1.0*D['mult'])
        return np.ndarray.astype(xyn,float)
    D['floats_to_pixels'] = _floats_to_pixels
    D['pixel_to_float'] = _pixel_to_float
    def _pts_plot(xy,c='b'):
        if type(xy) == list:
            xy = na(xy)
        if len(xy) < 1:
            print('warning, asked to plot empty pts')
            return
        xy_pix = D['floats_to_pixels'](xy)
        if len(shape(xy)) == 1:
            pass# plot(xy_pix[1],xy_pix[0],c+'.')
        else:
            pass #plot(xy_pix[:,1],xy_pix[:,0],c+'.')
    D['pts_plot'] = _pts_plot
    def _apply_fun(f):
        for x in range(0,2*D['origin']):
            for y in range(0,2*D['origin']):
                xy_float = D['pixel_to_float']((x,y))
                D['img'][x][y] = f(xy_float[0],xy_float[1])    # ???  
    D['apply_fun'] = _apply_fun
    def _show(name=None):
        if name == None:
            name = D['name']
        mi(D['img'],name)
        #prin(t d2s('name =',name))
    D['show'] = _show
    def _clear():
        D['img'] *= 0.0
    if len(xyz_sizes) == 2:
        D['img'] = zeros((xyz_sizes[0],xyz_sizes[1]),data_type)
    elif len(xyz_sizes) == 3:
        D['img'] = zeros((xyz_sizes[0],xyz_sizes[1],xyz_sizes[2]),data_type)
    else:
        assert(False)
    return D
#
###############

if __name__ == '__main__':
    
    eg(__file__)

    hist(rndn(10000))

    raw_enter()

#EOF
