# -*- coding: utf-8 -*-
__author__ = 'Cribbee'
__create_at__ = 2018 / 9 / 14

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
