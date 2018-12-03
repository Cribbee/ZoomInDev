# -*- coding: utf-8 -*-
__author__ = 'Cribbee'
__create_at__ = 2018 / 9 / 4

import codecs
import csv
import json
import os,base64
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

    def chart_filter(self, df,filter):
        '''

        :param df:
        :param filter:
        :return:
        '''

        logger = logging.getLogger('django')
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


        return df
    def chart_filter_past(self,df,filter_past):
        '''

        :param df:
        :param filter_past:
        :return:
        '''
        df_merger = []
        count = 0
        for f in filter_past:
            obj = f['filter_obj'].split(',')
            if f['filter_method']=='equal':
                for t in obj:
                    df_merger.append(df[df[f['field_name']] == (t)])
                    count+=1
            elif f['filter_method'] =='notEqual':
                for t in obj:
                    df_merger.append(df[~df[f['field_name']] == (t)])
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
        num = (len(set(df[x_axis[-1]])))

        if filter_past != [""]:
            if filter_past_logical_type =="&":
                df = self.chart_filter(df, filter_past)
            elif filter_past_logical_type == "|":
                df = self.chart_filter_past(df,filter_past)
        df2 = df

        df = self.process_result(df, x_axis, y_axis, chart_method)
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
            df = self.chart_filter(df, filter)
        # 如果绘图类型是饼图，则需要假如各数值占比
        if chart_type == 3:
            if x_axis == ['']:
                i = df.values.sum()
                df = df.append(df[y_axis] / i)
                df.index = ['Data', 'Percent']
            else:
                i = float(df.apply(lambda x: x.sum()))
                df['Percent'] = df[y_axis] / i

        if chart_type ==4:
            df3 = {}
            j = 0
            if len(x_axis) == 2:
                for i in range(len(df)):
                    df3[df.index[i][0]] = {}
                for t in range(len(df)):
                    df3[df.index[t][0]][j % num] = list(df.values[t]) + list(df.index[t])
                    j += 1
            elif len(x_axis) == 1:

                for i in range(len(df)):
                    df3[df.index[i]] = {}
                for t in range(len(df)):
                    a = list(df.values[t])

                    b = df.index[t].split(",") + a
                    df3[df.index[t]] = b
            df = df3
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
            if chart_type_2nd ==4:
                df3 = {}
                j = 0
                if len(x_axis) == 2:
                    for i in range(len(df)):
                        df3[df.index[i][0]] = {}
                    for t in range(len(df)):
                        df3[df.index[t][0]][j % num] = list(df.values[t]) + list(df.index[t])
                        j += 1
                elif len(x_axis) == 1:

                    for i in range(len(df)):
                        df3[df.index[i]] = {}
                    for t in range(len(df)):
                        a = list(df.values[t])

                        b = df.index[t].split(",") + a
                        df3[df.index[t]] = b
                df_2nd = df3
            secondary_axis_name = []
            for i in secondary_axis:
                i = i + "_2nd"
                secondary_axis_name.append(i)
            name = y_axis + secondary_axis_name

            df = pd.concat([df, df_2nd], join='outer', axis=1, ignore_index=True, sort=False)
            df.columns = name


        return df


class chart_pic():

    def __init__(self,dir_folder,upload_folder):
        self.dir_folder = dir_folder + "/Publish/"
        self.upload_folder = upload_folder

    def save_pic(self,chart_id,base_num):
        img = base64.b64decode(base_num)
        chart_folder_re = self.upload_folder+".png"
        chart_folder = self.dir_folder+str(chart_id)+".png"
        f1 = open(chart_folder,'wb')
        f1.write(img)
        f1.close()
        f2 = open(chart_folder_re,'wb')
        f2.write(img)
        f2.close()
        return chart_folder,chart_folder_re

