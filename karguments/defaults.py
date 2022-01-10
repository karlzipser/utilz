
from utilz import *
from utilz.karguments.parse_utils.classifying import *

parameter_types = ['int_','float_','bool_','name_','path_','list_']

def process_defaults(Defaults):

    W = {'value':{},'doc':{},'type':{}}

    D = Defaults

    for k in D:
        doc = ''
        if type(k) is tuple:
            assert len(k) == 2
            parameter_name = k[0]
            doc = k[1]
            assert doc
        else:
            assert type(k) is str
            parameter_name = k
        assert parameter_name
        #print(parameter_name,doc)

        q = D[k]
        if type(q) is tuple:
            if len(q) > 2:
                cE('type tuple',q,'must long be longer than 2 in length.')
            assert len(q) <= 2
            parameter_type = q[0]
            if parameter_type not in parameter_types:
                cE(parameter_type,'not in',parameter_types)
            if len(q) == 1:
                val = '<required>'
            else:
                val = q[1]
        else:
            val = q
            parameter_type,val = classify_token(q)
        W['value'][parameter_name] = val #cast_parameter(parameter_type,val)
        W['type'][parameter_name] = parameter_type
        W['doc' ][parameter_name] = doc

    return W

"""
def cast_parameter(parameter_type,val):
    cm(parameter_type,val)
    if parameter_type in ['name','path']:
        return str(val)
    elif parameter_type == 'bool':
        cr(val)
        if val in ['True',True]:
            return True
        elif val in ['False',False]:
            return False
        else:
            assert False
    elif parameter_type == 'int':
        return int(val)
    elif parameter_type == 'float':
        return float(val)
    elif parameter_type == 'list':
        return list(val)
    else:
        cE('Error, parameter_type',parameter_type,'not understood.')
        assert(False)
"""

if __name__ == '__main__':
    D = {
        'm'             :   'a/a',
        ('mm','mmmm!')  :   [1,2,3],
        'c'             :   ('name_',),
        'd'             :   ('path_','a/b')
    }
    #zprint(D,'D')
    W = process_defaults(D)
    zprint(W,'W')



#EOF
