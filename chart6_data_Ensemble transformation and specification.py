# -*- coding:utf-8 -*-
# @Time : 2022/7/26 5:45 下午
# @Author : Bin Bin Xue
# @File : chart6_data_Ensemble transformation and specification
# @Project : python_DataPreprocess

'''
    第六章 数据集成、变换与规约
        6.1 数据集成
            多个数据源的数据集成到一个，形成统一的数据源
            1.集成概述
                实体识别：指从不同的数据源中识别出相同的实体（不同表现形式）
                冗余属性识别；识别同义不同名的属性
                元组重复
            2.合并数据
                （1）主键合并数据（根据某个共有特征，进行合并）
                            pd.merge(df_left,df_right,on='key')
                                默认how='inner',内连接(取两表主键的交集)
                                how='left'为左外连接，保留左表的主键；='right'，同理
                                how='outer'为全外连接（取并集）
                （2）堆叠合并数据（按行或列直接合并，不管有无重复）
                            pd.concat([df_letf,df_right],axis=0)
                                默认axis=0，按行合并
                                设axis=1，表示按列合并
                （3）重叠合并数据（并不常用，索引重合但数据中存在缺失时可以用来填补缺失）
                            df_left.combine_first(df_right)

        6.2 数据变换
            1.数据变换概述
                数据转换成数据挖掘需要的形式，主要包括3类操作：
                （1）数据标准化处理
                            数据按一定的比例缩放到较小的特定区间，包括3种方法：
                                最小-最大标准化；均值标准化；小数定标标准化
                （2）数据离散化处理
                            将取值范围划分为若干离散化区间。包括：
                                等宽法和等频法
                （3）数据泛化处理
                            低层特征泛化到高层
            2.轴向旋转
                指的是重新指定一组数据的行索引和列索引，有两个方法：
                （1）df.pivot(index,columns,values)
                            将dataframe对象中的某一列转换为索引
                                index为行索引，columns为列索引，values为元素值
                            如：
                                df.pivot(index='var1',columns='var2',values='var3')
                （2）df.melt(value_name,ignore_index=false)
                            melt为pivot的逆操作，使用相同的value值即可得到原形状
                            如：
                                df.melt(value_name='var3',ignore_index=False)

            3.分组与聚合
                过程是先将数据按条件分成多组，分别计算得到统计标量，再将这些数据进行合并
                （1）分组：
                        group =df.groupby(by='key') - 返回多个dataframe组成的类对象，可用for遍历访问

                （2）聚合：
                        group.max() 分组计算最大值，自动聚合到一起（使用内置的统计方法聚合）
                        group.agg(my_range) 使用自定义的统计方法实现聚合
                        group.transform('max') 保持与原来一样的结构，每组结果给到原来的各组中的每个元素
                        group.apply() 前面两种方法的结合，用这个即可。

            4.哑变量处理
                哑变量又叫名义变量，用来反应某个变量的不同类别，常用的取值为0，1（不代表数值，只表明分类）
                - 类别变量转数值变量时，用于区分类别的数值就就叫哑变量
                - 类别变量是变量值为非数值，离散的，用于表示不同类别的变量
                - 独热编码：即有n类，每一类都编有n个码，代表本类的码为1，其他为0
                （1）pd.get_dummies(df,prefix=['col'])
                            prefix表示增加列索引名的前缀（前缀_列索引名）

            5.面元划分
                连续数值离散化：将连续数值划分成各个区间
                    pd.cut(x,bins)
                        x为各连续数据值组成的列表
                        bins为划分面元的依据。若为int类型的值，代表面元数；若为list、tuple、array则代表划分的区间，每两个值的间隔为一个区间

        6.3 数据规约
            1.概述
                大型数据集要降低数据规模，保留数据的完整性。有3种方法"
                    维度规约：减少特征，降低维度。方法如删除不相关特征，取样本子集
                    数量规约：用较小规模的数据替换或估计原有数据。方法如采样
                    数据压缩：一般用有损压缩（投影），如小波转换和主成分分析
            2.重塑分层索引
                将列标转为行索引，增加分层结构
                df.stack
            3.降采样
                高频采集的数据规约到低频（如按天采集的数据变为按周采集）
                df.resample(rule,axis)

'''
import pandas as pd
df_left = pd.DataFrame({'key':['K0','K1','K2'],'A':['A0','A1','A2'],'B':['B0','B1','B2']})
df_right = pd.DataFrame({'key': ['K0','K1','K2','K3'],'C':['C0','C1','C2','C3'],'D':['D0','D1','D2','D3']})

print('合并数据')
print('主键合并-内连接')
result = pd.merge(df_left,df_right,on='key')
print(result)
print('主键合并-左外连接')
result = pd.merge(df_left,df_right,on='key',how='left')
print(result)
print('主键合并-右外连接')
result = pd.merge(df_left,df_right,on='key',how='right')
print(result)
print('主键合并-全外连接')
result = pd.merge(df_left,df_right,on='key',how='outer')
print(result)
print('堆叠合并-行方向合并')
result = pd.concat([df_left,df_right],axis=0)
print(result)
print('堆叠合并-列方向合并')
result = pd.concat([df_left,df_right],axis=1)
print(result)
print('重叠合并')
result = df_left.combine_first(df_right)
print(result)

print('数据变换-轴向旋转')
df_obj = pd.DataFrame({'商品名称':['荣耀9X','小米6X','OPPO A1','荣耀9X','小米6X','OPPO A1'],
                       '出售日期':['5月25日','5月25日','5月25日','6月18日','6月18日','6月18日'],
                       '价格(元)':[999,1399,1399,800,1200,1250]})
print(df_obj)
new_df = df_obj.pivot(index='出售日期',columns='商品名称',values='价格(元)')
print(new_df)
print(new_df.melt(value_name='价格(元)',ignore_index=False))

print('数据变换-分组与聚合')
df_obj = pd.DataFrame({'key':['C','B','C','A','B','B','A','C','A'],
                       'data':[2,4,6,8,10,1,3,5,7]})
groupby_obj = df_obj.groupby(by='key')
print(groupby_obj)
for group in groupby_obj:
    print(group)
result = dict([x for x in groupby_obj])['A']
print(result)
print(groupby_obj.max())
def div_hun(df):
    return df.iloc[:,:]/100
print(groupby_obj.apply(div_hun))

print('数据变换-哑变量处理')
position_df = pd.DataFrame({'职业':['工人','学生','司机','教师','导游']})
result = pd.get_dummies(position_df,prefix=['col'])
print(result)

print('数据变换-面元划分')
ages = pd.Series([19,20,25,35,26,89,42,67,85,71])
bins = [0,18,30,40,50,100]
cuts = pd.cut(ages,bins)
print(cuts)
