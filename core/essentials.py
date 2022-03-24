from utilz.core.imports import *

    
def boxed(text,title=''):
    # https://stackoverflow.com/questions/20756516/python-create-a-text-border-with-dynamic-size
    text = str(text)
    lines = text.splitlines()
    width = max(max(len(s) for s in lines),len(title)+1)
    #res = ['┌' + '─' * width + '┐']
    top = '┌' + '─' + title
    top += (width-len(top)+1) * '─' + '┐'
    res = [top]
    for s in lines:
        res.append('│' + (s + ' ' * width)[:width] + '│')
    res.append('└' + '─' * width + '┘')
    return '\n'.join(res)
  

def box(text,title=''):
    print(boxed(text,title))


def sort_by_value(D,reverse=True):
    return {k: v for k, v in sorted(D.items(), reverse=reverse, key=lambda item: item[1])}


def print_dic_simple(D,title='<title>',html=False,print_=True,center=False):
    el = '\n'
    if html:
        el +=''
    if title != '':
        s = title+el
    else:
        s = ''
    if type(D) is not dict:
        if print_:
            print(D)
    else:
        longest = 0
        for k in sorted(D):
            if len(str(k)) > longest:
                longest = len(str(k))
        for k in sorted(D):
            if center:
                sk = ' '*(longest-len(str(k)))+str(k)
            else:
                sk = str(k)
            if k[0] != '-' and type(D[k]) is str:
                q = qtd(D[k],s=True)
            else:
                q = str(D[k])
            s += '   '+sk+':  '+q+el;
    if print_:
        print(s)
    return s


def clear_screen():
    print(chr(27) + "[2J")
    

def eg(f,cs=False):
    if cs:
        clear_screen()
    if False:
        s = "│ Examples from "+f+":"
        print('┌'+(len(s)-1)*'─'+'\n'+s+'\n')
    box('E.g.s from '+f)


def intr(n):
    import numpy as np
    return np.int(np.round(n))


def qtd(a,s=False):
    if a == '':
        return "''"
    if type(a) == str and ((a[0] == '\'' and a[-1] == '\'') or (a[0] == '\"' and a[-1] == '\"')):
        print('*** qtd(): Warning, '+a+' seems to be quoted already ***')
    if not s:
        return '\"'+str(a)+'\"'
    else:
        return '\''+str(a)+'\''


def qtds(a):
	return qtd(a,s=1)


def raw_enter(optional_str=''):
    return input(optional_str+'   Hit enter to continue > ')


def is_even(q):
    import numpy as np
    if np.mod(q,2) == 0:
        return True
    return False
    

def str_is_int(s):
    try:
        int(s)
        return True
    except:
        return False


def str_is_float(s):
    try:
        float(s)
        return True
    except:
        return False


def rlen(a):
    return range(len(a))


def getch():
    import sys, termios, tty, os, time
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


def k_in_D(k,D):
    if k not in D:
        return False
    else:
        return D[k]
kin = k_in_D


def is_number(n):
    import numbers
    if type(n) == bool:
        return False
    if type(n) == type(None):
        return False
    return isinstance(n,numbers.Number)


def bound_value(the_value,the_min,the_max):
    if the_value > the_max:
        return the_max
    elif the_value < the_min:
        return the_min
    else:
        return the_value


def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    def atoi(text):
        return int(text) if text.isdigit() else text
    return [ atoi(c) for c in re.split('(\d+)', text) ]



    

def all_values(D):
    def get_all_values(d):
        #https://stackoverflow.com/questions/7002429/how-can-i-extract-all-values-from-a-dictionary-in-python
        if isinstance(d, dict):
            for v in d.values():
                yield from get_all_values(v)
        elif isinstance(d, list):
            for v in d:
                yield from get_all_values(v)
        else:
            yield d
    return sorted(list(get_all_values(D)))


REQUIRED = '__REQUIRED__'


def kys(D):
    return list(D.keys())


def set_Defaults(Defaults,Dst,file='',verbose=True,r=False,t=1):
    for k in Dst.keys():
        if k not in Defaults.keys():
            if verbose:
                print("*** Warning,",file,"argument '"+k+"' not in Defaults:\n\t",
                    list(Defaults.keys())
                )
                if r:
                    raw_enter()
    for k in Defaults.keys():
        if k not in Dst.keys():
            if Defaults[k] is REQUIRED:
                print('*** Error. '+qtd(k)+\
                    ' is a required cmd line arg. ***')
                if r:
                    raw_enter()
                print_dic_simple(Defaults,'Defaults')
                os.sys.exit()
            else:
                Dst[k] = Defaults[k]
        else:
            if type(Defaults[k]) is tuple:
                if Defaults[k][0] is REQUIRED:
                    b = Defaults[k][1]
                else:
                    b = tuple
            else:
                b = type(Defaults[k])

            if type(Dst[k]) is not b:
                if type(Dst[k]) is str and b is list:
                    Dst[k] = [Dst[k]]
                else:
                    print("!*** Warning,",file,"argument '"+k+"' is not of the right type",
                        "should be",b)
                    if r:
                        raw_enter()
                    if t:
                        time.sleep(t)
                

def advance(lst,e,min_len=1):
    len_lst = len(lst)
    if len_lst < min_len:
        pass
    elif len_lst > 1.2*min_len:
        lst = lst[-min_len:]
    else:
        lst.pop(0)
    lst.append(e)


def a_key(dic):
    keys_ = kys(dic)
    import numpy as np
    k = np.random.randint(len(keys_))
    return keys_[k]


def an_element(dic):
    return dic[a_key(dic)]


def nth(dic,n):
    ks = kys(dic)
    return dic[ks[n]]


def remove_empty(l):
    m = []
    for a in l:
        if a != '':
            m.append(a)
    return m


def space(s):
    a = s.split(' ')
    return remove_empty(a)



"""
https://stackoverflow.com/questions/2673385/how-to-generate-random-number-with-the-specific-length-in-python
"""
from random import randint

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)


def limD(A,ks,deep=False,):
    B = {}
    for k in ks:
      B[k] = A[k]
    return B
    

def is_None(a):
    if type(a) == type(None):
        return True
    return False
    



if __name__ == '__main__':
    eg(__file__)
    print("int(1.9) =",int(1.9))
    box("intr(1.9) ="+str(intr(1.9)))

    
#EOF
