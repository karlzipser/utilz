from utilz.core import *

import numpy as np

def kprint(
    item,
    title='',
    t='',
    spaces='',
    space_increment='    ',
    ignore_keys=[],
    only_keys=[],
    ignore_types=[],
    numbering=True,
    max_items=999999,
    make_sorted=False,
    array_shape_only=False,
    ra=0,
    r=0,
    p=0,
):
    if len(t) > 0:
        title = t
    item_printed = False
    if type(item) in ignore_types:
        return
    if type(title) not in [str,type(None)]:

        title = str(title)
    lst = []
    for i in range(len(space_increment)):
        lst.append('-')
    lst.append('.')
    indent_text = ''.join(lst)

    n_equals = ''

    if numbering:
        if type(item) in [dict,list]:
            n_equals = cf(' (n=',len(item),')','`w-d',s0='',s1='')

            n_equals

    if title != None:
        if len(title) > len(indent_text):
            indent_title = title
        else:
            indent_title = title + indent_text[len(title):]
    if title != None:
        if type(item) in [dict,list]:
            color_print(spaces,'`',indent_title,'`',n_equals,s0='',s1='')
        else:
            color_print(spaces,'`',title,'','`y',' ','`',item,'`g',s1='',s0='' )
            item_printed = True
    else:
        if type(item) in [dict,list]:
            color_print(spaces,indent_text,n_equals,s0='',s1='')


    if type(item) == list:
        ctr = 0
        for i in item:
            kprint(i,title=None,spaces=spaces+space_increment,space_increment=space_increment,ignore_keys=ignore_keys,only_keys=only_keys,ignore_types=ignore_types,numbering=numbering,
                max_items=max_items,
                array_shape_only=array_shape_only,
            )
            ctr += 1
            #cm(ctr,max_items)
            if ctr >= max_items:
                cg('\t. . .')
                break
    elif type(item) == dict:
        ctr = 0
        ks = item.keys()
        if make_sorted:
            ks = sorted(ks)
        for k in ks:
            if k in ignore_keys:
                continue
            if len(only_keys) > 0:
                if k not in only_keys:
                    continue
            if type(item[k]) in [dict,list]:
                l = len(item[k])
            else:
                l = 1
            kprint(item[k],title=k,spaces=spaces+space_increment,space_increment=space_increment,ignore_keys=ignore_keys,only_keys=only_keys,ignore_types=ignore_types,numbering=numbering,
                max_items=max_items,
                array_shape_only=array_shape_only,
            )
            ctr += 1
            if ctr >= max_items:
                cg('\t. . .')
                break            
    elif not item_printed:
        if type(item) == type(np.zeros([0,0,0])) and array_shape_only:
            item = np.shape(item)
        color_print(spaces,item,'`g',s0='',s1='')

    if p:
        time.sleep(p)

    if ra or r:
        raw_enter()




def kpo(obj):
    kprint(obj.__dict__)



function_types = [type(sorted),type(fname)]



def color_format(*args,**Kwargs):
    set_Defaults({'s0':' ','s1':' ','ra':False,'r':False,'p':0,'l':0},Kwargs,)
    B = color_define_list(args)
    c = []
    for i in sorted(B.keys()):
        if len(B[i]['data']) > 0:
            if 'colors' in B[i] and B[i]['colors'] != None and len(B[i]['colors']) > 0:
                c.append(colored(
                    d2s_spacer(B[i]['data'],spacer=Kwargs['s0']),
                    B[i]['colors'][0],
                    B[i]['colors'][1],
                    B[i]['colors'][2]),
                )
            else:
                c.append(colored(*B[i]['data']))
    s = d2s_spacer(c,spacer=Kwargs['s1'])
    if 'strip_opjh' not in Kwargs or Kwargs['strip_opjh']:
        s = s.replace(opjh(),'')
    return s



