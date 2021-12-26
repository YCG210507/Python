# FilesBatchRename.py
# 导入os库
import os

# 图片存放的路径
path = r"F:\\Temp\\SM"

# 遍历更改文件名
num = 2000
for file in os.listdir(path):
    os.rename(os.path.join(path,file),os.path.join(path,"sm"+str(num))+".tif")
    num = num + 1

print("process over!")

