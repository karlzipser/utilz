from utilz.vis import *

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
        super().__init__()
        _.attribute_set=False
        _._name = type(_).__name__
    def attrs_to_dict(_):
        _.Ad = {}
        for k in _.__dict__.keys():
            if k[0] == '_':
                continue
            if type(_.__dict__[k]) not in [ int, float, str ]:
                continue
            _.Ad[k] = _.__dict__[k]
    def dict_to_attrs(_):
        if not _.attribute_set:
            _.attrs_to_dict()
            _.attribute_set=True
        for k in _.Ad:
            if k[0] == '_':
                continue
            assert k in _.__dict__.keys()
            _.__dict__[k] = _.Ad[k]
    def geta(_):
        if not _.attribute_set:
            _.attrs_to_dict()
            _.attribute_set=True
        return select_from_dict(_.Ad,title='\nget_attribute:')
    def seta(_):
        if not _.attribute_set:
            _.attrs_to_dict()
            _.attribute_set=True
        input_to_dict(_.Ad,title='\nset_attribute:')
        _.dict_to_attrs()
    def showa(_):
        if not _.attribute_set:
            _.attrs_to_dict()
            _.attribute_set=True
        box(
            print_dic_simple(
                _.Ad,
                title='int, float & str attribute dictonary',
                print_=False
            ),
            title=' '+_._name+' ',
        )



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



"""
class Run_with_menu(zClass):
    def __init__( _, **kwargs ):
        super().__init__()
        _.set_inst_vars(
            defaults = dict(
                # thread class
                # menu class
            )
            kwargs=kwargs,
        )
    def main():
        thread_ = threadclass
        menu = menu class
        # start thread
        # run loop
"""






if __name__ == '__main__':
    a = zClass()
    a.b = 1
    a.c = 'x'
    a.attrs_to_dict()
    a.showa()
    cy( a.geta() )
    a.seta()
    a.showa()


#EOF
