from tensorflow.examples.tutorials.mnist import input_data
import tensorflow as tf
import numpy as np
import pymysql
import model


def get_data(stock_name="AAPL"):
    connection = pymysql.connect(user='root', password='root',
                                 database='tickets')
    cursor = connection.cursor()
    commit = "select * from $%s;" % stock_name
    cursor.execute(commit)
    results = cursor.fetchall()
    times = len(results)
    return results, times


def train(model, mnist, training_iters = 1000):
    init = tf.global_variables_initializer()
    with tf.Session() as sess:
        sess.run(init)
        step = 1
        while step < training_iters:
            batch_xs, batch_ys = mnist.train.next_batch(model.batch_size)
            batch_xs = batch_xs.reshape((model.batch_size, model.steps, model.inputs))
            sess.run(model.optimizer, feed_dict={model.x: batch_xs, model.y: batch_ys, my_network.keep_prob: 0.5})
            if step % 10 == 0:
                acc = sess.run(model.accuracy, feed_dict={model.x: batch_xs, model.y: batch_ys, my_network.keep_prob: 1.0})
                loss = sess.run(model.cost, feed_dict={model.x: batch_xs, model.y: batch_ys, my_network.keep_prob: 1.0})
                print("Iter " + str(step) + ", Minibatch Loss= " + "{:.6f}".format(
                    loss) + ", Training Accuracy= " + "{:.5f}".format(acc))
            step += 1
        print("Optimization Finished!")


if __name__ == "__main__":
    mnist = input_data.read_data_sets("MNIST_data", one_hot=True)
    my_network = model.nerual_network(name="LSTM")
    my_network.LSTM_layer()
    my_network.set_optimizer()
    train(my_network, mnist)
