# -*- coding: utf-8 -*-
__author__ = 'Cribbee'
__create_at__ = 2018 / 6 / 3
import csv
import json
import sys
import codecs


class trans():

    def __init__(self, json_path, csv_path):
        self.jsonpath = json_path
        self.csvpath = csv_path

    def json2csv(self):
        fr = codecs.open(self.jsonpath, 'r', 'utf-8')
        ls = json.load(fr)
        print(fr)
        print(ls)
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