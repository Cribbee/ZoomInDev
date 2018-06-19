from db_tools import transformer
from db_tools import dataProcessing
import codecs
#
#
def test():
    a = "/Users/cribbee/Downloads/raw.2.json"
    b = "/Users/cribbee/Downloads/转换完成1.csv"
    c = "/Users/cribbee/Downloads/score.csv"
    d = "/Users/cribbee/Downloads/csv2json2222.json"
#     # data = transformer.trans(d, c)
#     # #data.json2csv()
#     # data.csv2json()
    data = dataProcessing.process(b)
    data.step2_save(1)
    print("ok")
#     dataProcessing.process.mkdir(floder="/Users/cribbee/Downloads/hahah")


if __name__ == '__main__':
    test()


