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
from sklearn.cluster import k_means,MiniBatchKMeans
from sklearn.metrics import silhouette_score


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
            plt.subplots(1, 1, figsize=(11, 5.5))
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
            plt.subplots(1, 1, figsize=(10, 5))
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

    def clustering(self, title, category,k_clustering,Datacsv_list, random_state, max_iter,batch_size , n_init,reassignment_ratio):
        df = pd.read_csv(self.open_path, header=0)
        chart_folder_re = self.upload_folder + title + ".png"
        chart_folder_err_re = self.upload_folder + title + "error.png"

        chart_folder = self.dir_folder + title + ".png"
        chart_folder_err = self.dir_folder + title + "error.png"
        f, ax = plt.subplots(figsize=(15, 10))

        list = Datacsv_list.split(',')
        # 判断是几维数据
        if len(list) == 1:  # 1维数据
            data = df[list[0]].values.reshape(-1, 1)
            print(data)
            if category == 13:

                km = k_means(data, n_clusters=k_clustering, random_state=random_state,n_init = n_init , max_iter = max_iter)
                df['categery'] = km[1]  # 添加聚类列为category列
                new_data = df[[list[0], 'categery']]  # 得到中考总分和聚类标签

                # *****
                # if error_type == 1:  # 分布密度散点图
                sns.swarmplot(x=new_data[list[0]])  # 带分布密度的散点图
                chart_folder1_err_re = self.upload_folder + title +"1.png"
                chart_folder1_err = self.dir_folder + title +"1.png"
                plt.savefig(chart_folder1_err)
                plt.savefig(chart_folder1_err_re)
                plt.cla()

                # elif error_type == 2:  # 计数统计图
                sns.countplot(x="categery", data=new_data)  # 计数统计图:每个类别分别有多少人
                chart_folder2_err_re = self.upload_folder + title + "2.png"
                chart_folder2_err = self.dir_folder + title  + "2.png"
                plt.savefig(chart_folder2_err)
                plt.savefig(chart_folder2_err_re)
                plt.cla()

                # elif error_type == 3:  # 小提琴图
                sns.violinplot(x="categery", y=list[0], data=new_data, palette="muted")  # 小提琴图
                chart_folder3_err_re = self.upload_folder + title  + "3.png"
                chart_folder3_err = self.dir_folder + title  + "3.png"
                plt.savefig(chart_folder3_err)
                plt.savefig(chart_folder3_err_re)
                plt.cla()

                sse = []  # 手肘法则
                lunkuo = []  # 轮廓系数存放距离
                start, end = 3, 15
                for i in range(start, end):
                    km = k_means(data, n_clusters=i, random_state=80)
                    sse.append(km[2])
                    lunkuo.append(silhouette_score(data, km[1], metric='euclidean'))
                fig, ax1 = plt.subplots(figsize=(10, 7))
                ax2 = ax1.twinx()
                lns1 = ax1.plot(range(start, end), sse, 'o-', c='g', label='zhou-bu')
                lns2 = ax2.plot(range(start, end), lunkuo, 'o-', c='r', label='lun-kuo')
                new_ticks = np.linspace(start, end, end - start + 1)
                plt.xticks(new_ticks)
                lns = lns1 + lns2
                labs = [l.get_label() for l in lns]
                ax1.legend(lns, labs, loc=0)
                ax1.set_xlabel('K')
                ax1.set_ylabel('SSE')
                ax2.set_ylabel('LUN-KUO-INDEX')

                plt.savefig(chart_folder)
                plt.savefig(chart_folder_re)
                plt.cla()
                return chart_folder, chart_folder1_err,chart_folder2_err,chart_folder3_err

            #MiniBatch, random_state=random_state,n_init = n_init , max_iter = max_iter,batch_size=batch_size,reassignment_ratio=reassignment_ratio
            if category == 14:
                mbk = MiniBatchKMeans(n_clusters=k_clustering, random_state=random_state,n_init = n_init , max_iter = max_iter,batch_size=batch_size,reassignment_ratio=reassignment_ratio)
                mbk.fit(data)
                df['categery'] = mbk.labels_  # 添加聚类列为category列
                new_data = df[[list[0], 'categery']]  # 得到中考总分和聚类标签

                # *****
                # if error_type == 1:  # 分布密度散点图
                sns.swarmplot(x=new_data[list[0]])  # 带分布密度的散点图
                chart_folder1_err_re = self.upload_folder + title  + "1.png"
                chart_folder1_err = self.dir_folder + title  + "1.png"
                plt.savefig(chart_folder1_err)
                plt.savefig(chart_folder1_err_re)
                plt.cla()

                # elif error_type == 2:  # 计数统计图
                sns.countplot(x="categery", data=new_data)  # 计数统计图:每个类别分别有多少人
                chart_folder2_err_re = self.upload_folder + title + "2.png"
                chart_folder2_err = self.dir_folder + title + "2.png"
                plt.savefig(chart_folder2_err)
                plt.savefig(chart_folder2_err_re)
                plt.cla()

                # elif error_type == 3:  # 小提琴图
                sns.violinplot(x="categery", y=list[0], data=new_data, palette="muted")  # 小提琴图
                chart_folder3_err_re = self.upload_folder + title  + "3.png"
                chart_folder3_err = self.dir_folder + title  + "3.png"
                plt.savefig(chart_folder3_err)
                plt.savefig(chart_folder3_err_re)
                plt.cla()

                sse = []  # 手肘法则
                lunkuo = []  # 轮廓系数存放距离
                start, end = 3, 15
                for i in range(start, end):
                    km = k_means(data, n_clusters=i, random_state=80)
                    sse.append(km[2])
                    lunkuo.append(silhouette_score(data, km[1], metric='euclidean'))
                fig, ax1 = plt.subplots(figsize=(10, 7))
                ax2 = ax1.twinx()
                lns1 = ax1.plot(range(start, end), sse, 'o-', c='g', label='zhou-bu')
                lns2 = ax2.plot(range(start, end), lunkuo, 'o-', c='r', label='lun-kuo')
                new_ticks = np.linspace(start, end, end - start + 1)
                plt.xticks(new_ticks)
                lns = lns1 + lns2
                labs = [l.get_label() for l in lns]
                ax1.legend(lns, labs, loc=0)
                ax1.set_xlabel('K')
                ax1.set_ylabel('SSE')
                ax2.set_ylabel('LUN-KUO-INDEX')

                plt.savefig(chart_folder)
                plt.savefig(chart_folder_re)
                plt.cla()
                return chart_folder, chart_folder1_err, chart_folder2_err, chart_folder3_err



        # *******二维数据
        elif len(list) == 2:  # 2维数据

            X = df[list[0]]
            Y = df[list[1]]
            data = np.column_stack((X, Y))
            if category == 13:
                km = k_means(data, n_clusters=k_clustering, random_state=10)
                df['categery'] = km[1]  # 添加聚类列为category列
                new_data = df[[list[0], list[1], 'categery']]  # 得到中考总分和聚类标签

                # if error_type == 4:  # 二维的散点图
                plt.scatter(data[:, 0], data[:, 1], s=20, c=df['categery'])  # c是标签
                chart_folder4_err = self.dir_folder + title  + "4.png"
                chart_folder4_err_re = self.dir_folder + title  + "4.png"
                plt.savefig(chart_folder4_err)
                plt.savefig(chart_folder4_err_re)
                plt.cla()


                sse = []  # 手肘法则
                lunkuo = []  # 轮廓系数存放距离
                start, end = 3, 15
                for i in range(start, end):
                    km = k_means(data, n_clusters=i, random_state=random_state)
                    sse.append(km[2])
                    lunkuo.append(silhouette_score(data, km[1], metric='euclidean'))
                print(km[1])
                print(sse)
                fig, ax1 = plt.subplots(figsize=(10, 7))
                ax2 = ax1.twinx()
                lns1 = ax1.plot(range(start, end), sse, 'o-', c='g', label='zhou-bu')
                lns2 = ax2.plot(range(start, end), lunkuo, 'o-', c='r', label='lun-kuo')
                new_ticks = np.linspace(start, end, end - start + 1)
                plt.xticks(new_ticks)
                lns = lns1 + lns2
                labs = [l.get_label() for l in lns]
                ax1.legend(lns, labs, loc=0)
                ax1.set_xlabel('K')

                ax1.set_ylabel('SSE')
                ax2.set_ylabel('LUN-KUO-INDEX')
                plt.savefig(chart_folder)
                plt.savefig(chart_folder_re)
                plt.cla()
                return chart_folder, chart_folder4_err

            if category == 14:
                mbk = MiniBatchKMeans(n_clusters=k_clustering, random_state=random_state, n_init=n_init,
                                      max_iter=max_iter, batch_size=batch_size, reassignment_ratio=reassignment_ratio)
                mbk.fit(data)
                df['categery'] = mbk.labels_  # 添加聚类列为category列
                new_data = df[[list[0], 'categery']]  # 得到中考总分和聚类标签


                # if error_type == 4:  # 二维的散点图
                plt.scatter(data[:, 0], data[:, 1], s=20, c=df['categery'])  # c是标签
                chart_folder4_err = self.dir_folder + title  + "4.png"
                chart_folder4_err_re = self.dir_folder + title  + "4.png"
                plt.savefig(chart_folder4_err)
                plt.savefig(chart_folder4_err_re)
                plt.cla()


                sse = []  # 手肘法则
                lunkuo = []  # 轮廓系数存放距离
                start, end = 3, 15
                for i in range(start, end):
                    km = k_means(data, n_clusters=i, random_state=random_state)
                    sse.append(km[2])
                    lunkuo.append(silhouette_score(data, km[1], metric='euclidean'))
                print(km[1])
                print(sse)
                fig, ax1 = plt.subplots(figsize=(10, 7))
                ax2 = ax1.twinx()
                lns1 = ax1.plot(range(start, end), sse, 'o-', c='g', label='zhou-bu')
                lns2 = ax2.plot(range(start, end), lunkuo, 'o-', c='r', label='lun-kuo')
                new_ticks = np.linspace(start, end, end - start + 1)
                plt.xticks(new_ticks)
                lns = lns1 + lns2
                labs = [l.get_label() for l in lns]
                ax1.legend(lns, labs, loc=0)
                ax1.set_xlabel('K')

                ax1.set_ylabel('SSE')   
                ax2.set_ylabel('LUN-KUO-INDEX')
                plt.savefig(chart_folder)
                plt.savefig(chart_folder_re)
                plt.cla()
                return chart_folder, chart_folder4_err




