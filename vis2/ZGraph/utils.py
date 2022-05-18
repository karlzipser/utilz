
from utilz.vis import *

print(__file__)

def pts2img(
    img,
    xys,
    xmin,
    xmax,
    ymin,
    aspect_ratio,
    colors=((255,255,255),),
    change=True,
):
    """Project array of x-y points into an RGB image.

    Keyword arguments:
    img  -- img to receive points
    xys  -- an array of shape nx2 holding n x-y point
    xmin -- the min x value to be plotted
    xmax -- the max x value to be plotted
    ymin -- the min y value to be plotted (a value for ymax is calculated.)    
    aspect_ratio -- aspect ratio applied to pixel representation
    colors -- is this is a single RGB value, it will be applied to every
            pixel. If an array of colors, it will be applied colorwise.
    """
    
    pixels,untrimmed_pixels = pts2pixels(
        xys,
        xmin,
        xmax,
        ymin,aspect_ratio,
        shape(img),
        colors = colors,
    )
    if change:
        if len(colors) == 3 and len(shape(colors)) == 1:
            img[shape(img)[0]-1-pixels[:,1],pixels[:,0]] = colors
        else:
            img[shape(img)[0]-1-pixels[:,1],pixels[:,0],:] = pixels[:,-3:]
    return pixels,untrimmed_pixels




def pts2pixels(
    xys,
    xmin,
    xmax,
    ymin,
    aspect_ratio,
    shape_of_img,
    colors=((255,255,255),),
):
    """Project array of x-y points into pixel array with optional indicies and colors.

    Keyword arguments:
    xys  -- an array of shape nx2 holding n x-y points
    xmin -- the min x value to be plotted
    xmax -- the max x value to be plotted
    ymin -- the min y value to be plotted (a value for ymax is calculated using aspect_ratio.)
    aspect_ratio -- aspect ratio applied to pixel representation
    shape_of_img -- shape(img) sent as a parameter to function
    add_indicies -- add an indicies column to pixels so that mapping to
                    xys is maintained after trimming (default True)
    colors -- 3 column of rgb values to concatenate to pixels (default None)

    pixels is an nxm array of int. It can't be uint8 because of the indicies column.
    If add_indicies is False, it is nx2.
    If add_indicies is true, it is nx3. If colors is not None, it is nx6.

    Both pixels and untrimmed_pixels are returned. In trimming points are lost
    which can cause problems later.

    [
        [ x, y, i, r, g, b ],
               . . . ,         
    ]
    """

    xys = na(xys)
    xymin = na( ( xmin, ymin ) )
    xymax = na( ( xmax, ymin+aspect_ratio*(xmax-xmin) ) )
    #cm(min(shape_of_img[:2]),(xys-xymin)/(xymax-xymin) )
    pixels = min(shape_of_img[:2]) * (xys-xymin)/(xymax-xymin)
    assert len(pixels[:,0]) >= 2
    pixels = pixels.astype(int)
    
    new_columns = 4
    nc = zeros((len(pixels),new_columns),int)
    pixels = np.concatenate((pixels,nc),axis=1) 

    pixels[:,2] = rlen(pixels)

    assert shape(colors)[1] == 3 # i.e., rgb value(s)
    assert len(colors) == 1 or len(colors) == len(pixels)
    pixels[:,-3:] = 1*colors

    untrimmed_pixels = pixels.copy()

    pixels = pixels[pixels[:,0]>=0]
    pixels = pixels[pixels[:,1]>=0]
    pixels = pixels[pixels[:,0]<shape_of_img[1]]
    pixels = pixels[pixels[:,1]<shape_of_img[0]]

    return pixels,untrimmed_pixels






def xyzs_to_4D(xyzs,assume_all_ones=True):
    s = shape(xyzs)
    assert len(s) == 2
    assert s[1] >= 3
    if s[1] == 4:
        if assume_all_ones:
            if xyzs[0,3] == 1:
                return xyzs
        xyzs[:,3] = 1
    elif s[1] == 3:
        xyzs = np.concatenate((xyzs,1+zeros((s[0],1))),1)
    else:
        assert False
    return xyzs





def _example(height=100,width=200,n_pts=400,xmin=-3,xmax=3,ymin=-3):
    """Test out """+__file__


    print('e.g. 1')
    img = get_blank_rgb(height,width);
    print(shape(img))
    raw_enter()


    print('e.g. 2')

    pixels,untrimmed_pixels = pts2pixels(
        xys=rndn(n_pts,2),
        xmin=xmin,
        xmax=xmax,
        ymin=ymin,
        aspect_ratio=1.0,
        shape_of_img=(width,height,3),
        colors=z55(randint(255,size=(n_pts,3))),
    )


    plot(pixels[:,:2],'k',label='pixel xys')
    plot(pixels[:,2],'b',label='indicies')
    plot(pixels[:,-3:],'r',label='RGBs')
    plt.legend(loc="upper left")
    plt.title('pts2pixels, trim=True')
    plt.ylabel('value')
    plt.xlabel('index')
    spause()
    raw_enter()


    print('e.g. 3')
    pts2img(
        img,
        xys=rndn(1000,2),
        xmin=xmin,
        xmax=xmax,
        ymin=ymin,
        aspect_ratio=1.0,
        colors=((23,98,243),),
    )

    CA()
    mi(img)
    spause()
    raw_enter()





    print('e.g. 4')
    pts2img(
        img,
        xys=rndn(n_pts,2)+(5,0),
        xmin=xmin,
        xmax=xmax,
        ymin=ymin,
        aspect_ratio=1.0,
        colors=randint(256,size=(n_pts,3))
    )

    CA()
    mi(img)
    raw_enter()
    





if __name__ == '__main__':
    fire.Fire(_example)





