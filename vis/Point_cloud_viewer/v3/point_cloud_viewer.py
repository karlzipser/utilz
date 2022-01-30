
from utilz.vis import *
from utilz.karguments.input__select__menu import *
from utilz.vis.ZGraph.zgraph import *



class Viewer(Attr_menu_enabled):
    def __init__(
        _,
        xyzs_list=[],
        xmin=-5,
        xmax=5,
        ymin=-5,
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
        _.xyzs_index = 0
        _.color_list = color_list
        _.line_endpoint_indicies_list = line_endpoint_indicies_list
        _.fill_indicies_list = fill_indicies_list
        _.xmin = xmin
        _.xmax = xmax
        _.ymin = ymin
        _.img_width,_.img_height = img_width,img_height
        _.title = title
        _.zgraph = ZGraph(_.img_width,_.img_height,_.title)
        _.transformation_list = []
        _.help_str = """'h' : help
         u : undo last transformation
         x<float> : rotate along x axis <float> degrees
             e.g., x9.3
         y<float> : rotate along y axis <float> degrees
         z<float> : rotate along z axis <float> degrees
         e<float> : translate along x axis
         r<float> : translate along y axis
         t<float> : translate along z axis
         l : show transformation_list
         - : back in point cloud list
         = : forward in point cloud list
         m : attribute menu

         # To Do:
         # change xymin,xymax
         # allow running from commandline with point cloud file
         # path, cloud index
         # plot size as argument
         # --also draw separate images with centered square representing
         # height
         # --find way to map output colors to correct colors
        """

        box(_.help_str)



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



    def get_img(_):
        xyzs_ = _.xyzs @ _.transform
        _.zgraph.add(xyzs_[:,:2],_.color,_.line_endpoint_indicies,_.fill_indicies)
        _.zgraph.graph(_.xmin,_.xmax,_.ymin)
        return _.zgraph.img



    def interactive_loop(
        _,
        MetaData=None,
        dont_interact=False,
        initial_rotation=(),
    ):
        if len(initial_rotation):
            for ir in initial_rotation:
                axis = ir[0]
                val = ir[1]
                assert type(axis) is str
                assert type(val) in [int,float]
                s = d2n(axis,val)
                A = _.Transformations[s[0]](initial_rotation)
                _.transformation_list.append( (s,A) )

        s = '='


        while True:

            A = None

            undo = False

            s_prev = s

            if s == '':
                s = s_prev

            if s == 'q':
                break

            if not s:
                continue

            if s[0] == 'h':
                box(_.help_str)

            elif s == 'm':
                print('hit enter to exit menu')
                while _.seta():
                    pass
                _.zgraph = _.zgraph = ZGraph(_.img_width,_.img_height,_.title)

            elif s[0] in _.Transformations.keys() and len(s) > 1:
                value = s[1:]
                if str_is_float(value):
                    value = float(value)
                    A = _.Transformations[s[0]](value)
                    print(s[0],value,'\n',A)
                else:
                    cE(qtds(value),'not float')
                    continue

            elif s[0] == 'u':
                undo = True
                if len(_.transformation_list):
                    print('undo',_.transformation_list[-1][0])
                else:
                    print('\tTransformation_list is empty.')

            elif s[0] == 'l':
                print('transformation_list:')
                for a in _.transformation_list:
                    print(a[0],'\n',a[1])

            elif s[0] == '-' and _.xyzs_list:
                _.xyzs_index -= 1
                if _.xyzs_index < 0:
                    _.xyzs_index = 0
                    print('At begining.')
                #_.xyzs_index = max(0,_.xyzs_index)
                _.xyzs = xyzs_to_4D(_.xyzs_list[_.xyzs_index])
                _.color = _.color_list[_.xyzs_index]
                if len(_.line_endpoint_indicies_list):
                    _.line_endpoint_indicies = _.line_endpoint_indicies_list[_.xyzs_index]
                else:
                    _.line_endpoint_indicies = []
                if len(_.fill_indicies_list):
                    _.fill_indicies = _.fill_indicies_list[_.xyzs_index]
                else:
                    _.fill_indicies = []

            elif s[0] == '=' and _.xyzs_list:
                _.xyzs_index = min(len(_.xyzs_list)-1,_.xyzs_index)
                _.xyzs = xyzs_to_4D(_.xyzs_list[_.xyzs_index])
                _.color = _.color_list[_.xyzs_index]
                if len(_.line_endpoint_indicies_list):
                    _.line_endpoint_indicies = _.line_endpoint_indicies_list[_.xyzs_index]
                else:
                    _.line_endpoint_indicies = []
                if len(_.fill_indicies_list):
                    _.fill_indicies = _.fill_indicies_list[_.xyzs_index]
                else:
                    _.fill_indicies = []

            else:
                print('\tHuh?')
                continue

            _.zgraph.clear()

            if not is_None(A):
                _.transformation_list.append( (s,A) )

            if len(_.transformation_list):
                B = _.transformation_list[0][1]
                if undo:
                    _.transformation_list.pop()
                if len(_.transformation_list) > 0:
                    for C in _.transformation_list[1:]:
                        B = B @ C[1]
                _.transform = B
                xyzs_ = _.xyzs @ _.transform

            else:
                xyzs_ = 1.0 * _.xyzs
            _.zgraph.add(xyzs_[:,:2],_.color,_.line_endpoint_indicies,_.fill_indicies)
            _.zgraph.graph(_.xmin,_.xmax,_.ymin)
            _.zgraph.show()
            if MetaData is not None:
                MetaData['imgs'][_.xyzs_index] = 1*_.zgraph.img
            if s[0] == '=' and _.xyzs_list:
                _.xyzs_index += 1
                if _.xyzs_index >= len(_.xyzs_list):
                    _.xyzs_index = len(_.xyzs_list)
                    print('At end.')
                    if dont_interact:
                        break

            if not dont_interact:
                s = input('command > ')



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



def _example(
    num_pts=1000,
    num_indicies=100,
    initial_rotation=(('x',10),('y',-5),('z',20))
):
    """
    Point cloud viewer, with example.
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
        initial_rotation=initial_rotation,
    )



if __name__ == '__main__':
    fire.Fire(_example)

#EOF
