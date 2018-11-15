# -*- coding: utf-8 -*-
import shutil

__author__ = 'Cribbee'
__create_at__ = 2018 / 6 / 3
import csv
import json
import base64
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
        json.dump(ls[1:], fw, separators=(',', ':'), ensure_ascii=False)
        fw.close()


def images2base64(url):
    base = []
    for i in url:
        img_file = open(i, 'rb')
        img_b64encode = base64.b64encode(img_file.read())
        base.append(img_b64encode)
        img_file.close()
    return base


# 修改'/home/ZoomInDataSet/2/Data/2213.csv'中的任务文件夹
def trans_taskid(str1, task_id):
    a = str1.split('/')
    a[3] = task_id
    new_path = '/'.join(a)
    return new_path


# 修改'/home/ZoomInDataSet/DataMining/Regression/445671.png'修改成'/home/ZoomInDataSet/Publish/4/445671_s.png'
def copy_dataMiningImages(path, task_id):
    a = path.split('/')
    a[3] = 'Publish/' + task_id
    del a[4]
    new_path = '/'.join(a)
    new_path = new_path.replace('.png', '_s.png')
    shutil.copy(path, new_path)
    return new_path


# 修改'/home/ZoomInDataSet/DataAnalyze/954.png'修改成'/home/ZoomInDataSet/Publish/3/954_s.png'
def copy_dataAnalyzeImages(path, task_id):
    a = path.split('/')
    a[3] = 'Publish/' + task_id
    new_path = '/'.join(a)
    new_path = new_path.replace('.png', '_s.png')
    shutil.copy(path, new_path)
    return new_path
