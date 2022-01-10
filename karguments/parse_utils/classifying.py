
from utilz import *
from utilz.karguments.parse_utils.matching import *


def classify_tokens_and_expand_implicit_True_args(tokens,verbose=True):

    classifications = []

    N = {}
    for t in tokens:
        c = classify_token(t)
        classifications.append( c )
        if c[0] in ['short_argname_','long_argname_']:
            if c[1] not in N:
                N[c[1]] = 0
            N[c[1]] += 1
            if N[c[1]] > 1:
                cE('Warning, command line arg',qtds(c[1]),'appears more than once')
                raw_enter()

    a = []

    if classifications:
        
        for i in range(len(classifications)-1):
            a.append( classifications[i] )
            if classifications[i][0] in ['short_argname_','long_argname_']:
                if classifications[i+1][0] in ['short_argname_','long_argname_']:
                    a.append( classify_token('True') )

        i = -1
        a.append( classifications[i] )
        if classifications[i][0] in ['short_argname_','long_argname_']:
            a.append( classify_token('True') )

        classifications = a

    return classifications




def classify_token(s):
    fs = [
        match_int,
        match_float,
        match_bool,
        match_name,
        match_short_argname,
        match_long_argname,
        match_list,
        match_path,
    ]
    for f in fs:
        type_,val_ = f(s)
        #print(type_,val_)
        if type_:
            return type_,val_
    return 'unknown_',s


if __name__ == '__main__':
    a = sys.argv[1:]

    for b in a:
        print(qtds(b),'-->',classify_token(b))

    print('------')
    zprint( classify_tokens_and_expand_implicit_True_args(a))

#EOF