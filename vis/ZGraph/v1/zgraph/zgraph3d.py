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
        img_width=300,
        img_height=300,
        title='Viewer',
    ):
        Attr_menu_enabled.__init__(_)
        _.xyzs_color_mode_list = []
        _.zgraph = ZGraph2d(img_width,img_height,title)

        _.Transformations = {
            'x' : get_xRotationMatrix,
            'y' : get_yRotationMatrix,
            'z' : get_zRotationMatrix,
            's' : get_xyzScalingMatrix,
            'e' : get_xTranslationMatrix,
            'r' : get_yTranslationMatrix,
            't' : get_zTranslationMatrix,
        }

        _.attrs_to_dict()


    def add(
        _,
        xyzs,
        mode='points',
        color=((255,255,255),),
    ):
        _.xyzs_color_mode_list.append((na(xyzs),color,mode))


    def graph(
        _,
        xmin=-5,
        xmax=5,
        ymin=-5,
        transform=None,
    ):
        _.zgraph.clear()

        for xyzs, color, mode in _.xyzs_color_mode_list:

            if transform is not None:

                xyzs = xyzs @ transform

            else:

                xyzs = 1.0 * xyzs

            _.zgraph.add( xyzs[:,:2], color, mode )

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
        """
        xyzs_list = []
        color_list = []
        line_endpoint_indicies_list = []
        fill_indicies_list = []

        
        for i in range(20):
            xyzs = rndn(num_pts,3)
            xyzs_list.append(xyzs)
            color_list.append(rndint(255,size=(len(xyzs_list[0]),3)))
            line_endpoint_indicies_list.append(rndint(num_indicies,size=(30,2)))
            fill_indicies_list.append(
                [
                    rndint(num_indicies,size=(3)),
                    rndint(num_indicies,size=(3)),
                    rndint(num_indicies,size=(3))
                ]
            )
        xmin,xmax,ymin = -5,5,-5
        """
        xyzs = rndn(1000,4)
        v = ZGraph3d()
        v.add(xyzs,color=rndint(255,size=(len(xyzs),3)),mode='points')
        v.graph()
        v.show()

        raw_enter()





if __name__ == '__main__':
    fire.Fire(_example)

#EOF
