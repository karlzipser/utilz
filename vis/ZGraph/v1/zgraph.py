import sys,os
parent_path = '/'.join(__file__.split('/')[:-2])
print('\n',__file__,'adding',parent_path,'to sys.path.','\n')
sys.path.append(parent_path)

from utilz.vis import *
from ZGraph.utils import *

class ZGraph:
    def __init__(
        _,
        width=400,
        height=400,
        title='ZGraph'
    ):
        """
        """
        _.title = title
        _.width = width
        _.height = height
        _.img = get_blank_rgb(height,width)
        _.xys_color_list = []

        _.graph_has_been_called = False
        _.xmin = None
        _.xmax = None
        _.ymin = None
        _.ymax = None
        _.aspect_ratio = 1.0
        _.pixels_list = []
        _.modes = ['point','line','fill']

    def add(
        _,
        xys,
        mode=_.modes[0]
        color=((255,255,255)),
    ):
        _.xys_color_list.append((na(xys),color,mode))


    def graph(
        _,
        xmin=None,
        xmax=None,
        ymin=None,
        aspect_ratio=1.0,
        thickness=1,
    ):
        if None not in [xmin,xmax,ymin]:
            _.xmin = xmin
            _.xmax = xmax
            _.ymin = ymin
            _.aspect_ratio = aspect_ratio
        else:
            _._find_min_max()

        _.graph_has_been_called = True

        for xys, color, mode _.xys_color_list:
            pixels,untrimmed_pixels = pts2img( _.img, xys, _.xmin, _.xmax, _.ymin, _.aspect_ratio, color )
            _.pixels_list.append(pixels)

            if mode == 'fill':
                cv2.fillPoly(
                    _.img,
                    xys,
                    color=color[0,
                )

            elif mode == 'line':
                cv2.drawContours(_.img,[xys],-1,color[0])

            else:
                _.img[xys] = color

        return pixels,untrimmed_pixels
                    
                    
    def show(_,scale=1.0):
        """
        Display image using cv2.
        """
        scale = float(scale)
        if not _.graph_has_been_called:
            cE('warning, ZGraph.graph() not called before ZGraph.show()')
        if scale != 1.0:
            img_ = zresize(_.img,scale)
        else:
            img_ = _.img
        return mci(img_,title=_.title)



    def clear(_):
        """
        Clear x-y data and zero image without reallocating it.
        """
        _.graph_has_been_called = False
        _.xys_color_list = []
        _.img *= 0
        

    def _find_min_max(_,aspect_ratio_one=True):
        """
        If xy min and maxes not provided, find them automatically.
        """
        xmins = []
        xmaxes = []
        ymins = []
        for xys,color,line_endpoint_indicies,fill_indicies in _.xys_color_list:
            xmins.append(xys[:,0].min())
            xmaxes.append(xys[:,0].max())
            ymins.append(xys[:,1].min())
        if is_None(_.xmin):
            _.xmin = min(xmins)
        if is_None(_.xmax):
            _.xmax = max(xmaxes)
        if is_None(_.ymin):
            _.ymin = min(ymins)










def _example():
    """
    The ZGraph class, with examples.

    Try running for example, 
    python utilz/vis/zgraph2/zgraph.py --egs [0,1,2,3]
    """

    CA()

    print('e.g. 0')
    xys=rndn(5000,2)
    z0=ZGraph(300,300,title='ZGraph z0')
    z0.add(xys+na([-3,0]),rndint(255,size=(len(xys),3)))
    z0.graph()
    z0.report()
    z0.show()
    raw_enter();CA()


    print('e.g. 1')
    xys=rndn(1000,2)
    z1=ZGraph(600,400,title='ZGraph z1')
    z1.add(
        xys=2*xys*na([-1,1])+na([8,-7]),
        color=rndint(255,size=(len(xys),3)),
        fill_indicies=( 
            [rndint(200,size=(10)),
            
            ]
        ),
    )
    z1.add(
        xys=2*xys*na([-1,1])+na([8,-7]),
        color=rndint(255,size=(len(xys),3)),
        fill_indicies=( 
            [rndint(200,size=(10)),
            rndint(200,size=(10)),
            rndint(200,size=(10)),]
        ),
    )        
    z1.add(
        xys=1*xys*na([-1,1])+na([12,3]),
        color=zeros((len(xys),3),np.uint8)+(255,127,31),
        line_endpoint_indicies=rndint(400,size=(30,2)),
    )

    z1.add(
        xys+na([-5,4]),
        color=(255,255,255),
        line_endpoint_indicies=rndint(200,size=(30,2)),

    )
    z1.add(
        xys=na([(1,1),(1,-1),(-1,-1),(-1,1),(1,1)]),
        color=(0,255,0),
        line_endpoint_indicies=((0,1),(1,2),(2,3),(3,4)),
    )
    z1.add(
        xys=0.75*na([(1,1),(1,-1),(-1,-1),(-1,1),(1,1)]),
        color=(255,0,0),
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


    



if __name__ == '__main__':
    fire.Fire(_example)





