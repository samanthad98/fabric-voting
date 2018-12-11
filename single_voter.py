#!/usr/bin/env python
import os
import signal
import subprocess
import sys
import time
import traceback
import pexpect

district_num = 1
running_time = 50

elec_term = pexpect.spawn('bin/start-store election')
elec_term.expect('Store started')
print('elec done!')

district_term = [None] * district_num
for i in range(district_num):
    district_term[i] = pexpect.spawn('bin/start-store district'+str(i+1))
    district_term[i].expect('Store started')

print('Done setting up term!')

setting_up = pexpect.run('bin/init-voting-state ' + str(district_num))
time.sleep(3)

for i in range(district_num):
    district_term[i].sendline('voting.main.Vote election ' + str(i+1) + ' 0 3 0.6 0.6 0 0')

time.sleep(running_time)

for i in range(district_num):
    district_term[i].kill(0)
elec_term.kill(0)
