def ImageHurst(imgpath,  outtif):
    """
    计算影像的hurst指数
    :param imgpath: 影像路径，多波段
    :param outtif: 输出结果路径
    :return: None
    """
    # 读取影像的信息和数据
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

    # 开始计算指数

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