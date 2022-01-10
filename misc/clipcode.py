from utilz.misc.printing import *
from utilz.misc.have_using import *
import subprocess

def get_code_snippet_(code_file=None,start='#,a',stop='#,b'):
    if code_file is None:
        code_file = most_recent_py_file()
    code_lst = txt_file_to_list_of_strings(code_file)
    snippet_lst = []
    started = False
    for c in code_lst:
        if not started and c == start:
            started = True
        if started and c == stop:
            break
        if started:
            snippet_lst.append(c)
    code_str = '\n'.join(snippet_lst)
    return code_str
gcsp = get_code_snippet_


def most_recent_py_file(path=opjk(),return_mtime=False):
    max_mtime = 0
    for dirname,subdirs,files in os.walk(path):
        for fname in files:
            if len(fname) >= 3:
                if fname[-3:] == '.py':
                    full_path = os.path.join(dirname,fname)
                    mtime = os.stat(full_path).st_mtime
                    if mtime > max_mtime:
                        max_mtime = mtime
                        max_dir = dirname
                        max_file = fname
    if return_mtime:
        return opj(max_dir,max_file),max_mtime
    else:
        return opj(max_dir,max_file)


def getClipboardData():
    p = subprocess.Popen(['pbpaste'], stdout=subprocess.PIPE)
    retcode = p.wait()
    data = p.stdout.read()
    if type(data) != str:
        data = data.decode("utf-8")
    return data
gcd = getClipboardData

def setClipboardData(data):
    """
    setClipboardData
    """
    p = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
    try:
        p.stdin.write(data)
    except:
        p.stdin.write(bytes(data,'utf-8'))
    p.stdin.close()
    retcode = p.wait()
scd = setClipboardData

_delimiter = '\n<====>\n'   

def load_clipboards(dst_,delimiter_=_delimiter):
    try:
        clipboards = file_to_text(dst_).split(delimiter_)
    except:
        clipboards = []
    return clipboards


def save_clipboards(clipboard_data,clipboards,dst_,delimiter_=_delimiter,n_=20,verbose=True):
    c = clipboard_data
    if len(clipboards) == 0 or c != clipboards[-1]:
        if c in clipboards:
            clipboards.remove(c)
        clipboards.append(c)
        if len(clipboards) > n_:
            clipboards = clipboards[-n_:]
        text_to_file(dst_,delimiter_.join(clipboards))
        if verbose:
            print('wrote to',dst_)


def access_clipboards(dst_,set_clipboard=True,as_menu=True,delimiter_=_delimiter,shorten=False):
    try:
        while True:

            try:
                clipboards = file_to_text(dst_).split(delimiter_)
            except:
                clipboards = []
            while None in clipboards:
                clipboards.remove(None)
            while '' in clipboards:
                clipboards.remove('')

            clear_screen()

            for i in rlen(clipboards):
                c = clipboards[i]
                if shorten:
                    c = c.replace('\n',' ')
                    c = c.replace('\t',' ')
                    if len(c) > 60:
                        c = c[:60] + '...'

                clp(str(i)+')','`w-b',c,'`y')
                
            j = input_int_in_range(0,len(clipboards),'choice > ')
            if j == '<quit>':
                break
            if j is not None:
                if set_clipboard:
                    setClipboardData(clipboards[j])
                if not as_menu:
                    return clipboards[j].split('\n')

    except KeyboardInterrupt:
        cw('\n\n*** KeyboardInterrupt, done ***\n')
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        cE(exc_type,file_name,exc_tb.tb_lineno) 


if __name__ == '__main__':
    


    code = """
clear_screen()
if '__file__' in locals(): eg(__file__)
clp('most_recent_py_file:', most_recent_py_file())
print('')
c = getClipboardData()
print("getClipboardData()")
print('')
clp(c,'`m--')
    """
    for c in code.split('\n'):
        if not c.isspace():
            clp(c,'`--u')
            exec(c)

#EOF
