import numpy as np
import matplotlib.pyplot as plt
import csv
DATA_PATH = sys.argv[1]

# import data from file
reader = csv.reader(open(DATA_PATH, 'r'), delimiter=' ')
data = np.array(list(reader)).astype('float')

# Draw the histogram of backofftime
data = data[:,1]
values, base = np.histogram(data, bins = (np.max(data) - np.min(data))/0.1)
cumulative = np.cumsum(values)
plt.plot(base[:-1], cumulative, c='blue')

plt.show()
