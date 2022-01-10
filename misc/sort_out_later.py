from utilz.misc.printing import *
from utilz.misc.sys import *




def k_addifnot_aslist(k,D):
    k_addifnot(k,D,[])


def k_addifnot_asdic(k,D):
    k_addifnot(k,D,{})


def append_if_not_None(lst,item):
    if type(item) != type(None):
        lst.append(item)


def k_addifnot(k,D,new_value=None):
    if k not in D:
        D[k] = new_value




def load_text_list(path,unique=False):
    try:
        lst = txt_file_to_list_of_strings(path)
        print('loaded',path)
    except:
        cE(path,'not loaded')
        lst = []
    if unique:
        lst = sorted(list(set(lst)),key=natural_keys)
    return lst


def find_images_from_paths(
    paths,
    start=opjh(),
    recursive=True,
    noisy=False,
    ignore=['Photos Library','Photo Booth','Library'],
):
    if paths == []:
        paths = select_folders(start)
    fs = []
    for p in paths:
        fs += find_files(
            start=p,
            patterns=['*.jpeg','*.jpg','*.png','*.JPG','*.JPEG','*.JPG','*.PNG'],
            ignore=ignore,
            recursive=recursive,
            noisy=noisy,
        )
    return fs





def display(f,Images={},extent=-1,selected=[],notable=[]):
    from utilz.vis import zimread,mci,cv2,resize_to_extent
    try:
        if f not in Images:
            Images[f] = 'temp'
            try:
                tmp = zimread(f)
            except:
                cE(f,'could not be loaded')
                from utilz.core.arrays import z55,rndn
                tmp = z55(rndn(300,300,3))
                return

            if extent > 0:
                #cE('resizeing')
                tmp = resize_to_extent(tmp,extent)

            Images[f] = tmp
            #print('read',f)
        
        if f in selected or f in notable:
            img = Images[f].copy()
        else:
            img = Images[f]

        if f in notable:
            img[-5:,:,:] = (100,200,100)

        if f in selected:
            img[:,:10,:] = (255,0,0)

        k = mci(img,title='rif')
        cv2.moveWindow('rif', 0, 0)
        #k = cv2.waitKey(1)
        return k
    except:
        cE('fail')


key_for = 'key for '
def handle_k(k,A):
    k = k & 0xFF
    for q in A:
        if key_for in q:
            if k == ord(A[q]):
                return q
    return 'key for: unknown'





def image_loader_thread(D={'Images':{},'done':False,'fs':[],'extent':400}):
    import keyboard
    from utilz.vis import zimread,resize_to_extent
    Images = D['Images']
    for f in D['fs']:
        if D['done']:
            return
        if f not in Images:
            tmp = zimread(f)
            #print('read',f)
            if D['extent'] > 0:
                tmp = resize_to_extent(tmp,D['extent'])
            if f not in Images:
                Images[f] = tmp
        time.sleep(0.01)
    #D['messages'] = ['loader_thread() finished']
    #cg(D['messages'])
    keyboard.press_and_release('@')











def get_sql(db_path):
    """
    Sql = get_sql(db_path)
    sql = Sql['sql']
    q = sql("select * from files")
    Sql['cursor'].execute("alter table files add column food text")
    Sql['col_names']()
    """
    import sqlite3
    #cm(db_path,sggo(db_path),r=0)
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    def sql(s,echo_query=False):
        if echo_query:
            cy(s)
        return cursor.execute(s).fetchall()
    def col_names(table):#='files'):
        cursor2 = connection.execute('select * from '+table)
        return [description[0] for description in cursor2.description]
    return {
        'sql':sql,
        'cursor':cursor,
        'col_names':col_names,
    }


