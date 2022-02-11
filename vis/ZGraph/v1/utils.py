
from utilz.vis import *


def pts2img(
    img,
    xys,
    xmin,
    xmax,
    ymin,
    aspect_ratio,
    color=(255,255,255),
):
    """Project array of x-y points into an RGB image.

    Keyword arguments:
    img  -- img to receive points
    xys  -- an array of shape nx2 holding n x-y point
    xmin -- the min x value to be plotted
    xmax -- the max x value to be plotted
    ymin -- the min y value to be plotted (a value for ymax is calculated.)    
    aspect_ratio -- aspect ratio applied to pixel representation
    color -- is this is a single RGB value, it will be applied to every
            pixel. If an array of colors, it will be applied colorwise.
    """

    if len(color) == 3 and len(shape(color)) == 1:
        colors = None
    else:
        colors = color
    pixels,untrimmed_pixels = pts2pixels(
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
    return pixels,untrimmed_pixels




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
    """Project array of x-y points into pixel array with optional indicies and colors.

    Keyword arguments:
    xys  -- an array of shape nx2 holding n x-y points
    xmin -- the min x value to be plotted
    xmax -- the max x value to be plotted
    ymin -- the min y value to be plotted (a value for ymax is calculated.)
    aspect_ratio -- aspect ratio applied to pixel representation
    shape_of_img -- shape(img) sent as a parameter to function
    trim -- remove pixels that are outside of image frame (default True)
    add_indicies -- add an indicies column to pixels so that mapping to
                    xys is maintained after trimming (default True)
    colors -- a column of colors to concatenate to pixels (default None)

    pixels is an nxm array of int. It can't be uint8 because of the indicies column.
    If add_indicies is False, it is nx2.
    If add_indicies is true, it is nx3. If colors is not None, it is nx6.
    """
    xys = na(xys)
    xymin = na((xmin,ymin))
    xymax = na((xmax,ymin+aspect_ratio*(xmax-xmin)))

    pixels = min(shape_of_img[:2]) * (xys-xymin)/(xymax-xymin)
    assert len(pixels[:,0]) >= 2
    pixels = pixels.astype(int)
    untrimmed_pixels = pixels.copy()

    new_columns = 0
    if add_indicies:
        new_columns += 1
    if not colors is None:
        new_columns += 3
    if new_columns:
        nc = zeros((len(pixels),new_columns),int)
        pixels = np.concatenate((pixels,nc),axis=1) 

    if add_indicies:
        pixels[:,2] = rlen(pixels)

    if not colors is None:
        assert len(colors) == len(pixels)
        pixels[:,-3:] = 1*colors

    if trim:
        pixels = pixels[pixels[:,0]>=0]
        pixels = pixels[pixels[:,1]>=0]
        pixels = pixels[pixels[:,0]<shape_of_img[1]]
        pixels = pixels[pixels[:,1]<shape_of_img[0]]

    return pixels,untrimmed_pixels







def _example(height=100,width=200,n_pts=400,xmin=-3,xmax=3,ymin=-3):
    """Test out """+__file__


    print('e.g. 1')
    img = get_blank_rgb(height,width);
    print(shape(img))
    raw_enter()


    print('e.g. 2')

    q = pts2pixels(
        xys=rndn(n_pts,2),
        xmin=xmin,
        xmax=xmax,
        ymin=ymin,
        aspect_ratio=1.0,
        shape_of_img=(width,height,3),
        trim=True,
        add_indicies=True,
        colors=z55(rndn(n_pts,3)),
    )


    plot(q[:,:2],'k',label='pixel xys')
    plot(q[:,2],'b',label='indicies')
    plot(q[:,-3:],'r',label='RGBs')
    plt.legend(loc="upper left")
    plt.title('pts2pixels, trim=True')
    plt.ylabel('value')
    plt.xlabel('index')
    spause()
    raw_enter()


    print('e.g. 3')
    pts2img(
        img,
        xys=rndn(n_pts,2),
        xmin=xmin,
        xmax=xmax,
        ymin=ymin,
        aspect_ratio=1.0,
        color=randint(256,size=(n_pts,3))
    )

    CA()
    mi(img)
    raw_enter()
    

if __name__ == '__main__':
    fire.Fire(_example)





