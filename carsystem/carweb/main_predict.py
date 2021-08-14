#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time   : 2021/1/9 16:54
# @Author : Jin Xuefeng
# @File   : predict.py
import numpy as np
from keras.models import load_model
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# 1. 输入特征
date_pre = [201709, 201612, 201711]
class_pre = 281301      # 车型
fuel_pre = 1            # 燃料类型
driven_pre = 1          # 驱动形式
combination_pre = [10.7, 1445, 5, 1, 0]     # 价格、车高、额定载客、排放标准、是否增压


# 2. 读取onehot编码字典、均值和标准差、模型信息
f = open('data/onehot_dict.txt', 'r')
onehot_dict = eval(f.read())
date_dict = onehot_dict['date']
class_dict = onehot_dict['classes']
fuel_dict = onehot_dict['fuel']
driven_dict = onehot_dict['driven']

es = np.load('data/epsilon_sigma.npy')
epsilon, sigma = es[0], es[1]

model = load_model('data/model.h5')


# 3. 检查非法输入
date_pre = np.array(date_pre)


# 4. 对输入特征预处理
# date_pre = date_dict.keys[-len-1:-1]     # 现在onehot编码截止201711
date_pre = [date_dict[x] for x in date_pre]     # 列表解析，5*75   len(date_pre)
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

# 5. 预测
res = model.predict(x=[date_pre, class_pre, fuel_pre, driven_pre, combination_pre], verbose=0)
res = np.expm1(res)     # 反平滑处理
res = np.clip(res, 0, 6284+3000)    # 数据最大值为6284
res = np.round(res)
print('\n', res)