def print_sql_table(query_results,column_names=[],max_col_width=10**10,row_start=0,row_end=10**10,header_interval=25):
    """
    q = sql("select * from files")
    print_sql_table(q,[],45,0)
    """
    if not query_results:
        print('no query_results')
        return
    q = list(query_results)
    if column_names:
        q.insert(0,column_names)
    rows = len(q)
    cols = len(q[0])
    maxes = []
    lines = []

    for c in range(cols):
        mx = 0
        for r in range(rows):
            #print(r,c,q[r])
            #print(r,c,len(q[r]))
            au = str(q[r][c])
            a = unescape_string(au)
            if a and len(a) > mx:
                mx = len(a)
        mx = min(max_col_width,mx)
        maxes.append(mx)
    for r in range(rows):
        rl = []
        for c in range(cols):
            s = str(q[r][c])
            if len(s) > max_col_width:
                s = s[:max_col_width-1] + cf(s[max_col_width-1],'`--r')
            s = s.replace('null','    ').replace('None','    ')
            rl.append(s + (maxes[c]-len(s))*' ')
        lines.append('    '.join(rl))
    if column_names:
        names = lines.pop(0)
    for i in range(row_start,min(row_end,len(lines))):
        if column_names and not (i-row_start) % header_interval:
            clp(names,'`--rb')
        print(lines[i])

def setup_table(db_path,table,column_definition_string):
    s = """create table """+table+" (" + column_definition_string + ')'
    import sqlite3
    os_system('rm',db_path)
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.execute(s)
    ce = cursor.execute
    connection.commit()
    Sql = get_sql(db_path) 
    cg("setup table '"+table+" with columns:")
    for p in Sql['col_names'](table):
        cb('\t',p)

def insert_data_into_table(D,db_path,table):
    import sqlite3
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    ce = cursor.execute
    for c_name in D:
        a = 'insert into '+table+' (' 
        b = '('
        a += 'c_name'
        b += qtd(c_name)
        for k in D[c_name]:
            a +=  ', ' + k
            c = D[c_name][k]
            if not is_number(c):
                c = qtd(c)
            b +=  ', ' + str(c)
        a += ')'
        b += ')'
        s = d2s(a,'values',b)
        ce(s)
    connection.commit()


def str_to_list(s):
    #return remove_empty(s.split('\n'))
    return re.findall('\s*(\S+)',s)

def get_query_results(sql,columns_str,conditions_str,table,do_print=True):
    a = conditions_str.split(' ')
    b = ' '.join(['\"%'+b.replace('`','%\"')  if '`' in b else b for b in a])
    qs = d2s(
        'select',
        columns_str,
        'from '+table+' where',
        b,
    )
    cy(qs)
    print()
    query_result = sql( qs )

    if do_print:
        print_sql_table(
            query_result,
            column_names=columns_str.split(','),
            header_interval = 2000,
        )
    return query_result





def get_table_and_col_names_dic(db_path,to_lower=False,start_char=0):
    import sqlite3
    connection = sqlite3.connect(db_path) 
    _cursor = connection.cursor()
    _cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_names = sorted( _cursor.fetchall() )
    T = {}
    for u in table_names:
        t = u[0]
        _cursor = connection.execute('select * from '+t)
        names = [description[0].lower() for description in _cursor.description]
        if to_lower:
            v = t.lower()
        else:
            v = t
        v = v[start_char:]
        T[v] = names #sorted(names)
    return T


def unixtime_to_MacTime(t):
    from datetime import datetime
    dt = datetime.fromtimestamp(t)
    tmp = datetime(2001,1,1,0,0)
    return int((dt - tmp).total_seconds()) * 1000000000


def MacTime_to_unixtime(coredata_timestamp):
    # https://www.thecodeship.com/general/converting-cocoa-unix-timestamp/
    from datetime import datetime
    from time import mktime
    coredata_start_date = datetime(2001, 1, 1, 0, 0, 0, 0, tzinfo=None)
    coredata_start_unix = int(mktime(coredata_start_date.timetuple()))
    unix_timestamp = coredata_start_unix + coredata_timestamp
    return unix_timestamp


def month_day_year_to_MacTime(m,d,y):
    import datetime
    dt = datetime.datetime(y, m, d, 0, 0)
    tmp = datetime.datetime(2001,1,1,0,0)
    return int((dt - tmp).total_seconds()) * 1000000000



