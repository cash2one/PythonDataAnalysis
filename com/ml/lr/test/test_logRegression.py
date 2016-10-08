# -*- coding: UTF-8 -*-
__author__ = 'Zealot'

#################################################
# logRegression: Logistic Regression
# Author : zouxy
# Date   : 2014-03-02
# HomePage : http://blog.csdn.net/zouxy09
# Email  : zouxy09@qq.com
#################################################


from logRegression import *


def load_data():
    train_x = []
    train_y = []
    file_in = open('../testSet.txt')
    for line in file_in.readlines():
        line_arr = line.strip().split()
        #常数项，第一列，第二列
        line = [1.0, float(line_arr[0]), float(line_arr[1])]
        train_x.append(line)
        train_y.append(float(line_arr[2]))
    return mat(train_x), mat(train_y).transpose()

if __name__ == '__main__':
    ## step 1: load data
    print "step 1: load data..."
    train_x, train_y = load_data()
    test_x = train_x
    test_y = train_y

    ## step 2: training...
    print "step 2: training..."
    #gradDescent           [[ 4.44850596]] [[ 1.49976379]] [[-0.06731028]]
    #stocGradDescent       [[ 2.79836526]] [[ 0.3850335]] [[-0.50730461]]
    #smoothStocGradDescent [[ 11.07202326]] [[ 0.80520534]] [[-1.57937794]]
    opts = {'alpha': 0.01, 'maxIter': 20, 'optimizeType': 'gradDescent'}
    optimalWeights = train_log_regres(train_x, train_y, opts)

    ## step 3: testing
    print "step 3: testing..."
    accuracy = test_log_regres(optimalWeights, test_x, test_y)

    ## step 4: show the result
    print "step 4: show the result..."
    print 'The classify accuracy is: %.3f%%' % (accuracy * 100)
    print optimalWeights[0],optimalWeights[1],optimalWeights[2]
    showLogRegres(optimalWeights, train_x, train_y)