from django.test import TestCase


# Create your tests here.
# if __name__ == '__main__':
#     str = '/home/ZoomInDataSet/2/Data/2213.csv'
#     print(str.split('/'))
#     a = str.split('/')
#     a[3] = '3'
#     print('/'.join(a))


def trans(str, id):
    a = str.split('/')
    a[2] = id
    return ('/'.join(a))


if __name__ == '__main__':
    print('D:\Task\1/Data/1212.csv'.split('/'))
