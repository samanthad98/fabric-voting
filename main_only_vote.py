#!/usr/bin/env python
import os
import signal
import subprocess
import sys
import time
import traceback
import pexpect

# district_num = int(sys.argv[1])
district_num = 2
# worker_num = int(sys.argv[2])
worker_num = 6
# max_threads = sys.argv[3]
max_threads = '0'
# avg_vote_interval = sys.argv[4]
avg_vote_interval = '100'
# start_bias = sys.argv[5]
start_bias = '0.6'
# end_bias = sys.argv[6]
end_bias = '0.6'
# shift_start_delay = sys.argv[7]
shift_start_delay = '0'
# shift_end_delay = sys.argv[8]
shift_end_delay = '0'
# avg_tally_interval = sys.argv[9]
avg_tally_interval = '100'
# running_time = int(sys.argv[10])
running_time = 150

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

# Start worker terms
worker_term = [None] * worker_num
for i in range(worker_num):
    worker_term[i] = pexpect.spawn('bin/start-worker worker'+str(i+1))
    worker_term[i].expect('Worker started')
print('Done setting up worker')

for i in range(district_num):
    district_term[i].sendline('voting.main.Vote election ' + str(i+1) + ' 0 5 0.6 0.6 0 0')
for i in range(worker_num):
    worker_term[i].sendline('voting.main.Vote election ' + str(i/3+1)  + ' 0 5 0.6 0.6 0 0')
print('line sent!')
time.sleep(running_time)

# worker_term = [None] * worker_num
# for i in range(worker_num)
#     worker_term[i] = pexpect.spawn('bin/start-worker worker'+str(i+1))
for i in range(worker_num):
    worker_term[i].kill(0)
for i in range(district_num):
    district_term[i].kill(0)
elec_term.kill(0)
