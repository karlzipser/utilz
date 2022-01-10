#!/usr/bin/env python3

from utilz.misc.printing import *
import copy

def zprint(
    Dictionary,
    t='',
    title='',
    r=0,
    p=0,
    use_color=0,
    use_line_numbers=0,
    do_print=1,
    ignore_keys=[],
    only_keys=[],
    ignore_types=[],
    ignore_underscore=False,
    max_items=999999,
    max_depth=999999,
    do_return = False,
    do_fname = False,
):
    if title:
        assert not t
        t = title
    if True:#type(Dictionary) is not dict:
        if len(t) > 0:
            n = t
        else:
            n = d2n('<',type(Dictionary).__name__,'>')
        Dictionary = {n:Dictionary}

    V = _preprocess( copy.deepcopy(Dictionary), use_color, do_fname )

    _,D = _get_j_and_W(
        copy.deepcopy(V),
        t=t,
        ignore_keys=ignore_keys,
        only_keys=only_keys,
        ignore_types=ignore_types,
        ignore_underscore=ignore_underscore,
        max_items=max_items,
        max_depth=max_depth,
    )

    E,print_lines = _post_process( D, use_line_numbers, use_color )

    for i in rlen(D):

        try:
            if leaf in D[i][-1]:
                D[i] = D[i][:-1]
        except:
            pass

    if do_print:
        print('\n'.join(print_lines))

    if p:
        time.sleep(p)

    if r:
        raw_enter()

    if do_return:
        return D,print_lines







leaf = 'leaf|'


def _get_j_and_W(
    item,
    t='',
    j=-1,
    r=0,
    p=0,
    use_color=0,
    ignore_keys=[],
    only_keys=[],
    ignore_types=[],
    ignore_underscore=True,
    max_items=999999,
    _top=True,
    _spaces='',
    _space_increment='    ',
    _W={},
    _keylist=[],
    depth=0,
    max_depth=0,
):
    if _top:
        _W = {}

    if 'init':

        if type(item) in ignore_types:
            return j,_W

        _keylist_ = copy.deepcopy(_keylist)

        if not _top:
            _keylist_.append(t)

        
        if j in _W:
            cE(j,'in',kys(_W))
        else:
            pass
        assert j not in _W

        _W[j] = _keylist_

        if t is not None and type(t) is not tuple:
            name = str(t)
        elif type(t) is tuple and len(t) == 1:
            name = d2n('(',t[0],')')
        else:
            name = t

    j += 1

    if type(item) == dict:
        if depth < max_depth:
            depth += 1
            ctr = 0
            if len(item.keys()) == 0:
                item = {'':True}
            for k in sorted(item.keys()):
                if k in ignore_keys:
                    continue
                if ignore_underscore and k[0] == '_':
                    continue
                if len(only_keys) > 0:
                    if k not in only_keys:
                        continue

                j,_ = _get_j_and_W(
                    item[k],
                    t=k,
                    use_color=use_color,
                    _top=False,
                    _spaces=_spaces+_space_increment,
                    _space_increment=_space_increment,
                    ignore_keys=ignore_keys,
                    only_keys=only_keys,
                    ignore_types=ignore_types,
                    ignore_underscore=ignore_underscore,
                    j=j,
                    _W=_W,
                    _keylist=_keylist_,
                    depth=depth,
                    max_depth=max_depth,
                )
                ctr += 1
                if ctr >= max_items:
                    break
    else:
        pass

    return j,_W



def _preprocess(Q,use_color,do_fname):

    for k in kys(Q):

        if type(Q[k]) is list:
            D = {}
            for i in rlen(Q[k]):
                D[(i,)] = Q[k][i]
            Q[k] = D

        if type(Q[k]) is dict:
            Q[k] = _preprocess(Q[k],use_color,do_fname)

        elif type(Q[k]) is None:
            pass

        else:
            if use_color:
                if is_number(Q[k]):
                    s = cf(Q[k],'`g-b')
                elif type(Q[k]) is str:
                    qk = Q[k]
                    if do_fname:
                        qk = fname(qk)
                    s = cf(qk,'`y-b')
                else:
                    s = cf(Q[k],'`b-b')
            else:
                s = str(Q[k])
            Q[k] = { leaf+s : None }
    return Q



def _post_process(Din,use_line_numbers,use_color):

    D = copy.deepcopy(Din)

    vert =  '|    '
    blank = '     '
    bend =  '────┐'

    max_width = 0

    for i in kys(D):
        max_width = max(max_width,len(D[i]))

    for u  in range(max_width):
        for i in sorted(kys(D),reverse=True):
                try:
                    if D[i][u] == D[i+1][u]:
                        D[i+1][u] = vert
                except:
                    pass
        in_line = False
        for i in sorted(kys(D),reverse=True):

                try:
                    if D[i][u] != vert:
                        in_line = True
                    if not in_line and D[i][u] == vert:
                        D[i][u] = blank
                except:
                    in_line = False

    for i in sorted(kys(D),reverse=False):
        if len(D[i]):
            if leaf in str(D[i][-1]):
                D[i][-1] = D[i][-1].replace(leaf,'')
                continue
            l = len(str(D[i][-1]))
            if type(D[i][-1]) is tuple and len(D[i][-1]) == 1:
                b = bend
            elif l <= len(bend):
                b = bend[l-1:]
            else:
                b = ''
            if use_line_numbers:
                if use_color:
                    b += cf('',i,'`--d')
                else:
                    b += ' '+str(i)
            D[i].append(b)

    print_lines = []
    for i in sorted(kys(D),reverse=False):
        w = []
        for y in D[i]:
            if type(y) is tuple:
                y = '└'# '•'
            w.append(str(y))
        print_lines.append(''.join(w))
    

    return D, print_lines



#def type_to_str(a):
#    return str(type(a)).split("'")[-2]

_Arguments = {
            'no-banner':'not relevant',
            'use_color':1,
            'use_line_numbers':1,
            'path':None,
            'html':False,
            'do_print':1,
        }




def main(**A):

    Example = {
        'A':{
            'B':{'G':{'a':'Big is beautiful!'},'H':'holy cow!',},    
            'I':{'G':[1,2,3],'H':[4,5,'6',(1,2)],}, 
        },
        'B':{
            'B':{'G':{'a':'Big is beautiful!'},'H':'holy cow!',},    
            'I':{'G':[1,2,3],'H':[4,5,'6',(1,2)],}, 
        },
    }


    Example = {
        'range':{
            'min':{
                'current':0,
                'min':0,
                'max':10,
            },
            'max':{
                'current':10,
                'min':0,
                'max':10,
            },
        },
        'toggle':False,
        'word': {
            'current':'cat',
            'options':['cat','dog','mouse','horse'],
        }   
    }



    if A['path'] is not None:
        Example = lo(A['path'])


    D, print_lines = zprint(
        Example,
        use_color=A['use_color'],
        use_line_numbers=A['use_line_numbers'],
        do_return=True,
        do_print=A['do_print'],
    )

    if A['html']:
        html_str = lines_to_html_str(print_lines)
        text_to_file(
            opjD('zprint_test.html'),
            d2s(
                """\n""",
                html_str
            )
        )

if __name__ == '__main__':
    main(get_Arguments(_Arguments))

#EOF




