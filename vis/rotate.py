





# https://stackoverflow.com/questions/31735499/calculate-angle-clockwise-between-two-points
from math import acos
from math import sqrt
from math import pi

def length(v):
    return sqrt(v[0]**2+v[1]**2)
def dot_product(v,w):
   return v[0]*w[0]+v[1]*w[1]
def determinant(v,w):
   return v[0]*w[1]-v[1]*w[0]
def inner_angle(v,w):
   cosx=dot_product(v,w)/(length(v)*length(w))
   if cosx > 1.0:
        cosx = 1.0
   elif cosx < -1.0:
        cosx = -1.0
   rad=acos(cosx) # in radians
   return rad*180/pi # returns degrees
def angle_clockwise(A, B):
    inner=inner_angle(A,B)
    det = determinant(A,B)
    if det<0: #this is a property of the det. If the det < 0 then B is clockwise of A
        return inner
    else: # if the det > 0 then A is immediately clockwise of B
        return 360-inner


def corrected_angle(slope,point,origin):

    alpha = angle_clockwise((1,0),(1,slope))

    x = point[0]-origin[0]
    y = point[1]-origin[1]

    if x >= 0 and y >= 0:
        alpha = 360 - alpha
    elif x < 0 and y >= 0:
        alpha = 180 - alpha
    elif x < 0 and y < 0:
        alpha = 180+360 - alpha
    elif x >= 0 and y < 0:
        alpha = 90-alpha+270
    else:
        assert False

    return alpha


    


def unit_vector(vector):
    """http://stackoverflow.com/questions/2827393/angles-between-two-n-dimensional-vectors-in-python
    Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)


def angle_between(v1, v2):
    """http://stackoverflow.com/questions/2827393/angles-between-two-n-dimensional-vectors-in-python
    Returns the angle in radians between vectors 'v1' and 'v2'::

            >>> angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            >>> angle_between((1, 0, 0), (1, 0, 0))
            0.0
            >>> angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))



def rotatePoint(centerPoint,point,angle):
    """http://stackoverflow.com/questions/20023209/function-for-rotating-2d-objects
    Rotates a point around another centerPoint. Angle is in degrees.
    Rotation is counter-clockwise"""
    angle = math.radians(angle)
    temp_point = point[0]-centerPoint[0] , point[1]-centerPoint[1]
    temp_point = ( temp_point[0]*math.cos(angle)-temp_point[1]*math.sin(angle) , temp_point[0]*math.sin(angle)+temp_point[1]*math.cos(angle))
    temp_point = temp_point[0]+centerPoint[0] , temp_point[1]+centerPoint[1]
    return temp_point



def rotatePolygon(polygon,theta):
    """http://stackoverflow.com/questions/20023209/function-for-rotating-2d-objects
    Rotates the given polygon which consists of corners represented as (x,y),
    around the ORIGIN, clock-wise, theta degrees"""
    theta = math.radians(theta)
    rotatedPolygon = []
    for corner in polygon :
        rotatedPolygon.append(( corner[0]*math.cos(theta)-corner[1]*math.sin(theta) , corner[0]*math.sin(theta)+corner[1]*math.cos(theta)) )
    return na(rotatedPolygon)


def rotatePolygon__array_version(polygon,theta):
    theta = math.radians(theta)
    for i in rlen(polygon):
        corner = polygon[i,:]
        polygon[i,:] = na(( corner[0]*math.cos(theta)-corner[1]*math.sin(theta) , corner[0]*math.sin(theta)+corner[1]*math.cos(theta)) )



def rotatePolygon_cuda(polygon,theta):
    import torch
    if len(shape(polygon)) == 2:
        new_shape = list(shape(polygon))+[1]
        A = zeros(new_shape)
        A[:,:,0] = polygon
        polygon = A
    theta = np.radians(theta)
    R = [[np.cos(theta),-np.sin(theta),],
        [np.sin(theta),np.cos(theta)]]
    S =  len(polygon) * [R]
    St = torch.Tensor(S).cuda()
    Pt = torch.Tensor(polygon).cuda()
    polygon = torch.bmm(St,Pt).cpu().numpy()[:,:,0]
    return polygon




def rigid_transform_3D(A, B):
    """
    http://nghiaho.com/uploads/code/rigid_transform_3D.py_
    Input: expects Nx3 matrix of points
    Returns R,t
    R = 3x3 rotation matrix
    t = 3x1 column vector
    """
    from math import sqrt
    assert len(A) == len(B)
    A = np.matrix(A); B = np.matrix(B)
    N = A.shape[0]
    centroid_A = np.mean(A, axis=0)
    centroid_B = np.mean(B, axis=0)
    AA = A - np.tile(centroid_A, (N, 1))
    BB = B - np.tile(centroid_B, (N, 1))
    H = np.transpose(AA) * BB
    U, S, Vt = np.linalg.svd(H)
    R = Vt.T * U.T
    if np.linalg.det(R) < 0:
       #print "Reflection detected"
       Vt[2,:] *= -1
       R = Vt.T * U.T
    t = -R*centroid_A.T + centroid_B.T
    return R, t

