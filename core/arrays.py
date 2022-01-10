from utilz.core.renaming import *
from utilz.core.znp import *


def zeroToOneRange(m):
    min_n = 1.0*np.min(m)
    return (1.0*m-min_n)/(1.0*np.max(m)-min_n)

z2o = zeroToOneRange


def z55(m):
    return (255*z2o(na(m))).astype(np.uint8)


def z2_255_by_channel(m):
    for i in range(3):
        m[:,:,i] = z55(m[:,:,i])


def get_blank_rgb(h,w):
    return zeros((h,w,3),np.uint8)


def zscore(m,thresh=np.nan,all_values=False):
    m_mean = np.mean(m)
    z = m - m_mean
    m_std = np.std(m)
    z /= m_std
    if not np.isnan(thresh):
        z[z < -thresh] = -thresh
        z[z > thresh] = thresh
    if all_values:
        return z,m_mean,m_std
    else:
        return z


def mean_of_upper_range(data,min_proportion,max_proportion):
    return array(sorted(data))[int(len(data)*min_proportion):int(len(data)*max_proportion)].mean()


def mean_exclude_outliers(data,n,min_proportion,max_proportion):
    """
    e.g.,

    L=lo('/media/karlzipser/ExtraDrive4/bair_car_data_new_28April2017/meta/direct_rewrite_test_11May17_16h16m49s_Mr_Blue/left_image_bound_to_data.pkl' )
    k,d = get_key_sorted_elements_of_dic(L,'encoder')
    d2=mean_of_upper_range_apply_to_list(d,30,0.33,0.66)
    CA();plot(k,d);plot(k,d2)
    
    """
    n2 = int(n/2)
    rdata = []
    len_data = len(data)
    for i in range(len_data):
        if i < n2:
            rdata.append(mean_of_upper_range(data[i:i-n2+n],min_proportion,max_proportion))
        elif i < len_data + n2:
            rdata.append(mean_of_upper_range(data[i-n2:i-n2+n],min_proportion,max_proportion))
        else:
            rdata.append(mean_of_upper_range(data[i-n2:i],min_proportion,max_proportion))
    return rdata

def meo(data,n):
    return mean_exclude_outliers(data,n,1/3.0,2/3.0)



  
if __name__ == '__main__':
    eg(__file__)
    a = na([1.,3.,5.])
    b = z2o(a)
    c = zeros((int('1'),int('2')),np.uint8)
    print("a = na([1.,3.,5.])")
    print(a)
    print("b = z2o(a)")
    print(b)
    print("c = zeros((int('1'),int('2')),np.uint8)")
    print(c)

#EOF
