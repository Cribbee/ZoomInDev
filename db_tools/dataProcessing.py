# -*- coding: utf-8 -*-
__author__ = 'Cribbee'
__create_at__ = 2018 / 6 / 4

import codecs
import csv
import json
import os
import logging

import pandas as pd
import numpy as np
from numpy import nan as NaN
from datetime import datetime

from scipy import stats
from scipy.stats import norm
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import linear_model
from matplotlib.font_manager import FontProperties


class process():

    def __init__(self, open_path):
        self.open_path = open_path

    @staticmethod
    def mkdir(floder):
        os.mkdir(floder)
        os.mkdir(floder + "/Data")
        os.mkdir(floder + "/Publish")
        os.mkdir(floder + "/Log")

    def original_save(self, jsondata):
        with codecs.open(self.open_path, 'w', 'utf-8') as f:
            f.writelines(json.dumps(jsondata, separators=(',', ':'), ensure_ascii=False))

    def step2_save(self, row_num):

        data = codecs.open(self.open_path, 'r', 'utf-8').readlines()
        data[0:row_num] = ''
        with codecs.open(self.open_path, 'w', 'utf-8') as f:
            f.writelines(data)

    def step3_save(self, write_path):

        data = codecs.open(self.open_path, 'r', 'utf-8').readlines()
        with codecs.open(write_path, 'w', 'utf-8') as f:
            f.writelines(data)

    def stepX1_save(self, open_path, write_path):
        df = pd.read_csv(open_path)
        Columns_name = df.columns.values.tolist()
        new_df = pd.DataFrame(columns=Columns_name, index=['字段类型', '字段描述', '源文件列名', '平均值', '方差', '标准差'])
        for i in Columns_name:
            new_df.loc['字段类型', i] = df[i].dtypes
            new_df.loc['源文件列名', i] = i
        new_df.to_csv(write_path, index_label=False)

    # def missing_data(self,**kwargs):
    #     self.allow_blan = kwargs.pop('allow_blank', False)
    #     self.trim_whitespace = kwargs.pop('trim_whitespace', True)
    #     self.max_length = kwargs.pop('max_length', None)
    #     self.min_length = kwargs.pop('min_length', None)

    def missing_value(self, axis, how):
        df = pd.read_csv(self.open_path)
        dfd = df.dropna(axis=axis, how=how)
        path = self.open_path.replace(".csv", "m.csv")
        dfd.to_csv(path, index_label=False)

    # 可优化为单步一次性处理
    def filter_processing(self, logical_type, filter):
        logger = logging.getLogger('django')
        df = pd.read_csv(self.open_path)

        # "与"的判断逻辑
        if logical_type == "&":
            for f in filter:
                if f['field_type'] == 0:
                    str_expression = "df['" + f['field_name'] + "']" + f['filter_method'] + f['filter_obj']
                    logger.debug("LogDebug<""str_expression : " + str_expression + ">")
                    df = df[eval(str_expression)]

                elif f['field_type'] == 1 and f['filter_method'] == "contains":
                    df = df[df[f['field_name']].str.contains(f['filter_obj'])]
                elif f['field_type'] == 1 and f['filter_method'] == "notContains":
                    df = df[~df[f['field_name']].str.contains(f['filter_obj'])]
                elif f['field_type'] == 1 and f['filter_method'] == "isNull":
                    df = df[df[f['field_name']].notnull]
                elif f['field_type'] == 1 and f['filter_method'] == "notNull":
                    df = df[df[f['field_name']].isnull]
            path = self.open_path
            df.to_csv(path, index_label=False, index=0)
            logger.debug("LogDebug<""logical_type : 与>")
        # "或"的判断逻辑
        elif logical_type == "|":
            df_merger = []
            count = 0
            for f in filter:
                if f['field_type'] == 0:
                    str_expression = "df['" + f['field_name'] + "']" + f['filter_method'] + f['filter_obj']
                    # df_merger[] = df[eval(str_expression)]
                    df_merger.append(df[eval(str_expression)])
                    count += 1
                elif f['field_type'] == 1 and f['filter_method'] == "contains":
                    df_merger.append(df[df[f['field_name']].str.contains(f['filter_obj'])])
                    count += 1
                elif f['field_type'] == 1 and f['filter_method'] == "notContains":
                    df_merger.append(df[~df[f['field_name']].str.contains(f['filter_obj'])])
                    count += 1
                elif f['field_type'] == 1 and f['filter_method'] == "isNull":
                    df_merger.append(df[df[f['field_name']].notnull])
                    count += 1
                elif f['field_type'] == 1 and f['filter_method'] == "notNull":
                    df_merger.append(df[df[f['field_name']].isnull])
                    count += 1
            # accumulate,then remove replicated
            i = 0
            dfs = pd.DataFrame(None)
            while i < count:
                dfs = pd.concat([dfs, df_merger[i]], join='outer', axis=0, ignore_index=True, )
                i += 1
            path = self.open_path
            df.to_csv(path, index_label=False, index=0)

    # 在指定位置增加序号列
    def set_index(self):
        df = pd.read_csv(self.open_path)
        df = df.set_index(np.arange(0, df[0].count(), 1))
        # df['index'] = df.index + 1
        # df.rename(columns={'index': col_name}, inplace=True)
        path = self.open_path.replace(".csv", "i.csv")
        df.to_csv(path)

    # 字段排序
    def sorting(self, col_name, ascending):
        df = pd.read_csv(self.open_path)
        df = df.sort_values(by=[col_name], ascending=ascending).reset_index(inplace=False).drop('index', axis=1,
                                                                                                inplace=False)
        df.to_csv(self.open_path, index_label=False)

    # 批量删除列
    def drop(self, drop, stepX_path):
        df = pd.read_csv(self.open_path)
        df_X = pd.read_csv(stepX_path)
        for delete in drop:
            df.drop(delete['field'], axis=1, inplace=True)
            df_X.drop(delete['field'], axis=1, inplace=True)
        path = self.open_path.replace(".csv", "d.csv")
        df.to_csv(path, index_label=False)
        df_X.to_csv(stepX_path, index_label=False)

    # 批量修改列名
    def reset_columns(self, reset, stepX_path):
        df = pd.read_csv(self.open_path)
        df_X = pd.read_csv(stepX_path)
        for rs in reset:
            df.rename(columns={rs['original_col']: rs['new_col']}, inplace=True)
            df_X.rename(columns={rs['original_col']: rs['new_col']}, inplace=True)
        # path = self.open_path.replace(".csv", "r.csv")
        df.to_csv(self.open_path, index_label=False, index=0)
        df_X.to_csv(stepX_path, index_label=False)

    # 展示数据集字段名与字段类型
    def show_dtypes(self):
        df = pd.read_csv(self.open_path)
        dtypes = df.loc['字段类型']
        return dtypes

    # 展示字段描述
    def show_desc(self):
        df = pd.read_csv(self.open_path)
        desc = df.loc['字段描述'].fillna('')
        return desc

    # 展示原文件列名
    def show_OriginColumnsName(self):
        df = pd.read_csv(self.open_path)
        Columns_name = df.loc['源文件列名']
        return Columns_name

    # 修改字段描述
    def changeDesc(self, data):
        df_X = pd.read_csv(self.open_path)
        for i in data:
            df_X.loc['字段描述', i['field']] = i['desc']
        df_X.to_csv(self.open_path, index_label=False)

    # 求和函数sum，操作两列，并在末尾生成新一列
    def sum(self, a, b, col_new, stepX_path):
        df = pd.read_csv(self.open_path)
        df_X = pd.read_csv(stepX_path)
        df.eval(col_new + "=" + a + "+" + b, inplace=True)
        df_X[col_new] = [df[col_new].dtype, str(a + "+" + b), col_new, '', '', '']
        df.to_csv(self.open_path, index_label=False, index=0)
        df_X.to_csv(stepX_path, index_label=False)

    # 求差函数sub
    def sub(self, a, b, col_new, stepX_path):
        df = pd.read_csv(self.open_path)
        df_X = pd.read_csv(stepX_path)
        df.eval(col_new + "=" + a + "-" + b, inplace=True)
        print(df[col_new].dtype)
        df_X[col_new] = [df[col_new].dtype, str(a + "-" + b), col_new, '', '', '']
        df.to_csv(self.open_path, index_label=False, index=0)
        df_X.to_csv(stepX_path, index_label=False)

    # 计算平均值、方差、标准差
    def average(self, data, stepX_path):
        df = pd.read_csv(self.open_path)
        df_X = pd.read_csv(stepX_path)
        average = {}
        for i in data:
            mean1 = df[i['field']].mean()
            df_X.loc['平均值', i['field']] = mean1
            average[i['field']] = mean1
        df_X.to_csv(stepX_path, index_label=False)
        return average

    # 求方差
    def var(self, data, stepX_path):
        df = pd.read_csv(self.open_path)
        df_X = pd.read_csv(stepX_path)
        var = {}
        for i in data:
            var1 = df[i['field']].var()
            df_X.loc['方差', i['field']] = var1
            var[i['field']] = var1
        df_X.to_csv(stepX_path, index_label=False)
        return var

    # 求标准差
    def std(self, data, stepX_path):
        df = pd.read_csv(self.open_path)
        df_X = pd.read_csv(stepX_path)
        std = {}
        for i in data:
            std1 = df[i['field']].std()
            df_X.loc['标准差', i['field']] = std1
            std[i['field']] = std1
        df_X.to_csv(stepX_path, index_label=False)
        return std

    # 修改字段类型
    def changeType(self, data, stepX_path):
        df = pd.read_csv(self.open_path)
        df_X = pd.read_csv(stepX_path)
        for i in data:
            df[i['field']] = df[i['field']].astype(i['type'])
            df_X.loc['字段类型', i['field']] = i['type']
        df.to_csv(self.open_path, index_label=False, index=0)
        df_X.to_csv(stepX_path, index_label=False)

    # 测试该字段是否含有违规行，若有则报违规率，若无则直接修改类型
    def test_changeType(self, data, stepX_path):
        df = pd.read_csv(self.open_path)
        df_X = pd.read_csv(stepX_path)
        total = len(df)
        result = {}
        for i in data:
            if df_X.loc['字段类型', i['field']] == 'object' and i['type'] == 'float64':
                num = 0
                for k in df[i['field']]:
                    try:
                        number = float(k)
                    except ValueError:
                        num = num + 1
                if num > 0:
                    result[i['field']] = ("%.3f" % (num / total))
                print(result)
        print(result)
        return result

    # 跟修改字段类型搭配，删除违法行
    def dropRow(self, data):
        df = pd.read_csv(self.open_path)
        for i in data:
            index = 0
            if (i['type']) == 'float64':
                for k in df[i['field']]:
                    try:
                        number = float(k)
                    except ValueError:
                        df = df.drop(index)
                    index = index + 1
        df.to_csv(self.open_path, index_label=False, index=0)

    #如果某一行有空值，则删去整行
    def dropnan(self):
        df = pd.read_csv(self.open_path)
        df = df.dropna()
        df.to_csv(self.open_path, index_label=False, index=0)

    # Rankit序列
    def BNUZRankitSeries(self, s):
        r = []
        n = max(s)
        a = 0.5
        if n <= 10:
            a = 3.0 / 8
        for i in s:
            r.append(norm.ppf((i - a) / (n + 1 - 2 * a)))
        return pd.Series(r)

    # Rankit序列

    # 生成RANKit，C_name 为列名
    def TScoreRankit(self, C_name, stepX_path):
        df = pd.read_csv(self.open_path)
        df_X = pd.read_csv(stepX_path)
        rank = df[C_name].rank(method='max')
        rankit = self.BNUZRankitSeries(rank)
        df[str(C_name + '_Rankit')] = rankit
        df_X[str(C_name + '_Rankit')] =[df[str(C_name + '_Rankit')].dtype, '', str(C_name + '_Rankit'), '', '', '']
        df.to_csv(self.open_path, index_label=False, index=0)
        df_X.to_csv(stepX_path, index_label=False)

    # 生成RANK排名，C_name为列名
    def TScoreRank(self, C_name, stepX_path):
        df = pd.read_csv(self.open_path)
        df_X = pd.read_csv(stepX_path)
        rank = df[C_name].rank(method='max')
        df[str(C_name + '_Rank')] = rank
        df_X[str(C_name + '_Rank')] = [df[str(C_name + '_Rank')].dtype, '', str(C_name + '_Rank'), '', '', '']
        df.to_csv(self.open_path, index_label=False, index=0)
        df_X.to_csv(stepX_path, index_label=False)

    # layers为层数，实现分层，并生成每个学生所在的层列，C_name为列名
    def score2Layer(self, layers, C_name, stepX_path):
        df = pd.read_csv(self.open_path)
        df_X = pd.read_csv(stepX_path)
        count = (df[C_name].count())
        countsPerlayer = count // layers
        rank = df[C_name].rank(method='max')
        df[str(C_name + '_LAYER')] = rank // (countsPerlayer + 1) + 1
        df_X[str(C_name + '_LAYER')] = [df[str(C_name + '_LAYER')].dtype, '', str(C_name + '_LAYER'), '', '', '']
        df.to_csv(self.open_path, index_label=False, index=0)
        df_X.to_csv(stepX_path, index_label=False)

    # 生成每个学生所在层的平均值
    def score2Layer_mean(self, layers, C_name, stepX_path):
        df = pd.read_csv(self.open_path)
        df_X = pd.read_csv(stepX_path)
        count = (df[C_name].count())
        countsPerlayer = count // layers
        rank = df[C_name].rank(method='max')
        layer = rank // (countsPerlayer + 1) + 1
        grouped = df.groupby(layer)
        grouped_score = grouped[C_name]
        grouped_score = grouped_score.agg(['mean'])
        layer_value = grouped_score['mean'].values
        temp = []
        for i in layer:
            temp.append(layer_value[int(i - 1)])
        df[str(C_name + '_LAYER_mean')] = temp
        df_X[str(C_name + '_LAYER_mean')] = [df[str(C_name + '_LAYER_mean')].dtype, '', str(C_name + '_LAYER_mean'), '', '', '']
        df.to_csv(self.open_path, index_label=False, index=0)
        df_X.to_csv(stepX_path, index_label=False)


    # 用户自定义表达式，生成新的一列。newColumnName是生成的新列名，expression是表达式内容
    def Expression(self, newColumnName, expression, stepX_path):
        df = pd.read_csv(self.open_path)
        df_X = pd.read_csv(stepX_path)
        try:
            df.eval(str(newColumnName + '=' + expression), inplace=True)
        except:
            return("表达式错误")
        else:
            df_X[newColumnName] = [df[newColumnName].dtype, expression, newColumnName, '', '', '']
            df.to_csv(self.open_path, index_label=False, index=0)
            df_X.to_csv(stepX_path, index_label=False)

            return("新增列添加成功")

