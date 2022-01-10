
from utilz.misc.printing import *

def using_platform():
    from sys import platform
    if platform == "linux" or platform == "linux2":
        return 'linux'
    elif platform == "darwin":
        return 'osx'
    else:
        spd2s('unknown system (not linux or osx)')
        assert False
def using_linux():
    if using_platform() == 'linux':
        return True
    return False
def using_osx():
    if using_platform() == 'osx':
        return True
    return False


try:
    import rospy
    HAVE_ROS = True
except:
    HAVE_ROS = False

try:
    if username == 'nvidia':
        HAVE_GPU = True
    else:
        unix('nvidia-smi',print_stdout=True)
        HAVE_GPU = True
        cr('*** warning, check HAVE_GPU ***',ra=1)
except:
    HAVE_GPU = False


if __name__ == '__main__':
    
    eg(__file__)

    clp(' using_platform():',using_platform())
    clp(' using_linux():',using_linux())
    clp(' using_osx():',using_osx())
    clp(' HAVE_ROS:',HAVE_ROS)
    clp(' HAVE_GPU:',HAVE_GPU)
    print('')

#EOF