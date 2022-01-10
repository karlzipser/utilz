
from utilz.dict_.zprint import *
from utilz.misc.sys import *
from utilz.vis import *




def find_folder_with_list_of_images(D):
    image_folders = []
    for i in D:
        try:
            q = da(*D[i])
            if type(q) == list:
                for f in q:
                    if '.jpeg' in f:
                        image_folders.append(D[i])
                        break
        except:
            pass
    return image_folders


top = opjD('Photos/all')


def _open_imgs_with_Preview(l):
    if type(l) is str:
        l = [l]
    for f in l:
        os_system('open',qtd(f))

def _quit_Preview():
    os_system(""" osascript -e 'quit app "Preview"' """)
    return

def _close_Finder_windows():
    os_system(""" osascript -e 'tell application "Finder" to close every window' """)
    return

def _open_imgs_with_Preview_action(f,Args=None,MiniMenu=None):
    keylist = Args['keylist']
    top = Args['top']
    True
    h = []
    kprint(f,'open_imgs_with_Preview_action')
    for g in f:
        g = opj(pn(g),fname(g).split('|')[-1])
        h.append(opj(top,'/'.join(keylist),g))
    quit_Preview()
    open_imgs_with_Preview(h)

def rating_from_filename(f):
    
    if 'ratings=' not in f:
        return None

    f = f.split('|')[0]
    f = f.split('ratings=')[-1]
    l = f.split(',')
    c = 0
    
    for a in l:
        c += int(a)

    c /= len(l)

    return c


def get_dictionary_of_Photos():
    D = {}
    years = []
    a = sggo(top,'*')
    for b in a:
        years.append(b.split('/')[-1])
    for y in years:
        D[y] = {}
    for y in years:
        months = []
        c = sggo(top,y,'*')
        for d in c:
            months.append(d.split('/')[-1])
        for m in months:
            D[y][m] = {}
            days = []
            e = sggo(top,y,m,'*')
            for f in e:
                days.append(f.split('/')[-1])
            for g in days:
                h = sggo(top,y,m,g,'.meta/*')
                D[y][m][g] = {}
                
                for j in h:
                    if os.path.isfile(j):
                        if '<unsorted>' not in D[y][m][g]:
                            D[y][m][g]['<unsorted>'] = []
                        D[y][m][g]['<unsorted>'].append(j.split('/')[-1])
                    else:
                        D[y][m][g][fname(j)] = []
                        k = sggo(j,'*.jpeg')
                        for u in k:
                            D[y][m][g][fname(j)].append(u.split('/')[-1])
    return D








offset = '\n     '



def input_int(s='> '):
    c = input(s)
    if str_is_int(c):
        return int(c)
    else:
        return None



def input_int_in_range(a,b,s):
    c = input_int(s)
    if c is None or c < a or c > b:
        return None
    else:
        return c



def list_select_(lst):
    for i in rlen(lst):
        clp('    ',i,') ',lst[i],s0='')
    i = input_int_in_range(0,len(lst)-1,offset+'>> ')
    return i





def _set_str(path,s='Enter str for'):
    v = input(d2s(s,path))
    di(path,e=v)  
    return d2s(path,'set to',di(path))



def set_str(path):
    #print('set_str',path)
    dst_kc = path.split('/')
    kp = cf(*dst_kc,s0='/')
    v = input(d2s(offset+'Enter str for',kp))
    da(*dst_kc,e=v)  
    return d2s(offset,kp,'set to',da(*dst_kc))



def set_number(dst_path,min_path,max_path):
    #print('set_number',dst_path,min_path,max_path)
    dst_kc = dst_path.split('/')
    min_kc = min_path.split('/')
    max_kc = max_path.split('/')
    mn = da(*min_kc)
    assert(is_number(mn))
    mx = da(*max_kc)
    assert(is_number(mx))

    kp = cf(*dst_kc,s0='/')

    target_type = type(da(*dst_kc))

    v = input(d2s(offset+'Enter',target_type.__name__,'for',kp,'in range',(mn,mx),'> '))

    no = False

    if target_type == int:

        if str_is_int(v):
            v = int(v)
        else:
            no = True

    elif target_type == float:
        if str_is_float(v):
            v = float(v)
        else:
            no = True
    else:
        no = True

    if no:
        return d2s(offset+'failed to set',kp,'to',v)

    if v < mn or v > mx:
        return d2s(offset,v,'not in range',(mn,mx))

    da(*dst_kc,e=v)
            
    return d2s(offset+kp,'set to',da(*dst_kc))



def list_select(dst_path,options_path,ig0):
    #print('list_select',dst_path,options_path)
    dst_kc = dst_path.split('/')
    options_kc = options_path.split('/')

    for i in rlen(da(*options_kc)):
        clp('    ',i,') ',da(*options_kc)[i],s0='')

    i = input_int_in_range(0,len(da(*options_kc))-1,offset+'>> ')
    if i is None:
        return offset+'failed'

    da(*dst_kc,e=(da(*options_kc)[i]))
    return offset+'okay'



def toggle(path,ig0,ig1):
    kc = path.split('/')
    da(*kc,e=not da(*kc))
    message = d2s(offset+'toggled','/'.join(kc),'to',da(*kc))
    return message



def placeholder(path,ig0,ig1):
    p = path.replace('menu','Desktop/Photos/all')
    f = di(path)[0]
    g = '/'.join(p.split('/')[:-1])
    h = g+'/'+f
    k = pn(h)
    imgs = sggo(k,'*.jpeg')
    open_imgs_with_Preview(imgs)
    i0 = zimread(h)
    meta = opj(pn(h),'.meta')
    os_system('open',meta)
    raw_enter()
    quit_Preview()
    close_Finder_windows()




