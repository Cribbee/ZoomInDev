import shutil

from django.test import TestCase


# Create your tests here.
# if __name__ == '__main__':
#     str = '/home/ZoomInDataSet/2/Data/2213.csv'
#     print(str.split('/'))
#     a = str.split('/')
#     a[3] = '3'
#     print('/'.join(a))


# 修改'/home/ZoomInDataSet/2/Data/2213.csv'中的任务文件夹
def trans_taskid(str1, task_id):
    a = str1.split('/')
    a[3] = task_id
    return ('/'.join(a))


# 修改'/home/ZoomInDataSet/DataMining/Regression/445671.png'修改成'/home/ZoomInDataSet/Publish/4/445671_s.png'
def copy_dataMiningImages(path, task_id):
    task_id = '4'
    str1 = '/home/ZoomInDataSet/DataMining/Regression/445671.png'
    a = str1.split('/')
    print(a[0])
    a[3] = 'Publish/' + task_id
    del a[4]
    new_path = '/'.join(a)
    new_path = new_path.replace('.png', '_s.png')
    print(new_path)
    # shutil.copy(path, new_path)
    # return new_path

# 修改'/home/ZoomInDataSet/DataAnalyze/954.png'修改成'/home/ZoomInDataSet/Publish/3/954_s.png'
def copy_dataAnalyzeImages(path, task_id):
    # a = path.split('/')
    # a[3] = 'Publish/' + task_id
    # new_path = '/'.join(a)
    # new_path = new_path.replace('.png', '_s.png')
    shutil.copy("F:\\PHOTO\\五一顺德之旅\\IMG_5524.jpg", "F:\\1.jpg")
    # print(new_path)
    # return new_path


if __name__ == '__main__':
    copy_dataAnalyzeImages('1', '3')
