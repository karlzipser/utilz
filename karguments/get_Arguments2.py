
from utilz import *
from utilz.karguments.parse_utils.parse_argument_string import parse_argument_string
from utilz.karguments.defaults import process_defaults



def get_Arguments2(Defaults,values_only=True,verbose=True,f=''):

    if 'h' in Defaults:
        cE('Error, "h" in Defaults is reserved for help')
        assert False

    Parsed_arguments = parse_argument_string(sys.argv[1:])

    Processed_defaults = process_defaults(Defaults)

    if 'h' in Parsed_arguments['value']:
        T = {}
        for k in Defaults:
            if type(k) is tuple:
                kk = d2n(k[0],' (',k[1],')')
            else:
                kk = k
            T[str(kk)] = Defaults[k]
           
        box(print_dic_simple(T,title='Defaults:',print_=False))
        sys.exit()

    for k in Parsed_arguments['value']:

        if k == 'positional_args' and not Parsed_arguments['value'][k]:
            continue
        
        if k not in Processed_defaults['value']:
            cE(qtds(k),"not in Processed_defaults['value']:")
            assert False

        if Processed_defaults['type'][k] != 'path_' and k != 'positional_args':
            if Parsed_arguments['type'][k] != Processed_defaults['type'][k]:
                cE("Parsed_arguments['type'][",qtds(k),
                    "] != Processed_defaults['type'][",qtds(k),"]:",qtds(Processed_defaults['type'][k]))
                assert False
        
        Processed_defaults['value'][k] = Parsed_arguments['value'][k]

    for k in Processed_defaults['value']:
        if Processed_defaults['value'][k] == '<required>':
            cE("Processed_defaults['value'][",qtds(k),"] == '<required>'")
            cE("This means required ",qtds(k),"not among command-line arguments")
            assert(False)

    Arguments2 = Processed_defaults

    if verbose:
        if f:
            ti = f + '\nArguments:'
        else:
            ti = 'Arguments:'
        box(print_dic_simple(Arguments2['value'],title=ti,print_=False))

    if values_only:
        Arguments2 = Arguments2['value']


    return Arguments2




# python k3/drafts/karguments/get_Arguments2.py lll -a 2 -b a3 -c /
def main():

    Defaults = {
        ('positional_args','some ints') : ('list_',),
        ('a','a is for apple') : 1,
        ('b','b is for butter') : ('name_',),
        ('c','c is for cake') : ('path_','/cccc'),
        'd'                   : False,
        'e'                   : ('list_',),
    }

    Arguments2 = get_Arguments2(Defaults)

    zprint(Arguments2,t='Arguments2')

    Arguments = Arguments2['value']
    for k in Arguments:
        print(k,Arguments[k],type(Arguments[k]))



if __name__ == '__main__':
    main()


#EOF