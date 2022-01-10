
from utilz.core.files.files import *
import h5py


def h5r(filename,assert_exists=True,use_real_path=False):
    if use_real_path:
        filename = os.path.realpath(filename)
    if assert_exists:
        #cy(filename,ra=1)
        assert_disk_locations(filename)
    return h5py.File(filename,'r')
def h5w(filename,use_real_path=False):
    if use_real_path:
        filename = os.path.realpath(filename)
    assert_disk_locations(pname(filename))
    return h5py.File(filename,'w')
def h5rw(filename,use_real_path=False):
    if use_real_path:
        filename = os.path.realpath(filename)
    assert_disk_locations(pname(filename))
    return h5py.File(filename,'r+')


def save_as_h5py(file_path,D,dtype='float16'):
    F = h5w(file_path)
    print('writing topics to',file_path)
    for k in D.keys():
        cm(k)
        D[k] = na(D[k])
        
        if type(dtype) == dict:
            dt = dtype[k]
        else:
            dt = dtype
        print('    ',k,len(D[k]),dt)
        F.create_dataset(k,data=D[k],dtype=dt)
    F.close()
    print('done.')


    
    
if __name__ == '__main__':
    eg(__file__)



#EOF
