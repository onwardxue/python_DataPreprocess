# -*- coding:utf-8 -*-
# @Time : 2022/7/26 10:19 下午
# @Author : Bin Bin Xue
# @File : info_analysis_basketball_athletes
# @Project : python_DataPreprocess

import numpy as np
import pandas as pd
import datetime
import matplotlib.pyplot as plt
# 读取数据
file_one = pd.read_csv("运动员信息采集01.csv",encoding='gbk')
file_two = pd.read_excel('运动员信息采集02.xlsx')
# 采用外连接的方式合并数据
all_data = pd.merge(left=file_one,right=file_two,how='outer')
# 筛选出中国籍运动员
all_data = all_data[all_data['国籍']=='中国']
print(all_data.info())

# 数据清理_重复值
print(all_data[all_data.duplicated().values==True])
all_data = all_data.drop_duplicates(ignore_index=True)
print(all_data.head(10))
# 数据清理_缺失值
# 分别针对各特征格式或缺失进行处理(出生日期、身高、体重）
basketball_data=all_data[all_data['项目']=='篮球']
print(basketball_data['出生日期']) #发现数据不一致
basketball_data = basketball_data.copy()
initial_time = datetime.datetime.strptime('1900-01-01','%Y-%m-%d')
for i in basketball_data.loc[:,'出生日期']:
    if type(i) == int:
        new_time = (initial_time + datetime.timedelta(days=i)).strftime('%Y{y}%m{m}%d{d}').format(
            y='年',m='月',d='日')
        basketball_data.loc[:,'出生日期'] = basketball_data.loc[:,'出生日期'].replace(i,new_time)
# 为保证出生日期的一致性，这里统一使用只保留到年份的日期
basketball_data.loc[:,'出生日期']=basketball_data['出生日期'].apply(lambda x: x[:5])
print(basketball_data['出生日期'].head(10))
# 处理缺失值
male_data = basketball_data[basketball_data['性别'].apply(lambda x: x == '男')]
male_data = male_data.copy()
male_height = male_data['身高'].dropna()
# 将身高属性转为整数，厘米
fill_male_height = round(male_height.apply(lambda x: x[0:-2]).astype(int).mean())
fill_male_height = str(int(fill_male_height))+'厘米'
male_data.loc[:,'身高'] = male_data.loc[:,'身高'].fillna(fill_male_height)
male_data.loc[:, '身高'] = male_data.loc[:,'身高'].apply(lambda x: x[0: -2]).astype(int)
#重命名列标签索引
male_data.rename(columns={'身高':'身高:cm'},inplace=True)
print(male_data)

#筛选女篮运动员数据，用平均身高替换缺失值
female_data = basketball_data[basketball_data['性别'].apply(lambda x: x =='女')]
female_data = female_data.copy()
data = {'191cm':'191厘米','1米89公分':'189厘米','2.01米':'201厘米','187公分':'187厘米',
                '1.97M':'197厘米','1.98米':'198厘米','192cm':'192厘米'}
female_data.loc[:,'身高']=female_data.loc[:,'身高'].replace(data)
# 计算女篮运动员平均身高
female_height = female_data['身高'].dropna()
fill_female_height = round(female_height.apply(lambda x: x[0:-2]).astype(int).mean())
fill_female_height = str(int(fill_female_height))+'厘米'
# 填充缺失值
female_data.loc[:,'身高']=female_data.loc[:, '身高'].fillna(fill_female_height)
#身高数据转为整数
female_data['身高'] = female_data['身高'].apply(lambda x: x[0: -2]).astype(int)
# 重命名列索引
female_data.rename(columns={'身高':'身高/cm'},inplace=True)
print(female_data)

#处理'体重'的缺失值，统一单位
female_data.loc[:,'体重'] = female_data.loc[:,'体重'].replace({'88千克':'88kg'})
print(female_data)
female_data['体重'].replace(to_replace='8kg',method='pad',inplace=True)
print(female_data)
# 计算平均体重
female_weight = female_data['体重'].dropna()
female_weight = female_weight.apply(lambda x: x[0:-2]).astype(int)
fill_female_weight = round(female_weight.mean())
fill_female_weight = str(int(fill_female_weight)) + 'kg'
# 填充缺失值
female_data.loc[:,'体重'].fillna(fill_female_weight,inplace=True)
# 合并男女运动员数据，转换'体重值'为int，改列名为'体重/kg'
basketball_data = pd.concat([male_data,female_data])
basketball_data['体重'] = basketball_data['体重'].apply(lambda x: x[0: -2]).astype(int)
basketball_data.rename(columns={'体重':'体重/kg'},inplace=True)
print(basketball_data.head(5))

# 数据清理_异常值
def three_sigma(ser):
    # 计算平均值
    mean_data = ser.mean()
    # 计算标准差
    std_data = ser.std()
    # 设置异常值范围
    rule = (mean_data-3*std_data>ser) | (mean_data+3*std_data<ser)
    # 返回异常值的位置索引
    index = np.arange(ser.shape[0])[rule]
    # 获取异常值
    outliers = ser.iloc[index]
    return outliers

female_weight = basketball_data[basketball_data['性别']=='女']
print(three_sigma(female_weight['体重/kg']))
male_weight = basketball_data[basketball_data['性别']=='男']
print(three_sigma(male_weight['体重/kg']))
# 非异常值，不做特殊处理

# 数据分析1_计算男、女运动员的平均身高和平均体重
group =basketball_data.groupby('性别').mean().round(1)
print(group)
# 数据分析2_分析中国篮球运动员的年龄分布
plt.rcParams['font.sans-serif'] = ['SimHei']
ages = 2020 - basketball_data['出生日期'].apply(lambda x: x[0:-1]).astype(int)
ax = ages.plot(kind='hist')
ax.set_xlabel('年龄(岁)')
ax.set_ylabel('频数')
ax.set_xticks(range(ages.min(),ages.max()+1,2))
plt.show()
# 数据分析3_计算中国篮球运动员的体质指数（BMI）
# 增加一个值为0的列
basketball_data['体质指数'] = 0
# 计算体脂数
def outer(num):
    def ath_bmi(sum_bmi):
        weight = basketball_data['体重/kg']
        height = basketball_data['身高/cm']
        sum_bmi = weight/(height/100)**2
        return num+ sum_bmi
    return ath_bmi
# 填充这一列
basketball_data['体质指数'] = basketball_data[['体质指数']].apply(outer(basketball_data['体质指数'])).round(1)
print(basketball_data)


