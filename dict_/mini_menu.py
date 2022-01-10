#!/usr/bin/env python3

from utilz.misc.printing import *
#,a


def input_something(name,current):

    assert name is not None
    assert current is not None

    type_ = type(current)

    if type(name) is str:
        istr = 'enter value for '+name+' > '
    else:
        istr = 'enter value > '

    if type_ is bool:
        return not current

    else:
        v = input('enter value for '+name+' > ')
        
        if type_ is int:
            if str_is_int(v):
                v = int(v)
                return v
            else:
                return None

        elif type_ is float:
            if str_is_float(v):
                v = float(v)
                return v
            else:
                return None

        elif type_ is str:
            return v

        else:
            return None





def mini_menu(
    A,
    clear=True,
    menu_name='MINI MEUNU',
    menu_keys=None,
    once=False,
    color=''
    ):

    while True:

        if True:#try:

            if clear:
                clear_screen()

            clp(menu_name,'(q-Enter or ctr-C to exit)',color)

            if menu_keys is None:
                menu_keys = kys(A)
            else:
                for k in menu_keys:
                    assert k in kys(A)


            ks = sorted(menu_keys)
            for i in rlen(ks):
                k = ks[i]
                if k[0] == '_':
                    continue
                s = A[k]
                if type(s) in [int,float,bool]:
                    pass
                elif type(s) is str:
                    s = qtd(s)
                elif type(s) is dict:
                    s = '<dict>'
                elif type(s) is list:
                    s = '<list>'
                elif type(s) is tuple:
                    s = '<tuple>'
                else:
                    s = '<other>'

                clp(str(i)+')',k,'=',s,color)

            n = input_int_in_range(0,len(ks),'# ? ')
            if type(n) == str:
                return n
            #cy(n,r=1)
            if n is None:
                continue

            k = ks[n]
            #cm(n,k)

            if n is None:
                continue
            #cg(k,A[k])
            m = input_something(k,A[k])

            cy(m)

            if m is not None:
                A[k] = m
            else:
                cE('failed to update',k,r=1)

            if once:
                return 'once'
        """
        except KeyboardInterrupt:
            cb('leaving mini_menu')
            return 'done'
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            cE(exc_type,file_name,exc_tb.tb_lineno)
        """





def _mini_menu(A,clear=True,menu_name='MINI MEUNU',menu_keys=None,once=False,color=''):

    while True:

        try:

            if clear:
                clear_screen()

            clp(menu_name,'(ctr-C to exit)',color)

            if menu_keys is None:
                menu_keys = kys(A)
            else:
                for k in menu_keys:
                    assert k in kys(A)


            ks = sorted(menu_keys)
            for i in rlen(ks):
                k = ks[i]
                if k[0] == '_':
                    continue
                s = A[k]
                if type(s) in [int,float,bool]:
                    pass
                elif type(s) is str:
                    s = qtd(s)
                elif type(s) is dict:
                    s = '<dict>'
                elif type(s) is list:
                    s = '<list>'
                elif type(s) is tuple:
                    s = '<tuple>'
                else:
                    s = '<other>'

                clp(str(i)+')',k,'=',s,color)

            n = input_int_in_range(0,len(ks),'# ? ')

            if n is None:
                continue

            k = ks[n]
            #cm(n,k)

            if n is None:
                continue
            #cg(k,A[k])
            m = input_something(k,A[k])

            #cy(m)

            if m is not None:
                A[k] = m
            else:
                cE('failed to update',k,r=1)

            if once:
                return 'once'

        except KeyboardInterrupt:
            cb('leaving mini_menu')
            return 'done'
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            cE(exc_type,file_name,exc_tb.tb_lineno)



















if False:
    A={
        'path':'k3',
        'condense_dict':False,
        'ignore_meta':{1:2},
        'max_depth':[1,2,3],
        'preview_x':0,
        'preview_y':(1,2,3),
        'preview_h':250,
        'preview_w':500,
    }
    while True:
        r = mini_menu(A)
        if r == 'done':
            break

#,b



#EOF
