from db_tools import transformer


def test():
    a = "/Users/cribbee/Downloads/raw.2.json"
    b = "/Users/cribbee/Downloads/转换完成1.csv"
    data = transformer.trans(a, b)
    print(data.json2csv())



if __name__ == '__main__':
    test()


