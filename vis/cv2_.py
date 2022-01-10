
from utilz.misc import *
from utilz.core.znp import *
import cv2
try:
    # pip install opencv-python==4.1.2.30
    import cv2
    imread = cv2.imread
    imsave = cv2.imwrite
except:
    if False:
        cr("*** Couldn't import cv2 ***")
        if 'torch' in sys.modules:
            cr("Note, torch already imported. This can block normal cv2 import.")




try:
    def function_close_all_windows():
        import matplotlib.pyplot as plt
        plt.close('all')
        try:
            cv2.destroyAllWindows()
        except:
            pass
    CA = function_close_all_windows

    def mci(
        img,
        delay=33,
        title='mci',
        extent=0,
        scale=1.0,
        color_mode=cv2.COLOR_RGB2BGR,
        fx=0,
        fy=0,
        interpolation=cv2.INTER_AREA,
    ):
        title = d2s(title)
        if not fx and not fx:
            fx = scale
            fy = scale
        if len(shape(img)) == 2:
            color_mode = cv2.COLOR_GRAY2BGR
        img = cv2.cvtColor(img,color_mode)
        if scale and not extent and fx * fy == 0:
            scale_img = zresize(img=img,p=1.0*scale,interpolation=interpolation)
        elif extent:
            assert type(extent) is int
            scale_img = zresize(img=img,p=extent,interpolation=interpolation)
        elif fx*fy > 0:
            scale_img = cv2.resize(img, (0,0), fx=fx, fy=fy, interpolation=interpolation)
        else:
            scale_img = img

        cv2.imshow(title,scale_img)
        k = cv2.waitKey(delay)
        return k


    def mcia(img_block,delay=33,title='mcia',scale=1.0,color_mode=cv2.COLOR_RGB2BGR):
        assert(len(shape(img_block)) == 4)
        for i in range(shape(img_block)[0]):
            k = mci(img_block[i,:,:,:],delay=delay,title=title,scale=scale,color_mode=color_mode)
            if k == ord('q'):
                return


    def mcia_folder(path,delay=33,title='mcia_folder',scale=1.0,color_mode=cv2.COLOR_RGB2BGR):
        l=load_img_folder_to_list(path)
        mcia(array(l),delay=delay,title=title,scale=scale,color_mode=cv2.COLOR_RGB2BGR)


    def resize_to_extent(img,extent,interpolation=cv2.INTER_AREA): #INTER_LINEAR):
        if extent != max(shape(img)):
            q = extent / max(shape(img))
            scale_percent = 60 # percent of original size
            width = int(img.shape[1] * q)
            height = int(img.shape[0] * q)
            dim = (width, height)
            return cv2.resize(img, dim, interpolation=interpolation)
        else:
            print('resize_to_extent(): no resizing')
            return img

    def xtrans(xs,min_,max_,dstmax):
        #a = (xs + offset) / scale
        #a = dstmax * a
        a = xs - min_
        b = a / (max_ - min_)
        c = b * dstmax
        return c

    def zplot(
        img,
        xs,
        ys,
        sym='.-',
        color=False,
        thickness=1,
        cthickness=1,
        radius=4,
    ):
        x,x_prev = False,False

        for i in rlen(xs):

            if type(x) is not bool:
                x_prev = x
                y_prev = y

            x,y = intr(xs[i]),intr(ys[i])

            if color:
                assert len(color)==3

            elif 'r' in sym:
                color = (255,0,0)

            elif 'b' in sym:
                color = (0,0,255)

            else:
                color = (128,128,0)

            if '.' in sym:
                cv2.circle(img,(x,y),radius,color,cthickness)

            if '-' in sym:
                if type(x_prev) is not bool:
                    cv2.line(img,(x_prev,y_prev),(x,y),color,thickness)



    def zresize(img,p,interpolation=cv2.INTER_AREA):
        if type(p) is int:
            return resize_to_extent(img,p,interpolation=interpolation)
        else:
            sz = (p * na(shape(img))[:2]).astype(int)
            #print(sz)
            sz = list(sz)
            #print(sz)
            sz.reverse()
            sz = tuple(sz)
            #sz  = list((p * na(shape(img))[:2]).astype(int)).reverse()
            #cm(sz)
            img = cv2.resize(img,dsize=sz,interpolation=interpolation)
            return img



except:
    print("Don't have cv2")







if __name__ == '__main__':
    
    eg(__file__)

    mci(z55(rndn(20,20,3)),scale=20)

    raw_enter()
#EOF