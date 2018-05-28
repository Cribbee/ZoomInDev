# -*- coding: utf-8 -*-
__author__ = 'Cribbee'
__create_at__ = 2018 / 5 / 28

import json
import csv
import codecs


def trans():
    fr = codecs.open("/Users/cribbee/Downloads/转换完成1.csv", 'r', 'utf-8')
    ls = []
    for line in fr:
        line = line.replace("\n", "")
        ls.append(line.split(','))
    fr.close()

    fw = codecs.open("/Users/cribbee/Downloads/csv2json.json", 'w', 'utf-8')
    for i in range(1,len(ls)):
        ls[i] = dict(zip(ls[0], ls[i]))
    json.dump(ls[1:], fw, sort_keys=True, indent=4, ensure_ascii=False)
    fw.close()


if __name__ == '__main__':
    trans()