def color_print(*args,**Kwargs):
    """
    e.g.,

        color_print(1,2,3,'`bgu',4,5,6,'`',7,8,9,'`gbb',s1='<==>',s0='-')
    """
    print(color_format(*args,**Kwargs))
    re = False
    if 'ra' in Kwargs:
        if Kwargs['ra']:
            re = True
    if 'r' in Kwargs:
        if Kwargs['r']:
            re = True
    if re:
        raw_enter()
    if 'p' in Kwargs:
        time.sleep(Kwargs['p'])


cf = color_format
clp = color_print

def color_define_list(a):
    B = {}
    ctr = 0
    B[ctr] = {}
    B[ctr]['data'] = []
    B[ctr]['colors'] = (None,None,None)
    for c in a:
        if type(c) == str and len(c) > 0:
            if c[0]=='`':
                B[ctr]['colors'] = translate_color_string(c[1:])
                ctr += 1
                B[ctr] = {}
                B[ctr]['data'] = []
                B[ctr]['colors'] = (None,None,None)
                continue
        B[ctr]['data'].append(c)
    del_list = []
    for i in B.keys():
        if len(B[i]['data']) == 0:
            del_list.append(i)
    for i in del_list:
        del B[i]
    return B


def translate_color_string(s):
    color,on_color,attrs = None,None,None
    Translate_color = {
        'g':'green',
        'b':'blue',
        'w':'white',
        'y':'yellow',
        'r':'red',
        'm':'magenta',
        'c':'cyan',
        'e':'grey',
        '-':None,
    }
    Translate_on_color = {
        'g':'on_green',
        'b':'on_blue',
        'w':'on_white',
        'y':'on_yellow',
        'r':'on_red',
        'm':'on_magenta',
        'c':'on_cyan',
        'e':'on_grey',
        '-':None,
    }
    Translate_attribute = {
        'b':'bold',
        'u':'underline',
        'd':'dark',
        'r':'reverse',
        '-':None,
    }
    if len(s) > 0:
        color = Translate_color[s[0]]
    if len(s) > 1:
        on_color = Translate_on_color[s[1]]
    if len(s) > 2:
        attrs = []
        for i in range(2,len(s)):
            attrs.append(Translate_attribute[s[i]])
    if attrs != None:
        attrs = list(set(attrs))
        if attrs[0] == None:
            attrs = None
    return color,on_color,attrs



# http://code.activestate.com/recipes/145297-grabbing-the-current-line-number-easily/
import inspect
def lineno():
    """Returns the current line number in our program."""
    return inspect.currentframe().f_back.f_lineno

def fline():
    try:
        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0])
        filename = module.__file__
        now = datetime.datetime.now()
        return cf('line',inspect.currentframe().f_back.f_lineno,'`--r',
            fname(filename),'`--u',
            pname(filename),now.strftime('(%H:%M:%S)'),'`--d')
    except:
        return "fline()"




def errPrint(*s,**kwargs):
    if 'f' not in kwargs or kwargs['f']:
        kwargs['f'] = 1
        del kwargs['f']
        #s = cf('*** Error: ','`wrb',' ',*s,' ','`wrbr',' ***','`wrb',s1='')
        s = cf('*** ','`wrb',' ',*s,' ','`wrbr',' ***','`wrb',s1='')
    clp(s,**kwargs)
    #sys.exit(0) #
    #raise Exception(fline()) #os._exit(1)
cE = errPrint

def assert_as(a,s):
    if not a:
        cE('Assertion failed:',s)
        

if __name__ == '__main__':
    
    eg(__file__)

    #cE('this is a test of cE()')
    #print('')
    clp('this','`','is a test of','`--r','clp()','`rgu','and fline():',fline())

    Q = {
        '1':{
            '2':{
                '.meta':[5,6],
                'a':1,
            '7':{'xx':['a','v','r',[1,2,3]]},
            '8':'eight',
            }
        },
        'qqq':'zzz',
    }
    print('')
    kprint(Q,'This is a test of kprint()')
    print('')




