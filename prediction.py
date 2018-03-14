import model
from HuobiService import *
import tensorflow as tf

def make_prediction(model, sess, data):
    result = sess.run(model.output, feed_dict={model.x: data})
    return result

if __name__ == '__main__':
    coin = 'btcusdt'
    length = 11
    my_network = model.LSTM_layer(name="TC")
    init = tf.global_variables_initializer()

    with tf.Session() as sess:
        saver = tf.train.Saver()
        saver.restore(sess, "model/model.ckpt")
        coin_60min = get_kline(coin, '60min', length)['data']
        data = coin_60min[1:]
        data.reverse()
        make_prediction(my_network, sess, data)
