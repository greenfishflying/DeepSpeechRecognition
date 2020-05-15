import os
import csv
import re
from shutil import copy
import random
import shutil
path='/home/null/Project/NLPData/普通话内部车上采集已完成/'

# file = open(path+'音频文字标注.txt.utf8')
def clean_data(path):
#清除与标签无法匹配的数据
    lines = []
    i = 0
    file = open(path+'音频文字标注.txt.utf8')
    while 1:
      line = file.readline()
      if not line:
        break
      pass # do something
      sp = line.split()
      filename =sp[0]
      old_name = path +'/2/'+filename
      new_name = path +'/对应标签/'+filename
      copy(old_name, new_name)
      i+=1
      lines.append(sp[0])
    file.close()
    print("lines",len(lines))
    print("i",i)

def rename(path,i=0):
    file = open(path + '音频文字标注.txt.utf8')
    file2 = open(path+'new_label.txt','w')
    lines = []
    while 1:
        line = file.readline()
        if not line:
            break
        pass  # do something
        sp = line.split()
        filename = sp[0]
        print(sp)
        # print(sp[0])
        label_context = sp[1]
        neww = 'rm_maren_'+str(i)+'.wav'
        old_name = path + '对应标签/' + filename
        # print("old_name",old_name)
        new_name = path + 'renamed/' + neww
        try:
            copy(old_name, new_name)
            print("copying....",old_name,new_name)
            sp[0]=neww
            neirong = sp[0]+'  '+sp[1]+'\n'

            file2.writelines(neirong)
            print("writing",neirong)
            i = i + 1
        except:
            pass
    file.close()
    file2.close
    print("i", i)

def creat_test_train(path):
    file_t = open(path+'new_train.txt')
    file_x= open(path+'xx.txt','w')
    file_y = open(path+'yy.txt', 'w')
    i = 20

    while 1:
        line = file_t.readline()
        if not line:
            break
        pass  # do something
        x = random.randint(1, 100)
        if x<=10:
            sp = line.split()
            old_name = './data/'+sp[0]
            new_name = './data/zanghua/test/'+'rm_test_'+str(i)+'.wav'
            shutil.move(old_name, new_name)
            print("copying....", old_name, new_name)
            pp1 =' '.join(sp[1:-1])
            print(pp1)
            neww = 'zanghua/train/rm_test_'+str(i)+'.wav'+'\t'+str(pp1)+'\t'+sp[-1]+'\n'
            print(neww)
            file_y.writelines(neww)
            i+=1
        else:
            file_x.writelines(line)
    print("=========i",i)
    file_x.close()
    file_y.close()

def make_filelist(path):
    # file_t = open(path+'new_train.txt')
    file_x = open('./data/train_all.txt', 'a+')
    # file_y = open('./data/test_all.txt', 'a+')
    # i = 20
    file_path = 'train/'
    fileList = os.listdir(path+file_path)
    for file in fileList:
        # print(file)
        path_name = file_path+file
        nn = file.split(".")[0]
        # print(nn)
        try:
            xx = 'txt/'+nn+'.txt'
            # print(xx)
            file_t = open(path+xx)
            # print(file_t)
            word = file_t.readline()
            new_name = path_name +'\t'+word+'\t'+'xxxxxxxxxxxxxxxxx'+'\n'
            file_x.writelines(new_name)
            print(new_name)
        except:
            pass
    file_x.close()
    # while 1:
    #     line = file_t.readline()
    #     if not line:
    #         break
    #     pass  # do something
    #     x = random.randint(1, 100)
    #     if x<=10:
    #         sp = line.split()
    #         old_name = './data/'+sp[0]
    #         new_name = './data/zanghua/test/'+'rm_test_'+str(i)+'.wav'
    #         shutil.move(old_name, new_name)
    #         print("copying....", old_name, new_name)
    #         pp1 =' '.join(sp[1:-1])
    #         print(pp1)
    #         neww = 'zanghua/train/rm_test_'+str(i)+'.wav'+'\t'+str(pp1)+'\t'+sp[-1]+'\n'
    #         print(neww)
    #         file_y.writelines(neww)
    #         i+=1
    #     else:
    #         file_x.writelines(line)
    # print("=========i",i)
    # file_x.close()
    # file_y.close()
# def clean_test(path):
#     file_x = open('./test.txt', 'a+')
#     fileList = os.listdir(path + 'test/')
#     for file in fileList:
#         new_name =
if __name__=='__main__':
    path='../NLPData/wav/'
    # rename(path,919)
    # creat_test_train(path)
    # make_filelist(path)
