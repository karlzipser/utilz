
from utilz import *


import sys, select
TIMEOUT = 10
i, o, e = select.select([sys.stdin], [], [], TIMEOUT)
if i:
    print("Você digitou: ", sys.stdin.readline().strip())
else:
    os_system("""osascript -e 'tell application "System Events" to tell process "Terminal" to keystroke "k" using command down'""")
    print('Você não digitou nada :(')



if False:
    print('here:\n')
    a = getch()
    print(a,end='')
    b = input()
    c = a+b
    print(c)
    os_system("""osascript -e 'tell application "System Events" to tell process "Terminal" to keystroke "k" using command down'""")



if False:
    import signal
    TIMEOUT = 5 # number of seconds your want for timeout

    def interrupted(signum, frame):
        "called when read times out"
        print('interrupted!')
    signal.signal(signal.SIGALRM, interrupted)

    def input2():
        try:
                print('You have 5 seconds to type in your stuff...')
                foo = input()
                return foo
        except:
                # timeout
                return

    # set alarm
    signal.alarm(TIMEOUT)
    s = input2()
    # disable the alarm after success
    signal.alarm(0)
    print('You typed', s)












"""
timed password lockout
replace selected names with codenames, or crossed-out characters that
    be toggled with password
have different safety modes
show/hide emojis
replace screen with other text also on quite/error
password locking
"""
None
#EOF