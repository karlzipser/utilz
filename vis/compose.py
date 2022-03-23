

from utilz.vis.matplotlib_ import *
import cv2



def vis_square2(
    data_in,
    padsize=1,
    padval=0.
):
    if type(data_in) is list:
        data_in = na(data_in)

    data = data_in.copy()
    
    # force the number of filters to be square
    n = int(np.ceil(np.sqrt(data.shape[0])))
    padding = ((0, n ** 2 - data.shape[0]), (0, padsize), (0, padsize)) + ((0, 0),) * (data.ndim - 3)
    data = np.pad(data, padding, mode='constant', constant_values=(padval, padval))
    
    # tile the filters into an image
    data = data.reshape((n, n) + data.shape[1:]).transpose((0, 2, 1, 3) + tuple(range(4, data.ndim + 1)))
    data = data.reshape((n * data.shape[1], n * data.shape[3]) + data.shape[4:])
    
    left = zeros((shape(data)[1],padsize,3),np.uint8) + 127
    data = np.concatenate((left,data),axis=1)
    top = zeros((padsize,shape(data)[1],3),np.uint8) + 127
    data = np.concatenate((top,data),axis=0)

    return data




def apply_rect_to_img(
    img,
    value,
    min_val,
    max_val,
    pos_color,
    neg_color,
    rel_bar_height,
    rel_bar_thickness,
    center=False,
    reverse=False,
    horizontal=False
):
    h,w,d = shape(img)
    p = (value - min_val) / (max_val - 1.0*min_val)
    if reverse:
        p = 1.0 - p
    if p > 1:
        p = 1
    if p < 0:
        p = 0
    wp = int(p*w)
    hp = int(p*h)
    bh = int((1-rel_bar_height) * h)
    bt = int(rel_bar_thickness * h)
    bw = int((1-rel_bar_height) * w)

    if horizontal:
        if center:
            if wp < w/2:
                img[(bh-bt/2):(bh+bt/2),(wp):(w/2),:] = neg_color
            else:
                img[(bh-bt/2):(bh+bt/2),(w/2):(wp),:] = pos_color
        else:
            img[(bh-bt/2):(bh+bt/2),0:wp,:] = pos_color
    else:
        if center:
            if hp < h/2:
                img[(hp):(h/2),(bw-bt/2):(bw+bt/2),:] = neg_color
            else:
                img[(h/2):(hp),(bw-bt/2):(bw+bt/2),:] = pos_color

        else:
            img[hp:h,(bw-bt/2):(bw+bt/2),:] = pos_color






def get_resize_scale(f_shape,f_max_width,f_max_height,f_min_width,f_min_height):
    s = []
    if f_shape[0] > f_max_height:
        s.append(f_max_height/(1.0*f_shape[0]))
    if f_shape[1] > f_max_width:
        s.append(f_max_width/(1.0*f_shape[1]))
    if len(s) > 0:
        #cm(0)
        return min(s)

    #print f_shape[0],f_min_height
    if f_shape[0] < f_min_height:
        s.append(f_min_height/(1.0*f_shape[0]))
    #print f_shape[1],f_min_width
    if f_shape[1] < f_min_width:
        s.append(f_min_width/(1.0*f_shape[1]))
    if len(s) > 0:
        #cm(1)
        return max(s)

    #cm(2)
    return 1.0



def get_resized_img(f,f_max_width,f_max_height,f_min_width,f_min_height):

    s = get_resize_scale(shape(f),f_max_width,f_max_height,f_min_width,f_min_height)

    if np.abs(s-1) < 0.00001:
        return f

    else:
        return cv2.resize(f, (0,0), fx=s, fy=s, interpolation=1)




def place_img_f_in_img_g(x0,y0,f,g,bottom=False,f_center=False,center_in_g=False):
    sf = shape(f)
    sg = shape(g)
    if center_in_g:
        x0 = sg[1]/2
        y0 = sg[0]/2
    x0 = intr(x0)
    y0 = intr(y0)

    if bottom:
        y0 -= sf[0]
    if f_center:
        x0 -= sf[1]/2
        y0 -= sf[0]/2

    def corner(a,b_min,b_max):
        if a <= b_max:
            if a >= b_min:
                aa = a
                da = 0
            else:
                aa = b_min
                da = a - b_min
        elif a > b_max:
            aa = b_max
            da = b_max - a
        return aa,da

    x0_,x0d_ = corner(x0,0,sg[1])
    x1 = x0 + sf[1]
    x1_,x1d_ = corner(x1,0,sg[1])

    y0_,y0d_ = corner(y0,0,sg[0])
    y1 = y0 + sf[0]
    y1_,y1d_ = corner(y1,0,sg[0])

    g0 = g.copy()

    if x1 > sg[1]:
        q = -x0_
    else:
        q = -x0d_
    if y1 > sg[0]:

        u = -y0_
    else:
        u = -y0d_
    g0[  y0_:y1_+y0d_-y0d_,  x0_:x1_+x0d_-x0d_,:] = f.copy()[-y0d_:y1_+u,-x0d_:x1_+q,:]

    return g0











def insure_rgb(img):
    if img.dtype != np.uint8:
        img = z55(img)
    if len(shape(img)) < 3 or shape(img)[2] != 3:
        img2 = zeros((shape(img)[0],shape(img)[1],3),np.uint8)
        for i in [0,1,2]:
            img2[:,:,i] = img
        img = img2
    return img


def get_image_column(img_lst):
    img = img_lst[0].copy()
    for i in range(1,len(img_lst)):
        img = np.concatenate((img,img_lst[i]),axis=0)
    return img


def get_image_row(
    img_lst,
    max_extent=0,
    blank_width=5,
    blank_color=(255,255,255),
    left_blank=True,
    right_blank=True,
    top_blank=True,
    bottom_blank=True,
):
    if not max_extent:
        for img in img_lst:
            y = shape(img)[0]
            if max_extent < y:
                max_extent = y

    blank_space = zeros((max_extent,blank_width,3),np.uint8)
    for i in rlen(blank_color):
        blank_space[:,:,i] = blank_color[i]

    img_lst2 = []
    len_img_lst = len(img_lst)
    if left_blank:
        img_lst2.append(blank_space)
    for i in range(len_img_lst):
        img = img_lst[i]
        img = insure_rgb(img)
        img = cv2.resize(
            img,
            (int(max_extent*(shape(img)[1]/shape(img)[0])),max_extent),
            interpolation=cv2.INTER_NEAREST,
        )
        img_lst2.append(img)
        if i < len_img_lst-1:
            img_lst2.append(blank_space)
    if right_blank:
        img_lst2.append(blank_space)
    img_row = np.concatenate(img_lst2,axis=1)
    if top_blank or bottom_blank:
        blank_space2 = zeros((blank_width,shape(img_row)[1],3),np.uint8)
        for i in rlen(blank_color):
            blank_space2[:,:,i] = blank_color[i]
    if top_blank and bottom_blank:
        img_lst3 = [blank_space2,img_row,blank_space2]
    elif top_blank:
        img_lst3 = [blank_space2,img_row]
    elif bottom_blank:
        img_lst3 = [img_row,blank_space2]
    else:
        img_lst3 = []
    if img_lst3:
        img_row = np.concatenate(img_lst3,axis=0)
    return img_row


#EOF


