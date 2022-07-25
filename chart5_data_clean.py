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
                    
        5.3 重复值的检测与处理
            1.重复值的检测
            2.重复值的处理

        5.4 异常值的检测与处理
            1.异常值的检测
            2.异常值的处理

'''

