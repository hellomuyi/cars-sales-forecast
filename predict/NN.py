#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time   : 2021/1/4 8:47
# @Author : Jin Xuefeng
# @File   : NN.py
from keras.layers import Input, Dense, Dropout, Lambda, Concatenate, Activation, LeakyReLU
from keras.models import Sequential, Model
from keras.optimizers import Adam
from keras.regularizers import l2
import keras.backend as K
import numpy as np
import matplotlib.pyplot as plt
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


class NN:
    def __init__(self, date_dim, class_dim, fuel_dim, driven_dim, combination_dim=5, layers=[64, 64]):
        self.date_dim = date_dim
        self.class_dim = class_dim
        self.fuel_dim = fuel_dim
        self.driven_dim = driven_dim
        self.combination_dim = combination_dim
        self.layers = layers

        optimizer = Adam(lr=0.0002)     # 学习率
        self.model = self.build_model()
        self.model.compile(loss='mse',
                           optimizer=optimizer,
                           metrics=['mae'])
        print('model.summary():')
        self.model.summary()

    def build_model(self):
        """构建网络"""
        date = Input(shape=(self.date_dim,))
        classes = Input(shape=(self.class_dim,))
        fuel = Input(shape=(self.fuel_dim,))
        driven = Input(shape=(self.driven_dim,))
        combination = Input(shape=(self.combination_dim,))
        inputs = Concatenate()([date, classes, fuel, driven, combination])
        inputs_dim = self.date_dim + self.class_dim + self.fuel_dim + self.driven_dim + self.combination_dim

        if len(self.layers) <= 0:  # 无隐含层
            outputs = Dense(1, input_shape=(inputs_dim,), activation='relu',
                            kernel_regularizer=l2(0.001))(inputs)    # 采用L2正则化
        else:     # 有隐含层
            outputs = Dense(self.layers[0], input_shape=(inputs_dim,),
                            kernel_regularizer=l2(0.002))(inputs)
            outputs = Activation('relu')(outputs)
            # outputs = LeakyReLU(alpha=0.3)(outputs)     # 高层激活函数
            outputs = Dropout(0.2)(outputs)  # dropout正则化
            for layer in self.layers[1:]:
                outputs = Dense(layer, kernel_regularizer=l2(0.002))(outputs)
                outputs = Activation('relu')(outputs)
                # outputs = LeakyReLU(alpha=0.3)(outputs)  # 高层激活函数
                # outputs = Dropout(0.1)(outputs)
            outputs = Dense(1, activation='relu', kernel_regularizer=l2(0.01))(outputs)
            # outputs = Lambda(lambda x: K.round(x))(outputs)  # 销量是整数，会导致没有梯度
        return Model(inputs=[date, classes, fuel, driven, combination], outputs=outputs)

    def build_model_old(self):
        model = Sequential()    # 序贯模型
        if len(self.layers) <= 0:    # 无隐含层
            model.add(Dense(1, input_shape=(self.x_dim, ), kernel_regularizer=l2(0.001)))  # 默认线性激活函数
            model.add(Dropout(0.2))     # dropout正则化
        else:
            model.add(Dense(self.layers[0], input_shape=(self.x_dim, ), activation='relu'))
            model.add(Dropout(0.2))  # dropout正则化
            for layer in self.layers[1:]:
                model.add(Dense(layer))
                model.add(Activation('relu'))
            model.add(Dense(1))     # 默认线性激活函数
        return model

    def train(self, date, classes, fuel, driven, combination, sale_q, validation_split=0.25, epochs=200, batch_size=64):
        """训练网络并验证调参、防止过拟合"""
        history = self.model.fit(x=[date, classes, fuel, driven, combination],
                                 y=sale_q,
                                 validation_split=validation_split,
                                 epochs=epochs,
                                 batch_size=batch_size,
                                 verbose=2).history
        if validation_split:
            train_loss, val_loss = history['loss'], history['val_loss']
            train_mae, val_mae = history['mean_absolute_error'], history['val_mean_absolute_error']

            # 画图
            epochs = range(1, len(train_loss) + 1)
            plt.close("all")
            plt.ion()   # 切换至交互模式
            fig = plt.figure()
            ax1 = plt.subplot(121)
            ax2 = plt.subplot(122)
            ax1.grid()
            ax2.grid()
            plt.tight_layout()
            # plt.subplots_adjust(left=0.08, bottom=0.09, right=0.95, top=0.96, wspace=0.01, hspace=0.1)
            ax1.plot(epochs, train_loss, 'b', label='training loss')
            ax1.plot(epochs, val_loss, 'r', label='validation loss')
            ax1.legend()
            ax1.set_xlabel('epochs')
            ax1.set_ylabel('loss')
            ax1.set_title('training and validation loss')
            ax2.plot(epochs, train_mae, 'b', label='training mae')
            ax2.plot(epochs, val_mae, 'r', label='validation_mae')
            ax2.legend()
            ax2.set_xlabel('epochs')
            ax2.set_ylabel('mae')
            ax2.set_title('training and validation mae')
            plt.ioff()
        # 可以返回模型
        return self.model

    def test(self, date, classes, fuel, driven, combination, sale_q):
        """在测试集上进行测试"""
        test_res = self.model.evaluate(x=[date, classes, fuel, driven, combination],
                                       y=sale_q,
                                       batch_size=64,
                                       verbose=0)
        # 这里输出loss和metrics
        print('\n测试集结果：')
        print('%s:%.3f\n%s:%.3f'
              % (self.model.metrics_names[0], test_res[0], self.model.metrics_names[1], test_res[1]))

        # 反平滑后看看
        sale_q_test_pre = self.model.predict(x=[date, classes, fuel, driven, combination], verbose=0)
        sale_q_test_pre = np.expm1(sale_q_test_pre)
        sale_q = np.expm1(sale_q)
        res = np.clip(sale_q_test_pre, 0, 2260 + 2000)  # 数据最大值为2260
        res = np.round(res)
        # print(sale_q_test_pre.shape, sale_q.shape)  # (2017,1) (2017,)，并不是你想当然那样的广播法则
        mae = np.sum(np.fabs(sale_q_test_pre-sale_q.reshape(len(sale_q), 1)))/len(sale_q)
        # print('mae:', mae)
        return test_res

    def predict(self, date, classes, fuel, driven, combination):
        """输入维度，进行预测"""
        predict_res = self.model.predict(x=[date, classes, fuel, driven, combination], verbose=0)
        predict_res = np.expm1(predict_res)     # 反平滑处理
        predict_res = np.clip(predict_res, 0, 6284+3000)    # 数据最大值为6284
        predict_res = np.round(predict_res)
        return predict_res
