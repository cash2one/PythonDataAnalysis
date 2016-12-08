# -*- coding: UTF-8 -*-
__author__ = 'Zealot'

import numpy as np
import math

'''
BFGS
12月04日
'''

# def lr_bfgs(data,alpha):


def hessian_r2(c, w, g):
    n = w.size
    d = g.dot(w)
    if math.fabs(d) < 1e-4:
        return np.identity(n)
    a = np.zeros((n, n))
    for i in range(n):
        a[i] = g[i] * g
    a /= d

    b = np.zeros((n, n))
    w2 = c.dot(w)
    for i in range(n):
        b[i] = w2[i] * w2;
    d2 = w.dot(w2)
    if math.fabs(d2) < 1e-4:
        return np.identity(n)
    b /= d2
    return c + a - b


def lr_bfgs(data, alpha):
    n = len(data[0]) - 1;
    w = np.zeros(n)
    g = np.zeros(n)
    c = np.identity(n)
    for times in range(1000):
        for d in data:
            x = np.array(d[:-1])
            y = d[-1]
            g0 = g
            w0 = w
            g = (y - predict(w, x)) * x
            w = w + alpha * c.dot(g)
            c = hessian_r2(c, w - w0, g - g0)
        print times, w
    return w


def predict(w, x):
    print "w: ", w
    print "x: ", x
    res = w * x
    print "res: ", res
    return res


if __name__ == '__main__':
    x = [[1, 2, 3, 4, 1], [2, 4, 6, 8, 1], [2, 4, 6, 9, 0]]
    print lr_bfgs(x,0.1)