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
from numpy import nan as NaN


class Process():

    def __init__(self, open_path):
        self.open_path = open_path

    def chart_sum(self, chart_type, x_axis, y_axis):
        df = pd.read_csv(self.open_path)
        x_axis = x_axis.split(',')
        y_axis = y_axis.split(',')
        if chart_type == 1:
            df = df.groupby(x_axis)[y_axis].sum()
            return df
        elif chart_type == 2:
            df = df.groupby(x_axis)[y_axis].sum()
            return df
        elif chart_type == 3:
            #饼图
            return df
        elif chart_type == 4:
            #散点图
            return df
        return df

    def chart_mean(self, chart_type, x_axis, y_axis):
        df = pd.read_csv(self.open_path)
        x_axis = x_axis.split(',')
        y_axis = y_axis.split(',')
        if chart_type == 1:
            df = df.groupby(x_axis)[y_axis].mean()
            return df
        elif chart_type == 2:
            df = df.groupby(x_axis)[y_axis].mean()
            return df
        elif chart_type == 3:
            #饼图
            return df
        elif chart_type == 4:
            #散点图
            return df
        return df
