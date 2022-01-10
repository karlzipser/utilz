
########################################################################################
########################################################################################
########################################################################################
####
def CV2Plot1(img,pixels_per_unit,x_origin_in_pixels=None,y_origin_in_pixels=None):
    height_in_pixels = shape(img)[0]
    width_in_pixels = shape(img)[0]
    if x_origin_in_pixels == None:
        x_origin_in_pixels = intr(width_in_pixels/2.0)
    if y_origin_in_pixels == None:
        y_origin_in_pixels = intr(height_in_pixels/2.0)
    D = {}
    D['verbose'] = False
    if D['verbose']:
        cy(x_origin_in_pixels,y_origin_in_pixels)
    D['image'] = zeros((height_in_pixels,width_in_pixels,3),np.uint8)
    def function_show(autocontrast=False,delay=1,title='image',scale=1.0):
        
        img = D['image']
        if autocontrast:
            img = z2_255_by_channel(img)
            #cg(img.min(),img.max())
        mci(img,scale=scale,delay=delay,title=title)
    def function_safe(px,py):
        if px >= 0:
            if py >= 0:
                if py < height_in_pixels:
                    if px < width_in_pixels:
                        return True
        if D['verbose']:
            cr('not safe')
        return False
    def function_get_pixel(x,y):
        px = intr(x * pixels_per_unit)
        py = intr(-y * pixels_per_unit)
        px += x_origin_in_pixels
        py += y_origin_in_pixels
        if D['verbose']:
            cb(x,y,"->",px,py)
        return px,py
    def function_plot_point_xy_version(x,y,c=[255,255,255],add_mode=False):
        px,py = D['get pixel'](x,y)
        if D['safe?'](px,py):
            if not add_mode:
                D['image'][py,px,:] = c
            else:
                D['image'][py,px,:] += na(c,np.uint8)
    def function_pts_plot(xys,c=[255,255,255],add_mode=False):
        if type(c) == str:
            if add_mode:
                n = 1
            else:
                n = 255
            if c == 'r':
                c = [n,0,0]
            elif c == 'g':
                c = [0,n,0]
            elif c == 'b':
                c = [0,0,n]  
            else:
                cr('warning, unknown color:',c)
                c = [255,255,255]
        for i in rlen(xys):
            D['plot point (xy_version)'](xys[i,0],xys[i,1],c,add_mode)
    def function_clear():
        D['image'] *= 0
    D['show'] = function_show
    D['safe?'] = function_safe
    D['plot point (xy_version)'] = function_plot_point_xy_version
    D['get pixel'] = function_get_pixel
    D['pts_plot'] = function_pts_plot
    D['clear'] = function_clear
    return D

#
########################################################################################
####
########################################################################################
########################################################################################
########################################################################################

########################################################################################
########################################################################################
########################################################################################
####
def CV2Plot(height_in_pixels,width_in_pixels,pixels_per_unit,x_origin_in_pixels=None,y_origin_in_pixels=None):
    if x_origin_in_pixels == None:
        x_origin_in_pixels = intr(width_in_pixels/2.0)
    if y_origin_in_pixels == None:
        y_origin_in_pixels = intr(height_in_pixels/2.0)
    D = {}
    D['type'] = 'CV2Plot'
    D['verbose'] = False
    if D['verbose']:
        cy(x_origin_in_pixels,y_origin_in_pixels)
    D['image'] = zeros((height_in_pixels,width_in_pixels,3),np.uint8)

    D['height_in_pixels'] = height_in_pixels
    D['width_in_pixels'] = width_in_pixels
    D['pixels_per_unit'] = pixels_per_unit
    D['x_origin_in_pixels'] = x_origin_in_pixels
    D['y_origin_in_pixels'] = y_origin_in_pixels


    def function_show(
        autocontrast=False,
        delay=1,
        title='image',
        scale=1.0,
        fx=0,
        fy=0,
        autocontrast2=False,
        threshold=0,
        return_img=False
        ):
        
        img = D['image']
        if threshold > 0:
            img[img>threshold] = threshold
        if autocontrast:
            img = z2_255_by_channel(img)
        elif autocontrast2:
            img = z2_255(img)
        if return_img:
            return img
        return mci(img,scale=scale,fx=fx,fy=fy,delay=delay,title=title)
    def function_safe(px,py):
        if px >= 0:
            if py >= 0:
                if py < height_in_pixels:
                    if px < width_in_pixels:
                        return True
        if D['verbose']:
            cr('not safe')
        return False
    def function_get_pixel(x,y):
        px = intr(x * pixels_per_unit)
        py = intr(-y * pixels_per_unit)
        px += x_origin_in_pixels
        py += y_origin_in_pixels
        if D['verbose']:
            cb(x,y,"->",px,py)
        return px,py
    def function_plot_point_xy_version(x,y,c=[255,255,255],add_mode=False):
        px,py = D['get pixel'](x,y)
        if D['safe?'](px,py):
            if not add_mode:
                D['image'][py,px,:] = c
            else:
                D['image'][py,px,:] += na(c,np.uint8)
    def function_pts_plot(xys,c=[255,255,255],add_mode=False):
        if type(c) == str:
            if add_mode:
                n = 1
            else:
                n = 255
            if c == 'r':
                c = [n,0,0]
            elif c == 'g':
                c = [0,n,0]
            elif c == 'b':
                c = [0,0,n]  
            else:
                cr('warning, unknown color:',c)
                c = [255,255,255]
        for i in rlen(xys):
            D['plot point (xy_version)'](xys[i,0],xys[i,1],c,add_mode)
    def function_grid(c=[255,0,0]):
        D['image'][:,int(width_in_pixels/2),:] = c
        D['image'][int(height_in_pixels/2),:,:] = c

    def function_clear():
        D['image'] *= 0
    D['show'] = function_show
    D['grid'] = function_grid
    D['safe?'] = function_safe
    D['plot point (xy_version)'] = function_plot_point_xy_version
    D['get pixel'] = function_get_pixel
    D['pts_plot'] = function_pts_plot
    D['clear'] = function_clear
    return D

#
########################################################################################
#



def wk(t_seconds):
    k = cv2.waitKey(int(t_seconds*1000.0))
    if k == ord('q'):
        print('quit')
        return
    else:
        return k

