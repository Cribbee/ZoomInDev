# -*- coding: utf-8 -*-
__author__ = 'Cribbee'
__create_at__ = 2018 / 6 / 4

import codecs
import csv
import json
import pandas as pd
import numpy as np



class pipe():

    def __init__(self, open_path):
        self.open_path = open_path
        #self.save_path = save_path

    def first_save(self, row_num):

        d = codecs.open(self.open_path, 'r', 'utf-8').readlines()
        d[row_num] = ''
        with codecs.open(self.open_path, 'w', 'utf-8') as f:
            f.writelines(d)




    # @staticmethod
    # def ():
    #     fr = codecs.open(pipe.save_path, 'r', 'utf-8')


