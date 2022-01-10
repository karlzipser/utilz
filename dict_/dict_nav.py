
from utilz.core import *
from utilz.dict_.dict_access import *
from utilz.dict_.mini_menu import *
from utilz.misc.sys import *
from utilz.misc.osx import *

Arguments = get_Arguments(
    Defaults={
        'path':'k3',
        'condense_dict':False,
        'ignore_meta':True,
        'max_depth':1,
        'preview_x':0,
        'preview_y':0,
        'preview_h':250,
        'preview_w':500,
    }
)

# python k3/utils/dict_/dict_nav.py --path Desktop --max_depth 5 --preview_h 800 --preview_w 800    
# python k3/utils/dict_/dict_nav.py --path iCloud_Links/jpg/2020/6 --max_depth 5 --preview_h 800 --preview_w 800



def main(**Arguments):
    eg(__file__)

    name = Arguments['path']

    if name == 'history':

        D = {}
        oD = dict_access(D,name)

        def lines_from_hist_file(path):
            r = r'(^\s*\d+\s+)([\w\./\-].*)'
            q = []
            h = txt_file_to_list_of_strings(path)
            for l in h:
                m = re.match(r,l)
                if m:
                    #cy(m.groups()[1],r=1)
                    a = m.groups()[1]
                    #print(qtd(a))
                    a = re.sub(r'\s*$','',a)
                    #print(qtd(a))
                    a = re.sub(r'\s+',' ',a)
                    #print(qtd(a))
                    q.append(a)
                else:
                    cr(l,r=0)
            return q

        histfile = opjD('hist.txt')
        q = lines_from_hist_file(histfile)

        for p in q:
            try:
                oD( p.replace(' ','/') + '/' , e=p )
            except KeyboardInterrupt:
                cr('*** KeyboardInterrupt ***')
                sys.exit()
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print('Exception!')
                print(d2s(exc_type,file_name,exc_tb.tb_lineno)) 

        
    else:

        D = files_to_dict(opjh(name))

        oD = dict_access(D,name)



    if Arguments['condense_dict']:
        D = condense_dict(D)

    close_Finder_windows()
    quit_Preview()

    navigate(D,oD,name,Arguments)


def navigate(D,oD,name,Arguments):

    if Arguments['ignore_meta']:
        oD('__meta__/ignore_keys/', e=['__meta__'])
    if Arguments['max_depth']:
        oD('__meta__/max_depth/', e=Arguments['max_depth'])

    clear_screen()
    oD(up_down='-',do_fname=1)

    c = None

    U = {}

    preview_on = False

    while True:

        os_system(""" osascript -e 'tell application "Terminal" to activate' """,e=0)

        c = input('-> ')

        if c in ['',None]:
            continue

        cc = '-'
        
        bounds_str = '{'+d2c(
            Arguments['preview_x'],
            Arguments['preview_y'],
            Arguments['preview_y']+Arguments['preview_w'],
            Arguments['preview_x']+Arguments['preview_h'],
            ) + '}'

        m = re.match( r'^\s*([a-zA-Z]+)\s*(\d*)$', c)

        if m:

            if m.groups()[0] == 'q':
                close_Finder_windows()
                if preview_on:
                    quit_Preview()
                    preview_on = False
                break

            elif m.groups()[0] == 'M':
                #cr(1,r=1)
                mini_menu(Arguments)

            elif m.groups()[0] == 'c':
                close_Finder_windows()
                if preview_on:
                    quit_Preview()
                    preview_on = False

            elif m and m.groups()[0] == 'm':
                cr(m.groups()[1], str_is_int(m.groups()[1]))
                if str_is_int(m.groups()[1]):
                    i = int(m.groups()[1])
                else:
                    i = input_int_in_range(
                        0,
                        10*10,
                        d2n('max depth (',D['__meta__']['max_depth'],') >>> ')
                    )
                if type(i) is int:
                    D['__meta__']['max_depth'] = i
                clear_screen()
                oD(up_down='-',do_fname=1)
                continue
        
            elif m.groups()[0] in ['u','d']:
                cc = m.groups()[0]

        clear_screen()
        U,print_lines = oD(up_down=cc,do_fname=1)
        if c[-1] in [' ','.']:
            flag = True
        else:
            flag = False

        m = re.match( r'^\s*(\d+)\s*(\w*)$', c)

        if m:
            if str_is_int(m.groups()[0]):
                i = int(m.groups()[0])

                if i in U:
                    p = U[i]['path']

                    if flag:#m.groups()[1] != 'o':
                        oD('__meta__/menu_path/',e=p)

                    clear_screen()

                    oD(up_down='-',do_fname=1)

                    oDp = oD(p)

                    if type(oDp) is dict:
                        #cm('dict')
                        oDp_show = '{...}'
                        if True:#len(m.groups()[1]) > 0:
                            if not flag:#if m.groups()[1] == 'o': # may use flag instead
                                os_system('open',qtd(name+'/'+p)) # may need to change as for images

                    elif type(oDp) is list:
                        #cm('list')
                        oDp_show = '' # '[...]'
                        if True:#len(m.groups()[1]) > 0:
                            #if m.groups()[1] == 'o':

                            rng = []

                            if U[i]['lst_indx'] is None:
                                if not flag:#m.groups()[1] == 'o':
                                    rng = range(len(oDp))
                            else:
                                rng = [U[i]['lst_indx']]

                            #qP = True

                            for j in rng:
                                e = oDp[j]
                                #cy(name,p,e)
                                #n = qtd(name+'/'+p+e)
                                n = qtd(e) # this may have to do with symbolic links
                                #cg(qtd(exname(e.lower())))
                                if exname(e.lower()) in [
                                    '',
                                    'txt','rtf','xml','html','doc',
                                    'py','c','cpp','c++',
                                    'jpg','jpeg',
                                    'png',
                                    'gif','giff',
                                    'tiff','tif',
                                ]:
                                    #if qP:
                                    #   quit_Preview()
                                    #    qP = False

                                    os_system('open',n)
                                    if exname(e.lower()) in [
                                        'jpg','jpeg',
                                        'png',
                                        'gif','giff',
                                        'tiff','tif',
                                    ]:
                                        if not preview_on:
                                            time.sleep(0.5) # let Preivew start up
                                        os_system("""osascript -e 'tell application "Preview" to set bounds of front window to """+bounds_str+"""' """,e=0)
                                        preview_on = True
                                else:
                                    if exname(e) != 'pyc':
                                        cr(
                                            'ignorning',
                                            n,
                                            'because of extension'
                                            )
                    elif type(oDp) is tuple:
                        oDp_show = '(...)'
                    elif type(oDp) is str:
                        oDp_show = oDp
                        os_system('open',qtd(name+'/'+out_))  # may need to change as for images
                    else:
                        oDp_show = str(oDp)

                    
                    if U[i]['lst_indx'] is None:
                        out_ = p + oDp_show
                        #cy('out:',out_)
                    else:
                        out_ = p+str(oDp[U[i]['lst_indx']])
                        #cg('out:',out_)










if not interactive() and __name__ == '__main__':
    main(**Arguments)



#EOF

# ,b



