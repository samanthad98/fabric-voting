#!/usr/bin/env python
import os
import signal
import subprocess
import sys
import time
import traceback

district_num = int(sys.argv[1])
worker_num = int(sys.argv[2])
max_threads = sys.argv[3]
avg_vote_interval = sys.argv[4]
start_bias = sys.argv[5]
end_bias = sys.argv[6]
shift_start_delay = sys.argv[7]
shift_end_delay = sys.argv[8]
avg_tally_interval = sys.argv[9]
running_time = int(sys.argv[10])

# Start the election store terminal
elec_term = subprocess.Popen(['/bin/bash'], stdin = subprocess.PIPE, stdout=subprocess.PIPE)

# Start the district store terminal
district_term = [None] * district_num
for i in range(district_num):
    district_term[i] = subprocess.Popen(['/bin/bash'], stdin = subprocess.PIPE, stdout=subprocess.PIPE)

# Start the worker terminal
worker_term = [None] * worker_num
for i in range(worker_num):
    worker_term[i] = subprocess.Popen(['/bin/bash'], stdin = subprocess.PIPE, stdout=subprocess.PIPE)

# Start the election store
elec_term.stdin.write('bin/start-store election\n')

# Start the district stores
for i in range(district_num):
    district_term[i].stdin.write('bin/start-store district' + str(i) +'\n')

# Start the voting state
elec_term.stdin.write('bin/init_voting_state' + str(district_term) + '\n')

# Start the workers
for i in range(worker_num):
    worker_term[i].stdin.write('bin/start-worker worker' + str(i) + '\n')

# Start the voting
voting_command = 'voting.main.Vote election ' + str(district_num) + ' '
                                              + max_threads  + ' '
                                              + avg_vote_interval + ' '
                                              + start_bias + ' '
                                              + end_bias + ' '
                                              + shift_start_delay + ' '
                                              + shift_end_delay + '\n'
for i in range(district_num):
    district_term[i].stdin.write(voting_command)
for i in range(worker_num - 1):
    worker_term[i].stdin.write(voting_command)

# Start the tallying
worker_term[worker_num - 1].write('voting.main.Tally election ' + avg_tally_interval + '\n')

# After running_time, terminate the voting
time.sleep(running_time)
for i in range(worker_num):
    worker_term[i].kill()
for i in range(district_num):
    district_term[i].kill()
elec_term.kill()
exit()
