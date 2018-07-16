# -*- coding: utf-8 -*-
__author__ = 'Cribbee'
__create_at__ = 2018 / 6 / 4

import codecs
import csv
import json
import os

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

    def orginal_save(self, jsondata):

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

    # def missing_data(self,**kwargs):
    #     self.allow_blan = kwargs.pop('allow_blank', False)
    #     self.trim_whitespace = kwargs.pop('trim_whitespace', True)
    #     self.max_length = kwargs.pop('max_length', None)
    #     self.min_length = kwargs.pop('min_length', None)

    def missing_value(self, axis, how):
        df = pd.read_csv(self.open_path)
        dfd = df.dropna(axis=axis, how=how)
        path = self.open_path.replace(".csv", "m.csv")
        dfd.to_csv(path)

    # 可优化为单步一次性处理
    def filter_processing(self, logical_type, filter):
        df = pd.read_csv(self.open_path)
        # "与"的判断逻辑
        if logical_type == "&":
            for f in filter:
                if f['field_type'] == "0":
                    df = df[eval((str(df[f['field_name']]) + f['filter_method'] + f['filter_obj']))]
                elif f['field_type'] == "1" and f['filter_method'] == "contains":
                    df = df[df[f['field_name']].str.contains(f['filter_obj'])]
                elif f['field_type'] == "1" and f['filter_method'] == "notContains":
                    df = df[~df[f['field_name']].str.contains(f['filter_obj'])]
                elif f['field_type'] == "1" and f['filter_method'] == "isNull":
                    df = df[df[f['field_name']].notnull]
                elif f['field_type'] == "1" and f['filter_method'] == "notNull":
                    df = df[df[f['field_name']].isnull]
        # "或"的判断逻辑
        elif logical_type == "|":
            df_merger = []
            count = 0
            for f in filter:
                if f['field_type'] == "0":
                    df_merger[count] = df[eval((str(df[f['field_name']]) + f['filter_method'] + f['filter_obj']))]
                    count += 1
                elif f['field_type'] == "1" and f['filter_method'] == "contains":
                    df_merger[count] = df[df[f['field_name']].str.contains(f['filter_obj'])]
                    count += 1
                elif f['field_type'] == "1" and f['filter_method'] == "notContains":
                    df_merger[count] = df[~df[f['field_name']].str.contains(f['filter_obj'])]
                    count += 1
                elif f['field_type'] == "1" and f['filter_method'] == "isNull":
                    df_merger[count] = df[df[f['field_name']].notnull]
                    count += 1
                elif f['field_type'] == "1" and f['filter_method'] == "notNull":
                    df_merger[count] = df[df[f['field_name']].isnull]
                    count += 1
            # accumulate,then remove replicated
            i = 0
            while i < count:

                df = pd.concat([df_merger[i], df_merger[i+1]], join='outer', axis=0,ignore_index=True,)
                i += 1
            path = self.open_path.replace(".csv", "f.csv")
            df.to_csv(path)





