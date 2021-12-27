import numpy as np
from osgeo import gdal
import os
"""
计算hurst指数
"""


def Hurst(x):
    # x为numpy数组
    n = x.shape[0]
    t = np.zeros(n - 1)  # t为时间序列的差分
    for i in range(n - 1):
        t[i] = x[i + 1] - x[i]
    mt = np.zeros(n - 1)  # mt为均值序列,i为索引,i+1表示序列从1开始
    for i in range(n - 1):
        mt[i] = np.sum(t[0:i + 1]) / (i + 1)

    # Step3累积离差和极差,r为极差
    r = []
    for i in np.arange(1, n):  # i为tao
        cha = []
        for j in np.arange(1, i + 1):
            if i == 1:
                cha.append(t[j - 1] - mt[i - 1])
            if i > 1:
                if j == 1:
                    cha.append(t[j - 1] - mt[i - 1])
                if j > 1:
                    cha.append(cha[j - 2] + t[j - 1] - mt[i - 1])
        r.append(np.max(cha) - np.min(cha))
    s = []
    for i in np.arange(1, n):
        ss = []
        for j in np.arange(1, i + 1):
            ss.append((t[j - 1] - mt[i - 1]) ** 2)
        s.append(np.sqrt(np.sum(ss) / i))
    r = np.array(r)
    s = np.array(s)
    xdata = np.log(np.arange(2, n))
    ydata = np.log(r[1:] / s[1:])

    h, b = np.polyfit(xdata, ydata, 1)
    return h

if __name__ == '__main__':

    x = np.array([1.59, 1.57, 1.56, 1.54, 1.52, 1.50, 1.47, 1.43, 1.41, 1.40, 1.39])
    print(Hurst(x))
 # 0.7486779334192257
