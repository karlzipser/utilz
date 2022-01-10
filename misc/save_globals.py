from utilz.misc.printing import *


def Record_vars(global_key_list,Globals):
    ls = [global_key_list]

    def update(global_key_list):
        ls.append(global_key_list)
    def get_new(global_key_list):
        N = {}
        for l in ls[-1]:
            if l not in ls[0]:
                print(l)
                if l[0] != '_':
                    g = Globals[l]
                    try:
                        pickle.dumps(g)
                        N[l] = g
                    except:
                        pd2s('Warning, cannot pickle',qtd(l),'so skipping it.')
                        N[l] = '--not able to pickle--'
        return N
    def save(global_key_list,f=opjD('D.pkl')):
        update(global_key_list)
        so(get_new(global_key_list),f)

    return namedtuple(
        '_',
        'update get_new save')(
         update, get_new, save
    )




if __name__ == '__main__':
    
    clear_screen()
    clp('Examples from',__file__,'`--r')

    R = Record_vars(list(globals().keys()),globals())

    if 'e.g. data':
        a = 1
        b = [2,3,4]
        c = {'a':a,'b':b}
        d = [a,b,c]
        #P = Percent('P','calculating','calculated')
        #P.show(5,10)
        #P.show()

    #R.save(list(globals().keys()))
    R.save(kys(globals()))
    
    o = loD('D')

    kprint(o,'reloaded R')

#EOF
