from utilz.core.printing import *

class Timer:
    def __init__(self, time_s=0):
        self.time_s = time_s
        self.start_time = time.time()
        self.count = 0
    def check(self):
        if time.time() - self.start_time > self.time_s:
            return True
        else:
            return False
    def rcheck(self):
        if self.check():#time.time() - self.start_time > self.time_s:
            self.reset()
            return True
        else:
            return False
    def time(self):
        return time.time() - self.start_time
    def reset(self):
        self.start_time = time.time()
        self.count = 0
    def trigger(self):
        self.start_time = 0
    def freq(self,name='',do_print=True):
        self.count += 1
        if self.check():
            value = self.count/self.time()
            if do_print:
                pd2s(name,'frequency =',dp(value,2),'Hz')
            self.reset()
            return value
        return False
    def message(self,message_str,color='grey',end='\r',flush=True):
        if self.check():
            print(message_str,end=end,flush=flush),
            #sys.stdout.flush()
            self.reset()
    def percent_message(self,i,i_max,flush=False):
        self.message(d2s(i,int(100*i/(1.0*i_max)),'%'),color='white')
    def wait(self):
        while not(self.check()):
            time.sleep(self.time_s/100.0)
        self.reset()   



second = 1.0
seconds = second
minute = 60*seconds
minutes = minute
hour = 60*minutes
hours = hour
day = 24*hours
days = day

"""

%a - abbreviated weekday name
%A - full weekday name
%b - abbreviated month name
%B - full month name
%c - preferred date and time representation
%C - century number (the year divided by 100, range 00 to 99)
%d - day of the month (01 to 31)
%D - same as %m/%d/%y
%e - day of the month (1 to 31)
%g - like %G, but without the century
%G - 4-digit year corresponding to the ISO week number (see %V).
%h - same as %b
%H - hour, using a 24-hour clock (00 to 23)
%I - hour, using a 12-hour clock (01 to 12)
%j - day of the year (001 to 366)
%m - month (01 to 12)
%M - minute
%n - newline character
%p - either am or pm according to the given time value
%r - time in a.m. and p.m. notation
%R - time in 24 hour notation
%S - second
%t - tab character
%T - current time, equal to %H:%M:%S
%u - weekday as a number (1 to 7), Monday=1. Warning: In Sun Solaris Sunday=1
%U - week number of the current year, starting with the first Sunday as the first day of the first week
%V - The ISO 8601 week number of the current year (01 to 53), where week 1 is the first week that has at least 4 days in the current year, and with Monday as the first day of the week
%W - week number of the current year, starting with the first Monday as the first day of the first week
%w - day of the week as a decimal, Sunday=0
%x - preferred date representation without the time
%X - preferred time representation without the date
%y - year without a century (range 00 to 99)
%Y - year including the century
%Z or %z - time zone or name or abbreviation
%% - a literal % character


"""


def time_str(mode='FileSafe',t=0):
    """
    modes are:
    FileSafe, Pretty, Pretty2, TimeShort
    """
    import datetime
    if not t:
        now = datetime.datetime.now()
    else:
        now = datetime.datetime.fromtimestamp(t)
    if mode=='FileSafe':
       return now.strftime('%d%b%y_%Hh%Mm%Ss')

    if mode=='Pretty':

       return now.strftime('%A, %d %b %Y, %r')

    if mode=='Pretty24':

       return now.strftime('%A, %d %b %Y, %R')

    if mode=='Pretty2':
       s = now.strftime('%A, %d %B %Y, %I:%M %p')
       s = s.replace('AM','a.m.')
       s = s.replace('PM','p.m.')
       s = s.replace(', 0',', ')
       return s

    if mode=='TimeShort':

       return now.strftime('%H:%M')

    assert False


def format_seconds(time):
    day = time // (24 * 3600)
    time = time % (24 * 3600)
    hour = time // 3600
    time %= 3600
    minutes = time // 60
    time %= 60
    seconds = time
    return "%d:%d:%d:%d" % (day, hour, minutes, seconds)


def date_to_timestamp(
    s,
    formats=[
        "%m/%d/%Y %H:%M",
        "%m/%d/%Y %H-%M",
        "%m/%d/%Y %H;%M",
        "%m/%d/%Y",
        "%m/%Y",
        "%m-%d-%Y %H:%M",
        "%m-%d-%Y %H-%M",
        "%m-%d-%Y %H;%M",
        "%m-%d-%Y",
        "%m-%Y",
        "%Y",
    ]):
    #https://stackoverflow.com/questions/9637838/convert-string-date-to-timestamp-in-python
    import time
    import datetime
    for format in formats:
        try:
            return time.mktime(datetime.datetime.strptime(s, format).timetuple())
        except:
            pass
    return None


if __name__ == '__main__':
    eg(__file__)
    t = 2
    pd2s('Setting timer for',t,'second:')
    timer = Timer(t)
    while not timer.check():
        print(timer.check())
        sleep(0.333)
    print(timer.check())
    t = 5731
    pd2s('format',t,'seconds:',format_seconds(t))
    pd2s('current, file safe:',time_str())
    pd2s('current, nice looking:',time_str('Pretty2',t=time.time()))

#EOF
