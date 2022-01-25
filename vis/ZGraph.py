
from utilz.vis import *


class ZGraph:
    def __init__(
        _,
        width=400,
        height=400,
        title='ZGraph'
    ):
        """
        Take float x-y data and project into image.
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


    def add(_,xys,color=(255,255,255),line_endpoint_indicies=[],do_fill=False):
        """
        Introduce collection of x-y points, colors and optional
        line point indicies to _.xys_color_list for later procesesing to
        pixels by _.graph().
        """
        _.xys_color_list.append((na(xys),color,line_endpoint_indicies))


    def graph(
        _,
        xmin=None,
        xmax=None,
        ymin=None,
        aspect_ratio=1.0,
        thickness=1,
        do_fill=False,
    ):
        """
        Transform xy data with respective colors and line endpoints
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

        for xys,color,line_endpoint_indicies in _.xys_color_list:
            pixels = pts2img(_.img,xys,_.xmin,_.xmax,_.ymin,_.aspect_ratio,color)
            _.pixels_list.append(pixels)

            if do_fill:
                contour_pts = []
                fill_color = ()

            if len(line_endpoint_indicies):
                
                valid_enpoint_indicies = []
                p = pixels[:,2]
                for a in line_endpoint_indicies:
                    si = np.where(p==a[0])[0]
                    ei = np.where(p==a[1])[0]
                    if len(si) > 0 and len(ei) > 0:

                        valid_enpoint_indicies.append((si[0],ei[0]))
                        #cg((si[0],ei[0]),'is valid')
                    else:
                        pass #cr((si,ei),'is invalid')
                for j in rlen(valid_enpoint_indicies):
                    a,b = valid_enpoint_indicies[j]
                    x0,y0 = pixels[a][:2]
                    x1,y1 = pixels[b][:2]
                    if do_fill:
                        contour_pts.append((x0,shape(_.img)[0]-1-y0))
                        contour_pts.append((x1,shape(_.img)[0]-1-y1))

                    if len(pixels[a]) < 6:
                        c = color#[255,0,0]
                    else:
                        c = pixels[a][3:6].tolist()
                    if do_fill:
                        fill_color = c
                    cv2.line(
                        _.img,
                        (x0,shape(_.img)[0]-1-y0),(x1,shape(_.img)[0]-1-y1),
                        color=c,
                        thickness=thickness,
                    )
                if do_fill:
                    cv2.fillPoly(
                        _.img,
                        [na(contour_pts)],
                        color=fill_color,
                    )
                    
                    
    def show(_,scale=1.0):
        """
        Display image using cv2.
        """
        scale = float(scale)
        if not _.graph_has_been_called:
            cE('warning, ZGraph.plot() not called before ZGraph.show()')
        if scale != 1.0:
            img_ = zresize(_.img,scale)
        else:
            img_ = _.img
        return mci(img_,title=_.title)



    def report(_):
        s = [d2n('w x h = ',_.width,' x ',_.height)]
        s += [d2s('xmin:',dp(_.xmin),'xmax:',dp(_.xmax),
                    'ymin:',dp(_.xmin),'ymax:',dp(_.xmax)),]            
        for xys,color,line_endpoint_indicies in _.xys_color_list:
            s += [
                d2s(len(xys),'points'),
                d2s('shape(color) =',shape(color)),
                d2s('len(line_endpoint_indicies):',len(line_endpoint_indicies)),
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
        for xys,color,line_endpoint_indicies in _.xys_color_list:
            xmins.append(xys[:,0].min())
            xmaxes.append(xys[:,0].max())
            ymins.append(xys[:,1].min())
        if is_None(_.xmin):
            _.xmin = min(xmins)
        if is_None(_.xmax):
            _.xmax = max(xmaxes)
        if is_None(_.ymin):
            _.ymin = min(ymins)

def plot_xys(
    xys,
    color=(255,255,255),
    width=400,
    height=400,
    xmin=None,
    xmax=None,
    ymin=None,
    img=None,
    aspect_ratio=1.0,
    title='plot_xys',
    report=False,
    return_img=True,
):
    if not is_None(img):
        height = shape(img)[0]
        width = shape(img)[1]
        z = ZGraph(title=title,height=height,width=width)
        z.img = img
    else:
        z = ZGraph(title=title,height=height,width=width)
    z.add(xys,color)
    z.graph(
        xmin=xmin,
        xmax=xmax,
        ymin=ymin,
        aspect_ratio=aspect_ratio,
    )
    if report:
        z.report()
    z.show()
    if return_img:
        return z.img



def get_blank_rgb(h,w):
    return np.zeros((h,w,3),np.uint8)



def pts2pixels(
    xys,
    xmin,
    xmax,
    ymin,
    aspect_ratio,
    shape_of_img,
    trim=True,
    add_indicies=True,
    colors=None,
):
    xys = na(xys)
    xymin = na((xmin,ymin))
    xymax = na((xmax,ymin+aspect_ratio*(xmax-xmin)))

    pixels = min(shape_of_img[:2]) * (xys-xymin)/(xymax-xymin)
    assert len(pixels[:,0]) >= 2
    pixels = pixels.astype(int)

    new_columns = 0
    if add_indicies:
        new_columns += 1
    if not is_None(colors):
        new_columns += 3
    if new_columns:
        nc = zeros((len(pixels),new_columns),int)
        pixels = np.concatenate((pixels,nc),axis=1) 

    if add_indicies:
        pixels[:,2] = rlen(pixels)

    if not is_None(colors):
        assert len(colors) == len(pixels)
        pixels[:,-3:] = 1*colors

    if trim:
        pixels = pixels[pixels[:,0]>=0]
        pixels = pixels[pixels[:,1]>=0]
        pixels = pixels[pixels[:,0]<shape_of_img[1]]
        pixels = pixels[pixels[:,1]<shape_of_img[0]]

    return pixels



def pts2img(
    img,
    xys,
    xmin,
    xmax,
    ymin,
    aspect_ratio,
    color=(255,255,255),
):
    if len(color) == 3 and len(shape(color)) == 1:
        colors = None
    else:
        colors = color
    pixels = pts2pixels(
        xys,
        xmin,
        xmax,
        ymin,aspect_ratio,
        shape(img),
        colors = colors,
        trim=True,
    )
    if len(color) == 3 and len(shape(color)) == 1:
        img[shape(img)[0]-1-pixels[:,1],pixels[:,0]] = color
    else:
        img[shape(img)[0]-1-pixels[:,1],pixels[:,0],:] = pixels[:,-3:]
    return pixels







if __name__ == '__main__':
    CA()

    xys=rndn(1000,2)

    if False:
        z0=ZGraph(100,100,title='ZGraph z0')
        z0.add(xys+na([-3,0]),rndint(255,size=(len(xys),3)))
        z0.graph()
        z0.report()
        z0.show()

    if True:
        z1=ZGraph(800,400,title='ZGraph z1')
        z1.add(
            xys=2*xys*na([-1,1])+na([8,-7]),
            color=rndint(255,size=(len(xys),3)),
            line_endpoint_indicies=rndint(400,size=(30,2)),
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
            xys=na([(1,1),(1,-1),(0,0)]),
            color=(255,255,0),
            line_endpoint_indicies=((0,1),(1,2),(2,0)),
            do_fill=True,
        )
        z1.graph(-9,9,-9,thickness=1,do_fill=False)
        z1.show(1.)
        z1.report()



    if False:
        plot_xys(xys*0.3+na([0.4,1.3]),img=z1.img,color=(30,127,0),width=300,height=300,xmin=-5,xmax=5,ymin=-5,aspect_ratio=1,title='using plot_xys')


    if False:
        img = get_blank_rgb(100,100)
        xys = rndn(1000,2)
        pixels=pts2img(img,xys,-3,3,-3,1,color=rndint(256,size=(len(xys),3)))
        mci(img,title='using pts2img')


    raw_enter()



