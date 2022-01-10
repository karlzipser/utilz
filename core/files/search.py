from utilz.core.files.files import *


os.environ['GLOG_minloglevel'] = '2'

def sgg(d,r=0):
    return sorted(gg(d,recursive=r),key=natural_keys)

def sggo(d,*args,r=0):
    a = opj(d,*args)
    return sgg(a,r=r)

def sorted_by_cmtime(list_of_files):#,c=True):
    Mtimes = {}
    #if c:
    #    fn = os.path.getctime
    #else:
    #    fn = os.path.getmtime
    for f in list_of_files:
        Mtimes[f] = min(os.path.getctime(f),os.path.getmtime(f))
    lst0 = sorted(Mtimes.items(), key=lambda x:x[1])
    lst1 = []
    for l in lst0:
        lst1.append(l[0])
    return lst1

def get_files_sorted_by_mtime(path_specification):
    files = sggo(path_specification)
    Mtimes = {}
    for f in files:
        Mtimes[f] = os.path.getmtime(f)
    return sorted(Mtimes.items(), key=lambda x:x[1])

def tsggo(d,*args):
    a = opj(d,*args)
    #CS_(a)
    return get_files_sorted_by_mtime(a)


def most_recent_file_in_folder(
    path,str_elements=[],
    ignore_str_elements=[],
    return_age_in_seconds=False
):
    files = gg(opj(path,'*'))
    if len(files) == 0:
        return None
    candidates = []
    for f in files:
        fn = fname(f)
        is_candidate = True
        for s in str_elements:
            if s not in fn:
                is_candidate = False
                break
        for s in ignore_str_elements:
            if s in fn:
                is_candidate = False
                break
        if is_candidate:
            candidates.append(f)
    mtimes = {}
    if len(candidates) == 0:
        return None
    for c in candidates:
        mtimes[os.path.getmtime(c)] = c
    mt = sorted(mtimes.keys())[-1]
    c = mtimes[mt]
    if return_age_in_seconds:
        return c,time.time()-mt
    else:
        return c




IMAGE_EXTENSIONS = ['jpg','jpeg','JPG','JPEG','png','PNG','tif','tiff','TIF','TIFF']



def files_to_dict(
    path,
    ignore_underscore=True,
    require_extension=[],
    ignore_extension=['pyc'],
    ignore=[],
    save_stats=False,
    list_symbol='*',
    process_symbol=True,
):
    D = {list_symbol : []}
    fs = sggo(path,'*')
    timer = Timer(0.01)
    for f in fs:
        if timer.check():
            timer.reset()
            #print(time.time())
            print(rndchoice(['/','\\']),end='\r',flush=True)
        if fname(f)[0] == '_' and ignore_underscore:
            continue
        do_continue = False
        for ig in ignore:
            if ig in f:
                do_continue = True
                break
        if do_continue:
            continue
        if not os.path.isdir(f):
            if save_stats:
                f_ = {
                    f:{
                        'mtime':os.path.getctime(f),
                        #'ctime':os.path.getctime(f),
                        'size':os.path.getsize(f),
                    }
                }
            else:
                f_ = f
            if not require_extension or exname(f) in require_extension:
                if not ignore_extension or exname(f) not in ignore_extension:
                    D[list_symbol].append(f_)
        else:
            D[fname(f)] =\
             files_to_dict(
                path=f,
                ignore_underscore=ignore_underscore,
                require_extension=require_extension,
                ignore=ignore,
                save_stats=save_stats,
                )
    return D
    
    


def files_to_list(path,**K):
    return all_values(files_to_dict(path,**K))



def find_list_of_files_recursively(path,pattern,verbose=True,ignore=[]):
    F = find_files_recursively(path,pattern,FILES_ONLY=True,verbose=verbose)
    l = []
    if 'o' not in locals():
        o = []
    for p in F['paths']:
        continue_ = False
        for i in ignore:
            #print('ignore =',i,'p =',p)
            #cy('ignore =',i,'p =',p)
            if i in p:
                continue_ = True
                break
        if continue_:
            #cr('ignoring',p)
            continue
        for f in F['paths'][p]:
            #if verbose:
            #    clp(p,'`r--',f,'`g--')        
            assert (p,f) not in l
            g = opj(F['src'],p,f)
            #g = opj(p,f)
            #g = g.encode('unicode_escape')
            #print('***',g,os.path.exists(g))
            l.append((p,f))
            assert os.path.exists(g)
            o.append(g)
    return o



#,a
def find_files(
    start=opjD(),
    patterns=["*"],
    ignore=['Photos Library','Photo Booth','Library'],
    file_list=[],
    __top=True,
    recursive=True,
    timer=Timer(1),
    noisy=False,
):
    if timer.rcheck() and noisy:
        print('find_files found',len(file_list),'files')
    if __top:
        file_list = []
    if type(patterns) == str:
        patterns = [patterns]
    for pattern in patterns:
        #print('start:',start,'len(file_list):',len(file_list))
        _fs= sggo(start,pattern)

        for f in _fs:
            #print(f)
            if os.path.isfile(f):
                file_list.append(f)

    a = sggo(start,'*')

    if recursive:
        ds = []
        for b in a:
            if os.path.isdir(b):
                _ignore = False
                for ig in ignore:
                    if ig in b:
                        _ignore = True
                        break
                if not _ignore:
                    ds.append(b)
                else:
                    print('ignoring',b)

        for d in ds:
            find_files(
                start=d,patterns=patterns,ignore=ignore,file_list=file_list,__top=False,
                recursive=True,timer=timer)
    if noisy:
        print('find_files found',len(file_list),'files. done.')
    if __top:
        return sorted(list(set(file_list)),key=natural_keys)

#,b






if __name__ == '__main__':
    eg(__file__)
    l = find_files(
        opjD(),
        "*.png",
    )
    l = sorted(l)
    for m in l:
        print(m)

#EOF
