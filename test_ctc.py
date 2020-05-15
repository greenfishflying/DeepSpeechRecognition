#coding=utf-8
import os
import difflib
import tensorflow as tf
import numpy as np
from utils import decode_ctc, GetEditDistance,cal_ctc_acc


# 0.准备解码所需字典，参数需和训练一致，也可以将字典保存到本地，直接进行读取
from utils import get_data, data_hparams
data_args = data_hparams()
data_args.data_length=20000
train_data = get_data(data_args)
print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
print("=====train_data_amvocab",len(train_data.pny_vocab) )




# 1.声学模型-----------------------------------
from model_speech.cnn_ctc import Am, am_hparams
# from model_speech.gru_ctc import Am, am_hparams

am_args = am_hparams()
am_args.vocab_size = len(train_data.am_vocab)
am = Am(am_args)
print('loading acoustic model...')
am.ctc_model.load_weights('logs_am/model.h5')
# am.ctc_model.load_weights('checkpoint/model_01-0.00.hdf5')
# 2.语言模型-------------------------------------------


# 3. 准备测试所需数据， 不必和训练数据一致，通过设置data_args.data_type测试，
#    此处应设为'test'，我用了'train'因为演示模型较小，如果使用'test'看不出效果，
#    且会出现未出现的词。
data_args = data_hparams()
data_args.data_type = 'test'
data_args.zanghua = True
data_args.data_length=20000
test_data = get_data(data_args)
print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
print("=====test_data_amvocab",len(test_data.pny_vocab) )
print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
# 4. 进行测试-------------------------------------------
am_batch = test_data.get_am_batch()
word_num = 0
word_error_num = 0
cicuo_list = []
for i in range(13000):
    print('\n the ', i, 'th example.')
    # 载入训练好的模型，并进行识别
    inputs, _ = next(am_batch)
    x = inputs['the_inputs']
    print("x.shape",x.shape)
    # print(test_data.pny_lst)
    y = test_data.pny_lst[i]
    # print(y)
    result = am.model.predict(x, steps=1)
    # 将数字结果转化为文本结果
    result, text = decode_ctc(result, train_data.am_vocab)

    cicuo = cal_ctc_acc(text,y)
    cicuo_list.append(cicuo)
    text = ' '.join(text)
    print('数字结果：', result)
    print('文本结果：', text)
    print('原文结果：', ' '.join(y))
    print("cicuo",cicuo)
    print("cicuowulv",np.mean(cicuo_list))


am.ctc_model.load_weights('logs_am/model.h5')

