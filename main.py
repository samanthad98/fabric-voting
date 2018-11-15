#!/usr/bin/env python
import os
import signal
import subprocess
import sys
import time
import traceback
import pexpect

# district_num = int(sys.argv[1])
district_num = 1
# worker_num = int(sys.argv[2])
worker_num = 1
# max_threads = sys.argv[3]
max_threads = '5'
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
running_time = 500

# # Start the election store terminal
# elec_term = subprocess.Popen(['/bin/bash'], stdin = subprocess.PIPE, stdout=subprocess.PIPE)
#
# # Start the district store terminal
# district_term = [None] * district_num
# for i in range(district_num):
#     district_term[i] = subprocess.Popen(['/bin/bash'], stdin = subprocess.PIPE, stdout=subprocess.PIPE)
#
# # Start the worker terminal
# worker_term = [None] * worker_num
# for i in range(worker_num):
#     worker_term[i] = subprocess.Popen(['/bin/bash'], stdin = subprocess.PIPE, stdout=subprocess.PIPE)
#
# # Start the election store
# elec_term.stdin.write('bin/start-store election\n')
#
# # Start the district stores
# for i in range(district_num):
#     district_term[i].stdin.write('bin/start-store district' + str(i+1) +'\n')
#
# # Start the voting state
# elec_term.stdin.write('bin/init_voting_state ' + str(district_num) + '\n')
#
# # Start the workers
# for i in range(worker_num):
#     worker_term[i].stdin.write('bin/start-worker worker' + str(i+1) + '\n')
#
# # Start the voting
# voting_command = 'voting.main.Vote election 1 5 100 0.6 0.6 0 0\n'
# # + str(district_num) + ' ' + max_threads  + ' ' + avg_vote_interval + ' '+ start_bias + ' ' + end_bias + ' ' + shift_start_delay + ' ' + shift_end_delay + '\n'
# for i in range(district_num):
#     district_term[i].stdin.write(voting_command)
# for i in range(worker_num - 1):
#     worker_term[i].stdin.write(voting_command)
#
# # Start the tallying
# worker_term[worker_num - 1].stdin.write('voting.main.Tally election ' + avg_tally_interval + '\n')
#
# # After running_time, terminate the voting
# time.sleep(running_time)
# for i in range(worker_num):
#     worker_term[i].kill()
# for i in range(district_num):
#     district_term[i].kill()
# elec_term.kill()
# exit()
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
    district_term[i] = pexpect.sendline('voting.main.Vote election 1 5 100 0.6 0.6 0 0')
for i in range(worker_num - 1):
    worker_term[i].sendline('voting.main.Vote election 1 5 100 0.6 0.6 0 0')
worker_term[-1].sendline('voting.main.Tally election 100')
print('line sent!')
time.sleep(200)

# worker_term = [None] * worker_num
# for i in range(worker_num)
#     worker_term[i] = pexpect.spawn('bin/start-worker worker'+str(i+1))
for i in range(worker_num):
    worker_term[i].kill(0)
for i in range(district_num):
    district_term[i].kill(0)
elec_term.kill(0)
