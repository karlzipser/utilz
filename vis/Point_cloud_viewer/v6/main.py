
from utilz.vis import *
from utilz.karguments.input__select__menu import *
from utilz.vis.ZGraph.v1.zgraph import *
from utilz.vis.other import pseudocolors


class Viewer(Attr_menu_enabled):
    def __init__(
        _,
        xyzs_list=[],

        img_width=300,
        img_height=300,
        color_list=[],
        line_endpoint_indicies_list=[],
        fill_indicies_list=[],
        title='Viewer',
    ):
        Attr_menu_enabled.__init__(_)
        assert type(xyzs_list) == list
        assert type(color_list) == list
        assert type(line_endpoint_indicies_list) == list
        assert type(fill_indicies_list) == list
        _.xyzs_list = xyzs_list
        _.color_list = color_list
        _.line_endpoint_indicies_list = line_endpoint_indicies_list
        _.fill_indicies_list = fill_indicies_list
        _.xmin = xmin
        _.xmax = xmax
        _.ymin = ymin
        _.img_width, _.img_height = img_width, img_height
        _.title = title
        _.zgraph = ZGraph(_.img_width,_.img_height,_.title)


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
        ymin=-5,,
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


        v = Viewer(
            xyzs_list=xyzs_list,
            xmin=xmin,
            xmax=xmax,
            ymin=ymin,
            color_list=color_list,
            line_endpoint_indicies_list=line_endpoint_indicies_list,
            fill_indicies_list=fill_indicies_list,
        )

        v.interactive_loop(
        )


    

    if 'example 2':
        print('e.g. 2')
        try:
            xyzs_list = lo(opjD('sample_point_cloud_list'))
        except:
            print("opjD('sample_point_cloud_list.pkl') not found")
            return

        color_list = []
        
        for i in rlen(xyzs_list):
            #xyzs_list[i][:,2] *= -1
            if verbose:
                percent(i,len(xyzs_list),title='color_list')
            """
            for j in rlen(xyzs_list[i]):
                z = xyzs_list[i][j][2]
                colors.append(  255*na(pseudocolors(z,-2,5,243))  )
            """
            rgbs = pseudocolors(xyzs_list[i][:,2],-1.5,1.5,243)
            color_list.append(rgbs)
        

        line_endpoint_indicies_list = []
        fill_indicies_list = []
        
        xmin,xmax,ymin = -10,50,-30

        MetaData = dict(
            imgs={},
            xyzs={},
            fill={},
            pixels={},
        )

        v = Viewer(
            xyzs_list=xyzs_list,
            xmin=xmin,
            xmax=xmax,
            ymin=ymin,
            img_height=1000,
            img_width=1000,
            color_list=color_list,
            line_endpoint_indicies_list=line_endpoint_indicies_list,
            fill_indicies_list=fill_indicies_list,
        )

        v.interactive_loop(
            initial_rotation_x=initial_rotation_x,
            initial_rotation_y=initial_rotation_y,
            initial_rotation_z=initial_rotation_z,
            initial_scale=initial_scale,
            MetaData=MetaData,
        )



if __name__ == '__main__':
    fire.Fire(_example)

#EOF
