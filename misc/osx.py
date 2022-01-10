from utilz.misc.sys import *


def quit_Preview():
    os_system(""" osascript -e 'quit app "Preview"' """)
    return

def close_Finder_windows():
    os_system(""" osascript -e 'tell application "Finder" to close every window' """)
    return

def quit_Application(app):
    s = """ osascript -e 'quit app "APPLICATION"' """.replace("APPLICATION",app)
    os_system(s)
    return
   
#EOF
