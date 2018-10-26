# -*- coding: utf-8 -*-
__author__ = 'Cribbee'
__create_at__ = 2018 / 9 / 14

import codecs
import csv
import json
import os
import logging
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split #这里是引用了交叉验证
from sklearn.linear_model import LinearRegression  #线性回归
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import  r2_score
import pandas as pd
import seaborn as sns
import numpy as np
from numpy import nan as NaN
import matplotlib.pyplot as plt


class Process():

    def __init__(self, open_path, dir_folder, upload_folder):
        self.open_path = open_path
        self.dir_folder = dir_folder + "/Publish/"
        self.upload_folder = upload_folder

    def regression(self, title, category, x_axis, y_axis, xlabel, ylabel, test_size, mth_power, error_type, ):
        df = pd.read_csv(self.open_path)
        X = df[[x_axis]]
        y = df[y_axis]
        chart_folder_re = self.upload_folder + title + ".png"
        chart_folder_err_re = self.upload_folder + title + "error.png"

        chart_folder = self.dir_folder + title + ".png"
        chart_folder_err = self.dir_folder + title + "error.png"
        sns.set_style('darkgrid')
        if category == 11:  #线性回归
            linreg = LinearRegression()
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=100)
            model = linreg.fit(X_train, y_train)
            y_pred = linreg.predict(X_test)

            # 做ROC曲线
            plt.rcParams['font.sans-serif'] = ['SiHei']
            plt.rcParams['axes.unicode_minus'] = False
            plt.figure()
            plt.rcParams['figure.dpi'] = 300  # 分辨率
            # plt.plot(range(len(y_pred)), y_pred, 'b', label="predict")
            # plt.plot(range(len(y_pred)), y_test, 'r', label="test")
            plt.scatter(X, y, label='training points')
            linear_r2 = r2_score(y_test, y_pred)
            plt.plot(X_test, y_pred, color='r', label='linear fit, $R^2=%.2f$' % linear_r2)
            plt.legend(loc="upper left")  # 显示图中的标签
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.savefig(chart_folder)
            plt.savefig(chart_folder_re)
            # plt.show()

            if error_type == 1:
                #  MSE
                error_sum = mean_squared_error(y_test, y_pred)
                return error_sum, chart_folder
            elif error_type == 2:
                #  MAE
                error_sum = mean_absolute_error(y_test, y_pred)
                return error_sum, chart_folder
            elif error_type == 3:
                # RMSE
                error_sum = mean_squared_error(y_test, y_pred) ** 0.5
                return error_sum, chart_folder
            # elif error_type == 4:
            #     # R2
            #     error_sum = r2_score(y_test, y_pred)
            #     return error_sum, chart_folder_re, chart_folder

        elif category == 12:  #非线性回归

            m = mth_power
            lr = LinearRegression()
            pr = LinearRegression()

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=100)

            X_train = X_train.sort_values(by=x_axis, ascending=True)
            X_test = X_test.sort_values(by=x_axis, ascending=True)
            y_train = y_train.sort_values(ascending=True)
            y_test = y_test.sort_values(ascending=True)

            #  线性
            lr.fit(X_train, y_train)
            X_fit = X_train
            y_lin_fit = lr.predict(X_test)  # 利用线性回归对构造的X_fit数据预测

            plt.rcParams['font.sans-serif'] = ['SiHei']
            plt.rcParams['axes.unicode_minus'] = False
            plt.figure()
            plt.rcParams['figure.dpi'] = 300  # 分辨率
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.scatter(X, y, label='training points')
            plt.plot(X_test, y_lin_fit, label='linear fit', linestyle='--')

            for m in range(2, m + 1):
                high_order = PolynomialFeatures(degree=m, include_bias=False)
                x_m = high_order.fit_transform(X)
                pr.fit(x_m, y)
                y_m_fit = pr.predict(high_order.fit_transform(X_fit))
                plt.plot(X_fit, y_m_fit, label='m=' + str(m))
                plt.legend(loc='upper left')
                plt.tight_layout()

            plt.savefig(chart_folder)
            plt.savefig(chart_folder_re)

            error_sum = []
            error_sum_show = []
            pic = []
            n = 1
            n_max = 20
            plt.subplots(1, 1, figsize=(10, 5))
            while n <= n_max:
                model = make_pipeline(PolynomialFeatures(n, include_bias=False), LinearRegression())
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                if error_type == 1:
                    #  MSE
                    error_sum.append(mean_squared_error(y_test, y_pred.flatten()))
                    error_sum_show.append("m=" + str(n) + ", MSE=" + str(error_sum[n - 1]))
                    plt.xlabel('m')
                    plt.ylabel('MSE')
                elif error_type == 2:
                    #  MAE
                    error_sum.append(mean_absolute_error(y_test, y_pred.flatten()))
                    error_sum_show.append("m=" + str(n) + ", MAE=" + str(error_sum[n - 1]))
                    plt.xlabel('m')
                    plt.ylabel('MAE')
                elif error_type == 3:
                    # RMSE
                    error_sum.append(mean_squared_error(y_test, y_pred.flatten()) ** 0.5)
                    error_sum_show.append("m=" + str(n) + ", RMSE=" + str(error_sum[n - 1]))
                    plt.xlabel('m')
                    plt.ylabel('RMSE')
                elif error_type == 4:
                    #  R2
                    error_sum.append(r2_score(y_test, y_pred.flatten()))
                    error_sum_show.append("m=" + str(n) + ", R2_SCORE=" + str(error_sum[n - 1]))
                    plt.xlabel('m')
                    plt.ylabel('R2_SCORE')

                if n <= mth_power:
                    pic.append(plt.scatter(n, error_sum[n - 1], s=60))
                n = n + 1

            plt.plot([i for i in range(1, n_max + 1)], error_sum, 'r')
            plt.scatter([i for i in range(mth_power + 1, n_max + 1)], error_sum[mth_power:], c='black', marker='x', s=55)
            plt.legend((pic), (error_sum_show[0:mth_power]))
            plt.savefig(chart_folder_err)
            plt.savefig(chart_folder_err_re)

            return chart_folder_re, chart_folder_err_re, chart_folder, chart_folder_err


