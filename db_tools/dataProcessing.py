# -*- coding: utf-8 -*-
__author__ = 'Cribbee'
__create_at__ = 2018 / 6 / 4

import codecs
import csv
import json
import pandas as pd
import numpy as np



class process():

    def __init__(self, open_path):
        self.open_path = open_path
        #self.save_path = save_path

    def first_save(self, row_num):

        data = codecs.open(self.open_path, 'r', 'utf-8').readlines()
        data[row_num] = ''
        with codecs.open(self.open_path, 'w', 'utf-8') as f:
            f.writelines(data)

    def missing_data(self,**kwargs):
        self.allow_blan = kwargs.pop('allow_blank', False)
        self.trim_whitespace = kwargs.pop('trim_whitespace', True)
        self.max_length = kwargs.pop('max_length', None)
        self.min_length = kwargs.pop('min_length', None)

    # @staticmethod
    # def ():
    #     fr = codecs.open(self.save_path, 'r', 'utf-8')


