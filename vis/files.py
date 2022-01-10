
from utilz.misc import *
from utilz.core.znp import *
import cv2
imread = cv2.imread
imsave = cv2.imwrite


"""
l=load_img_folder_to_list('/Users/karlzipser/caffe_models/temp')
l=1.0*array(l)
l/=l.max()
mi(vis_square(l))
"""

def load_img_folder_to_dict(img_folder):
    '''Assume that *.* selects only images.'''
    img_fns = gg(opj(img_folder,'*.*'))
    imgs = {}
    for f in img_fns:
        imgs[fname(f)] = imread(f)
    return imgs

def load_img_folder_to_list(img_folder):
    return dict_to_sorted_list(load_img_folder_to_dict(img_folder))



# take an array of shape (n, height, width) or (n, height, width, channels)
# and visualize each (height, width) thing in a grid of size approx. sqrt(n) by sqrt(n)
def vis_square(data_in, padsize=1, padval=0):
    data = data_in.copy()
    data -= data.min()
    data /= data.max()
    
    # force the number of filters to be square
    n = int(np.ceil(np.sqrt(data.shape[0])))
    padding = ((0, n ** 2 - data.shape[0]), (0, padsize), (0, padsize)) + ((0, 0),) * (data.ndim - 3)
    data = np.pad(data, padding, mode='constant', constant_values=(padval, padval))
    
    # tile the filters into an image
    data = data.reshape((n, n) + data.shape[1:]).transpose((0, 2, 1, 3) + tuple(range(4, data.ndim + 1)))
    data = data.reshape((n * data.shape[1], n * data.shape[3]) + data.shape[4:])
    
    return data


    


def read_img_and_get_orientation_correction_degrees(path):
    import exifread
    """https://pypi.org/project/ExifRead/"""
    tags = {}
    with open(path, 'rb') as f:
        tags = exifread.process_file(f, details=False)
    if "Image Orientation" in tags.keys():
        orientation = tags["Image Orientation"]
        val = orientation.values
        if 3 in val:
            return 180
        if 6 in val:
            return 270
        if 8 in val:
            return 90
    return 0

def has_exif(path):
    import exifread
    with open(path,'r') as f:
        l = len(exifread.process_file(f))
    if l:
        return True
    else:
        return False

def load_image_with_orientation(filepath,change_rgb=True):
    from PIL import Image, ExifTags
    from numpy import asarray
    theta = read_img_and_get_orientation_correction_degrees(filepath)
    if theta in [90,180,270]:
        image=Image.open(filepath)
        image = image.rotate(theta, expand=True)
        image = na(image)[:,:,:3]
    else:
        image = imread(filepath)[:,:,:3]
        if change_rgb:
            image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    return image, theta

def zimread(p):
    return load_image_with_orientation(p)[0]
    