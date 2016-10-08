# -*- coding: UTF-8 -*-
__author__ = 'Zealot'
#################################################
# logRegression: Logistic Regression
# Author : zouxy
# Date   : 2014-03-02
# HomePage : http://blog.csdn.net/zouxy09
# Email  : zouxy09@qq.com
#################################################

from numpy import *
import matplotlib.pyplot as plt
import time


# calculate the sigmoid function
def sigmoid(inX):
    return 1.0 / (1 + exp(-inX))


# train a logistic regression model using some optional optimize algorithm
# input: train_x is a mat datatype, each row stands for one sample
#		 train_y is mat datatype too, each row is the corresponding label
#		 opts is optimize option include step and maximum number of iterations
def train_log_regres(train_x, train_y, opts):
    # calculate training time
    start_time = time.time()

    num_samples, num_features = shape(train_x)
    alpha = opts['alpha']
    max_iter = opts['maxIter']
    weights = ones((num_features, 1))

    # optimize through gradient descent algorilthm
    for k in range(max_iter):
        if opts['optimizeType'] == 'gradDescent': # gradient descent algorilthm
            w_x = train_x * weights#用所有的样本更新权重（train_x为所有样本），得到y值
            temp = mat(weights).transpose() * train_x.transpose()
            # print len(temp)
            # print temp.transpose()==w_x
            output = sigmoid(w_x)#计算logit函数，归一化到0~1之间
            error = train_y - output#y-wx
            weights += alpha * train_x.transpose() * error#(y-wx)x
        elif opts['optimizeType'] == 'stocGradDescent': # stochastic gradient descent
            for i in range(num_samples):
                output = sigmoid(train_x[i, :] * weights)
                error = train_y[i, 0] - output
                weights += alpha * train_x[i, :].transpose() * error
        elif opts['optimizeType'] == 'smoothStocGradDescent': # smooth stochastic gradient descent
            # randomly select samples to optimize for reducing cycle fluctuations
            data_index = range(num_samples)
            for i in range(num_samples):
                alpha = 4.0 / (1.0 + k + i) + 0.01
                randIndex = int(random.uniform(0, len(data_index)))
                output = sigmoid(train_x[randIndex, :] * weights)
                error = train_y[randIndex, 0] - output
                weights += alpha * train_x[randIndex, :].transpose() * error
                del(data_index[randIndex]) # during one interation, delete the optimized sample
        else:
            raise NameError('Not support optimize method type!')

    print 'Congratulations, training complete! Took %fs!' % (time.time() - start_time)
    return weights


# test your trained Logistic Regression model given test set
def test_log_regres(weights, test_x, test_y):
    num_samples, num_features = shape(test_x)
    match_count = 0
    for i in xrange(num_samples):
        predict = sigmoid(test_x[i, :] * weights)[0, 0] > 0.5
        if predict == bool(test_y[i, 0]):
            match_count += 1
    accuracy = float(match_count) / num_samples
    return accuracy


# show your trained logistic regression model only available with 2-D data
def showLogRegres(weights, train_x, train_y):
    # notice: train_x and train_y is mat datatype
    numSamples, numFeatures = shape(train_x)
    if numFeatures != 3:
        print "Sorry! I can not draw because the dimension of your data is not 2!"
        return 1

    # draw all samples
    for i in xrange(numSamples):
        if int(train_y[i, 0]) == 0:
            plt.plot(train_x[i, 1], train_x[i, 2], 'or')
        elif int(train_y[i, 0]) == 1:
            plt.plot(train_x[i, 1], train_x[i, 2], 'ob')

    # draw the classify line
    min_x = min(train_x[:, 1])[0, 0]
    max_x = max(train_x[:, 1])[0, 0]
    weights = weights.getA()  # convert mat to array
    y_min_x = float(-weights[0] - weights[1] * min_x) / weights[2]
    y_max_x = float(-weights[0] - weights[1] * max_x) / weights[2]
    plt.plot([min_x, max_x], [y_min_x, y_max_x], '-g')
    plt.xlabel('X1'); plt.ylabel('X2')
    plt.show()