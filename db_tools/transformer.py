# -*- coding: utf-8 -*-
__author__ = 'Cribbee'
__create_at__ = 2018 / 6 / 3
import csv
import json
import sys
import codecs
import os
import logging


class trans():

    def __init__(self, json_path, csv_path):
        self.jsonpath = json_path
        self.csvpath = csv_path

    def json2csv(self):
        logger = logging.getLogger('django')
        fr = codecs.open(self.jsonpath, 'r', 'utf-8')
        ls = json.load(fr)
        data = [list(ls[0].keys())]
        for item in ls:
            # print(item)
            data.append(list(item.values()))
        fr.close()

        fw = codecs.open(self.csvpath, 'w', 'utf-8')
        writer = csv.writer(fw)
        for item in data:
            writer.writerow(item)
        fw.close()

    def csv2json(self):
        fr = codecs.open(self.csvpath, 'r', 'utf-8')
        ls = []
        for line in fr:
            line = line.replace("\n", "")
            line = line.replace("\r", "")
            ls.append(line.split(','))
        fr.close()

        fw = codecs.open(self.jsonpath, 'w', 'utf-8')
        for i in range(1, len(ls)):
            ls[i] = dict(zip(ls[0], ls[i]))
        json.dump(ls[1:], fw,  separators=(',', ':'), ensure_ascii=False)
        fw.close()
