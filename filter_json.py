import os
import numpy as np
import pandas as pd
import shutil


file_path='/home/stone/project/tese_oss/jsonInfo/'
#被筛选文件所在路径

filename_path='/home/stone/project/tese_oss/.vscode/shuju.xlsx'
#目标文件名称列表
houzhuijiaxiaoshudianweishu=5
#这里要更改目标文件的后缀名加上一个小数点的位数 例子.xlsx 对应的位数为5
filelist=os.listdir(file_path)
#获取被筛选文件夹中的被筛选文件名称

file_name=pd.read_excel(filename_path,sheet_name='sheet1')

#读取所需文件列表 将目标文件名读取并储存在file_name中
#读入excel数据是一个dataframe格式数据 需要转换成list
file_name=file_name.iloc[0:59,0:1]#取第一列的固定行数，存储的是目标文件名列形式
file_name = np.array(file_name)
#np.ndarray()
file_name=file_name.tolist()
#list
#这里的list是[[1],[2],[3],[4]]需要转换成[1，2，3]
b=[]
for i in file_name:
    for j in i:
        b.append(j)
file_name=b
print(file_name)
#完成转换
n=0
m=0
#将被筛选文件名遍历，依次对照目标文件名组成的列表
for file in filelist :
    olddir=os.path.join(file_path,file)
    print(olddir)
     #如果被筛选当前个体文件名存在于目标名单，将把该文件复制到目标文件夹（结果）
    file_quhouzhui = file[:-houzhuijiaxiaoshudianweishu]
    file_quhouzhui=int(file_quhouzhui)

    if file_quhouzhui in file_name :
        print(file,'在目标目录中')
        n = n+1
        print(n)
        F="/home/stone/project/tese_oss/down_json/"
        #新文件夹名称（先建好）用于存放结果文件
        newdir=os.path.join(F,file)
        #file是一个带有文件类型后缀的字符串，与F连接起来生成新的存储路径
        shutil.copy(olddir,newdir)
        #复制到新文件夹中 shutil.copy(文件1，文件2)：拷贝文件和权限都进行copy。把1拷贝给2
    else :
        print(file,'不在目标目录中')
        m=m+1
        continue
print('不符合的文件数',m)
print('符合的文件数',n)





