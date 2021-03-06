from utilz.vis import *


class Viewer:
    def __init__(
        _,
        xyzs_list=[],
        xmin=-5,
        xmax=5,
        ymin=-5,
        img_width=300,
        img_height=300,
        color_list=[],
        title='Viewer',
    ):
        assert type(xyzs_list) == list
        assert type(color_list) == list
        _.xyzs_list = xyzs_list
        _.xyzs_index = 0
        _.xyzs = xyzs_to_4D(_.xyzs_list[_.xyzs_index])
        _.color_list = color_list
        _.color = _.color_list[_.xyzs_index]
        _.xmin = xmin
        _.xmax = xmax
        _.ymin = ymin
        _.transform = get_IdentityMatrix()
        _.zgraph = ZGraph(img_width,img_height,title)
        _.zgraph.add(1.0*_.xyzs[:,:2], _.color)#rndint(255,size=(len(xyzs),3)))#(255,255,255))
        _.zgraph.graph(_.xmin,_.xmax,_.ymin)
        _.zgraph.show()
        _.transformation_list = []
        _.good_transforms = [

          na([[  1.12012796,   0.26691821,  -0.96128457,   0.        ],
           [ -0.99669454,   0.36276714,  -1.06066017,   0.        ],
           [  0.04374197,   1.43078813,   0.44825436,   0.        ],
           [-33.60383872,  -8.00754616,  28.83853719,   1.        ]]),

        ]
        _.transform = _.good_transforms[-1]
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
         # change xymin,xymax
         # allow running from commandline with point cloud file
         # path, cloud index
         # plot size as argument
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

    def attributes_to_dict(lst):
        U = {}
        for name in lst:
            U[name] = getattr(_,name)
        return U




    def get_img(_):
        xyzs_ = _.xyzs @ _.transform
        _.zgraph.add(xyzs_[:,:2],_.color)
        _.zgraph.graph(_.xmin,_.xmax,_.ymin)
        return _.zgraph.img

    def interactive_loop(_):
        while True:
            A = None
            undo = False
            s = input('command > ')
            if s == 'q':
                break
            if not s:
                continue
            if s[0] == 'h':
                box(_.help_str)
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
                _.xyzs_index = max(0,_.xyzs_index)
                _.xyzs = xyzs_to_4D(_.xyzs_list[_.xyzs_index])
                _.color = _.color_list[_.xyzs_index]
            elif s[0] == '=' and _.xyzs_list:
                _.xyzs_index += 1
                _.xyzs_index = min(len(_.xyzs_list)-1,_.xyzs_index)
                _.xyzs = xyzs_to_4D(_.xyzs_list[_.xyzs_index])
                _.color = _.color_list[_.xyzs_index]
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
            _.zgraph.add(xyzs_[:,:2],_.color)
            _.zgraph.graph(_.xmin,_.xmax,_.ymin)
            _.zgraph.show()



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


if __name__ == '__main__':
    
    xyzs_list = []
    color_list = []
    xyzs = rndn(1000,3)
    for i in range(20):
        xyzs_list.append(xyzs)
        color_list.append(rndint(255,size=(len(xyzs_list[0]),3)))

    xmin,xmax,ymin = -5,5,-5

    v = Viewer(xyzs=None,xyzs_list=xyzs_list,xmin=xmin,xmax=xmax,ymin=ymin,
        color=None,color_list=color_list)

    if False:
        mi(v.get_img(),'img')
        spause()

    v.interactive_loop()

#EOF
