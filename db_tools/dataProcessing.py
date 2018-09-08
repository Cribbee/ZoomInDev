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
            f.writelines(json.dumps(jsondata, sort_keys=True, indent=4, ensure_ascii=False))

    def step2_save(self, row_num):

        data = codecs.open(self.open_path, 'r', 'utf-8').readlines()
        data[row_num] = ''
        with codecs.open(self.open_path, 'w', 'utf-8') as f:
            f.writelines(data)

    def step3_save(self, write_path):

        data = codecs.open(self.open_path, 'r', 'utf-8').readlines()
        with codecs.open(write_path, 'w', 'utf-8') as f:
            f.writelines(data)

    def stepx1_save(self,write_path):

        data = codecs.open(self.open_path, 'r', 'utf-8').readlines()
        with codecs.open(write_path, 'w', 'utf-8') as f:
            f.writelines(data)

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
                    str_expression = "df['"+f['field_name']+"']" + f['filter_method'] + f['filter_obj']
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
            path = self.open_path.replace(".csv", "f.csv")
            df.to_csv(path, index_label=False)
            logger.debug("LogDebug<""logical_type : 与>")
        # "或"的判断逻辑
        elif logical_type == "|":
            df_merger = []
            count = 0
            for f in filter:
                if f['field_type'] == 0:
                    str_expression = "df['" + f['field_name'] + "']" + f['filter_method'] + f['filter_obj']
                    print(str_expression)
                    #df_merger[] = df[eval(str_expression)]
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

                dfs = pd.concat([dfs, df_merger[i]], join='outer', axis=0, ignore_index=True,)
                i += 1
            path = self.open_path.replace(".csv", "f.csv", index_label=False)
            dfs.to_csv(path)

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
        df = df.sort_values(by=[col_name], ascending=ascending).reset_index(inplace=False).drop('index', axis=1, inplace=False)
        df.to_csv(self.open_path, index_label=False)

    # 求和函数sum，操作两列，并在末尾生成新一列
    def sum(self, a, b, col_new):
        df = pd.read_csv(self.open_path)
        df.eval(col_new + "=" + a + "+" + b, inplace=True)
        df.to_csv(self.open_path, index_label=False)

    # 批量删除列
    def drop(self, drop):
        df = pd.read_csv(self.open_path)
        for delete in drop:

            df.drop(delete['field'], axis=1, inplace=True)
        path = self.open_path.replace(".csv", "d.csv")
        df.to_csv(path, index_label=False)

    # 批量修改列名
    def reset_columns(self, reset):
        df = pd.read_csv(self.open_path)
        for rs in reset:
            df.rename(columns={rs['original_col']: rs['new_col']}, inplace=True)
        path = self.open_path.replace(".csv", "r.csv")
        df.to_csv(path, index_label=False)

    # 展示数据集字段名与字段类型
    def show_dtypes(self):
        df = pd.read_csv(self.open_path)
        dtypes = df.dtypes
        return dtypes

    # 计算每列的平均值
    def average(self, data):
        df = pd.read_csv(self.open_path)
        Columns_name = df.columns.values.tolist()
        insertRow = pd.DataFrame(columns=Columns_name)
        newdf = df.append(insertRow, ignore_index=True)
        for i in data:
            print(i)
            print(i['field'])
            mean1 = df[i['field']].mean()
            newdf.loc[len(df), i['field']] = mean1
        newdf.rename(index={len(newdf) - 1: 'average'}, inplace=True)
        newdf.to_csv(self.open_path, index_label=False)