def SQL_get_paths_select_str(paths=[],topics=[],rating_min=-1,rating_max=-1):
    s = []
    for n in paths:
        s.append(d2n('name like ',qtd('%'+n+'%',s=1)))
    paths_str = ' or '.join(s)
    if len(paths_str):
        paths_str = d2s('(',paths_str,')')
    s = []
    for n in topics:
        s.append(d2n(n,"='",n,"'"))
    topics_str = ' and '.join(s)
    
    jn = []
    query_list = [topics_str,paths_str]
    #cm(rating_max,rating_min)
    if rating_min >=0 and rating_max >= 0:
        rating_str = d2s("rating between",rating_min,'and',rating_max)
        query_list.append(rating_str)
    #cm(query_list)
    for j in query_list:
        if j:
            jn.append(j)
    if jn:
        where_str = d2s('where',' and '.join(jn))
    else:
        where_str = ''
    select_str = d2s( 'select * from files', where_str )
    return select_str














I2k = {
    chr(127):   '<delete>',
    chr(13):    '<enter>',
    chr(9):     '<tab>',
    chr(27):    '<escape>'
}
for o in range(ord('a'),1+ord('z')):
    if chr(o-96) not in I2k:
        I2k[chr(o-96)] = '<ctrl-'+chr(o)+'>'
for o in range(ord(' '),1+ord('z')):
    I2k[chr(o)] = chr(o)





def remove_vowels(c):
    #https://stackoverflow.com/questions/21581824/correct-code-to-remove-the-vowels-from-a-string-in-python
    vowels = ('a', 'e', 'i', 'o', 'u')
    return ''.join([l for l in c if l not in vowels]);


def get_name_from_vowel_cleared_strings(lst):
    a = []
    for l in sorted(list(set(lst))):
        b = remove_vowels(l[1:])
        a.append(l[0]+b)
    return '-'.join(a)


