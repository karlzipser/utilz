
from utilz import *


alp = '[_A-Za-z]'
alpnum = '[A-Za-z0-9_]'
path_ = '[-~/.A-Za-z0-9_]'
path_s = '[-~/.A-Za-z0-9_\s]'


def match_int(s):
    if type(s) is int:
        return 'int_',s
    if type(s) is not str:
        return None,None
    if str_is_int(s):
        return 'int_',int(s)
    return None,None


def match_float(s):
    if type(s) is float:
        return 'float_',s
    if type(s) is not str:
        return None,None
    if str_is_int(s):
        return None,None
    if str_is_float(s):
        return 'float_',float(s)
    return None,None


def match_bool(s):
    if type(s) is bool:
        return 'bool_',s
    if type(s) is not str:
        return None,None
    if s == 'True':
        return 'bool_',True
    if s == 'False':
        return 'bool_',False
    return None,None


def match_name(s):
    if type(s) is not str:
        return None,None
    if match_whole([alp,alpnum,'*'],s):
        return 'name_',s
    return None,None


def match_short_argname(s):
    if type(s) is not str:
        return None,None
    if match_whole(['-',alp],s):
        return 'short_argname_',s
    return None,None


def match_long_argname(s):
    if type(s) is not str:
        return None,None
    if match_whole(['--',alp,alpnum,'+'],s):
        return 'long_argname_',s
    return None,None


def match_list(s):
    if type(s) is list:
        return 'list_',s
    if ',' in s:
        return 'list_',s.split(',')
    return None,None


def match_path(s):
    if type(s) is not str:
        return None,None
    if len(s) > 2:
        if s[0] == '"' and s[-1] == '"':
            s = s[1:-1]
        if s[0] == "'" and s[-1] == "'":
            s = s[1:-1]
    if match_whole(['[~/.]+'],s):
        return 'path_',s
    if match_whole(['[~/.]*',alpnum,path_s,'*'],s):
        return 'path_',s
    return None,None


def match_whole(pattern,s):
    if type(pattern) is list:
        pattern = ''.join(pattern)
    return re.match(d2n('^',pattern,'$'),s)


if __name__ == '__main__':
    a = ['Frank','a1','1','1.1',2,'~/Desktop','1.1',1.1,'1,2,a',[1,2,3]]
    for b in a:
        print(qtds(b),match_int(b))
        print(qtds(b),match_float(b))
        print(qtds(b),match_path(b))
        print(qtds(b),match_list(b))


#EOF