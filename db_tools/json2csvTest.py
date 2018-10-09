# -*- coding: utf-8 -*-
__author__ = 'Cribbee'
__create_at__ = 2018 / 5 / 15

import csv
import json
import sys
import codecs


def trans():
    jsonData = codecs.open('/Users/cribbee/Downloads/raw.2.json', 'r', 'utf-8')
    # csvfile = open(path+'.csv', 'w') # 此处这样写会导致写出来的文件会有空行
    # csvfile = open(path+'.csv', 'wb') # python2下
    data = {}
    keys_write = True
    csvfile = codecs.open('/Users/cribbee/Downloads/转换完成1.csv', 'w', 'utf-8')  # python3下
    writer = csv.writer(csvfile)

    for line in jsonData:  # 获取属性列表
        dic = json.loads(line[0:-1])
        keys = dic.keys()
        break

    for dic in jsonData:  # 读取json数据的每一行，将values数据一次一行的写入csv中

        print(dic)
        dic = json.loads(dic[0:])

        for key in keys:
            if key in dic:
                data[key] = dic[key]
            else:
                data[key] = ""
        print(data)

        if keys_write == True:
            writer.writerow(data.keys())
        writer.writerow(data.values())
        keys_write = False

    jsonData.close()
    csvfile.close()


if __name__ == '__main__':
    trans()