import numpy as np
from utilz.core.arrays import *

def get_IdentityMatrix():
	return na(
	[
		[ 1, 0, 0, 0 ],
		[ 0, 1, 0, 0 ],
		[ 0, 0, 1, 0 ],
		[ 0, 0, 0, 1 ],
	]
)

def get_TranslationMatrix(x,y,z):
	return na(
	[
		[ 1, 0, 0, 0 ],
		[ 0, 1, 0, 0 ],
		[ 0, 0, 1, 0 ],
		[ x, y, z, 1 ],
	]
)
	
def get_xTranslationMatrix(x):
	return get_TranslationMatrix(x,0,0)

	
def get_yTranslationMatrix(y):
	return get_TranslationMatrix(0,y,0)
	
def get_zTranslationMatrix(z):
	return get_TranslationMatrix(0,0,z)


def get_ScalingMatrix(x,y,z):
	return na(
	[
		[ x, 0, 0, 0 ],
		[ 0, y, 0, 0 ],
		[ 0, 0, z, 0 ],
		[ 0, 0, 0, 1 ],
	]
)
def get_xyzScalingMatrix(a):
	return get_ScalingMatrix(a,a,a)
def get_xScalingMatrix(x):
	return get_ScalingMatrix(x,1,1)
def get_yScalingMatrix(y):
	return get_ScalingMatrix(1,y,1)
def get_zScalingMatrix(z):
	return get_ScalingMatrix(1,1,z)


def get_xRotationMatrix(theta):
	c = np.cos(np.radians(theta))
	s = np.sin(np.radians(theta))
	return na(
	[
		[ 1, 0, 0, 0 ],
		[ 0, c, -s, 0 ],
		[ 0, s, c, 0 ],
		[ 0, 0, 0, 1 ],
	]
)

def get_yRotationMatrix(theta):
	c = np.cos(np.radians(theta))
	s = np.sin(np.radians(theta))
	return na(
	[
		[ c, 0, s, 0 ],
		[ 0, 1, 0, 0 ],
		[ -s,0, c, 0 ],
		[ 0, 0, 0, 1 ],
	]
)

def get_zRotationMatrix(theta):
	c = np.cos(np.radians(theta))
	s = np.sin(np.radians(theta))
	return na(
	[
		[ c, -s, 0, 0 ],
		[ s, c, 0, 0 ],
		[ 0, 0, 1, 0 ],
		[ 0, 0, 0, 1 ],
	]
)

def xyzs_to_4D(xyzs,assume_all_ones=True):
    s = shape(xyzs)
    assert len(s) == 2
    assert s[1] >= 3
    if s[1] == 4:
        if assume_all_ones:
            if xyzs[0,3] == 1:
                return xyzs
        xyzs[:,3] = 1
    elif s[1] == 3:
        xyzs = np.concatenate((xyzs,1+zeros((s[0],1))),1)
    else:
        assert False
    return xyzs
    
#EOF
