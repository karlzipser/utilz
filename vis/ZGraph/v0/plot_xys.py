import sys,os
parent_path = '/'.join(__file__.split('/')[:-2])
print('\n',__file__,'adding',parent_path,'to sys.path.','\n')
sys.path.append(parent_path)

from utilz.vis import *
from ZGraph.zgraph import *



def plot_xys(
    xys,
    color=(255,255,255),
    width=400,
    height=400,
    xmin=None,
    xmax=None,
    ymin=None,
    img=None,
    aspect_ratio=1.0,
    title='plot_xys',
    report=False,
    return_img=True,
):
    """
    An x-y points plotter function built on ZGraph class.
    Allows use of ZGraph without overhead of building class.

    """

    if not img is None:
        height = shape(img)[0]
        width = shape(img)[1]
        z = ZGraph(title=title,height=height,width=width)
        z.img = img
    else:
        z = ZGraph(title=title,height=height,width=width)
    z.add(xys,color)
    z.graph(
        xmin=xmin,
        xmax=xmax,
        ymin=ymin,
        aspect_ratio=aspect_ratio,
    )
    if report:
        z.report()
    z.show()
    if return_img:
        return z.img




def _example():
    """
    The ZGraph class, with examples.

    Try running for example, 
    python utilz/vis/ZGraph.py --egs [0,1,2,3]
    """

    print('e.g. 1')

    xys=rndn(1000,2)

    plot_xys(
        xys*0.5+na([0.4,1.3]),
        (255,127,255),
        300,
        300,
        title='using plot_xys'
    )
    spause()
    raw_enter();CA()



if __name__ == '__main__':
    fire.Fire(_example)





