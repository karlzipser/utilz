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
        title='ZGraph3d'
    ):
        _.xyzs_color_mode_list = []
        _.zgraph = ZGraph2d(width,height,title)


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
        transform=None,
    ):
        _.zgraph.clear()

        for xyzs, colors, mode in _.xyzs_color_mode_list:

            xyzs = xyzs_to_4D(xyzs)

            if transform is not None:

                xyzs_trans = xyzs @ transform

            else:

                xyzs_trans = 1.0 * xyzs

            _.zgraph.add( xyzs_trans[:,:2], colors, mode )

        pixels, untrimmed_pixels = _.zgraph.graph( xmin, xmax, ymin )

        return pixels, untrimmed_pixels



    def show(_,scale=1.0):

        _.zgraph.show(scale)


            




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
        v = ZGraph3d()
        v.add(rndn(4,3),colors=((45,78,198),),mode='fill')
        colors=rndint(255,size=(len(xyzs),3))
        v.add(xyzs,colors,mode='points')
        a = rndn(10,3)
        v.add(a,colors=((255,255,255),),mode='line')
        
        v.graph()
        v.show()

        raw_enter()
        for j in range(5):
            for i in range(45):
                v.graph(transform=get_xRotationMatrix(i))
                v.show()
                spause()
                time.sleep(0.01)
            for i in range(45):
                v.graph(transform=get_yRotationMatrix(i))
                v.show()
                spause()
                time.sleep(0.01)

        raw_enter()


if __name__ == '__main__':
    fire.Fire(_example)

#EOF
