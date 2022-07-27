# -*- coding:utf-8 -*-
# @Time : 2022/7/26 10:20 下午
# @Author : Bin Bin Xue
# @File : data_analysis_data_analsyst_job
# @Project : python_DataPreprocess

import time
import pandas as pd
from pyecharts.charts import Bar, Line,Pie
from pyecharts import  options as opts
from pyecharts.globals import SymbolType,ThemeType

# 1_读取数据
recruit_obj = pd.read_csv('lagou01.csv',encoding='gbk')
print(recruit_obj)
print(recruit_obj.columns)

#2_过滤与分析目标无关的数据，保留有关的数据
new_df_01 = pd.DataFrame([recruit_obj['city'],recruit_obj['companyFullName'],recruit_obj['salary'],recruit_obj['companySize'],
                         recruit_obj['district'],recruit_obj['education'],recruit_obj['firstType'],recruit_obj['positionAdvantage'],recruit_obj['workYear'],
                         recruit_obj['createTime']]).T
print(new_df_01.head(5))

#3_第二份数据同上
recruit_obj2 = pd.read_excel('lagou02.xlsx')
print(recruit_obj2)
new_df_02 = pd.DataFrame([recruit_obj['city'],recruit_obj['companyFullName'],recruit_obj['salary'],recruit_obj['companySize'],
                         recruit_obj['district'],recruit_obj['education'],recruit_obj['firstType'],recruit_obj['positionAdvantage'],recruit_obj['workYear'],
                         recruit_obj['createTime']]).T
print(new_df_02.head(5))

#4_统一特定字段的格式
new_df_01['createTime'] = pd.to_datetime(new_df_01['createTime'])
new_df_02['createTime'] = pd.to_datetime(new_df_02['createTime'])
new_df_02.head(5)

#5_使用上下堆叠的方式合并数据集，并修改各列的特征名
final_df = pd.concat([new_df_01,new_df_02],ignore_index=True)
final_df = final_df.rename(columns={'city':'城市','companyFullName':'公司全称','salary':'薪资',
                         'companySize':'公司规模','district':'区','education':'学历','firstType':'第一类型',
                         'positionAdvantage':'职位优势','workYear':'工作经验','createTime':'发布时间'})
print(final_df.head(5))

# 6_数据预处理_重复值处理
print(final_df[final_df.duplicated().values==True])
final_df = final_df.drop_duplicates()
print(final_df)

# 7_数据预处理_缺失值处理
print(final_df[final_df.isna().values==True])
print(final_df.loc[28])
final_df = final_df.fillna('未知')
print(final_df.loc[28])

# 8_数据分析与展现
# 8_1_分析展现数据分析师岗位的需求趋势
# # 设置时间数据格式
# final_df['发布时间'] = final_df['发布时间'].dt.strftime('%Y-%m-%d')
# print(final_df.head(10))
# # 按时间分组，并统计各城市之和
# jobs_count = final_df.groupby(by='发布时间').agg({'城市':'count'})
# print(jobs_count)
# # 绘制曲线图
# line_demo = (
#     Line(init_opts=opts.InitOpts(theme=ThemeType.ROMA))
#     # 添加x轴的数据、y轴的数据、系列名称
#     .add_xaxis(jobs_count.index.tolist())
#     .add_yaxis(' ', jobs_count.values.tolist(),symbol='diamond',symbol_size=10)
#
#     # 设置标题
#     .set_global_opts(title_opts=opts.TitleOpts(title='数据分析师岗位的需求趋势'),
#                      yaxis_opts=opts.AxisOpts(name='需求数量 (个)',
#                      name_location='center',name_gap=30))
# )
# line_demo.render('sample1.html')

# 8_2_分析展现数据分析师岗位的热门城市TOP10
# 统计每个城市的岗位和
# city_num = final_df['城市'].value_counts()
# print(city_num.head())
# # 绘制图表
# city_value = city_num.values[:10].tolist()
# city_index = city_num.index[:10].tolist()
# bar_demo=(
#     Bar()
#     # 添加x轴的数据、y轴的数据、系列名称
#     .add_xaxis(city_index)
#     .add_yaxis('',city_value)
#     # 设置标题
#     .set_global_opts(title_opts=opts.TitleOpts(
#         title='数据分析师岗位的热门城市TOP10'),
#         xaxis_opts=opts.AxisOpts(
#             axislabel_opts=opts.LabelOpts(rotate=-15)),
#         visualmap_opts=opts.VisualMapOpts(max_=450),
#         yaxis_opts=opts.AxisOpts(name='需求数量(个)',
#         name_location='center',name_gap=30))
# )
# bar_demo.render('sample2.html')

# 8_3_分析展现不同城市数据分析师岗位的薪资水平
# 将数据里面的大写字母K转化为小写k
# final_df['薪资'] = final_df['薪资'].str.lower().fillna(' ')
# # 增加两列，一列是薪资的最大值，一列是薪资的最小值
# final_df['薪资最大值'] = final_df['薪资'].str.extract(r'(\d+)').astype(int)
# final_df['薪资最小值'] = final_df['薪资'].str.extract(r'\-(\d+)').astype(int)
# average_df = final_df[['薪资最小值','薪资最大值']]
# final_df['薪资平均值'] = average_df.mean(axis=1)
# final_df.drop(columns=['薪资'],inplace=True)
# print(final_df.head(10))
# # 分组
# companyNum=final_df.groupby('城市')['薪资平均值'].mean().sort_values(ascending=False)
# companyNum = companyNum.astype(int)
# # 绘图
# company_values = companyNum.values.tolist()
# company_index = companyNum.index.tolist()
# bar_demo2 = (
#     Bar()
#     # 添加x轴、y轴的数据，系列名称
#     .add_xaxis(company_index)
#     .add_yaxis('',company_values)
#     # 设置标题
#     .set_global_opts(title_opts=opts.TitleOpts(
#         title='不同城市数据分析师岗位的薪资水平'),
#         xaxis_opts=opts.AxisOpts(
#             axislabel_opts=opts.LabelOpts(rotate=-15)),
#         visualmap_opts = opts.VisualMapOpts(max_=21),
#         yaxis_opts=opts.AxisOpts(name='薪资(k)',
#         name_location='center',name_gap=30))
# )
# bar_demo2.render('sample3.html')

# 8_4_分析展现数据分析师岗位的学历要求
education = final_df['学历'].value_counts()
cut_index = education.index.tolist()
cut_values = education.values.tolist()
# 将学历和统计值打包成元组，再转成列表
data_pair = [list(z) for z in zip(cut_index,cut_values)]
# 绘图
pie_obj = (
    Pie(init_opts=opts.InitOpts(theme=ThemeType.ROMA))
    .add(' ',data_pair,radius=['35%','70%'])
    .set_global_opts(title_opts=opts.TitleOpts(
        title='数据分析时岗位的学历要求'),
        legend_opts=opts.LegendOpts(orient='vertical',
                        pos_top='15%',pos_left='2%'))
    .set_series_opts(label_opts=opts.LabelOpts(formatter='{b}:{d}%'))
)
pie_obj.render('sample4.html')
