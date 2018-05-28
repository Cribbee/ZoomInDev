# -*- coding: utf-8 -*-
__author__ = 'Cribbee'
__create_at__ = 2018 / 5 / 28

import json
import codecs
import csv


def trans():

    fr = codecs.open("/Users/cribbee/Downloads/raw.2.json", 'r', 'utf-8')
    ls = json.load(fr)
    data = [list(ls[0].keys())]
    for item in ls:
        print(item)
        data.append(list(item.values()))
    fr.close()

    fw = codecs.open("/Users/cribbee/Downloads/转换完成1.csv", 'w', 'utf-8')
    writer = csv.writer(fw)
    for item in data:
        writer.writerow(item)
    fw.close()


if __name__ == '__main__':
    trans()