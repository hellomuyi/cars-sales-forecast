#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time   : 2021/1/4 14:20
# @Author : Jin Xuefeng
# @File   : data_processing.py
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
import numpy as np


def one_hot(x):
    """
    :param x: 输入待编码的数据(列表或一维ndarray数组)
    :return: 编码后的数据，映射关系字典
    """
    label_encoder = LabelEncoder()
    label_encoder.fit(x)
    integer_encoded = label_encoder.transform(x)  # 对原数据进行标签编码
    x_set = label_encoder.classes_
    integer_encoded_set = label_encoder.transform(x_set)  # 对原数据去重后进行标签编码

    onehot_encoder = OneHotEncoder(sparse=False, handle_unknown='ignore')
    integer_encoded = integer_encoded.reshape(len(integer_encoded), 1)
    # 对原数据在标签编码的基础上进行独热编码
    # 在这可以取余100，散列独热编码
    onehot_encoded = onehot_encoder.fit_transform(integer_encoded)
    integer_encoded_set = integer_encoded_set.reshape(len(integer_encoded_set), 1)
    # 对去重数据，在标签编码的基础上进行独热编码
    onehot_encoded_set = onehot_encoder.fit_transform(integer_encoded_set)

    # 设计字典
    x_set_dict = dict(zip(x_set, np.matrix.tolist(onehot_encoded_set)))     # 不转成列表，无法保存为txt
    return onehot_encoded, x_set_dict


def normalize(x):
    """
    :param x: 输入原数据(二维ndarray数组即矩阵，一列为一个特征)
    :return: 标准化数据，均值，标准差
    """
    epsilon = np.mean(x, axis=0)
    sigma = np.std(x, axis=0)
    x_nor = (x-epsilon)/sigma
    return x_nor, epsilon, sigma
