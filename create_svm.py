# This file is for creating the SVM that will be used in cervical_main.py
import cervical as cer
import helpers as helps
import json
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
from sklearn import svm, datasets


def main():

    # 1. Read in params data
    param1 = cer.read_jsonfile('svm_param1.txt')
    param2 = cer.read_jsonfile('svm_param2.txt')

    # 2. Reorganize data
    color = 'blue'
    stat = 'mean'
    x1 = param1['healthy']
    x2 = param1['dysplasia']
    x = x1+x2
    y1 = [0] * len(param1['healthy'])
    y2 = [0] * len(param1['dysplasia'])
    for i in range(0, len(param1['healthy'])):
        y1[i] = param2['healthy'][i][str(i)][color][stat]

    for i in range(0, len(param1['dysplasia'])):
        y2[i] = param2['dysplasia'][i][str(i)][color][stat]

    y = y1 + y2

    # 3. Find SVM
    output = cer.rearrange_svm(x1, x2, y1, y2)
    X = output['X']
    Y = output['Y']

    clf = cer.find_svm(X, Y)

    # 4. Plot SVM
    w = clf.coef_[0]
    m = -w[0] / w[1]
    xx = np.linspace(0, 0.1, 10)
    yy = m * xx - clf.intercept_[0] / w[1]

    fig1 = plt.scatter(x[0:len(x1)], y1, color='red')
    fig1 = plt.scatter(x[len(x1):], y2, color='blue')
    fig1 = plt.plot(xx, yy, 'k-')
    plt.xlabel('Critical Pixel Density')
    plt.ylabel('Blue Channel Mean')
    plt.title('SVM Classification of healthy and dysplasia cervix')
    filename = color+'-'+stat
    plt.savefig(filename, bbox_inches='tight')
    plt.show(fig1)

    # 5. Save SVM Model
    cer.save_svm_model(clf, 'svm_model.pkl')


if __name__ == "__main__":
    main()
