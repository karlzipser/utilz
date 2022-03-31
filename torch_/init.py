from utilz.vis import *
import torch
import torchvision
import torchvision.transforms as transforms
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

def shape_from_tensor(x):
    return shape( x.cpu().detach().numpy() )

def cuda_to_rgb_image(cu):
    return z55(cu.detach().cpu().numpy()[0,:].transpose(1,2,0))

def shape_from_torch(x):
    s = shape(x)
    so = []
    for i in rlen(s):
        so.append(s[i])
    return tuple(so)
    
"""
__required__ = '__required__'
__required_types__ = dict(
    __required_array__ =    type(na([0,0])),
    __required_dict__ =     dict,
    __required_list__ =     list,
    __required_tuple__ =    tuple,
    __required_str__   =    str,
    __required_int__   =    int,
    __required_float__ =    float,
)
for k in __required_types__:
    exec(d2s(k,'=',qtd(k)))


class Int_float_str_attr_menu_enabled():
    def __init__(_):
        pass
    def attrs_to_dict(_):
        _.Ad = {}
        for k in _.__dict__.keys():
            if k[0] == '_':
                continue
            if type(_.__dict__[k]) not in [int,float,str]:
                continue
            _.Ad[k] = _.__dict__[k]
    def dict_to_attrs(_):
        for k in _.Ad:
            assert k in _.__dict__.keys()
            _.__dict__[k] = _.Ad[k]
    def geta(_):
        return select_from_dict(_.Ad,title='\nget_attribute:')
    def seta(_):
        input_to_dict(_.Ad,title='\nset_attribute:')
        _.dict_to_attrs()
    def showa(_):
        print_dic_simple(_.Ad,title='int,float,str attributes dict')



class zClass(Int_float_str_attr_menu_enabled):
    def __init__( _ ):
        super().__init__()
    def set_inst_vars( _, defaults, kwargs, ):
        for k in defaults:
            r = defaults[k]
            if ( type(r) is str and '__required' in r ):
                assert k in kwargs
                if r in __required_types__:
                    assert type( kwargs[ k ] ) is type( __required_types__[ r ] )
            if k in kwargs:
                val = kwargs[ k ]
            else:
                val = defaults[ k ]
            _.__dict__[ k ] = val


if __name__ == '__main__':
    a = zClass()
    a.b = 1
    a.c = 'x'
    a.attrs_to_dict()
    a.showa()
    cy( a.geta() )
    a.seta()
    a.showa()
"""

#EOF
