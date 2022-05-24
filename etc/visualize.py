import csv
import matplotlib.pyplot as plt

threshold = []
A_acc = []
D_acc = []
for thr in range(0, 20, 2):
    f = open('all_count2.csv', 'r')
    rdr = csv.reader(f)
    threshold.append(thr)

    count_dic = {'A': 0, 'D': 0}
    total_dic = {'A': 0, 'D': 0}
    for line in rdr:
        if line[1] == 'A':
            if int(line[-1]) > thr:
                count_dic['A'] += 1
            total_dic['A'] += 1
        elif line[1] == 'D':
            if int(line[-1]) <= thr:
                count_dic['D'] += 1
            total_dic['D'] += 1

    A_acc.append(round(count_dic['A'] / total_dic['A'], 3))
    D_acc.append(round(count_dic['D'] / total_dic['D'], 3))

    f.close()


plt.plot(threshold, A_acc, label='A_Class')
plt.plot(threshold, D_acc, label='D_Class')
plt.xlabel('Threshold')
plt.ylabel('Accuracy')
plt.legend(loc='best', ncol=2)

plt.show()

