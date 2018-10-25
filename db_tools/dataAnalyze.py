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

    def chart_count(self,df, x_axis, y_axis):
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

    def chart_sum(self,df, x_axis, y_axis):
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

    def chart_mean(self,df, x_axis, y_axis):
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

    def process_result(self,x_axis, y_axis, chart_method):
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

        open_path = self.open_path
        df = pd.read_csv(open_path)
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



    def chart_filter(self,df,filter):
        '''

        :param df:
        :param filter:
        :return:
        '''
        df_merger = []
        count = 0


        for f in filter:
            if f['field_type'] == 0:
                str_expression = "df['" + f['field_name'] + "']" + f['filter_method'] + f['filter_obj']
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
        i = 0
        dfs = pd.DataFrame(None)
        while i < count:
            dfs = pd.concat([dfs, df_merger[i]], join='outer', axis=0)
            i += 1
        return dfs

    def process(self,x_axis,y_axis,chart_method,chart_type,sort,sort_value,filter):
        '''

        :param x_axis: 数据维度
        :param y_axis: 数据数值
        :param chart_method: 数据处理方法
        :param chart_type: 绘图样式
        :return:
        '''
        chart_method = chart_method.split(",")
        x_axis = x_axis.split(',')
        y_axis = y_axis.split(',')
        df = self.process_result(x_axis, y_axis, chart_method)
        if chart_type ==3:
            if x_axis == ['']:
                i = df.values.sum()
                df = df.append(df[y_axis] / i)
                df.index = ['Data', 'Percent']
            else:
                i = float(df.apply(lambda x: x.sum()))
                df['Percent'] = df[y_axis] / i
        if sort == 1:
            if sort_value !="":
                df = df.sort_values(by=sort_value, ascending=1)
        elif sort == 0:
            if sort_value !="":
                df = df.sort_values(by=sort_value, ascending=0)
        if filter =="":
            df = df
        else:

            df = self.chart_filter(df,filter)

        return df