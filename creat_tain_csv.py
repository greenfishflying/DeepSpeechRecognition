import os
import csv
import re
f = open('train.csv','w',encoding='utf-8')
csv_writer = csv.writer(f)
csv_writer.writerow(["wav_filename","wav_length_ms","transcript"])

path='/home/null/Project/NLPData/TIMIT/'
def get_filelist(dir):
    Filelist = []
    t_path = 'TRAIN/'
    for home, dirs, files in os.walk(path+t_path):
          # print("home",home)
          # print("dirs",dirs)
          for filename in files:
            (filepath, tempfilename) = os.path.split(filename)
            (name, extension) = os.path.splitext(tempfilename)
            # print("filepath,tempfilename", filepath, tempfilename)
            # print("filename,extension",filename,extension)
            TxTfile = os.path.join(home, name+'.TXT')
            file = open(TxTfile, 'r', encoding='utf-8')
            userlines = file.readlines()
            # csv_writer.writerow()
            # print(type(userlines[0]))
            # user = ''.join(userlines[0])
            user = userlines[0].split(' ',2)
            user_n = user [1:]
            # user.split()
            # print("userlines",user_n)
            voicename = os.path.join(home, filename)
            # user[2].replace('''''')
            csv_writer.writerow([voicename,user[1],user[2]])
            Filelist.append(os.path.join(home, filename))
# # 文件名列表，只包含文件名
    # Filelist.append( filename)
    f.close()
    return Filelist

if __name__ =="__main__":

    Filelist = get_filelist(dir)
    print(len(Filelist))
    print(Filelist[0])
    # for file in Filelist:
    #     print(file)