def divide_path(path,i):
    if path[-1] == '/':
        path = path[:-1]
    if path[0] == '/':
        path = path[1:]    
    kc = path.split('/')
    assert (i > 0 and i < len(kc)) or (i < 0 and i > -len(kc))
    path0 = '/'.join(kc[:i])
    path1 = '/'.join(kc[i:])
    return path0, path1



def print_menu(
    top,
    ignore_underscore=True,
    ignore_keys=['options'],
    max_depth=999999,action_paths=[],
):
    top = top.split('/')
    D, print_lines = zprint(
        da(*top),
        t=top[-1],
        use_color=True,
        use_line_numbers=False,
        ignore_underscore=ignore_underscore,
        do_return=True,
        do_print=False,
        ignore_keys=ignore_keys,
        max_depth=max_depth,
    )
    for i in kys(D):
        if i+1 in D:
            if D[i] == D[i+1]:
                D[i+1].append('---')
    V = {}
    ctr = 1
    for i in kys(D):
        d = []
        for a in top[:-1]+D[i]:
            d.append(str(a))
        p = '/'.join(d)
        if p in action_paths:
            V[ctr] = p
            print_lines[i+1] += cf(' (',ctr,')','`m',s0='')
            ctr += 1
    #clear_screen()
    clp()
    print('\n'.join(print_lines))
    return V,D



def test_for_valid_path(p):
    try:
        _ = da(*(p.split('/')))
        return True
    except:
        return False


max_depth = 5





if __name__ == '__main__':
        
    if 'setup menu':
        _words = ['cat','toggle','range','horse']
        _menu = {
            'range':{
                'min':{
                    'current':0,
                },
                'max':{
                    'current':10,
                },
                '_min':0,
                '_max':10,
            },
            'toggle':False,
            'word': {
                'current':_words[-1],
                '_options':_words,
            }   
        }
        ENV.D['menu'] = get_dictionary_of_Photos()#_menu


    if 'setup keychains':
        curmax =    'menu/range/max/current'
        maxmax =    'menu/range/_max'
        maxmin =    'menu/range/_min'
        curmin =    'menu/range/min/current'
        tog =       'menu/toggle'
        curword =   'menu/word/current'
        woptions =  'menu/word/_options'
        place =     'menu/range/_min'
        place2 =    'menu/word/_options'

    """
        'max/current':{
            'path':'menu/range',
            'function':set_number,
            'args':['_min','_max'],
        },
    """

    Actions = {
        curmax:{
            'function':set_number,
            'args':[curmax,maxmin,maxmax],
        },
        curmin:{
            'function':set_number,
            'args':[curmin,maxmin,maxmax],
        },
        tog:{
            'function':toggle,
            'args':[tog,None,None],
        },
        curword:{
            'function':list_select,
            'args':[curword,woptions,None],
        },
        place:{
            'function':placeholder,
            'args':[place,None,None],
        },
        place2:{
            'function':placeholder,
            'args':[place2,None,None],
        },    }



    message = ''
    top = 'menu'

    targets = ['menu','menu/range','menu/word']

    V,D = print_menu(
        top,
        ignore_underscore=False,
        ignore_keys=[],
        max_depth=max_depth,
        action_paths=kys(Actions),
    )
    image_folder_paths = find_folder_with_list_of_images(D)
    for f in image_folder_paths:
        f = '/'.join(f)
        Actions[f] = {'function':placeholder,'args':[f,None,None]}


    while True:

        V,D = print_menu(
            top,
            ignore_underscore=False,
            ignore_keys=[],
            max_depth=max_depth,
            action_paths=kys(Actions),
        )



        print(message)

        if True:#try:
            c = input('> ')

            if c == 'q':
                break

            elif c == 'm':
                m = input_int('enter max_depth > ')
                if type(m) is int and m > 0:
                    max_depth = m

            elif c == 'j':
                done = False
                while done == False:
                    p = input('enter new path > ')
                    if p[-1] == '/':
                        if test_for_valid_path(p):
                            print(kys(da(*(p[:-1].split('/')))))
                            message = d2s(p,'is valid')
                        else:
                            message = d2s(p,'is not a good path')
                    else:
                        done = True
                t = p.split('/')
                if test_for_valid_path(p):
                    q = da(*t)
                    top = t
                    message = d2s(p,'is valid')
                else:
                    message = d2s(p,'is not a good path')

            elif c == 't':
                i = list_select_(targets)
                top = targets[i]

            elif c == 'u':
                if len(top.split('/')) > 1:
                    top = '/'.join(top.split('/')[:-1])
                    message = "went up"
                else:
                    message = "already at the top"

            elif c == 'd':
                toplist = top.split('/')
                if type(da(*toplist)) is not dict:
                    message = "can't go down"
                else:
                    i = list_select_(kys(da(*toplist)))
                    if i is None:
                        message = 'invalid selection'
                    else:
                        toplist.append(kys(da(*toplist))[i])
                        message = 'went down to '+toplist[-1]
                top = '/'.join(toplist)

            elif str_is_int(c):
                i = int(c)
                if i in V:
                    kc = V[i]

                    X = Actions[kc]

                    X['function'](X['args'][0],X['args'][1],X['args'][2],)


                                        
                else:
                    message = d2s(i,'is not a valid index')
            else:
                message = ''
        """
        except KeyboardInterrupt:
            cE('*** KeyboardInterrupt ***')
            sys.exit()
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            message = cf('Exception:',exc_type,file_name,exc_tb.tb_lineno,'`rwb')        
        """




#EOF
