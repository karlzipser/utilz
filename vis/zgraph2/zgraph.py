import sys,os
parent_path = '/'.join(__file__.split('/')[:-2])
print('\n',__file__,'adding',parent_path,'to sys.path.','\n')
sys.path.append(parent_path)

from utilz.vis import *
from zgraph2.utils import *

class ZGraph:
    def __init__(
        _,
        width=400,
        height=400,
        title='ZGraph'
    ):
        """
        Take float x-y data and project into RGB image.

        _.xys_color_list
            list of tuples as shown below:
            [ (xys, color, line_endpoint_indicies, fill_indicies), etc... ]
            tuples added by _.add()
            line and fill are not indicated by coordinates but by indices of xys points
            
            line_endpoint_indicies has dimensions (n,2), with the first entry an index to the start 
            point and the second entry an index to the end point.
            e.g.,
                
                line_endpoint_indicies=rndint(200,size=(30,2))

            fill_indicies have the form of a list of arrays of indices, as for example:

                fill_indicies=( 
                    [
                        rndint(200,size=(10)),
                        rndint(200,size=(10)),
                        rndint(200,size=(10)),
                    ]
                )
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


    def add(
        _,
        xys,
        color=(255,255,255),
        line_endpoint_indicies=[],
        fill_indicies=[]):
        """
        Introduce collection of x-y points, colors and optional
        line point indices and fill point indices to _.xys_color_list for
        later procesesing to pixels by _.graph().
        """
        _.xys_color_list.append((na(xys),color,line_endpoint_indicies,fill_indicies))


    def graph(
        _,
        xmin=None,
        xmax=None,
        ymin=None,
        aspect_ratio=1.0,
        thickness=1,
    ):
        """
        Transform x-y data with respective colors, line endpoints and fill endpoints
        into image matrix.
        """
        if None not in [xmin,xmax,ymin]:
            _.xmin = xmin
            _.xmax = xmax
            _.ymin = ymin
            _.aspect_ratio = aspect_ratio
        else:
            _._find_min_max()

        _.graph_has_been_called = True

        for xys, color, line_endpoint_indicies, fill_indicies in _.xys_color_list:
            pixels = pts2img( _.img, xys, _.xmin, _.xmax, _.ymin, _.aspect_ratio,color )
            _.pixels_list.append(pixels)


            if len(fill_indicies):
                
                for fi in fill_indicies:
                    contour_pts = []
                    valid_enpoint_indicies = []
                    fill_color = ()
                    p = pixels[:,2]
                    for a in fi:
                        si = np.where(p==a)[0]
                        if len(si) > 0:
                            valid_enpoint_indicies.append(si[0])
                        else:
                            pass
                    fill_color = None
                    for j in rlen(valid_enpoint_indicies):
                        a = valid_enpoint_indicies[j]
                        x0,y0 = pixels[a][:2]
                        contour_pts.append((x0,shape(_.img)[0]-1-y0))
                    if fill_color is None:
                        #print(len(pixels),a)
                        if len(pixels) < a+1:
                            cr('warning, len(pixels) < a+1')
                            c = (255,255,255)
                        else:
                            if len(pixels[a]) < 6:
                                c = color
                            else:
                                c = pixels[a][3:6].tolist()
                        fill_color = c
                    try:
                        cv2.fillPoly(
                            _.img,
                            [na(contour_pts)],
                            color=fill_color,
                        )
                    except:
                        cr('cv2.fillPoly failed with',contour_pts)



            if len(line_endpoint_indicies):
                
                valid_enpoint_indicies = []
                p = pixels[:,2]
                for a in line_endpoint_indicies:
                    si = np.where(p==a[0])[0]
                    ei = np.where(p==a[1])[0]
                    if len(si) > 0 and len(ei) > 0:
                        valid_enpoint_indicies.append((si[0],ei[0]))
                    else:
                        pass
                for j in rlen(valid_enpoint_indicies):
                    a,b = valid_enpoint_indicies[j]
                    x0,y0 = pixels[a][:2]
                    x1,y1 = pixels[b][:2]

                    if len(pixels[a]) < 6:
                        c = color
                    else:
                        c = pixels[a][3:6].tolist()

                    cv2.line(
                        _.img,
                        (x0,shape(_.img)[0]-1-y0),(x1,shape(_.img)[0]-1-y1),
                        color=c,
                        thickness=thickness,
                    )

                    
                    
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



    def report(_):
        s = [d2n('w x h = ',_.width,' x ',_.height)]
        s += [d2s('xmin:',dp(_.xmin),'xmax:',dp(_.xmax),
                    'ymin:',dp(_.xmin),'ymax:',dp(_.xmax)),]            
        for xys,color,line_endpoint_indicies,fill_indicies in _.xys_color_list:
            s += [
                d2s(len(xys),'points'),
                d2s('shape(color) =',shape(color)),
                d2s('len(line_endpoint_indicies):',len(line_endpoint_indicies)),
                d2s('len(fill_indicies):',len(fill_indicies)),
            ]
        box('\n'.join(s),title=' '+_.title+' ')

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










def example(egs=[0,1,2,3]):
    """
    The ZGraph class, with examples.

    Try running for example, 
    python utilz/vis/zgraph2/zgraph.py --egs [0,1,2,3]
    """
    kprint(locals())
    CA()

    xys=rndn(1000,2)

    if 0 in egs:
        z0=ZGraph(100,100,title='ZGraph z0')
        z0.add(xys+na([-3,0]),rndint(255,size=(len(xys),3)))
        z0.graph()#-5,3,-5,3)
        z0.report()
        z0.show()
        raw_enter();CA()

    if 1 in egs:
        z1=ZGraph(800,400,title='ZGraph z1')
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




    



if __name__ == '__main__':
    fire.Fire(example)





