import shutil

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


def copy_dataMiningImages(path, task_id):
    str1 = '/home/ZoomInDataSet/DataMining/Regression/445671.png'
    a = str1.split('/')
    print(a[0])
    a[3] = 'Publish/' + str(task_id)
    del a[4]
    new_path = '/'.join(a)
    new_path = new_path.replace('.png', '_s.png')
    print(new_path)
    # shutil.copy(path, new_path)
    # return new_path


def copy_dataAnalyzeImages(path, task_id):
    a = path.split('/')
    a[3] = 'Publish/' + str(task_id)
    new_path = '/'.join(a)
    new_path = new_path.replace('.png', '_s.png')
    shutil.copy(path, new_path)
    return new_path


if __name__ == '__main__':
    print('D:\Task\1/Data/1212.csv'.split('/'))
