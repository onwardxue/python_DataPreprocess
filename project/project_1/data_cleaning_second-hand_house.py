# -*- coding:utf-8 -*-
# @Time : 2022/7/26 10:17 下午
# @Author : Bin Bin Xue
# @File : data_cleaning_second-hand_house
# @Project : python_DataPreprocess

import pandas as pd
import numpy as np

#读取数据
second_hand_house = pd.read_excel('handroom.xlsx')
print(second_hand_house)

# 查看数据摘要信息
print(second_hand_house.info())

# 缺失值处理
second_hand_house = second_hand_house.dropna(subset=['小区名称'])
print(second_hand_house)

# 重复值处理
print(second_hand_house[second_hand_house.duplicated().values==True])
second_hand_house = second_hand_house.drop_duplicates(ignore_index=True)
print(second_hand_house[second_hand_house.duplicated().values==True])

# 异常值处理
# from matplotlib import pyplot as plt
# plt.rcParams['font.sans-serif'] = ['SimHei']
# estate = second_hand_house[second_hand_house['小区名称'].values =='翡翠城四期']
# box = estate.boxplot(column='单价(元/平米)')
# plt.show()
def box_outliers(ser):
    new_ser = ser.sort_values()
    if new_ser.count()%2==0:
        Q3=new_ser[int(len(new_ser)/2):].median()
        Q1=new_ser[:int(len(new_ser)/2)].median()
    else:
        Q3=new_ser[int((len(new_ser)-1)/2):].median()
        Q1=new_ser[:int((len(new_ser)-1)/2)].median()
    IQR = round(Q3-Q1,1)
    rule = (round(Q3+1.5*IQR,1)<ser)|(round(Q1-1.5*IQR,1)>ser)
    index = np.arange(ser.shape[0])[rule]
    # 获取包含异常值的数据
    outliers = ser.iloc[index]
    return outliers

# 保存异常值索引
outliers_index_list=[]
for i in set(second_hand_house['小区名称']):
    estate = second_hand_house[second_hand_house['小区名称'].values==i]
    outliers_index = box_outliers(estate['单价(元/平米)'])
    if len(outliers_index) != 0:
        outliers_index_list.append(outliers_index.index.tolist())
outliers_index_single_li = sum(outliers_index_list,[])
print(second_hand_house.loc[[i for i in outliers_index_single_li]])
second_hand_house=second_hand_house.drop(0)
print(second_hand_house)