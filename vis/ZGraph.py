
from utilz.vis.cv2_ import *



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




class ZGraph:
    def __init__(
        _,
        width=400,
        height=400,
        title='ZGraph'
    ):
        _.title = title
        _.width = width
        _.height = height
        _.img = get_blank_rgb(height,width)
        _.xys_color_list = []
        _.plot_called = False
        _.xmin = None
        _.xmax = None
        _.ymin = None
        _.ymax = None
        _.aspect_ratio = 1.0
<<<<<<< HEAD
        _.pixels_list = []
=======
        _.pixels = []
>>>>>>> a2f601e9987f0572eba136c0c3a54ca2b84641e2

    def add(_,xys,color=(255,255,255),line_endpoint_indicies=[]):
        _.xys_color_list.append((na(xys),color,line_endpoint_indicies))

    def _find_min_max(_,aspect_ratio_one=True):
        xmins = []
        xmaxes = []
        ymins = []
        for xys,color in _.xys_color_list:
            xmins.append(xys[:,0].min())
            xmaxes.append(xys[:,0].max())
            ymins.append(xys[:,1].min())
        if is_None(_.xmin):
            _.xmin = min(xmins)
        if is_None(_.xmax):
            _.xmax = max(xmaxes)
        if is_None(_.ymin):
            _.ymin = min(ymins)
<<<<<<< HEAD

=======
>>>>>>> a2f601e9987f0572eba136c0c3a54ca2b84641e2

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

        _.plot_called = True
<<<<<<< HEAD

        for xys,color,line_endpoint_indicies in _.xys_color_list:
            pixels = pts2img(_.img,xys,_.xmin,_.xmax,_.ymin,_.aspect_ratio,color)
            _.pixels_list.append(pixels)

            if len(line_endpoint_indicies):
                
                valid_enpoint_indicies = []
                p = pixels[:,2]
                for a in line_endpoint_indicies:
                    si = np.where(p==a[0])[0]
                    ei = np.where(p==a[1])[0]
                    if len(si) > 0 and len(ei) > 0:
                        valid_enpoint_indicies.append((si[0],ei[0]))
                for j in rlen(valid_enpoint_indicies):
                    a,b = line_endpoint_indicies[j]
                    x0,y0 = pixels[a][:2]
                    x1,y1 = pixels[b][:2]
                    if len(pixels[a]) < 6:
                        c = [255,0,0]
                    else:
                        c = pixels[a][3:6].tolist()
                    cv2.line(
                        _.img,
                        (x0,shape(_.img)[0]-1-y0),(x1,shape(_.img)[0]-1-y1),
                        color=c,
                        thickness=thickness,
=======
        for xys,color in _.xys_color_list:
            pixels = pts2img(_.img,xys,_.xmin,_.xmax,_.ymin,_.aspect_ratio,color)
            if not len(_.pixels):
                _.pixels = pixels
            else:
                _.pixels = np.concatenate((_.pixels,pixels))

        if False:
            pixels = _.pixels
            line_endpoint_indicies = rndint(1000,size=(30,2))#((1,2),(4,9),(100,200))
            valid_enpoint_indicies = []
            p = pixels[:,2]
            for a in line_endpoint_indicies:
                si = np.where(p==a[0])[0]
                ei = np.where(p==a[1])[0]
                if len(si) > 0 and len(ei) > 0:
                    valid_enpoint_indicies.append((si[0],ei[0]))
            for j in rlen(valid_enpoint_indicies):
                a,b = line_endpoint_indicies[j]
                x0,y0 = pixels[a][:2]
                x1,y1 = pixels[b][:2]
                cg(x0,y0,x1,y1)
                #p = pixels[i][2:]
                #c = na([p[0],p[1],p[2]])
                #c = c.astype(np.uint8)
                #print(type(c[0]),type(c[1]))
                print(pixels[a])
                if len(pixels[a]) < 6:
                    c = [255,0,0]
                else:
                    c = [0,255,0]
                    c=[int(pixels[a][3]),int(pixels[a][4]),int(pixels[a][5])]
                    #c = [0,255,0]
                    cm(c)
                #cm(c,r=1)
                cv2.line(
                    _.img,
                    (x0,shape(_.img)[0]-1-y0),(x1,shape(_.img)[0]-1-y1),
                    #(x0,y0),(x1,y1),
                    color=c,
                    thickness=3,
>>>>>>> a2f601e9987f0572eba136c0c3a54ca2b84641e2
                )
    def show(_,scale=1.0):
        scale = float(scale)
        if not _.plot_called:
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
        _.plot_called = False
        _.xys_color_list = []
        _.img *= 0
        

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



def _test_ZGraph():
    xys=rndn(1000,2)
    z=ZGraph(400,200,title='zgraph1')
<<<<<<< HEAD
    z.add(
        xys=2*xys*na([-1,1])+na([8,-7]),
        color=rndint(255,size=(len(xys),3)),
        line_endpoint_indicies=rndint(400,size=(30,2)),
    )
    z.add(
        xys=1*xys*na([-1,1])+na([12,3]),
        color=zeros((len(xys),3),np.uint8)+(255,127,31),
        line_endpoint_indicies=rndint(400,size=(30,2)),
    )
    z.add(xys+na([-5,4]),(50,255,255),line_endpoint_indicies=rndint(200,size=(30,2)))# rndint(255,size=(len(xys),3)))# 
    z.graph(-9,9,-9,thickness=2)
=======
    z.add(3*xys*na([-1,1])+na([8,-6]),rndint(255,size=(len(xys),3)))#(255,128,0))#
    z.add(xys+na([-5,4]), rndint(255,size=(len(xys),3)))#,(50,255,255)) 
    z.graph(-9,9,-9)
>>>>>>> a2f601e9987f0572eba136c0c3a54ca2b84641e2
    z.show(1.)
    z.report()

    if False:
        z2=ZGraph(400,400,title='zgraph2')
        z2.add(xys+na([-3,0]),rndint(255,size=(len(xys),3)))
        z2.graph(-9,9,-9)
        z2.report()
        z2.show()

    if False:
        plot_xys(xys,img=z.img,width=300,height=300,xmin=-5,xmax=5,ymin=-5,aspect_ratio=1,title='plot_xys')
        plot_xys(xys*0.1+na([0.4,1.3]),img=z.img,color=(30,127,0),width=300,height=300,xmin=-5,xmax=5,ymin=-5,aspect_ratio=1,title='plot_xys')


    if False:
        img = get_blank_rgb(100,100)
        xys = rndn(1000,2)
        pixels=pts2img(img,xys,-3,3,-3,1,color=rndint(256,size=(len(xys),3)))
        mi(img)



    raw_enter()



if __name__ == '__main__':
    CA()
    _test_ZGraph()


