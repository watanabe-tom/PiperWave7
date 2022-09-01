#!/usr/bin/env python3

import ADC0832
import time
import datetime
import subprocess

flag = 0
time_start = 0.0
time_end = 0.0

def init():
    ADC0832.setup()

def line_notify(a):
    global flag
    global time_start
    global time_end

    if flag == 0:
       if a == 1:
           time_start = time.time()
           date_start = str(datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S'))
           subprocess.run(["bash", "notify_evening.sh", date_start])
           flag = 1
    else:
       if a == 0:
           time_end = time.time()
           date_end = str(datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S'))
           subprocess.run(["bash", "notify_morning.sh", date_end, str(int(time_end - time_start))])
           flag = 0

    return 0

def loop():
    while True:
        #The ADC0832 has two channels
        #res = ADC0832.getResult()   <-- It reads channel 0 by default. Equivalent to getResult(0)
        #res = ADC0832.getResult(1)  <-- Use this to read the second channel

        res = ADC0832.getResult() - 80
        if res < 0:
            res = 0
            line_notify(1)
        if res > 100:
            res = 100
            line_notify(0)
        print ('res = %d' % res)
        time.sleep(2)

def main():
    init()
    try:
        loop()
    except KeyboardInterrupt:
        ADC0832.destroy()
        print ('Cleanup ADC!')

if __name__ == '__main__':
    main()
