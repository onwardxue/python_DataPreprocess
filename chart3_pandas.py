# -*- coding:utf-8 -*-
# @Time : 2022/7/25 12:44 下午
# @Author : Bin Bin Xue
# @File : chart3_pandas
# @Project : python_DataPreprocess

'''
    第3章 pandas库介绍
        3.1 数据结构
            1.series
                结构类似于一维数组：索引位于左侧，数据位于右侧
                构造方法：
                    pd.Series(data=None,...) 可以是ndarry、列表和字典
                如：
                    (1) pd.Series(['Python','Java']) - 默认索引为0,1...
                    (2) list = ['Python','Java']
                          index = ['one','two']
                          pd.Series(list,index=index) - 自定义索引
                    (3) data = {'one':'python','two':'java'}
                          pd.Series(data) - 直接用字典建立索引和值映射关系

            2.dataframe
                结构类似于表格，索引由行索引和列索引组成
                构造方法：
                    pd.DataFrame(data,...)可以是ndarray、字典、列表或可迭代对象
                如：
                    (1) data = np.array([['a','b','c'],['d','e','f']])
                          df_obj = pd.DataFrame(data)
                    (2) 指定行索引和列索引：
                          df_obj = pd.DataFrame(data,index=['r1",'r2'],columns=['c1','c2','c3'])

        3.2 索引操作（略过高级部分）
            1.索引对象
                单层索引 - 4种类型
                多层索引 - MultiIndex
            2.单层索引访问
                (1)使用'[]' 访问数据 - 变量[索引]（按列索引，返回列）
                    如：df['A']
                (2)使用loc和iloc访问 - 变量.loc[索引]，变量.iloc[索引]（按行索引，返回行）
                    注：iloc必须用于原始生成的索引序列
                            loc必须用于自定义的标签索引
                    如：df.iloc[2],df.loc['two']
                (3)使用at和iat访问数据 - 变量.at[行索引,列索引]，变量.iat[行索引,列索引]（按位置索引，返回某个位置的值）
                    注：at索引为自定义的标签
                            iat索引为自动生成的标签序列
                    如：df.at[5,'b']，df.iat[1,1]
            3.多层索引访问
                三种方法：[]、loc、iloc
            4.重新索引
                重新设置行索引、列索引和处理缺失值
                    df.reindex(index=None,columns=None,fill_value=None)
                如：
                    new_index = ['s','a','c']
                    new_columns = ['status_1','status_2']
                    fill_value = 'missing
                    new_df = df.reindex(index=new_index,columns=new_columns,fill_value=fill_value)

        3.3 数据排序
            1.按索引排序
                df对象的索引按行/列排序：
                    df.sort_index()
                    df.sort_index(axis=1)
            2.按值排序
                    df.sort_values(by='col_b') - 根据列索引'col_b'进行排序
                    df.sort_values(by='col_b', na_position='first') - 设置空值放在前面显示

        3.4 统计计算与统计描述
            1.统计计算
                df.max() -获取每列最大值
                df.idxmax() - 每列最大值对应的行索引
                (sum、mean、max、min、count、var、std...)

            2.统计描述
                df.describe()

        3.5绘制图表
            df.plot()
                注意：要添加库和设置中文
                import matplotlib.pyplot as plt
                plt.rcParams['font.sans-serif'] = ['SimHei]
                举例：
                df.plot(kind='bar',xlabel='季度',ylabel='销售额',rot=0) -绘制柱状图
                df.plot(kind='box',ylabel='销售额(万元)') - 箱型图
'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print('Series：')
list = ['Java','Python','PHP']
ser_obj = pd.Series(list)
print(ser_obj)

print('DataFrame：')
demo_arr = np.array([['a','b','c','d'],['e','f','g','h']])
df_obj = pd.DataFrame(demo_arr)
df_obj_1 = pd.DataFrame(demo_arr,index=['row_01','row_02'],columns = ['col_01','col_02','col_03','col_04'])

print(df_obj)
print(df_obj_1)

print('单层访问：')
print(df_obj[0][0])
print(df_obj_1['col_01'])
print(df_obj_1.loc['row_01'])
print(df_obj.iloc[0])
print(df_obj_1.at['row_01','col_01'])
print(df_obj.iat[0,0])

print('重新索引')
print(df_obj.reindex(index=['one','two'],fill_value='missing'))

print('按索引排序：')
df = pd.DataFrame(np.arange(9).reshape(3,3),index=['B','C','A'],columns=['c','a','b'])
print(df)
print('排序后：')
row_sort = df.sort_index()
print(row_sort)
print('按行重排序：')
row_sort = df.sort_index(axis=1)
print(row_sort)


print('按值排序：')
df = pd.DataFrame({'col_A':[1,1,4,6], 'col_B':[4,np.nan,4,2],'col_C':[6,3,8,0]})
print(df)
new_df = df.sort_values(by='col_B',na_position='first')

print(df.max)
print(df.describe())

plt.rcParams['font.sans-serif'] = ['SimHei']
df.plot(kind='bar',xlabel='0',ylabel='1',rot=0)
plt.show()
