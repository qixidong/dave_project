#!/usr/bin/python3.4

import logging
import time
import re
import os
import sys
import argparse
from netmiko import ConnectHandler

def banner():
    print('#==========================================================#')



def flapLinksAndMeasure(hdl, iterations):
    # shut case
    linkup_max_time = 1
    linkup_min_time = 1
    linkup_total_time = 0

    for i in range(1, iterations+1 ):
        banner()
        print('Iteration = {0}'.format(i))
        linkup_time = 1
        banner()
        hdl.execute('ifconfig ionic0 down')
#        hdl.execute('ifconfig ionic1 down')
        time.sleep(3)
        hdl.execute('ifconfig ionic0 up')
#        hdl.execute('ifconfig ionic1 up')
        ionic_up_flag=False 

        count = 1
        while ionic_up_flag is False and count < 50:
              ionic0_status = hdl.execute('ifconfig ionic0')
#              ionic1_status = hdl.execute('ifconfig ionic1')
              count = count + 1
#              if not re.search('status: active', ionic0_status ) or not re.search('status: active', ionic1_status):
              if not re.search('status: active', ionic0_status ):
                 time.sleep(0.99)
                 linkup_time = linkup_time + 1
              else:
                 ionic_up_flag=True
        if count > 30:
           print('Link did not come up even after 30 secs .. Aborting !!!')
           print(ionic0_status)
#           print(ionic1_status)
#           print('Link did not come up even after 50 secs .. Aborting !!!')
           sys.exit(1)

        if linkup_max_time < linkup_time:
           linkup_max_time = linkup_time
        if linkup_time < linkup_min_time:
           linkup_min_time = linkup_time
        linkup_total_time = linkup_total_time + linkup_time

        banner()
        print('Iteration = {0}, linkup_time = {1}'.format(i, linkup_time))
        print('Iteration = {0}, linkup_min_time = {1}'.format(i, linkup_min_time))
        print('Iteration = {0}, linkup_max_time = {1}'.format(i, linkup_max_time))
        banner()
        time.sleep(10)

    linkup_avg_time = linkup_total_time/iterations
    return (linkup_max_time,linkup_min_time,linkup_avg_time)



# main()
if __name__ == '__main__':

   parser = argparse.ArgumentParser(description = "link flapper" )
   parser.add_argument('--mgmt_ip', dest = 'mgmt_ip', required=True )
   parser.add_argument('--username', dest = 'username', default='root')
   parser.add_argument('--password', dest = 'password', default='docker')
   parser.add_argument('--iterations', dest = 'iterations', default=100 )

   args, sys.argv[1:] = parser.parse_known_args(sys.argv[1:])

   hdl = ConnectHandler( device_type='linux', ip=args.mgmt_ip, \
         username=args.username, password=args.password, blocking_timeout=500 )


   (linkup_max_time,linkup_min_time,linkup_avg_time) = flapLinksAndMeasure( hdl, int(args.iterations) )
   print("\n\n")
   banner()
   print('Test completed {0} iterations !!!!!!!!!!'.format(args.iterations))
   print('Maximum link up time = {0} secs'.format(linkup_max_time))
   print('Minimum link up time = {0} secs'.format(linkup_min_time))
   print('Avg link up time = {0} secs'.format(linkup_avg_time))
   banner()
