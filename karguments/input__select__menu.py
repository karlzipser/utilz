from utilz.karguments.parse_utils.classifying import *

def inputz( desired_type, prompt='> ', convert_unknown_to_str=False, verbose=True):
    if desired_type in (int,'int','int_'):
        desired_type = 'int_'
    elif desired_type in (float,'float','float_'):
        desired_type = 'float_'
    elif desired_type in (bool,'bool','bool_'):
        desired_type = 'bool_'
    elif desired_type in ('path','path_'):
        desired_type = 'path_'
    elif desired_type in ('name','name_'):
        desired_type = 'name_'

    s = input(prompt)
    classified_type = classify_token(s)
    if not convert_unknown_to_str and classified_type[0] == 'unknown':
        if verbose:
            cy("Warning, classified_type == 'unknown'")
        return
    if desired_type not in ['path','str']:
        if desired_type == classified_type[0]:
            if desired_type == 'int_':
                return int(s)
            elif desired_type == 'float_':
                return float(s)
            elif desired_type == 'bool_':
                if s == 'False':
                    return False
                else:
                    return True
            elif desired_type == 'name_':
                return s
            else:
                if verbose:
                    cy('Warning,',s,'not understood')
                return None
        else:
            if verbose:
                cy('Warning, desired_type ('+desired_type+') != classified_type ('+classified_type[0]+')')
            return None
    else:
        return s



def select_from_dict(
    D,
    ignore_underscore=False,
    prefix='',
    print_one_element_lst=True,
    title='',
    max_val_string_len=get_terminal_size()[1]//2,
    return_key=False,
):
    ks = sorted(list(D.keys()))
    print_lst = []
    longest = 0
    for k in ks:
        if len(k) > longest:
            longest = len(k)
    for k in ks:
        s = D[k]
        if type(s) is str:
            s = qtds(s)
        else:
            s = str(s)
        s = s.replace('\t',' ').replace('\n',' ')
        if len(s) > max_val_string_len:
            s = s[:max_val_string_len] + '...'

        print_lst += [ k + (longest-len(k))*' ' + ': ' + s ]
    
    k = select_from_list(
        ks,
        ignore_underscore=False,
        prefix=prefix,
        print_lst=print_lst,
        print_one_element_lst=True,
        title=title,
    )
    if k:
        if return_key:
            return k
        else:
            return D[k]
    

def input_to_dict(
    D,
    ignore_underscore=False,
    prefix='',
    print_one_element_lst=True,
    title='',
    max_val_string_len=get_terminal_size()[1]//2,
    prompt='Enter new value for key XXX: ',
    verbose=True,
):
    Atomic = {}

    for k in D:
        if type(D[k]) in [str,int,float,bool,str]:
            Atomic[k] = D[k]

    k = select_from_dict(
        Atomic,
        title=title,
        return_key=True,
        max_val_string_len=get_terminal_size()[1]//2
    )
    if k:
        v = inputz( 
            type(D[k]).__name__,
            prompt=prompt.replace('XXX',qtds(k)),
            convert_unknown_to_str=True,
        )
        if type(v) is not type(None):
            D[k] = v
            return True

    if verbose:
        if k:
            cy('No change for key',qtds(k))
        else:
            cy('No change')

    return False



class Attr_menu_enabled():
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
        if input_to_dict(_.Ad,title='\nset_attribute:'):
            _.dict_to_attrs()
            return True
        else:
            return False
    def showa(_):
        print_dic_simple(_.Ad,title='(A)ttributes (d)ict')



if __name__ == '__main__':

    D = {
    'one' : 1,
    '2': '2',
    'three':(1,2,3,4,5,6,7,8,9,10,),
    'a txt' : """Four score and seven years ago
our fathers brought forth upon this continent,
a new nation, conceived in Liberty,
and dedicated to the proposition that all
men are created equal.
""",
    'xxx' : {1:2,3:{4:5}},
    }

    a = select_from_dict(D,title='\nselect_from_dict:')

    print('You selected:\n'+boxed(a))

    input_to_dict(D,title='\ninput_to_dict:')

    zprint(D,t='D')
    



#EOF

