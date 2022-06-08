import csv
import matplotlib.pyplot as plt

def draw_result():
    f = open('cls_4_ALL_count.csv', 'r')
    rdr = csv.reader(f)
    count_dic = {'A': 0, 'B': 0, 'D': 0, 'E': 0}
    total_dic = {'A': 0, 'B': 0, 'D': 0, 'E': 0}

    a_thre = 18
    b_thre = 4
    e_thre = 4
    for line in rdr:
        if line[1] == 'A':
            if int(line[3]) > a_thre and int(line[4]) <= e_thre and int(line[-1]) <= b_thre:
                count_dic['A'] += 1
            total_dic['A'] += 1

        if line[1] == 'B':
            if int(line[3]) <= a_thre and int(line[4]) <= e_thre and int(line[-1]) > b_thre:
                count_dic['B'] += 1
            total_dic['B'] += 1

        if line[1] == 'D':
            if int(line[3]) <= a_thre and int(line[4]) <= e_thre and int(line[-1]) <= b_thre:
                count_dic['D'] += 1
            total_dic['D'] += 1

        elif line[1] == 'E':
            if int(line[3]) <= a_thre and int(line[4]) > e_thre and int(line[-1]) <= b_thre:
                count_dic['E'] += 1
            total_dic['E'] += 1

    f.close()

    acc = [round(count_dic['A'] / total_dic['A'], 3), round(count_dic['B'] / total_dic['B'], 3), round(count_dic['D'] / total_dic['D'], 3), round(count_dic['E'] / total_dic['E'], 3)]
    print(acc)
    print(round(sum(acc)/len(acc), 3))
    print(total_dic)

# line[0]: file name
# line[1]: file label
# line[2]: cut
# line[3]: process
# line[4]: wire
# line[5]: f_process

def main():
    cls = 'A'
    a_acc = []
    b_acc = []
    d_acc = []
    e_acc = []
    threshold = range(0,20,2)

    for limit in threshold:
        f = open('cls_4_ALL_count.csv', 'r')
        rdr = csv.reader(f)
        count_dic = {'A': 0, 'B': 0, 'D': 0, 'E': 0}
        total_dic = {'A': 0, 'B': 0, 'D': 0, 'E': 0}
        for line in rdr:
            label = line[1]
            total_dic[label] += 1
            if line[1] != cls:
                if int(line[4]) <= limit:
                    count_dic[label] += 1
            else:
                if int(line[4]) > limit:
                    count_dic[label] += 1

        a_acc.append(round(count_dic['A'] / total_dic['A'], 3))
        b_acc.append(round(count_dic['B'] / total_dic['B'], 3))
        d_acc.append(round(count_dic['D'] / total_dic['D'], 3))
        e_acc.append(round(count_dic['E'] / total_dic['E'], 3))

        f.close()

    avg = []
    for i in range(len(a_acc)):
        total = sum([a_acc[i], b_acc[i], d_acc[i], e_acc[i]])
        avg_acc = round(total/4, 3)
        avg.append(avg_acc)

    print(avg.index(max(avg)))
    plt.plot(threshold, avg, label='AVG_Acc')

    # plt.plot(threshold, a_acc, label='B_Class')
    # plt.plot(threshold, b_acc, label='B_Class')
    # plt.plot(threshold, d_acc, label='D_Class')
    # plt.plot(threshold, e_acc, label='E_Class')

    # plt.plot(threshold, b_acc, label='B_Class')
    # plt.plot(threshold, d_acc, label='D_Class')

    plt.xlabel('Threshold')
    plt.ylabel('Accuracy')
    plt.legend(loc='best', ncol=4)

    plt.show()


draw_result()
# main()