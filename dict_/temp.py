from utilz.dict_.zprint import *

import_str = """
I = {}
exec(get_import_str(ps,I))
fun_name = fnamene(__file__)
"""

main_str = """
if __name__ == '__main__':
    eg(__file__)
    A = get_Arguments(_In)
    _Out = _do(**A)
    zprint(_Out,t=__file__)
"""

def Out_dict(fun_name,out,A,l=[],p=1):
    if p:
        s = l+[{fun_name:{'in':A,'out':out}}]
    else:
        s = []
    return {
        'out':out,
        'str':s,
    }

def get_import_str(ps,I):
    s = ''
    for p in ps:
        m = p.replace('/','.').replace('.py','')
        I[p] = importlib.import_module(m)
        if os.path.getmtime(p) > os.path.getmtime(__file__):
            print('reloading',p)
            importlib.reload(I[p])
        f = fnamene(p)
        s += f +" = I['"+p+"']._do\n"
    return s