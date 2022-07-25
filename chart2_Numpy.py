# -*- coding:utf-8 -*-
# @Time : 2022/7/25 10:11 上午
# @Author : Bin Bin Xue
# @File : chart1_data_preprocess_summary
# @Project : python_DataPreprocess

'''
    第二章 科学计算库-NumPy
        2.1 数组对象(ndarray)
            ndarray是numpy专有的一种数据结构
                常用属性：ndim(返回维度)、shape(返回几行几列)、size(数组中元素总数)、dtype(数组中元素类型)

        2.2 创建数组
            1.根据现有列表创建
                    np.array(list) - 如：np.array([[1,2,3],[4,5,6]])
            2.根据特定数组创建
                    np.zeros(维度) - 如：np.zeros((2,3)) - 创建一个2行3列的0矩阵
                    np.ones -值为1
                    np.empty - 值为随机数
            3.根据指定数据范围创建
                    arr = np.arrange(1,30,5) - 生成均匀分布的数据
                    arr.reshape(2,3) - 再用reshape调成指定维度

        2.3 访问数组元素
            1.整数索引
                array(m,n)
            2.花式索引和布尔索引
                花式索引 - 以数组或列表作为索引，并以数组形式返回
                    如：array[[2,5,8]] - 若为一维数组，返回下标为2，5，8的值；
                                                     若为二维数组，返回第2、5、8行的所有数值；
                            array[[0,2],[1,1]] - 返回[0,1]、[2,1]位置的数值
                布尔索引 - 按条件筛选元素
                    如：array[array>5] - 遍历数组并返回符合条件的数
            3.使用切片访问元素（左闭右开）
                一维切片：array[1:3] - 访问索引为1、2的元素
                                  array[::2] - 访问从开头到末尾，步长为2的元素
                                  array[:-1] - 访问从末尾元素外的其他元素
                                  array[:] - 访问所有元素
                二维切片：array[:2] - 访问前两行的元素
                                  array[:2,0:1] - 访问前两行、第一列的元素
                                  array[:2,1] - 访问前两行、第二列的元素

        2.4 数组运算
            1.形状相同的数组间运算
                对应位置运算
            2.形状不同的数组间运算
                广播机制：将两个数组扩大到同一维度（要求：数组的某一维度为1；存在某一维度相等）
                如： 8*1*6* + 7*1*5 = 8*7*6*5（符合）
                        2*1 + 8*4*3 （异常报错）
            3.数组与标量运算
                加减乘除都会作用到数组每一个元素上：array + num

        2.5 数组操作
            1.排序
                array.sort()
                    默认用快排，按行从小到大排序，返回排好序后的数组
                    (axis=-1,kind='quicksort',order)
                    若要按列操作：
                    (axis=0)

            2.检查
                np.all(array>0) - 是否全部大于0
                np.any(array>0) - 是否至少有1个大于0

            3.元素唯一化
                np.unique(array) - 将数组中的元素唯一化（去重）

        2.6 数组转置（三种方式）
            1.T属性 - 主要二维数组
                array.T
            2.swapaxes()方法 - 可交换任意两个轴的元素
                array.swaoaxes(2,1) - 交换1、2轴的元素
            3.transpose()方法 - 交换多个轴的元素（传入一个轴交换编号的元组）
                array.transpose((1,2,0))

'''
import numpy as np

print('创建随机numpy数组')
arr1 = np.arange(10).reshape(2,5)
arr2 = np.array([[5,3,5,7,9],[4,2,3,7,8]])
print(f'arr维度：{arr1.ndim}')
print(f'arr形状：{arr1.shape}')
print(f'arr总数：{arr1.size}')
print(f'arr类型：{arr1.dtype}')
print(arr1)

print('数组访问')
print(f'花式索引: {arr1[:2,0:1]}')
print(f'布尔索引: {arr1[arr1>5]}')

print('数组操作')
print(f'数组排序: {arr2.sort(axis=0)}')
print(f'数组检查: {np.all(arr2>5)}{np.any(arr2>5)}')
print(f'元素唯一值：{np.unique(arr2)}')

print('数组转置')
print(arr2.transpose((1,0)))
