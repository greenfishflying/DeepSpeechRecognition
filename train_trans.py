import os
import tensorflow as tf
from utils import get_data, data_hparams
from keras.callbacks import ModelCheckpoint



# 0.准备训练所需数据------------------------------
data_args = data_hparams()
data_args.data_type = 'train'
data_args.data_path = './data/'

data_args.data_length = 20
train_data = get_data(data_args)
continue_training =True
# 0.准备验证所需数据------------------------------
data_args = data_hparams()
data_args.data_type = 'dev'
data_args.data_path = './data/'

# data_args.data_length = None
data_args.data_length = 1

dev_data = get_data(data_args)

batch_num = 5
# 2.语言模型训练-------------------------------------------
# from model_language.transformer import Lm, lm_hparams
from model_language.cbhg import Lm, lm_hparams
# from model_language.cbhg import Lm, lm_hparams
lm_args = lm_hparams()
lm_args.num_heads = 8
lm_args.num_blocks = 6
lm_args.input_vocab_size = len(train_data.pny_vocab)
lm_args.label_vocab_size = len(train_data.han_vocab)
lm_args.max_length = 20
lm_args.hidden_units = 512
lm_args.dropout_rate = 0.2
lm_args.lr = 0.0003
lm_args.is_training = True
lm = Lm(lm_args)

epochs = 2000
with lm.graph.as_default():
    saver =tf.train.Saver()
with tf.Session(graph=lm.graph) as sess:
    merged = tf.summary.merge_all()
    sess.run(tf.global_variables_initializer())
    add_num = 0
    if continue_training == True:
        if os.path.exists('logs_lm/checkpoint'):
            print('loading language model...')
            latest = tf.train.latest_checkpoint('logs_lm')
            add_num = int(latest.split('_')[-1])
            saver.restore(sess, latest)
    writer = tf.summary.FileWriter('logs_lm/tensorboard', tf.get_default_graph())
    for k in range(epochs):
        total_loss = 0
        batch = train_data.get_lm_batch()
        for i in range(batch_num):
            try:
                input_batch, label_batch = next(batch)
                feed = {lm.x: input_batch, lm.y: label_batch}
                cost,_ = sess.run([lm.mean_loss,lm.train_op], feed_dict=feed)
                total_loss += cost
                if (k * batch_num + i) % 10 == 0:
                    rs=sess.run(merged, feed_dict=feed)
                    writer.add_summary(rs, k * batch_num + i)
            except:
                pass
        print('epochs', k+1, ': average loss = ', total_loss/batch_num)
    saver.save(sess, 'logs_lm/model_%d' % (epochs + add_num))
    writer.close()
