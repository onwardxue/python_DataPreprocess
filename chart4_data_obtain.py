# -*- coding:utf-8 -*-
# @Time : 2022/7/25 12:44 下午
# @Author : Bin Bin Xue
# @File : chart3_pandas
# @Project : python_DataPreprocess

'''
    第4章 数据获取
        4.1 从CSV和TXT文件读取数据
            pd.read_csv(filepath,encoding='utf-8'或'gbk')，返回一个DataFrame数据结构
        4.2 从Excel文件读取数据
            pd.read_excel(filepath,sheet_name=2)，返回一个DataFrame
        4.3 从JSON文件读取数据
            pd.read_json(...)
        4.4 从HTML表格读取数据
            pd.read_html(...)
        4.5 从数据库读取数据
            pd.read_sql(...)
        4.6 从word读取数据
        4.7 从PDF读取数据

'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

temp = '-'*5
print(temp+'test'+temp)
