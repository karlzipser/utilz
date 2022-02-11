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
        title='ZGraph2d'
    ):
        _.title = title
        _.width = width
        _.height = height
        _.img = get_blank_rgb(height,width)
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
        _.img *= 0
        












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
        300,
        300,
        title='ZGraph2d z0')
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

    """
    print('e.g. 1')
    xys=rndn(1000,2)
    z1=ZGraph(600,400,title='ZGraph z1')
    z1.add(
        xys=2*xys*na([-1,1])+na([8,-7]),
        colors=rndint(255,size=(len(xys),3)),
        fill_indicies=( 
            [rndint(200,size=(10)),
            
            ]
        ),
    )
    z1.add(
        xys=2*xys*na([-1,1])+na([8,-7]),
        colors=rndint(255,size=(len(xys),3)),
        fill_indicies=( 
            [rndint(200,size=(10)),
            rndint(200,size=(10)),
            rndint(200,size=(10)),]
        ),
    )        
    z1.add(
        xys=1*xys*na([-1,1])+na([12,3]),
        colors=zeros((len(xys),3),np.uint8)+(255,127,31),
        line_endpoint_indicies=rndint(400,size=(30,2)),
    )

    z1.add(
        xys+na([-5,4]),
        colors=(255,255,255),
        line_endpoint_indicies=rndint(200,size=(30,2)),

    )
    z1.add(
        xys=na([(1,1),(1,-1),(-1,-1),(-1,1),(1,1)]),
        colors=(0,255,0),
        line_endpoint_indicies=((0,1),(1,2),(2,3),(3,4)),
    )
    z1.add(
        xys=0.75*na([(1,1),(1,-1),(-1,-1),(-1,1),(1,1)]),
        colors=(255,0,0),
        fill_indicies=([[0,1,2,3,4]]),
    )
    z1.graph(-9,9,-9,thickness=1)
    z1.show(1.)
    z1.report()
    raw_enter();CA()

    print('e.g. 2')
    xys=rndn(20000,2)
    z0=ZGraph(1000,1000,title='ZGraph z0')
    t0 = 10
    timer = Timer(t0)
    print('wait',timer.time_s,'seconds')
    ctr = 0
    while not timer.rcheck():
        z0.clear()
        z0.add(xys+na([0,0]),rndint(255,size=(len(xys),3)))
        z0.graph(-5,5,-5)
        ctr += 1
    print('rate =',dp(ctr/t0),'Hz')
    z0.report()
    z0.show()
    raw_enter();CA()
    """

    



if __name__ == '__main__':
    fire.Fire(_example)