class chart_sort():

    def __init__(self,chart_sort):
        self.chart_sort = chart_sort




    def show_chart(self,charts,info):
        for chart in charts:
            if chart.chart_folder2 !="":
                if chart.chart_folder2 not in info:
                    info[chart.chart_folder2] = {}
                    info[chart.chart_folder2]["title"] = chart.title
                    info[chart.chart_folder2]['desc'] = chart.desc
                    info[chart.chart_folder2]['chart_folder'] = chart.chart_folder2
                    info[chart.chart_folder2]['data_set'] = chart.data_set
                    info[chart.chart_folder2]['updated_time'] = chart.updated_time
        return info

    def show_Clustering_charts(self,Clustering_charts,info):
        for Cluster_chart in Clustering_charts:
            if Cluster_chart.chart_folder2!="":
                if Cluster_chart.chart_folder2 not in info:
                    info[Cluster_chart.chart_folder2] = {}
                    info[Cluster_chart.chart_folder2]["title"] = Cluster_chart.title
                    info[Cluster_chart.chart_folder2]['desc'] = Cluster_chart.desc
                    info[Cluster_chart.chart_folder2]['chart_folder'] = Cluster_chart.chart_folder2
                    info[Cluster_chart.chart_folder2]['data_set'] = Cluster_chart.data_set
                    info[Cluster_chart.chart_folder2]['updated_time'] = Cluster_chart.updated_time

            if Cluster_chart.chart_folder1!="":
                if Cluster_chart.chart_folder1 not in info:

                    info[Cluster_chart.chart_folder1] = {}
                    info[Cluster_chart.chart_folder1]["title"] = Cluster_chart.title
                    info[Cluster_chart.chart_folder1]['desc'] = Cluster_chart.desc
                    info[Cluster_chart.chart_folder1]['chart_folder'] = Cluster_chart.chart_folder1
                    info[Cluster_chart.chart_folder1]['data_set'] = Cluster_chart.data_set
                    info[Cluster_chart.chart_folder1]['updated_time'] = Cluster_chart.updated_time
        return info

    def show_Regression_charts(self,Regression_charts,info):
        for Regress_chart in Regression_charts:
            if Regress_chart.chart_folder3!="":
                if Regress_chart.chart_folder3 not in info:

                    info[Regress_chart.chart_folder3] = {}
                    info[Regress_chart.chart_folder3]["title"] = Regress_chart.title
                    info[Regress_chart.chart_folder3]['desc'] = Regress_chart.desc
                    info[Regress_chart.chart_folder3]['chart_folder'] = Regress_chart.chart_folder3
                    info[Regress_chart.chart_folder3]['data_set'] = Regress_chart.data_set
                    info[Regress_chart.chart_folder3]['updated_time'] = Regress_chart.updated_time

            if Regress_chart.chart_folder2!="":
                if Regress_chart.chart_folder2 not in info:

                    info[Regress_chart.chart_folder2] = {}
                    info[Regress_chart.chart_folder2]["title"] = Regress_chart.title
                    info[Regress_chart.chart_folder2]['desc'] = Regress_chart.desc
                    info[Regress_chart.chart_folder2]['chart_folder'] = Regress_chart.chart_folder2
                    info[Regress_chart.chart_folder2]['data_set'] = Regress_chart.data_set
                    info[Regress_chart.chart_folder2]['updated_time'] = Regress_chart.updated_time


            if Regress_chart.chart_folder1!="":
                if Regress_chart.chart_folder1 not in info:

                    info[Regress_chart.chart_folder1] = {}
                    info[Regress_chart.chart_folder1]["title"] = Regress_chart.title
                    info[Regress_chart.chart_folder1]['desc'] = Regress_chart.desc
                    info[Regress_chart.chart_folder1]['chart_folder'] = Regress_chart.chart_folder1
                    info[Regress_chart.chart_folder1]['data_set'] = Regress_chart.data_set
                    info[Regress_chart.chart_folder1]['updated_time'] = Regress_chart.updated_time

        return info







