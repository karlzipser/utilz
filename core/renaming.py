from utilz.core.essentials import *

host_name = socket.gethostname()
home_path = os.path.expanduser("~")
username = getpass.getuser()

sleep = time.sleep
sys = os.sys
gg = glob.glob


    
if __name__ == '__main__':
    eg(__file__)
    print('home_path =',home_path)
    print('username =',username)
    print('host_name =',host_name)

#EOF
