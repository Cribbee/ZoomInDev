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

    def missing_value(self, axis, how, thresh):
        df = pd.read_csv(self.open_path)
        dfd = df.dropna(axis=axis, how=how, thresh=thresh)
        dfd.to_csv("m"+self.open_path)











    # @staticmethod
    # def ():
    #     fr = codecs.open(self.save_path, 'r', 'utf-8')


