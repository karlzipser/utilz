from utilz.core.printing import *


def input_int(s='> '):
    c = input(s)
    if c == 'q':
        return '<quit>'
    if str_is_int(c):
        return int(c)
    else:
        return None


def input_from_choices(s='> ',choices=[]):
    c = input(s)
    if str_is_int(c):
        c = int(c)
    if c in choices:
        return c
    else:
        return None


def input_int_in_range(a,b,s=''):
    if not s:
        s = d2s('input_int_in_range',a,b,' > ')
    c = input_int(s)
    if c == '<quit>':
        return c
    if c is None or c < a or c > b:
        return None
    else:
        return c


def select_from_list(
    lst,
    ignore_underscore=False,
    prefix='    ',
    print_lst=None,
    print_one_element_lst=True,
    title='',
):
    if not lst:
        return None
    ctr = 0
    if print_one_element_lst or len(lst) > 1:
        if title:
            print(title)
        for i in rlen(lst):
            if print_lst:
                e = print_lst[i]
            else:
                e = lst[i]
            print(prefix,d2n(i,')'),e)
            ctr += 1
    if ctr > 1:
        i = input_int_in_range(0,len(lst)-1,'>> ') #d2s(prefix,'>> ')) #,fmt))
    else:
        i = 0
    if i is None:
        return None
    return lst[i]


def multi_select_from_list(lst,selected,ignore_underscore=False):
    lst_star = []
    lst = sorted(lst)
    for l in lst:
        if l in selected:
            lst_star.append('* '+l)
        else:
            lst_star.append(l)
    s = select_from_list(lst_star)
    if s:
        s = s.replace('* ','')
        if s in selected:
            selected.remove(s)
        else:
            selected.append(s)
    return sorted(selected)



    

if __name__ == '__main__':
    eg(__file__)
    a = input_int_in_range(1,10)
    print('entered',a)

#EOF
