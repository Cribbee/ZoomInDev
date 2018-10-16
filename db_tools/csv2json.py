# -*- coding: utf-8 -*-
__author__ = 'Cribbee'
__create_at__ = 2018 / 5 / 28

import json
import csv
import codecs
import pandas as pd


def trans():
    # df = pd.read_excel("D:\\2018原始分.xls", sheetname=[0, 1, 2])
    # df0 = df[0].sort_values(by='身份证号', axis=0, ascending=True)
    # df1 = df[1].sort_values(by='身份证号', axis=0, ascending=True)
    # dfw = pd.merge(df1, df0, on="身份证号")
    # dfw['总分'] = round(dfw['总分'].astype(float), 0)
    # dfw = dfw[dfw['总分'] > 0]
    # dfw.to_json("D:\\2018文科原始分333.json", force_ascii=False, orient='records')
    # dfw.to_csv("D:\\2018文科原始 分1.csv")

    fr = codecs.open("D:\\Task\\12\\Data\\122213.csvy", 'r', 'utf-8')
    ls = []
    for line in fr:
        line = line.replace("\n", "")
        ls.append(line.split(','))
    fr.close()

    fw = codecs.open("D:\\2018文科原始分4444.json", 'w', 'utf-8')
    for i in range(1,len(ls)):
        ls[i] = dict(zip(ls[0], ls[i]))
    json.dump(ls[1:], fw, separators=(',', ':'), ensure_ascii=False)
    fw.close()


def test():
    jsondata = [
    {
        "RANK": "1277",
        "RANK_H": "1293",
        "姓名_x": "赵一钦",
        "学校名称": "市三中",
        "性别_x": "女",
        "毕业学校": "紫荆中学凤凰路校区",
        "考生号": "170010508",
        "﻿": "0"
    },
    {
        "RANK": "303",
        "RANK_H": "352",
        "姓名_x": "王海鑫",
        "学校名称": "北大附校",
        "性别_x": "男",
        "毕业学校": "市十中",
        "考生号": "270100587",
        "﻿": "1"
    }]

    with codecs.open("~/Downloads/chuci.json", 'w', 'utf-8') as f:
        f.writelines(json.dumps(jsondata, sort_keys=True, indent=4, ensure_ascii=False))


if __name__ == '__main__':
    trans()

