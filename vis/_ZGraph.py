
from utilz.vis.cv2_ import *

def get_blank_rgb(h,w):
    return np.zeros((h,w,3),np.uint8)


def pts2pixels(xys,xymin,xymax,shape_of_img):
    xys = na(xys)
    xymin = na(xymin)
    xymax = na(xymax)
    shape_of_img = na([shape_of_img[1],shape_of_img[0]])
    pixels = shape_of_img * (xys-xymin)/(xymax-xymin)
    pixels = pixels.astype(int)
    pixels = pixels[pixels[:,0]>=0]
    pixels = pixels[pixels[:,1]>=0]
    pixels = pixels[pixels[:,0]<shape_of_img[0]]
    pixels = pixels[pixels[:,1]<shape_of_img[1]]
    return pixels

def pts2img(img,xys,xymin,xymax,color=(255,255,255)):
    pixels = pts2pixels(xys,xymin,xymax,shape(img))
    img[shape(img)[0]-1-pixels[:,1],pixels[:,0]] = color


class ZGraph:
    def __init__(
        self,
        width=400,
        height=400,
        title='ZGraph'
    ):
        self.title = title
        self.width = width
        self.height = height
        self.img = get_blank_rgb(height,width)
        self.xys_color_list = []
        self.plot_called = False
        self.xymin = None
        self.xymax = None

    def add(self,xys,color):
        self.xys_color_list.append((na(xys),color))
    def find_min_max(self,aspect_ratio_one=True):
        all_xys = None
        for xys,color in self.xys_color_list:
            if type(all_xys) == type(None):
                all_xys = xys
            else:
                all_xys = np.concatenate((all_xys,xys),0)
        self.xymin = (min(all_xys[:,0]),min(all_xys[:,1]))
        self.xymax = (max(all_xys[:,0]),max(all_xys[:,1]))
        if aspect_ratio_one:
            mn = min(self.xymin)
            mx = max(self.xymax)
            self.xymin = (mn,mn)
            self.xymax = (mx,mx)
    # mask or name
    def plot(
        self,
        xymin=None,
        xymax=None,
    ):
        self.img *= 0
        if xymin and xymax:
            self.xymin = xymin
            self.xymax = xymax
        else:
            self.find_min_max()
        self.plot_called = True
        for xys,color in self.xys_color_list:
            pts2img(self.img,xys,self.xymin,self.xymax,color)

    def show(self,scale=1.0):
        scale = float(scale)
        if not self.plot_called:
            cE('warning, ZGraph.plot() not called before ZGraph.show()')
        if scale != 1.0:
            img_ = zresize(self.img,scale)
        else:
            img_ = self.img
        return mci(img_,title=self.title)

    def report(self):
        print(d2n('ZGraph ',self.title,', w x h = ',self.width,' x ',self.height))
        for xys,color in self.xys_color_list:
            print('\t',color,len(xys),'points')

    def clear(self):
        self.plot_called = False
        self.xys_color_list = []
        self.img *= 0
        
def _test_ZGraph():
    xys=rndn(1000,2)
    z=ZGraph(200,200,'_test_ZGraph')
    z.add(xys,(0,255,0)) 
    z.add(0.3*xys*na([-1,1])+na([13,6]),(255,0,0))
    z.plot()#z.plot((-6,-2),(6,2))
    z.show(2.)
    fs = (2,2)
    #figure(1,figsize=fs);clf();plt_square()
    #pts_plot(xys)
    raw_enter()



if __name__ == '__main__':

    _test_ZGraph()


