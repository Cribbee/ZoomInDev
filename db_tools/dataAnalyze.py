# -*- coding: utf-8 -*-
__author__ = 'Cribbee'
__create_at__ = 2018 / 9 / 4

import codecs
import csv
import json
import os
import logging

import pandas as pd
import numpy as np


class Process():

    def __init__(self, open_path):
        self.open_path = open_path

    def chart_count(self, df, x_axis, y_axis):
        '''

        :param df:
        :param x_axis:数据维度
        :param y_axis:数据数值
        :return:计数处理后的Dataframe
        '''
        if x_axis == ['']:

            y_axis_str = df[y_axis].count()
            str_data = {y_axis: [y_axis_str]}
            df = pd.DataFrame(str_data)
        else:

            df = df.groupby(x_axis)[y_axis].count()

        return df

    def chart_sum(self, df, x_axis, y_axis):
        '''

        :param df:
        :param x_axis:数据维度
        :param y_axis:数据数值
        :return:求和处理后的Dataframe
        '''
        if x_axis == [""]:

            if str(df[y_axis].dtypes) == "object":
                df_sum = self.chart_count(df, x_axis, y_axis)

            else:

                df_sum = df[y_axis].sum()
                str_data = {y_axis: [df_sum]}
                df_sum = pd.DataFrame(str_data)


        else:
            if str(df[y_axis].dtypes) == "object":

                df[y_axis] = 1

                df_sum = df.groupby(x_axis)[y_axis].sum()
            else:
                df_sum = df.groupby(x_axis)[y_axis].sum()
        return df_sum

    def chart_mean(self, df, x_axis, y_axis):
        '''

        :param df:
        :param x_axis:数据维度
        :param y_axis:数据数值
        :return:求平均数处理后的Dataframe
        '''
        if x_axis == [""]:

            if str(df[y_axis].dtypes) == "object":
                df_mean = self.chart_count(df, x_axis, y_axis)

            else:

                df_mean = df[y_axis].sum()
                str_data = {y_axis: [df_mean]}
                df_mean = pd.DataFrame(str_data)
            df_mean.index = ['mean']


        else:
            if str(df[y_axis].dtypes) == "object":

                df[y_axis] = 1

                df_mean = df.groupby(x_axis)[y_axis].mean()
            else:
                df_mean = df.groupby(x_axis)[y_axis].mean()
        return df_mean

    def process_result(self, df, x_axis, y_axis, chart_method):
        '''

        :param x_axis:
        :param y_axis:
        :param y_axis_method: 不同数值所要进行的数值处理方法
        1：计数
        2：求和
        3：求平均数
        :return:
        '''
        # 数据处理函数

        result = pd.DataFrame()
        processed_data = pd.DataFrame()
        t = 0
        for i in y_axis:
            if int(chart_method[t]) == 1:
                processed_data = self.chart_count(df, x_axis, i)
            elif int(chart_method[t]) == 2:
                processed_data = self.chart_sum(df, x_axis, i)
            elif int(chart_method[t]) == 3:
                processed_data = self.chart_mean(df, x_axis, i)

            result = pd.concat([result, processed_data], axis=1, sort=True)
            t += 1
        return (result)

    def chart_filter(self, df, filter_past_logical_type, filter):
        '''

        :param df:
        :param filter:
        :return:
        '''

        logger = logging.getLogger('django')
        if filter_past_logical_type == "&":
            for f in filter:
                if f['field_type'] == 0:
                    str_expression = "df['" + f['field_name'] + "']" + f['filter_method'] + f['filter_obj']
                    logger.debug("LogDebug<""str_expression : " + str_expression + ">")
                    df = df[eval(str_expression)]

                elif f['field_type'] == 1 and f['filter_method'] == "equal":
                    df = df[df[f['field_name']].astype(str) == (f['filter_obj'])]
                elif f['field_type'] == 1 and f['filter_method'] == "notEqual":
                    df = df[~df[f['field_name']].astype(str) == (f['filter_obj'])]
                elif f['field_type'] == 1 and f['filter_method'] == "contains":
                    df = df[df[f['field_name']].str.contains(f['filter_obj'])]
                elif f['field_type'] == 1 and f['filter_method'] == "notContains":
                    df = df[~df[f['field_name']].str.contains(f['filter_obj'])]

                elif f['field_type'] == 1 and f['filter_method'] == "isNull":
                    df = df[df[f['field_name']].astype(str).isnull()]
                elif f['field_type'] == 1 and f['filter_method'] == "notNull":
                    df = df[df[f['field_name']].astype(str).notnull()]
        elif filter_past_logical_type == "|":
            df_merger = []
            count = 0
            for f in filter:
                if f['field_type'] == 0:
                    str_expression = "df['" + f['field_name'] + "']" + f['filter_method'] + f['filter_obj']
                    df_merger.append(df[eval(str_expression)])
                    count += 1
                elif f['field_type'] == 1 and f['filter_method'] == "equal":
                    df_merger.append(df[df[f['field_name']] == (f['filter_obj'])])
                    count += 1
                elif f['field_type'] == 1 and f['filter_method'] == "notEqual":
                    df_merger.append(df[~df[f['field_name']] == (f['filter_obj'])])
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
            i = 0
            df = pd.DataFrame(None)
            while i < count:
                df = pd.concat([df, df_merger[i]], join='outer', axis=0, ignore_index=True, )
                i += 1

        return df

    def process(self, x_axis, y_axis, chart_method, chart_type, sort, sort_value, filter, filter_past,
                secondary_axis, chart_method_2nd, chart_type_2nd, filter_past_logical_type):
        '''

        :param x_axis: 维度
        :param y_axis: 数值
        :param chart_method: 数值计算方法
        :param chart_type: 绘图类型
        :param sort: 排序方法，1升序，0倒序
        :param sort_value: 排序基准
        :param filter: 处理后的筛选器
        :param filter_past: 处理前筛选
        :param secondary_axis: 次轴
        :param chart_method_2nd: 次轴数值计算方法
        :param chart_type_2nd: 次轴绘图类型
        :return:
        '''
        chart_method = chart_method.split(",")
        secondary_axis = secondary_axis.split(",")
        chart_method_2nd = chart_method_2nd.split(',')
        open_path = self.open_path
        df = pd.read_csv(open_path)
        x_axis = x_axis.split(',')
        y_axis = y_axis.split(',')
        if filter_past != [""]:
            df = self.chart_filter(df, filter_past_logical_type, filter_past)
        df2 = df

        df = self.process_result(df, x_axis, y_axis, chart_method)

        # 如果绘图类型是饼图，则需要假如各数值占比
        if chart_type == 3:
            if x_axis == ['']:
                i = df.values.sum()
                df = df.append(df[y_axis] / i)
                df.index = ['Data', 'Percent']
            else:
                i = float(df.apply(lambda x: x.sum()))
                df['Percent'] = df[y_axis] / i
        #         次轴拼接，并且次轴数值名后加_2nd以便区分
        if secondary_axis == [""]:
            df = df
        else:
            df_2nd = self.process_result(df2, x_axis, secondary_axis, chart_method_2nd)
            if chart_type_2nd == 3:
                if x_axis == ['']:
                    i = df.values.sum()
                    df_2nd = df_2nd.append(df[secondary_axis] / i)
                    df_2nd.index = ['Data', 'Percent']
                else:
                    i = float(df.apply(lambda x: x.sum()))
                    df_2nd['Percent'] = df_2nd[secondary_axis] / i
            secondary_axis_name = []
            for i in secondary_axis:
                i = i + "_2nd"
                secondary_axis_name.append(i)
            name = y_axis + secondary_axis_name

            df = pd.concat([df, df_2nd], join='outer', axis=1, ignore_index=True, sort=False)
            df.columns = name
        # 排序
        if sort == 1:
            if sort_value != "":
                df = df.sort_values(by=sort_value, ascending=1)
        elif sort == 0:
            if sort_value != "":
                df = df.sort_values(by=sort_value, ascending=0)
        if filter == "":
            df = df
        else:
            # 计算后的筛选强制只有&
            filter_past_logical_type = "&"
            df = self.chart_filter(df, filter_past_logical_type,filter)

        return df