# sql("alter table files add sexy text")
# sql("alter table files rename sexy to ignore_sexy")
# UPDATE TABLE1 SET Answer = 'N' WHERE userID=1 AND Answer = 'Y';
def list_multiselect(E,topic,update_lines=None,title=''):

    Usage = {
        '<ctrl-c>':'quit',
        '<escape>':'return to previous level',
        '<nothing>+':'add topic',
        '<topic>-':'remove topic',
        '<tab>':'complete',
        '<enter>':'toggle topic once complete',
        '<delete>':'remove last character',
        'alpha-numerics':'add characters',
        ',':'up',
        '.':'down',
    }
    #cy(topic,topic in E)
    choices = E[topic]['topics'].copy()
    characters = []
    string_ = ''
    message = ''
    usage_closed = True
    divier_char = '='
    line_prefix = '' # '  '

    while True:
        
        if topic in ['Filters','Labels']:
            E[topic]['topics'] = E['get_valid_col_names'](E['Sql'])

        if update_lines:
            update_lines(E)
        current_screen_lines = E['current_screen_lines']
        lines = '\n'.join(current_screen_lines)
    
        choices = []
        string_ = ''.join(characters)
        for l in E[topic]['topics']:
            if len(l) >= len(string_) and l[:len(string_)] == string_:
                choices.append(l)
        choices = sorted(list(set(choices)))

        string_ = ''.join(characters)

        if not choices:
            characters.pop()
            string_ = ''.join(characters)
            beep()
            continue
        
        s_ = ''.join(characters)
        s_ = cf(s_[:],'`',' ','`--rb',s1='')



        width = get_terminal_size()[1]
        message_lines = [ title + divier_char * (width-len(title)) ]

        if message:
            message_lines += message.split('\n')
        message = ''
                    
        if len(choices) == len(E[topic]['topics']):
            q_ = 'All:'
        elif len(choices) == 1:
            q_ = 'Matched:'
        else:
            q_ = 'Filtered:'

        message_lines += [cf(q_,'`w-bu')]

        qqs = []
        for cc in choices:
            if cc in E[topic]['chosen_topics']:
                qqs.append(cf(cc,'`--rb'))
            else:
                qqs.append(cc)
        qqs_ = get_lines_without_breaks(qqs,width)

        message_lines += [line_prefix + qqs_[0]] + qqs_[1:]
        message_lines += [d2s(s_)]


        mls = current_screen_lines.copy()
        for i in rlen(current_screen_lines):
            if len(mls[i]) > width:
                #cm(0)
                mls[i] = current_screen_lines[i][:width-1]+cf(current_screen_lines[i][width-1],'`--r')


        n = min(len(message_lines),len(mls))
        #to_print = mls[:-n] + message_lines
        to_print = mls + message_lines


        clear_screen()

        print('\n'.join(to_print)) #,end='\r',flush=True)

        c = getch()

        if c not in I2k:
            beep()

        if I2k[c] == '<ctrl-c>':
            return '<ctrl-c>'

        if I2k[c] == '<escape>':
            return '<escape>'

        elif c == '-':
            if not characters:
                E[topic]['chosen_topics'].clear()
            else:
                string_ = ''.join(characters)
                if string_ in E[topic]['topics']:
                    E[topic]['topics'].remove(string_)
                    E['Sql']['sql'](d2s("alter table files rename",string_,"to",
                        d2n('ignore_',string_,'_',time_str('FileSafe') )))
                    "alter table files rename sexy to ignore_sexy"
                    if string_ in E[topic]['chosen_topics']:
                        E[topic]['chosen_topics'].remove(string_)
                    characters.clear()


        elif c == '=':
            if not characters:
                for l in E[topic]['topics']:
                    if l not in E[topic]['chosen_topics']:
                        E[topic]['chosen_topics'].append(l)


        elif I2k[c] == '<ctrl-u>':
            if not characters:
                if usage_closed:
                    message = boxed(print_dic_simple(Usage,title='Usage:',print_=False))
                    usage_closed = False
                else:
                    message = ''
                    usage_closed = True
            else:
                pass

        elif I2k[c] == '<enter>':
            if False:#not characters:
                if usage_closed:
                    message = boxed(print_dic_simple(Usage,title='Usage:',print_=False))
                    usage_closed = False
                else:
                    message = ''
                    usage_closed = True
            else:
                string_ = ''.join(characters)
                if string_ in E[topic]['topics']:
                    if string_ in E[topic]['chosen_topics']:
                        E[topic]['chosen_topics'].remove(string_)
                    else:
                        E[topic]['chosen_topics'].append(string_)
                    characters.clear()
                else:
                    beep()

        elif c == '+' and not characters:
            q = input('add topic: ')
            q_safe = get_safe_name(q)
            if q_safe != q:
                cr('warning,',qtd(q),'changed to',qtd(q_safe),r=1)
                q = q_safe
            if len(q) > 0:
                if q not in E[topic]['topics']:
                    E['Sql']['sql'](d2s("alter table files add",q,"text"))
                    E[topic]['topics'].append(q)
                    E[topic]['chosen_topics'].append(q)
                else:
                    cE(q,'already in E[\'topics\']',r=True)


        elif I2k[c] == '<ctrl-s>' and not characters:
            k = get_name_from_vowel_cleared_strings(E[topic]['chosen_topics'])
            E[topic]['Saved_chosen_topics'][k] = E[topic]['chosen_topics'].copy()
            message = cf('Saved:',k,'`g--')


        elif I2k[c] == '<ctrl-l>' and not characters:
            if len(E[topic]['Saved_chosen_topics']):
                k = select_from_list(sorted(kys(E[topic]['Saved_chosen_topics'])))
                if k in E[topic]['Saved_chosen_topics']:
                    E[topic]['chosen_topics'] = E[topic]['Saved_chosen_topics'][k].copy()
                    message = cf('Loaded:',k,'`g--')
                else:
                    message = cf('No selection made.','`r--')
            else:
                message = cf('No saved topic lists.','`r--')

        elif I2k[c] == '<ctrl-d>' and not characters:
            if len(E[topic]['Saved_chosen_topics']):
                k = select_from_list(sorted(kys(E[topic]['Saved_chosen_topics'])))
                if k in E[topic]['Saved_chosen_topics']:
                    del E[topic]['Saved_chosen_topics'][k]
                    message = cf('Deleted:',k,'`g--')
                else:
                    message = cf('No selection made.','`r--')
            else:
                message = cf('No saved topic lists.','`r--')

        elif I2k[c] == '<delete>':
            if len(characters):
                characters.pop()

        elif I2k[c] == '<tab>':
            characters = list(get_longest(string_,E[topic]['topics']))

        elif c in [',','.']:
            if c == ',':
                d = -1
            else:
                d = 1
            n = E['current_line_number']+d
            if n < 0:
                n = 0
            elif n >= len(E['current_screen_lines']):
                n = len(E['current_screen_lines']) -1
            E['current_line_number'] = n
            
        elif c == '<':
            E['current_line_number'] = 0

        elif c == '>':
            E['current_line_number'] = len(E['current_screen_lines']) -1

        elif c in [' ','x'] and topic == 'Labels':
            for k in E[topic]['chosen_topics']:
                name = E['current_screen_lines'][E['current_line_number']].split('•')[0]
                name = unescape_string(name)
                if c == ' ':
                    k1 = k
                    if E['current_line_number'] < len(E['current_screen_lines']) - 1:
                        E['current_line_number'] += 1
                else:
                    k1 = 'null'
                E['Sql']['sql'](d2s(
                    "update files set",k,"=","\'"+k1+"\' where name =",qtd(name,s=1)
                    ))

        else:
            characters.append(c)





