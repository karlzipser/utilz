import sys,os
parent_path = '/'.join(__file__.split('/')[:-2])
print('\n',__file__,'adding',parent_path,'to sys.path.','\n')
sys.path.append(parent_path)

from utilz.vis import *
from utilz.karguments.input__select__menu import *
from zgraph.zgraph2d import *
from utilz.vis.other import pseudocolors


class ZGraph3d(Attr_menu_enabled):
    def __init__(
        _,
        width=400,
        height=400,
        img=None,
        title='ZGraph3d'
    ):
        _.xyzs_color_mode_list = []
        _.zgraph = ZGraph2d(
            width=width,
            height=height,
            img=img,
            title=title,
        )

    def add(
        _,
        xyzs,
        colors=((255,255,255),),
        mode='points',
    ):
        _.xyzs_color_mode_list.append((na(xyzs),colors,mode))


    def graph(
        _,
        xmin=-5,
        xmax=5,
        ymin=-5,
        transforms=[],
    ):
        for xyzs, colors, mode in _.xyzs_color_mode_list:

            xyzs = xyzs_to_4D(xyzs)

            if len(transforms):

                B = transforms[0]

                if len(transforms) > 1:
                    for C in transforms[1:]:
                        B = B @ C

                transform = B

                xyzs_trans = xyzs @ transform

            else:

                xyzs_trans = 1.0 * xyzs

            _.zgraph.add( xyzs_trans[:,:2], colors, mode )

        pixels, untrimmed_pixels = _.zgraph.graph( xmin, xmax, ymin )

        return pixels, untrimmed_pixels


    def show(_,scale=1.0):

        _.zgraph.show(scale)


    def clear(_):
        _.zgraph.clear()




def _example(
    num_pts=1000,
    num_indicies=100,
    initial_rotation_x=0,
    initial_rotation_y=0,
    initial_rotation_z=0,
    initial_scale=1,
    verbose=True,
):
    """Point cloud viewer, with examples"""

    if 'example 1':
        print('e.g. 1')

        xyzs = rndn(1000,3)
        v = ZGraph3d(img=z55(rndn(300,300,3))//2)
        v.add(rndn(4,3),colors=((45,78,198),),mode='fill')
        colors=rndint(255,size=(len(xyzs),3))
        v.add(xyzs,colors,mode='points')
        a = rndn(10,3)
        v.add(a,colors=((255,255,255),),mode='line')
        
        v.graph()
        v.show()

        raw_enter()
        for j in range(2):
            for i in range(45):
                v.zgraph.clear()
                v.graph(transforms=[get_xRotationMatrix(i)])
                v.show()
                spause()
                time.sleep(0.01)
            for i in range(45):
                v.graph(transforms=[get_yRotationMatrix(i),get_zRotationMatrix(i)])
                v.show()
                spause()
                time.sleep(0.01)

        raw_enter()



    if 'e.g. 2':

        print('e.g. 2')

        try:
            xyzs_list = lo(opjD('sample_point_cloud_list'))
        except:
            print("opjD('sample_point_cloud_list.pkl') not found")
            return


        color_list = []
        i = 30
        t0 = time.time()
        r = xyzs_list[i][:,2].copy()
        b = z55(r)
        r[r>0.5]=0.5
        r=z2o(r)
        r *= 255
        r = r.astype(np.uint8)
        g = 255-r
        rgb = zeros((len(xyzs_list[i]),3),np.uint8)
        rgb[:,0] = r
        rgb[:,1] = g
        rgb[:,2] = b
        color_list.append(rgb)

        olist = []
        for j in [20]:#range(10,33,3):
            v = ZGraph3d(300,600)
                
            v.add(xyzs_list[i][:,:3],color_list[0],mode='points')

            pixels, untrimmed_pixels = v.graph(-j,j,0,transforms=[get_zRotationMatrix(-90)])
            #v.show()

            t1 = time.time()-t0
            print(dp(1/t1))

            ol, P, O = check_pixel_overlap(pixels,j)
            olist.append(ol)
            if False:
                for p in P:
                    if len(P[p]) > 1:
                        v.zgraph.img[2000-p[1],p[0],:] = 255
            mi(v.zgraph.img,0);spause()
            raw_enter()


def check_pixel_overlap(pixels,f):
    P = {}
    for p in pixels:
        x,y = p[0],p[1]
        xy = (x,y)
        if xy not in P:
            P[xy] = []
        P[xy].append(p)
    O = {}
    for xy in P:
        n = len(P[xy])
        if n not in O:
            O[n] = 0
        O[n] += 1

    vals = na(list(O.values()))
    figure(f)
    clf()
    plot(O.keys(),vals/np.sum(vals),'o')
    spause()
    return (f,O[1]/np.sum(vals)),P,O






if __name__ == '__main__':
    fire.Fire(_example)

#EOF
