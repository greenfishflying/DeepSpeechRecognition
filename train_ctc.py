import os
import tensorflow as tf
from utils import get_data, data_hparams
from keras.callbacks import ModelCheckpoint
import time


# 0.准备训练所需数据------------------------------
data_args = data_hparams()
data_args.data_type = 'train'
data_args.data_path = './data/'
data_args.thchs30 = False
data_args.aishell = False
data_args.prime = False
data_args.stcmd = False
data_args.zanghua = True
data_args.batch_size = 4
data_args.data_length = 20000
# data_args.data_length = None
data_args.shuffle = True
train_data = get_data(data_args)
continue_training =True
# 0.准备验证所需数据------------------------------
data_args = data_hparams()
data_args.data_type = 'test'
data_args.data_path = './data/'
data_args.thchs30 = False
data_args.aishell = False
data_args.prime = False
data_args.stcmd = False
data_args.zanghua = True
data_args.batch_size = 4
# data_args.data_length = None
data_args.data_length = 20000
data_args.shuffle = True
dev_data = get_data(data_args)

# 1.声学模型训练-----------------------------------
from model_speech.cnn_ctc import Am, am_hparams
# from model_speech.gru_ctc import Am, am_hparams
# from model_speech.deepspeech2 import Am, am_hparams
am_args = am_hparams()
am_args.vocab_size = len(train_data.am_vocab)
am_args.gpu_nums = 1
am_args.lr = 0.0008
am_args.is_training = True
am = Am(am_args)

if continue_training ==True:
    if os.path.exists('logs_am/saved_model/model.h5'):
        print('load acoustic model...')
        am.ctc_model.load_weights('logs_am/model.h5')

epochs = 10
batch_num = len(train_data.wav_lst) // train_data.batch_size

# checkpoint
ckpt = "model_{epoch:02d}-{val_acc:.2f}.h5"
checkpoint = ModelCheckpoint(os.path.join('./checkpoint', ckpt), monitor='val_loss', save_weights_only=False, verbose=1, save_best_only=True)

#
for k in range(epochs):
    print('this is the', k+1, 'th epochs trainning !!!')
    st = time.time()
    batch = train_data.get_am_batch()
    se = time.time()
    print("batch time ",se-st)

    dev_batch = dev_data.get_am_batch()
    see = time.time()
    print("dev branch time ",see-se)

    am.ctc_model.fit_generator(batch, steps_per_epoch=batch_num, epochs=20, callbacks=[checkpoint], workers=1, use_multiprocessing=False, validation_data=dev_batch, validation_steps=2)
    print('saving models')
    am.ctc_model.save_weights('logs_am/model.h5')
    ettt= time.time()
    print("训练一轮需要消耗时间为",ettt-st)
# batch = train_data.get_am_batch()
# dev_batch = dev_data.get_am_batch()
#
# am.ctc_model.fit_generator(batch, steps_per_epoch=batch_num, epochs=1, callbacks=[checkpoint], workers=1, use_multiprocessing=False, validation_data=dev_batch, validation_steps=200)
am.ctc_model.save_weights('logs_am/model.h5')