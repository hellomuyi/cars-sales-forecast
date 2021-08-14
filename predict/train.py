#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time   : 2021/1/2 15:52
# @Author : Jin Xuefeng
# @File   : train.py
import pandas as pd
import numpy as np
from data_processing import one_hot, normalize
from NN import NN
import matplotlib.pyplot as plt
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
"""
输入：日期、车型、燃料类型、驱动形式、  价格、车高、额定载客、排放标准、是否增压
      date, class,fuel,   driven                整体输入
             one hot编码                         标准化
"""

# 预测标志。调参时flag置False，validation_split=0.25;调参后评估时、预测时flag置True，validation_split=0
flag_predict = False
validation_split = 0.25
# 评估性能标志（调参之后）
flag_evaluate = False
# 保存信息标志。调好超参数后保存模型结构和参数、onehot编码字典、训练集均值和标准差
flag_save = False


# ****************************************************************************************
#                                       1. 读入数据
# ****************************************************************************************
df = pd.read_excel(io='data/data_NN.xlsx', sheet_name=0, index_col=None, header=1)
data = np.array(df)
# 第1-4列、第5-9列、第10列为销量数据
# print(data.shape)   # (10083, 10)
# print(data)   # 无误
np.random.seed(0)   # 指定随机种子，复原结果
np.random.shuffle(data)     # 随机打乱数据    # 如何固定能复原结果


# ****************************************************************************************
#                      2. one-hot编码、(特征标准化、)销量平滑处理
# ****************************************************************************************
date_pre = np.array([201711])   # , 201712, 201801, 201802, 201803])
date_whole = np.hstack((data[:, 0], date_pre))    # 加入预测日期
date_onehot, date_dict = one_hot(date_whole)        # 日期onehot编码
class_onehot, class_dict = one_hot(data[:, 1])      # 车型onehot编码
fuel_onehot, fuel_dict = one_hot(data[:, 2])        # 燃料类型onehot编码
driven_onehot, driven_dict = one_hot(data[:, 3])    # 驱动类型onehot编码
# combination_nor, epsilon, sigma = normalize(data[:, 4:-1])  # 数值数据标准化  # 错误，不能整体标准化
sale_quantity_log1p = np.log1p(data[:, -1])         # 销量平滑处理
if flag_save:    # 保存onehot编码字典
    onehot_dict = {'date': date_dict,
                   'classes': class_dict,
                   'fuel': fuel_dict,
                   'driven': driven_dict}
    f = open('data/onehot_dict.txt', 'w')  # 先清除原内容再写
    f.write(str(onehot_dict))
    f.close()


# ****************************************************************************************
#                       3. 划分训练集、验证集、测试集，6:2:2
#                               6049   2017    2017
# ****************************************************************************************
tmp = int(data.shape[0]/5*4)    # 训练集(含验证集)：测试集=4:1
# print(tmp) 15128
date_train, date_test = date_onehot[0:tmp], date_onehot[tmp:-len(date_pre)]  # 去除预测日期
class_train, class_test = class_onehot[0:tmp], class_onehot[tmp:]
fuel_train, fuel_test = fuel_onehot[0:tmp], fuel_onehot[tmp:]
driven_train, driven_test = driven_onehot[0:tmp], driven_onehot[tmp:]
combination_train, combination_test = data[0:tmp, 4:-1], data[tmp:, 4:-1]   # 后面单独标准化处理
# combination_train, combination_test = combination_nor[0:tmp], combination_nor[tmp:]
sale_quantity_train, sale_quantity_test = sale_quantity_log1p[0:tmp], sale_quantity_log1p[tmp:]


# ****************************************************************************************
#                        4. 数值意义的特征单独处理，划分后还需标准化
# ****************************************************************************************
# 对训练集的数值意义特征(combination)标准化，对测试集，用训练集的均值、标准差来标准化
combination_train, epsilon, sigma = normalize(combination_train)
combination_test = (combination_test-epsilon)/sigma
if flag_save:   # 保存均值和标准差
    np.save('data/epsilon_sigma.npy', np.array([epsilon, sigma]))


# ****************************************************************************************
#                5. 实例化网络，进行训练、验证、测试，调整超参数、防止过拟合
# ****************************************************************************************
# 实例化网络，220输入，1输出
nn = NN(date_dim=date_onehot.shape[1],
        class_dim=class_onehot.shape[1],
        fuel_dim=fuel_onehot.shape[1],
        driven_dim=driven_onehot.shape[1],
        combination_dim=combination_train.shape[1],
        layers=[64, 16, 9])
model = nn.train(date=date_train,
                 classes=class_train,
                 fuel=fuel_train,
                 driven=driven_train,
                 combination=combination_train,
                 sale_q=sale_quantity_train,
                 validation_split=validation_split,    # 取值0.25，当用验证集调好超参数后，将其置零后重新训练，用于测试、预测
                 epochs=400,                 # 400-200
                 batch_size=32)
# 保存模型
if flag_save:
    model.save('data/model.h5')

if flag_evaluate:
    nn.test(date=date_test,
            classes=class_test,
            fuel=fuel_test,
            driven=driven_test,
            combination=combination_test,
            sale_q=sale_quantity_test
            )


# ****************************************************************************************
#                       6. 调整好超参数后重新训练，输入特征进行预测
# ****************************************************************************************
# 输入车型，燃料类型，驱动形式，   价格，车高，额定载客，排放标准，是否增压
# 循环输入，非法输入抛出异常，待补充
if flag_predict is True:
    class_pre = 347384
    fuel_pre = 1
    driven_pre = 1
    combination_pre = [10.7, 1445, 5, 1, 0]

    # 输入数据预处理
    date_pre = [date_dict[x] for x in date_pre]     # 列表解析，5*75
    # print(date_pre)
    num = len(date_pre)
    class_pre = class_dict[class_pre]
    class_pre = np.tile(class_pre, num).reshape(num, len(class_pre))
    fuel_pre = fuel_dict[fuel_pre]
    fuel_pre = np.tile(fuel_pre, num).reshape(num, len(fuel_pre))
    driven_pre = driven_dict[driven_pre]
    driven_pre = np.tile(driven_pre, num).reshape(num, len(driven_pre))
    combination_pre = (np.array(combination_pre)-epsilon)/sigma
    combination_pre = np.tile(combination_pre, num).reshape(num, len(combination_pre))
    res = nn.predict(date=date_pre,
                     classes=class_pre,
                     fuel=fuel_pre,
                     driven=driven_pre,
                     combination=combination_pre)
    print('\n预测结果：', res)


plt.show()

# np.log1p(x)
# np.expm1(x)

"""
记录：
Adam(lr=0.0005), λ=0.001, [64, 32, 9], batch_size=32, epochs=200-200, mae=0.5952，有点震荡
Adam(lr=0.0002), λ=0.001、0.01, [64, 32, 9], batch_size=32, dropout(0.2), epochs=400-400, mae=0.6103
Adam(lr=0.0002), λ=0.001、0.01, [32, 32, 16], batch_size=32, dropout(0.2), epochs=400-400, mae=0.6062
Adam(lr=0.0002), λ=0.001、0.01, [64, 16, 9], batch_size = 32, dropout(0.2), epochs=400-200, mae=0.5916
√√√Adam(lr=0.0002), λ=0.002、0.01, [64, 16, 9], batch_size = 32, dropout(0.2), epochs=400-200, mae=0.5907


学习率选择0.0002，大于此值震荡明显
正则化参数选择0.001，最后一层0.01
dropout正则化，只在第一层取0.2
"""