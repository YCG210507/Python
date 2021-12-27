import numpy as np
from osgeo import gdal
import os
from tqdm import tqdm
"""
计算hurst指数
"""

def s(inputdata):
    # 输入numpy数组
    n = inputdata.shape[0]
    t = 0
    for i in np.arange(n):
        if i <= (n - 1):
            for j in np.arange(i + 1, n):
                if inputdata[j] > inputdata[i]:
                    t = t + 1
                elif inputdata[j] < inputdata[i]:
                    t = t - 1
                else:
                    t = t
    return t


def beta(inputdata):
    n = inputdata.shape[0]
    t = []
    for i in np.arange(n):
        if i <= (n - 1):
            for j in np.arange(i + 1, n):
                t.append((inputdata[j] - inputdata[i]) / ((j - i) * 1.0))
    return np.median(t)


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
    # 分母加个小数防止分母为0
    #ydata = np.log(r[1:] / (s[1:] + 0.0000001))

    h, b = np.polyfit(xdata, ydata, 1)
    return h

def ImageHurst(imgpath,  outtif):
    """
    计算影像的hurst指数
    :param imgpath: 影像1，多波段
    :param outtif: 输出结果路径
    :return: None
    """
    # 读取影像1的信息和数据
    ds1 = gdal.Open(imgpath)
    projinfo = ds1.GetProjection()
    geotransform = ds1.GetGeoTransform()
    rows = ds1.RasterYSize
    colmns = ds1.RasterXSize
    data1 = ds1.ReadAsArray()
    print(data1.shape)

    src_nodta = ds1.GetRasterBand(1).GetNoDataValue()

    # 创建输出图像
    format = "GTiff"
    driver = gdal.GetDriverByName(format)
    dst_ds = driver.Create(outtif, colmns, rows, 1,gdal.GDT_Float32)
    dst_ds.SetGeoTransform(geotransform)
    dst_ds.SetProjection(projinfo)

    # 删除对象
    ds1 = None

    # 开始计算相关系数

    band1 = data1[0]
    out = band1 * 0 - 2222
    for row in tqdm(range(rows)):
        for col in range(colmns):
            if src_nodta is None:
                x = data1[:, row, col]
                hindex  =  Hurst(x)
                out[row, col] = hindex
            else:
                if band1[row, col] != src_nodta:
                    x = data1[:, row, col]
                    hindex = Hurst(x)
                    out[row, col] = hindex
    # 写出图像
    dst_ds.GetRasterBand(1).WriteArray(out)

    # 设置nodata
    dst_ds.GetRasterBand(1).SetNoDataValue(-2222)
    dst_ds = None


if __name__ == '__main__':

    x = np.array([1.59, 1.57, 1.56, 1.54, 1.52, 1.50, 1.47, 1.43, 1.41, 1.40, 1.39])
    print(Hurst(x))

    imgpath = r"E:\data\一元回归\降水sub.tif"
    outtif = r"E:\data\一元回归\降水hurst3.tif"
    ImageHurst(imgpath,  outtif)
