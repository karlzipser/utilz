
from utilz import *
from utilz.karguments.get_Arguments2 import get_Arguments2


def main():

    Defaults = {
        ('a','a is for apple') : ('int_',),
        ('b','b is for butter') : ('float_',),
        ('c','c is for cake') : ('path_','/cccc'),
        'd'                   : False,
        'e' : 1,
        'f' : [1,2,3]
    }

    A = get_Arguments2(Defaults) #['value']

    if A['d']:
        print(A['a']*A['b'])





if __name__ == '__main__':
    main()


#EOF