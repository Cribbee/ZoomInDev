# -*- coding: utf-8 -*-
__author__ = 'Cribbee'
__create_at__ = 2018 / 5 / 28

import json
import csv
import codecs


def trans():
    fr = codecs.open("/Users/cribbee/Downloads/score.csv", 'r', 'utf-8')
    ls = []
    for line in fr:
        line = line.replace("\n", "")
        ls.append(line.split(','))
    fr.close()

    fw = codecs.open("/Users/cribbee/Downloads/csv2json2222.json", 'w', 'utf-8')
    for i in range(1,len(ls)):
        ls[i] = dict(zip(ls[0], ls[i]))
    json.dump(ls[1:], fw, sort_keys=True, indent=4, ensure_ascii=False)
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
        f.writelines(json.dumps(jsondata,))



if __name__ == '__main__':
    trans()
    
