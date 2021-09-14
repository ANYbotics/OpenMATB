import matplotlib.pyplot as plt
from datetime import datetime

LOG_FILE = 'plant_20210914_1007.log'

with open(LOG_FILE, 'r') as f:
    tankA_level = []
    tankA_time = []

    tankB_level = []
    tankB_time = []

    user_time = []
    event_time = []
    pause_time = []

    tolerance = 0
    participant = 0

    for line in f:
        split_string = line.split("\t")

        if 'PARTID' in split_string:
            participant = split_string[-1][:-1]

        if 'TOLERANCE' in split_string:
            tolerance = int(split_string[-1][:-1])

        if 'TANKA' in split_string:
            tankA_time.append(datetime.strptime(split_string[0], "%H:%M:%S"))
            tankA_level.append(split_string[-1][:-1])

        if 'TANKB' in split_string:
            tankB_time.append(datetime.strptime(split_string[0], "%H:%M:%S"))
            tankB_level.append(split_string[-1][:-1])

        if 'INPUT' in split_string and 'MAIN' in split_string:
            user_time.append(datetime.strptime(split_string[0], "%H:%M:%S"))

        if 'FAIL\n' in split_string:
            event_time.append(datetime.strptime(split_string[0], "%H:%M:%S"))

        if 'PAUSE\n' in split_string:
            pause_time.append(datetime.strptime(split_string[0], "%H:%M:%S"))

        if 'RESUME\n' in split_string:
            pause_time.append(datetime.strptime(split_string[0], "%H:%M:%S"))

combined = [(abs(int(a) - 2500) + abs(int(b) - 2500)) // 2 for a, b in zip(tankA_level, tankB_level)]
plt.plot(tankA_time, combined, label='Combined Tanks')
for xc in user_time:
    plt.axvline(x=xc, color='g', linestyle='dotted', label='User Input')
for xc in event_time:
    plt.axvline(x=xc, color='r', linestyle='dashdot', label='Tank Failure')
for xi in range(0, len(pause_time), 2):
    plt.axvspan(pause_time[xi], pause_time[xi+1], color=(0.1, 0.2, 0.5, 0.3), linestyle='solid', label='Pause')
plt.axhline(y=tolerance, color='b', linestyle='dashed', label='Critical Tolerance')
# Add title and axis names
plt.title('Participant ' + participant + ': ' + LOG_FILE)
plt.xlabel('Time')
plt.ylabel('Tank Level Δ')
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys(), loc=1)
plt.xlim([tankA_time[0], tankA_time[-1]])
plt.show()
