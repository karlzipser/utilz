from utilz.core.essentials import *

def get_safe_name(
    name,
    safe_chars=[],
    replacement_char='_',
    condense=False
):
    lst = []
    for i in range(len(name)):
        if name[i].isalnum():
            lst.append(name[i])
        elif name[i] in safe_chars:
            lst.append(name[i])
        else:
            lst.append(replacement_char)
    s = "".join(lst)
    if condense:
        lst = s.split(replacement_char)
        d = []
        for e in lst:
            if e != '':
                d.append(e)
        s = replacement_char.join(d)
    return s
    

def num_from_str(s):
    try:
        return int(s)
    except:
        try:
            return float(s)
        except:
            #print('String does not represent a number.')
            return None


def checksum_string(s):
    import hashlib
    return hashlib.md5(str(s).encode('utf-8')).hexdigest()



if __name__ == '__main__':
    eg(__file__)
    s = "Is this name: @ safe for a file!!!!"
    print('unsafe name:',s)
    print('get_safe_name():',get_safe_name(s))
    print('abcd123.3 is a string')
    print(num_from_str('123.3'),'is a number from a string')

    
#EOF
  
  
