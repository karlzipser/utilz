from utilz.core.renaming import *


def opj(*args):
    if len(args) == 0:
        args = ['']
    str_args = []
    for a in args:
        str_args.append(str(a))
    return os.path.join(*str_args)


def opjh(*args):
    return opj(home_path,opj(*args))


def opjD(*args):
    return opjh('Desktop',opj(*args))


def opjb(*args):
    return opjh('bucket',opj(*args))


def opjk(*args):
    return opjh('k3',opj(*args))


def opjm(*args):
    if not using_osx():
        media_path = opj('/media',username)
        return opj(media_path,opj(*args))
    else:
        media_path = '/Volumes'
        return opj(media_path,opj(*args))


def opjiC(*args):
    return opj(opjh('Library/Mobile Documents/com~apple~CloudDocs'),opj(*args))  


def fname(path):
    return path.split('/')[-1]
fn = fname


def fnamene(path):
    """
    filename, no extension
    """
    return fname(path).split('.')[0]


def exname(path):
    """
    file extension
    """
    try:
        a = fname(path).split('.')
        if len(a) == 1:
            return ''
        return a[-1]
    except:
        return ''


def pname(path):
    return '/'.join(  path.split('/')[:-1]  )
pn = pname



if __name__ == '__main__':
    eg(__file__)
    p = __file__
    print(p)               
    print(fname(p))     
    print(fnamene(p))    
    print(exname(p))       
    print(fname(p))        
    print(pname(p))        
    print(fname(pname(p)))


#EOF
  