def get_longest(string_,lst):
    F = {}
    for l in lst:
        if len(l) >= len(string_):
            if l[:len(string_)] == string_:
                for i in range(len(string_),len(l)+1):
                    if i not in F:
                        F[i] = []
                    F[i].append(l[:i])
    to_delete = []
    longest = string_
    double_break = False
    for k in sorted(F):
        F[k] = list(set(F[k]))
        longests = []
        for a in F[k]:
            if a in lst:
                longests.append(a)
        if len(longests) == 1:
            longest = longests[0]
            break
        if len(F[k]) > 1:
            break
        else:
            longest = F[k][0]

    return longest



def unescape_string(s):
    return re.sub('(\\x1b)\[[0-9]+m','',s)



def get_lines_without_breaks(word_list,width):
    lines = []
    line_words = []
    for w in word_list:
        a = unescape_string(' '.join(line_words))
        b = unescape_string(w)
        if len(a) + len(b) + len(' ') >= width:
            lines.append(' '.join(line_words))
            line_words = [w]
        else:
            line_words.append(w)
    if line_words:
        lines.append(' '.join(line_words))
    return lines


def truncate_name(s,mx=32):
    if len(s) > mx:
        a = s[:mx//2-2]
        b = s[-(mx//2-1):]
        return a+'...'+b
    else:
        return s



def get_Count(text):
    if not text:
        return 0
    c = []
    for d in text: 
        if d.isalpha(): 
            c.append(d) 
        else: 
            c.append(' ')
    e=''.join(c)
    f=e.split(' ')
    g=remove_empty(f)
    C = {}
    for h in g:
        if h not in C:
            C[h] = 1
        else:
            C[h] += 1
    return len(g)




def project_path__to__project_import_prefix(project_path):
    project_path = project_path.replace(opjh(),'')
    a = project_path.split('/')
    c = []
    for b in a:
        if len(b) > 0:
            c.append(b)
    project_import_prefix = '.'.join(c)
    return project_import_prefix

get_import_version = project_path__to__project_import_prefix



def reset_screen():
    os_system("""osascript -e 'tell application "System Events" to tell process "Terminal" to keystroke "k" using command down'""")


def write_complete_sh(path,name,Defaults):
    l = []
    use_bool = False
    for k in Defaults:
        if type(Defaults[k]) is bool:
            use_bool = True
        if len(k) == 1:
            l.append('-'+k)
        else:
            l.append('--'+k)
    if use_bool:
        l += ['True','False']
    sh = """
    # DATE
    echo "sourcing complete.sh for NAME"
    alias wine='python PATH'
    complete -o default -W "LIST" NAME
    """.replace('LIST',' '.join(l)).replace('DATE',time_str('Pretty',time.time())).replace('NAME',name).replace('PATH',path)
    text_to_file(opjk('misc/wine/complete.sh'),sh)
    
#EOF





