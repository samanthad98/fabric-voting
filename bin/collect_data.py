import os
import sys
import time
import os.path
import csv
import re
LOG_ORIGIN = sys.argv[1]
DATA_PATH = sys.argv[2]
TRIAL_NUM = sys.argv[3]

if not os.path.isdir(DATA_PATH):
    os.mkdir(DATA_PATH)

with open(LOG_ORIGIN, "r") as f:
    lines = f.readlines()
    f.close()

with open(DATA_PATH + '/output' + str(TRIAL_NUM) + '.csv', 'w') as f:
    writer = csv.writer(f, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for line in lines:
        attempts = re.search(r'\s[0-9]*\sTXN\sATTEMPTS', line).group(0)
        attempts = attempts[1:-13]
        backofftime = re.search(r'BACKOFFTIME:\s[0-9]*\s').group(0)
        backofftime = backofftime[13:-1]
        writer.writerow([attempts, backofftime])
    f.close()
