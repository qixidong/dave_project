#!/usr/local/bin/python
import os
import re
import time
import sys
import pdb
import subprocess
for i in range(104,9001,10):
    print("starting iperf with packet size %s"%i)
    os.system("iperf3 -c 100.0.0.2 -l %s -t 5 > /tmp/iperf_current_run_log"%i)
    output = subprocess.run(['cat', '/tmp/iperf_current_run_log'], stdout=subprocess.PIPE)
    output=output.stdout.decode('utf-8')
    print(output)
#    output = os.system("cat /tmp/iperf_current_run_log")
#    pdb.set_trace()
    match=re.search('[G|M]Bytes\s+([0-9\.]+) ([G|M])bits\/sec\s+receiver',output)
    if match:
        bw_num = float(match.group(1))
        bw_speed = match.group(2)
    else:
        print("couldn't identify the iperf result ")
        sys.exit(1)
    if bw_speed == "M":
        if bw_num < 200:
            print ("iperf result is below 200 Mbits/sec ")
            sys.exit(1)
        else:
            print ("iperf with packet size %s passed"%i)
            print (" ")
    elif bw_speed == "G":
        if bw_num < 1:
            print ("iperf result is below 1 Gbits/sec ")
            sys.exit(1)
        else:
            print ("iperf with packet size %s passed"%i)
            print (" ")
    os.system('echo "start iperf3 packet size %s" >> /tmp/iperf_total_log'%i)
    os.system('echo "############################" >> /tmp/iperf_total_log')
    os.system('cat /tmp/iperf_current_run_log >> /tmp/iperf_total_log')
    os.system('echo "" >> /tmp/iperf_total_log')
