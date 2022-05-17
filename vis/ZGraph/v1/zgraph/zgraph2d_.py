import sys,os
parent_path = '/'.join(__file__.split('/')[:-2])
print('\n',__file__,'adding',parent_path,'to sys.path.','\n')
sys.path.append(parent_path)

from utilz.vis import *
from zgraph.utils import *

class ZGraph2d:
    def __init__(
        _,
        width= 512,
        height= 512,
        img= None,
        temp_offset= 0,
        title= 'ZGraph2d'
    ):
        _.title = title
        if img is not None:
            _.img_bkp = img.copy()
            _.img = img
            height = shape(_.img)[0]
            width = shape(_.img)[1]
        else:
            _.img = get_blank_rgb(height,width)
            _.img_bkp = None
        _.xys_color_mode_list = []
        #cr(width,height)
        q = get_blank_rgb(height+2*temp_offset,width+2*temp_offset)
        if temp_offset:
            q[temp_offset:-temp_offset,temp_offset:-temp_offset] = _.img
        _.img2 = q
        cm(shape(_.img2),shape(_.img))
        cg(shape(_.img2[temp_offset:-temp_offset,temp_offset:-temp_offset]))
        _.temp_offset = temp_offset

    def add(
        _,
        xys,
        colors=((255,255,255),),
        mode='points',
    ):
        _.xys_color_mode_list.append( ( na(xys), colors, mode ) )


    def graph(
        _,
        xmin= -5,
        xmax= 5,
        ymin= -5,
        aspect_ratio= 1.0,
    ):

        _.graph_has_been_called = True
        for xys, colors, mode in _.xys_color_mode_list:
            if mode  in ['points']:
                change = True
            else:
                change = False
            pixels, untrimmed_pixels = pts2img( 
                _.img, 
                xys, 
                xmin, 
                xmax, 
                ymin, 
                aspect_ratio, 
                colors,
                change,
                _.temp_offset,
            )
            #untrimmed_pixels += _.temp_offset
            if mode == 'fill':
                try:
                    if len(untrimmed_pixels):
                        cv2.drawContours(_.img2, [untrimmed_pixels[:,:2]], -1, (colors[0]), -1)
                except:
                    cr( 'fill failed, pixels =', untrimmed_pixels )
            elif mode == 'line':
                try:
                    cv2.drawContours(_.img2,[untrimmed_pixels[:,:2]],-1,color=colors[0])
                except:
                    cr( 'contour failed, pixels =', untrimmed_pixels )

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
    wh = 300
    z0=ZGraph2d(
        title='ZGraph2d z0',
        img=z55(rndn(wh,wh,3))//2,
        temp_offset= wh,
    )
    temp_offset = z0.temp_offset
    z0.add(5*rndn(10,2),colors=((0,255,0),),mode='fill')
    z0.add((xys+na([-2,0])),colors=rndint(255,size=(len(xys),3)),mode='points')
    z0.add(10*rndn(10,2),colors=((0,0,255),),mode='line')


    z0.graph(
        xmin=-5,
        xmax=5,
        ymin=-5,
    )
    if temp_offset:
        pass#z0.img2 = z0.img2[temp_offset:-temp_offset,temp_offset:-temp_offset]
    print(temp_offset,shape(z0.img2))
    #z0.show()
    mi(z0.img2)
    raw_enter();CA()




if __name__ == '__main__':
    fire.Fire(_example)





