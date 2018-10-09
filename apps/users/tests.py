from db_tools import transformer
from db_tools import dataProcessing
import codecs
import pandas as pd
import numpy as np
from numpy.random import ranf
import time


#
#
def test():
    a = "/Users/cribbee/Downloads/raw.2.json"
    b = "/Users/cribbee/Downloads/转换完成1.csv"
    c = "/Users/cribbee/Downloads/score.csv"
    d = "/Users/cribbee/Downloads/csv2json2222.json"
#     # data = transformer.trans(d, c)
#     # #data.json2csv()
#     # data.csv2json()
#     data = dataProcessing.process(b)
#     data.step2_save(1)
#     print("ok")
#     dataProcessing.process.mkdir(floder="/Users/cribbee/Downloads/hahah")
#     print(a)
#     a = a.replace(".json", "m.ss")
#
#     print(a)

    # #  交换列的位置
    # df1 = pd.DataFrame(np.random.randn(6, 4), index=list(range(0, 12, 2)), columns=("学生", "id", "名字", "假的"))
    # print(df1)
    #
    # df_data = df1.学生
    # df = df1.drop("id", axis=1)
    # df.insert(3, "id", df_data)
    # print(df)

    #  过滤
    # df = pd.DataFrame(np.random.rand(10, 3), columns=list('abc'))
    # print(df)
    #
    # # df2 = df[(df.a < df.b) & (df.b < df.c)] #等价于 df.query('(a < b) & (b < c)')
    # df2 = df[(eval("df.a"+ a + "0.6"))]
    # print(df2)

    # # 字符串过滤
    # df = pd.DataFrame({'a': ['one', 'one', 'two', 'three', 'two', 'one', 'six'], 'b': ['x', 'y', 'y', 'x', 'y', 'x', 'x'], 'c': np.random.randn(7)})
    # print(df)
    #
    # df2 = df[~df.a.str.contains('one|three')]
    # print(df2)

    # words = ['one', 'one', 'two', 'three', 'two', 'one', 'six']
    # p = 0
    # for i in words:
    #     p=p+1

    df1 = pd.DataFrame({'语文': [100, 'A5', 'A6', 'A7'],
                        '数学': ['99', 'B1', 'B2', 'B3'],
                        '英语': ['100', 'C1', 'C2', 'C3'],
                        '化学': ['100', 'D1', 'D2', 'D3']},)

    df2 = pd.DataFrame({'语文': [100, 95, 96, 97],
                        '数学': [99, 95, 96, 97],
                        '姓名': ["小明", "闫雨", "小军", "小红"],
                        '化学': [100, 95, 96, 97],
                        '时间': [21/2017, 21/2017, 21/2017, 1],
                        '性别': ["男", "女", "男", "女"],
                        '浮点型': [21 / 2017, 21 / 2017, 21 / 2017, 21 / 2017],
                        'double': [-2.323579E-01, -2.323579E-01, -2.323579E-01, -2.323579E-01],
                        },)
    df2['时间'] = pd.to_datetime(df2['时间'])

    df3 ={"filter": [
        {
            "field_type": 0,
            "field_name": "语文",
            "filter_method": ">",
            "filter_obj": "95"
        },
        {
            "field_type": 1,
            "field_name": "姓名",
            "filter_method": "contains",
            "filter_obj": "sb"
        }

    ]}

    # print(df2)
    # for f in df3['filter']:
    #     if f['field_type'] == 0:
    #         print(f['filter_method'])
    #         print(f['filter_method'], type(f['filter_method']))
    #         str_expression = "df2['" + f['field_name'] + "']" + f['filter_method'] + f['filter_obj']
    #         df2 = df2[eval(str_expression)]
    #         print(df2)
    #     elif f['field_type'] == 1 and f['filter_method'] == "contains":
    #         df2 = df2[df2[f['field_name']].str.contains(f['filter_obj'])]
    #         print(df2)
    # # print(df2)
    # # df2 = df2[df2.eval('语文 < 数学')]
    # print(df2)
    # col_name = df2.columns.tolist()
    # print(col_name)
    # df2.insert(0,'Ordinal',np.arange(0, df2[col_name[0]].count(), 1))
    # print(df2)
    # col_name = df2.columns.tolist()
    # df2 = df2.set_index(np.arange(1, df2[col_name[0]].count()+1, 1))
    # # df2 = df2.reset_index()
    # # df2['index'] = df2.index+1
    # # df2.rename(columns={'index':'or'},inplace=True)
    # print(df2)

    # # drop删除的方法，也可以用 del (df2['语文'],df2['数学'])
    # df2.drop({'语文', '数学'}, axis=1, inplace=True)
    # print(df2)

    # 修改列名
    # df = df2.dtypes
    #
    # df3=df2.sort_values(by=["数学"],ascending=False).reset_index(inplace=False).drop('index', axis=1, inplace=False)
    # print(df3)

    # re = pd.concat([df3, df2], join='outer', axis=0,ignore_index=True,)
    # print(re)

    # #图表测试
    # print(df2)
    # string = "性别,姓名"
    # stringg = "化学,语文"
    # arr = string.split(',')
    # arrr = stringg.split(',')
    # df = df2.groupby(arr)[arrr].sum()
    # print(df)
    # #print(df.to_json(orient='columns', force_ascii=False,))

# def chart_mean(chart_type, x_axis, y_axis):
#     open_path = "/Users/cribbee/Downloads/2/Data/2213.csv"
#     df = pd.read_csv(open_path)
#
#     x_axis = x_axis.split(',')
#     y_axis = y_axis.split(',')
#     if chart_type == 1:
#         df = df.groupby(x_axis)[y_axis].mean()
#         return df
#     elif chart_type == 2:
#         df = df.groupby(x_axis)[y_axis].mean()
#         return df
#     elif chart_type == 3:
#         # 饼图
#         df = df.groupby(x_axis)[y_axis].sum()
#         i = float(df.apply(lambda x: x.sum()))
#         df['Percent'] = df[y_axis] / i
#         print(df)
#         return df









def hha():
    m = 4
    for m in range(2, m+1):
        print(m)



def chart_mean(chart_type, x_axis, y_axis):
    open_path = "/Users/cribbee/Downloads/2/Data/2213.csv"
    df = pd.read_csv(open_path)

    x_axis = x_axis.split(',')
    y_axis = y_axis.split(',')
    if chart_type == 1:
        df = df.groupby(x_axis)[y_axis].mean()
        return df
    elif chart_type == 2:
        df = df.groupby(x_axis)[y_axis].mean()
        return df
    elif chart_type == 3:

        df_sum_sum = pd.DataFrame(df[y_axis].sum()).sum().values[0]
        df_sum = pd.DataFrame(df[y_axis].sum()).T / df_sum_sum

        df = df.append(df_sum)
        print(df_sum_sum)

        print(df[y_axis])

        print(df['RANK'].dtype)


def main():
    chart_type = 3
    x_axis = ""
    y_axis = "RANK,RANK_H"
    chart_mean(chart_type, x_axis, y_axis)


if __name__ == '__main__':
    main()