def Percent(title='',prefix='',end_prefix=None):
    D = {
        'first':True,
        'prefix':prefix
    }
    def show(a=None,b=None):
        end = '\r'
        flush = True
        if a is None and b is None:
            a,b = 100,100
            end = '\n'
            flush = False
            if end_prefix is not None:
                D['prefix'] = end_prefix
        if D['first']:
            D['first'] = False
            try:
                clp(title,'`wbb')
            except:
                print(title)
        print(D['prefix']+' '+as_pct(a,b),end=end,flush=flush)
    return namedtuple(
        '_',
        'show')(
        show
    )



def percent(i,n,title='',timer=None):
    if timer is not None:
        if not timer.check():
            return
        else:
            timer.reset()
    cs = get_terminal_size()[1]
    p = int(100*i/n)
    s = '  '+title+' |' + (intr(0.6*p/100*cs)) * '*' + max(0,(intr(0.6*(100-p)/100*cs))-1) * ' ' + str(p) + '% '
    #s = ' ' * max(0,(3-len(str(p)))-1) + s
    print(s,end='\r',flush=True)    





#,a
def print_list_segment(
    list_of_paths,
    blanked_list_of_paths,
    i,
    minus=0,
    plus=1,
    Extra={},
    colorize=False,
    list_of_loaded = [],
):
    
    import numpy as np
    if i - minus < 0:
        start = 0
    else:
        start = i - minus

    if i + plus > len(list_of_paths):
        stop = len(list_of_paths)
    else:
        stop = i + plus

    #clear_screen()

    if start == 0:
        print("┏"+ (len(list_of_paths[0])+8)*'━')
    for j in range(start,stop):

        if j == i:
            fmt = '`--rb'
        elif list_of_paths[j] in list_of_loaded:
            fmt = '`---'
        else:
            fmt = '`--d'

        if j == start:
            s = list_of_paths[j]
        else:
            s = blanked_list_of_paths[j]

        if j == 0:
            l = 0
        else:
            l = int(np.log10(j))
            l = min(5,l)
        
        offset = ' ' * (5-l)
        extra = []
        #if list_of_paths[j] in list_of_loaded:
        #    extra.append('*')
        for k in sorted(kys(Extra)):
            #print(k)
            if list_of_paths[j] in Extra[k]:
                extra.append(k.replace('rating_',''))
        u = d2n(offset,j,') ',s,'    ',', '.join(extra))
        if colorize:
            clp('┃'+u,fmt)
        else:
            print('┃'+u)
    if stop == len(list_of_paths):
        print("┗"+ (len(list_of_paths[j])+8)*'━')

def print_paths(path_list):
    b,c = get_lists_of_paths(path_list) 
    print_list_segment(b,c,0,0,10**10,colorize=False) 
#,b

def get_lists_of_paths(path_list):
    fs = path_list
    fs = sorted(fs,key=natural_keys)
    #from natsort import natsorted
    #fs = natsorted(fs)
    lfs = []
    ls = []
    for f in fs:
        f = f.replace(' ','@')
        f = re.sub('^.*Users\/'+username+'\/','',f)
        lfs.append(f.split('/'))
        #ls.append('/'+f)
        ls.append(f)
    bs = [ls[0]]
    for i in range(1,len(lfs)):
        a = lfs[i-1]
        b = lfs[i]
        d = []
        no_difference = True
        for j in rlen(b):
            if j < len(a) and no_difference and b[j] == a[j]:
                c = ' '*(len(b[j])+1)
            else:
                c = '/'+b[j]
                no_difference = False
            d.append(c)
        bs.append(''.join(d))

    list_of_paths = ls
    blanked_list_of_paths = bs

    for i in range(len(blanked_list_of_paths)-1,0,-1):
        f = blanked_list_of_paths[i]
        g = blanked_list_of_paths[i-1]
        k = 0
        h = list(g)
        st = ['/','|']
        first = True
        for k in rlen(g):
            if not first:
                st = ['|']
            if len(f) > k and f[k] in st:
                if f[k] == '/':
                    first = False
                if h[k] == ' ':
                    h[k] = '|'
        blanked_list_of_paths[i-1] = ''.join(h).replace('@',' ')

    for i in rlen(list_of_paths):
        list_of_paths[i] = list_of_paths[i].replace('@',' ')

    return list_of_paths, blanked_list_of_paths





#EOF
