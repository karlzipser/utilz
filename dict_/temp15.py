from k3 import *



def sigma(m):
    P = Percent(str(m))
    timer = Timer(1)
    q = 0
    for n in range(1,m+1):
        if n % 500 == 0:
            P.show(n,m+1)
        q += 1/n
    return q

if __name__ == '__main__':
    A = get_Arguments({'k':10})
    k = A['k']
    k = 20
    a = sigma(3**k) - sigma(3**(k-1))
    print(a)