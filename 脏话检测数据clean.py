import os
import csv
import re
from shutil import copy
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


if __name__=='__main__':
    path='/home/null/Project/NLPData/普通话内部车上采集已完成/2/'
    rename(path,919)
