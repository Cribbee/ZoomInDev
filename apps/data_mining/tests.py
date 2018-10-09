#_*_ coding:utf-8 _*_
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl   #显示中文
from sklearn.model_selection import train_test_split #这里是引用了交叉验证
from sklearn.linear_model import LinearRegression  #线性回归
from sklearn.preprocessing import  PolynomialFeatures
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import  r2_score
from sklearn import metrics

df2 = pd.DataFrame({'语文': [100, 95, 96, 97, 98,100, 95, 96, 97, 98],
                        '数学': [4, 8, 12, 25, 32, 43, 58, 63, 69, 79],
                        '姓名': ["小明", "闫雨", "小军", "小红", "小法","小明", "闫雨", "小军", "小红", "小法"],
                        '化学': [20, 33, 50, 56, 42, 31, 33, 46, 65, 75],
                        '时间': [21/2017, 21/2017, 21/2017, 1, 97,21/2017, 21/2017, 21/2017, 21/2017, 21/2017],
                        '性别': ["男", "女", "男", "女", "男","男", "女", "男", "女", "男"],
                        },)



def mul_lr():   #续前面代码

    df = df2
    linreg = LinearRegression()
    sns.set_style('darkgrid')
    X = df[['化学','语文']]
    print(type(X))
    print("xxxxxxx")
    print(type(df['化学']))

    y = df['数学']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=100)
    model = linreg.fit(X_train, y_train)
    # linreg.fit(X.reshape(len(X), 1), y)
    y_pred = linreg.predict(X_test)

    print("预测值：", y_pred)

    # sum_mean = 0
    # for i in range(len(y_pred)):
    #     sum_mean += (y_pred[i] - y_test.values[i]) ** 2
    #     sum_erro = np.sqrt(sum_mean / len(y_pred))  # 这个除数是你测试级的数量
    #     # calculate RMSE by hand
    #     print("RMSE by hand:", sum_erro)
    mae = mean_absolute_error(y_test, y_pred)
    print(y_test.shape)
    print(1111111)
    print(y_pred.shape)

    mse = mean_squared_error(y_test, y_pred)
    rmse = mean_squared_error(y_test, y_pred) ** 0.5
    r2 = r2_score(y_test, y_pred)


        # 做ROC曲线
    plt.rcParams['font.sans-serif'] = ['SiHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.figure()
    plt.plot(range(len(y_pred)), y_pred, 'b', label="predict")
    plt.plot(range(len(y_pred)), y_test, 'r', label="test")
    plt.legend(loc="upper right")  # 显示图中的标签
    plt.xlabel(u"哈哈")
    plt.ylabel(u"哈哈")
    plt.savefig("/Users/cribbee/Downloads/hhh.png")

    plt.show()
    p =1
    q =2
    return p,q

def mul_nlr():
    df = pd.read_csv('/Users/cribbee/Downloads/course-6-vaccine.csv',header=0)
    m = 2
    X = df['Year'].values
    y = df['Values'].values
    X = np.array(X).reshape(-1, 1)
    y = np.array(y).reshape(-1, 1)
    ylabel = "hah"
    xlabel = "sisi"

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=100)
    sns.set_style('darkgrid')


    X_train = X_train.reshape(len(X_train), 1)
    y_train = y_train.reshape(len(y_train), 1)
    X_test = X_test.reshape(len(X_test), 1)

    poly_train_x = PolynomialFeatures(degree=m, include_bias=False).fit_transform(X_train)
    poly_test_x = PolynomialFeatures(degree=m, include_bias=False).fit_transform(X_test)
    model = LinearRegression()
    model.fit(poly_train_x, y_train)
    pred_2 = model.predict(poly_test_x)

    plt.scatter(X, y, label='training points')
    plt.plot(poly_test_x, pred_2, label='m=' + str(m))
    plt.legend(loc='upper left')
    plt.tight_layout()
    plt.show()
    #
    # df = pd.read_csv('/Users/cribbee/Downloads/course-6-vaccine.csv', header=0)
    # m = 2
    # X = df[['Year']]
    # y = df['Values']
    # ylabel = "values"
    # xlabel = "year"
    #
    # lr = LinearRegression()
    # pr = LinearRegression()
    #
    #
    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=100)
    # sns.set_style('darkgrid')
    #
    # #  线性
    # lr.fit(X_train, y_train)
    # X_fit = np.arange(X.min(), X.max(), 1)[:, np.newaxis]  # X_fit是构造的预测数据,数据量大的时候是X_tain,X是训练数据
    # # X_fit = X_train
    # y_lin_fit = lr.predict(X_fit)  # 利用线性回归对构造的X_fit数据预测
    #
    # plt.xlabel(xlabel)
    # plt.ylabel(ylabel)
    # plt.scatter(X, y, label='training points')
    # plt.plot(X_fit, y_lin_fit, label='linear fit', linestyle='--')
    #
    # for m in range(2, m+1):
    #     high_order = PolynomialFeatures(degree=m)  # degress设置多项式拟合中多项式的最高次数
    #     X_m = high_order.fit_transform(X)
    #     pr.fit(X_m, y)  # X_m是训练数据,使用它进行建模得多项式系数
    #     y_m_fit = pr.predict(high_order.fit_transform(X_fit))  # 利用高次多项式对构造的X_fit数据预测
    #     plt.plot(X_fit, y_m_fit, label='m='+str(m))
    #     plt.legend(loc='upper left')
    #     plt.tight_layout()
    #
    # plt.show()




    # X_quad = poly_features.fit_transform(X)
    # X_fit = np.arange(X.min(), X.max(), 1)[:, np.newaxis]
    # print(X_fit)
    # model = model.fit(X, y)
    # y_lin_fit = model.predict(X_fit)
    #
    # linear_r2 = r2_score(y, model.predict(X))
    #
    # model = model.fit(X_quad, y)
    # y_quad_fit = model.predict(poly_features.fit_transform(X_fit))
    # quadratic_r2 = r2_score(y, model.predict(X_quad))
    #
    # plt.scatter(X, y)
    # plt.plot(X_fit, y_lin_fit,label='linear (d=1), $R^2=%.2f$' % linear_r2, color='blue', lw=2, linestyle=':')
    # plt.plot(X_fit, y_quad_fit, label='quadratic (d=2), $R^2=%.2f$' % quadratic_r2, color='red', lw=2, linestyle='-')
    #
    # plt.legend(loc='upper right')
    # plt.tight_layout()
    #
    # plt.show()


    # X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.8, random_state=100)
    #
    # X_train = X_train.reshape(1, len(X_train))
    #
    # print(type(X_train))
    # X_test = X_test.reshape(1, len(X_test))
    # y_train = y_train.reshape(1, len(y_train))
    # y_test = y_test.reshape(1, len(y_test))

def test():
    a = "jhh"
    b = "ss"
    return a,b




if __name__ == '__main__':
     # mul_nlr()
     # mul_lr()

    # print(np.arange(1,10,0.7)[:, np.newaxis])
    print(len(test()))




