import sys,os
parent_path = '/'.join(__file__.split('/')[:-2])
print('\n',__file__,'adding',parent_path,'to sys.path.','\n')
sys.path.append(parent_path)

from utilz.vis import *
from zgraph.utils import *

class ZGraph2d:
    def __init__(
        _,
        width=400,
        height=400,
        img=None,
        title='ZGraph2d'
    ):
        _.title = title
        if img is not None:
            _.img_bkp = img.copy()
            _.img = img
        else:
            _.img = get_blank_rgb(height,width)
            _.img_bkp = None
        _.xys_color_mode_list = []


    def add(
        _,
        xys,
        colors=((255,255,255),),
        mode='points',
    ):
        _.xys_color_mode_list.append( ( na(xys), colors, mode ) )


    def graph(
        _,
        xmin=-5,
        xmax=5,
        ymin=-5,
        aspect_ratio=1.0,
    ):

        _.graph_has_been_called = True

        for xys, colors, mode in _.xys_color_mode_list:

            pixels, untrimmed_pixels = pts2img( 
                _.img, 
                xys, 
                xmin, 
                xmax, 
                ymin, 
                aspect_ratio, 
                colors,
            )
            if mode == 'fill':
                cv2.fillPoly(_.img, pts = [pixels[:,:2]], color=colors[0])

            elif mode == 'line':
                cv2.drawContours(_.img,[pixels[:,:2]],-1,color=colors[0])

            elif mode == 'points':
                pass

            else:
                print('unknown mode',mode)
                assert False

        return pixels,untrimmed_pixels
                    
                    
    def show(_,scale=1.0):
        """
        Display image using cv2.
        """
        scale = float(scale)
        if scale != 1.0:
            img_ = zresize(_.img,scale)
        else:
            img_ = _.img
        return mci(img_,title=_.title)



    def clear(_):
        """
        Clear x-y data and zero image without reallocating it.
        """
        _.xys_color_mode_list = []
        if _.img_bkp is None:
            _.img *= 0
        else:
            _.img = _.img_bkp.copy()        




def _example():
    """
    The ZGraph class, with example.

    Try running for example, 
    python utilz/vis/ZGraph/v1/zgraph.py 
    """

    CA()

    print('e.g. 0')
    xys=rndn(5000,2)
    z0=ZGraph2d(
        title='ZGraph2d z0',
        img=z55(rndn(300,300,3))//2,
    )
    z0.add(rndn(10,2),colors=((0,255,0),),mode='fill')
    z0.add(xys+na([-2,0]),colors=rndint(255,size=(len(xys),3)),mode='points')
    z0.add(rndn(10,2),colors=((0,0,255),),mode='line')


    z0.graph(
        xmin=-5,
        xmax=5,
        ymin=-5,
    )
    z0.show()
    raw_enter();CA()




if __name__ == '__main__':
    fire.Fire(_example)





