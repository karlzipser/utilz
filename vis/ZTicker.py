
from utilz.vis.ZGraph import *


class ZTicker:
    """
    Show timeseries data
    """
    def __init__(self, width, height, title='no-name'):
        self.title = title
        self.img = get_blank_rgb(height,width)
        self.ctr = -1
    def _add(self,ys,ymin,ymax,colors):
        xys = zeros((len(ys),2))
        xys[:,1] = na(ys)
        pixels = self.pts2pixels(xys,(ymin,ymin),(ymax,ymax),shape(self.img))
        for p,color in zip(pixels,colors):
            #print(p)
            self.img[p[1],-1,:] = color
        #self._shift()
    def _shift(self):
        self.img[:,:-1,:] = self.img[:,1:,:]
        self.img[:,-1,:] *= 0
    def show(self,scale=1.0,every=1):
        self.ctr += 1
        if self.ctr % every:
            return
        scale = float(scale)
        if scale != 1.0:
            img_ = zresize(self.img,scale)
        else:
            img_ = self.img
        mci(img_,title=self.title)


    def pts2pixels(self,xys,xymin,xymax,shape_of_img):
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

def example(
    height=200,
    width=500,
    step=1,
    every=2
):
    """
    The ZTicker class with an example usage.

    Used to animate timeseries data.
    """

    A = locals()
    kprint(A)
    w = ZTicker(width,height)
    for i in range(1,10*360,step):
        if i > 0:
            w._shift()
        w._add(
            [
                np.cos(np.radians(i)),
                0.5*np.cos(np.radians(2*i)),
                0.3*np.cos(np.radians(5*i)),
                np.cos(np.radians(i))+\
                0.5*np.cos(np.radians(2*i))+\
                0.3*np.cos(np.radians(5*i)),
            ],
            -2,2,
            [(255,0,0),(0,255,0),(0,0,255),(255,255,255)])
        w.show(every=every)

    raw_enter()


if __name__ == '__main__':

    fire.Fire(example)









