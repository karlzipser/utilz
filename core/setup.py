from utilz.core.renaming import *


_which_python = sys.version.split(' ')[0]
if _which_python[0] == '3':
    raw_input = input
    using_python3 = True
else:
    using_python3 = False
del _which_python

os.environ['PYTHONUNBUFFERED'] = '1'

    
if __name__ == '__main__':
    eg(__file__)
    print('using_python3',using_python3)
    
#EOF
