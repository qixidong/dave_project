#!/usr/bin/env python3.6
import pexpect
import sys
import time
ip = sys.argv[1]
username = sys.argv[2]
password = sys.argv[3]

expect_list = ['continue connecting \(yes\/no\)\? $', 'Password: $', 'Password for', 'password: $',pexpect.EOF,pexpect.TIMEOUT]
hdl = pexpect.spawn('ssh %s@%s'%(username,ip))
for i in range(5):
    i = hdl.expect(expect_list, timeout = 5)
    if i == 0:
        hdl.sendline('yes')
        continue
    if i == 1 or i == 2 or i ==3:
        time.sleep(0.5)
        hdl.sendline(password)
        break
    if i == 4 or i == 5:
        sys.exit("target device seems unavailable right now")
hdl.setwinsize(40,200)
#print(hdl.getwinsize())
hdl.interact()
