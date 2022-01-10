
from utilz import *
from utilz.karguments.parse_utils.classifying import *

"""
python k3/drafts/karguments/parse_argument_string.py a b1b_l 1,2,3 2.2 3.a /a.3 '/Users/karl zipser/Desktop' ~/Desktop    -a False --bb -c 0 --xx --dogs -d 1,2,a --dog
"""

def parse_argument_string(arglist,verbose=True,convert_unknown_to_str=False):
    #import shlex
    #ts = shlex.split(argstr)
    ts = arglist
    tokens = []
    for t in ts:
        if re.findall('\s',t):
            t = qtd(t)
        tokens.append(t)

    classifications = classify_tokens_and_expand_implicit_True_args(tokens)

    if convert_unknown_to_str:
        for i in rlen(classifications):
            if classifications[i][0] == 'unknown_':
                v = classifications[i][1]
                classifications[i] = ('str_',v)

    for c in classifications:
        if c[0] == 'unknown_':
            if verbose:
                cE('Error, token',qtds(c[1]),"is of 'unknown_' type")
                raw_enter()
            return None

    current_arg = ''

    A = {'positional_args':[]}

    for c in classifications:

        if not current_arg:
            if '_argname_' not in c[0]:
                A['positional_args'] += [c]
            else:
                current_arg = c[1]
        elif '_argname_' in c[0]:
            current_arg = c[1]
        else:
            if current_arg in A:
                if verbose:
                    cE(arglist)
                    cE('Error,',(c,t),'with current_arg',qtds(current_arg),"already used")
                    cE('Check for positional arguments after first keyword argument or repeat of keyword argument.')
                    raw_enter()
                return None
            A[current_arg] = c
    Args = {'type':{},'value':{}}


    for k in A:
        if k != 'positional_args':
            t = A[k][0]
            v = A[k][1]
        else:
            t = 'list'
            v = ','
        if t == 'list':
            v = v.split(',')
        if len(k) == 2 and k[0] == '-':
            Args['type'][k[1]] = t
            Args['value'][k[1]] = v
        elif len(k) > 3 and k[0:2] == '--':
            Args['type'][k[2:]] = t
            Args['value'][k[2:]] = v
        else:
            assert k == 'positional_args'
            Args['type'][k] = []
            Args['value'][k] = []
            for p in A[k]:
                t = p[0]
                v = p[1]
                if t == 'list':
                    v = v.split(',')
                Args['type'][k].append( t )
                Args['value'][k].append( v )
    return Args




if __name__ == '__main__':
    kprint(
        parse_argument_string(sys.argv[1:],),
        t=' '.join(sys.argv[1:])
    )

#EOF
