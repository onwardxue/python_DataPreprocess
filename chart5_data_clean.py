# -*- coding:utf-8 -*-
# @Time : 2022/7/25 12:44 下午
# @Author : Bin Bin Xue
# @File : chart3_pandas
# @Project : python_DataPreprocess

'''
    第5章 数据清理
        5.1 数据清理概述
            主要解决三个问题：数据缺失、数据重复、数据异常
            1.缺失值的处理方式
                3种方式：删除、填充、插补
            2.重复值的处理方式
                2种方式：删除或保留（类不平衡数据中重复值有一定的使用价值）
            3.异常值的处理方式
                3种方式：保留、删除、替换
        5.2 缺失值的检测与处理
            1.缺失值的检测
                缺失值中None或NaN代表缺失值。检测缺失值的方法包括：
                isnull(),isna()，返回True的位置即为缺失值
                df.isna()
            2.缺失值的处理
                (1)删除
                    df.dropna(axis,how,thresh,subset,inplace)
                        axis=1表示列
                        how='any'表示只要存在一个就删除；='all'表示全部都是空才删除
                        thresh='n'表示只要一行/列有n个非空值就保留
                        subset表示删除指定列的缺失值
                        inplace表示是否在原数据上进行删减操作
                (2)填充
                    df.fillna(value,method,axis,limit)
                        value表示要填充的数据
                        method='ffill'表示后向填充，即用前一个有效数字填充后一个缺失值
                        常用某列均值，保留一位小数，填充该列缺失值：
                            col_a = np.around(np.mean(na_df['A']),1)
                            na_df.fillna({'A':col_a})

                (3)插补
                    df.interpolate(method,limit,limit_direction)
                        method默认为linear

        5.3 重复值的检测与处理
            1.重复值的检测
                df.duplicated(subset,keep)
                    subset默认识别所有列，可设特定列
                    keep默认为'first'，表示只留第一个，其他的标识为重复值
            2.重复值的处理
                删除
                df.drop_duplicates()

        5.4 异常值的检测与处理
            1.异常值的检测
                2种方式：kS检测正态分布；箱型图检测
            2.异常值的处理
                通过检测异常值返回异常值所在位置后执行以下处理：
                删除或替换
                (1)删除
                    df.drop(labels=None,axis=0...)
                        根据索引删除指定行的数据
                        如；
                        excel_data.drop([121,710]) - 删除这两行数据
                (2)替换（保证数据完整性）
                    df.replace({a:b}.loc[t])
                        更换a为b，在t行上
                        如：
                            df.replace({13.2:10.2,13.1:10.5})
'''
import numpy as np
import scipy.stats as stats
import pandas as pd

# 使用k-S检测查看特征分布是否符合正态分布（需要传入dataframe数据和特征名）
def if_Gaussian_distribution(dataframe,feature='value'):
    u = dataframe[feature].mean()
    std = dataframe[feature].std()
    kstestresult = stats.kstest(dataframe[feature],'norm',(u,std))
    # ks检测中的结果pvalue>=0.05证明符合正态分布，返回1；否则不符合，返回0
    if(float((kstestresult[1])[8:12])>=0.05):
        return 1
    else:
        return 0

# 使用3sigma法则判断df中的异常值（要求特征数值符合正态分布，返回有异常值的行和异常值）
def three_sigma(ser):
    mean_data = ser.mean()
    std_data = ser.std()
    rule = (mean_data-3*std_data>ser) | (mean_data+3*std_data < ser)
    index = np.arange(ser.shape[0])[rule]
    outliers = ser.iloc[index]
    return outliers

#箱型图检测异常值（不要求正态分布）
def box_outliers(ser):
    new_ser = ser.sort_values()
    if new_ser.count()%2==0:
        Q3 = new_ser[int(len(new_ser)/2):].median()
        Q1 = new_ser[:int(len(new_ser)/2)].median()
    else:
        Q3 = new_ser[int((len(new_ser)-1) / 2):].median()
        Q1 = new_ser[:int((len(new_ser) -1)/ 2)].median()
    IQR =round(Q3-Q1,1)
    rule = (round(Q3+1.5*IQR,1)<ser)|(round(Q1-1.5*IQR,1) > ser)
    index = np.arange(ser.shape[0])[rule]
    outliers = ser.iloc[index]
    return outliers


na_df = pd.DataFrame({'A':[1,2,np.NaN,4],'B':[3,4,4,5],'C':[5,6,7,8],'D':[7,5,np.NaN,np.NaN]})
print(na_df)

print('-----检测缺失值-----')
print(na_df.isna())
print('-----缺失值删除-----')
after_df =na_df.dropna(thresh=3)
print(after_df)
print('-----缺失值填充-----')
col_a = np.around(np.mean(na_df['A']),1)
after_df =na_df.fillna({'A':col_a})
print(after_df)
print('-----缺失值插补-----')
after_df =na_df.interpolate()
print(after_df)

print('-----检测重复值-----')
person_info = pd.DataFrame({'name':['ltt','ws','py','lh','lh','zy'],
                            'age':[24,23,29,22,22,27],
                            'height':[162,165,175,175,175,178],
                            'gender':['f','f','m','m','m','m']})
print(person_info)
print(person_info.duplicated())
print('-----删除重复值-----')
after_df =person_info.drop_duplicates()
print(after_df.duplicated())

print('-----检测异常值-----')
#没有数据支持
print('-----删除异常值-----')
print('-----替换异常值-----')
# df.drop
# df.replace
