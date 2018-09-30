# -*- coding: utf-8 -*-
__author__ = 'Cribbee'
__create_at__ = 2018 / 9 / 29
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl   #显示中文
from sklearn.model_selection import train_test_split #这里是引用了交叉验证
from sklearn.linear_model import LinearRegression  #线性回归
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import  PolynomialFeatures
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import  r2_score
from sklearn import metrics

def mul_nlr():

    df = pd.read_csv('/Users/cribbee/Downloads/course-6-vaccine.csv', header=0)
    m = 5
    X = df[['Year']]
    y = df['Values']
    ylabel = "values"
    xlabel = "year"
    sns.set_style('darkgrid')

    lr = LinearRegression()
    pr = LinearRegression()

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=100)
    X_train = X_train.sort_values(by='Year', ascending=True)
    X_test = X_test.sort_values(by='Year', ascending=True)
    y_train = y_train.sort_values(ascending=True)
    y_test = y_test.sort_values(ascending=True)



    #  线性
    lr.fit(X_train, y_train)
    #  X_fit = np.arange(X.min(), X.max(), 1)[:, np.newaxis]  # X_fit是构造的预测数据,数据量大的时候是X_tain,X是训练数据
    X_fit = X_train
    y_lin_fit = lr.predict(X_test)

    plt.rcParams['font.sans-serif'] = ['SiHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.figure()
    plt.subplots(1, 1, figsize=(10, 5))
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.scatter(X, y, label='training points')
    plt.plot(X_test, y_lin_fit, label='linear fit', linestyle='--')

    for m in range(2, m+1):
        high_order = PolynomialFeatures(degree=m, include_bias=False)  # degress设置多项式拟合中多项式的最高次数
        # 真实预测
        X_m = high_order.fit_transform(X_fit)
        pr.fit(X_m, y_train)  # X_m是训练数据,使用它进行建模得多项式系数
        y_m_fit = pr.predict(high_order.transform(X_test))  # 利用高次多项式对构造的X_fit数据预测

        #  画图看趋势
        # X_m = high_order.fit_transform(X_fit)
        # pr.fit(X_m, y_train)  # X_m是训练数据,使用它进行建模得多项式系数
        # y_m_fit = pr.predict(high_order.fit_transform(X_fit))  # 利用高次多项式对构造的X_fit数据预测

        # error_sum = mean_absolute_error(y_test, y_m_fit)
        # print(error_sum)

        plt.plot(X_test, y_m_fit, label='m='+str(m))
        plt.legend(loc='upper left')
        plt.tight_layout()
    plt.show()

    mse = []
    mse_show = []
    pic = []
    m = 1
    mth_power = 5
    m_max = 20
    plt.subplots(1, 1, figsize=(10, 5))
    while m <= m_max:
        model = make_pipeline(PolynomialFeatures(m, include_bias=False), LinearRegression())
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        mse.append(mean_squared_error(y_test, y_pred.flatten()))
        mse_show.append("m="+str(m)+", mse="+str(mse[m-1]))

        if m <= mth_power:
            pic.append(plt.scatter(m, mse[m-1], s=60))

        m = m + 1

    plt.plot([i for i in range(1, m_max + 1)], mse, 'r')
    plt.scatter([i for i in range(mth_power+1, m_max + 1)], mse[mth_power:], c='black', marker='x', s=55)
    plt.legend((pic), (mse_show[0:mth_power]))
    plt.xlabel('m')
    plt.ylabel('MSE')
    plt.show()


def mul_nlr2():

    df = pd.read_csv('/Users/cribbee/Downloads/course-6-vaccine.csv', header=0)
    m = 2
    X = df[['Year']].values
    y = df['Values'].values

    ylabel = "values"
    xlabel = "year"

    lr = LinearRegression()
    pr = LinearRegression()

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=100)
    sns.set_style('darkgrid')

    high_order = PolynomialFeatures(degree=m, include_bias=False)
    poly_train_x_2 = high_order.fit_transform(X_train.reshape(len(X_train), 1))
    X_fit = high_order.fit_transform(X_test.reshape(len(X_test), 1))

    pr.fit(poly_train_x_2, y_train.reshape(len(X_train), 1))
    y_m_fit = pr.predict(high_order.fit_transform(X_fit))
    plt.plot(X_fit, y_m_fit, label='m=' + str(m))
    plt.legend(loc='upper left')
    plt.tight_layout()
    plt.show()











if __name__ == '__main__':
     mul_nlr()