import tensorflow as tf
import model
import matplotlib.pyplot as plt


def train(model, x_batch, y_batch, sess, training_iters=45000, display_step=1000):
    train_writer = tf.summary.FileWriter('./train', sess.graph)
    sess.run(init)
    step = 1
    while step <= training_iters:
        batch_xs, batch_ys = sess.run([x_batch, y_batch])
        sess.run(model.optimizer, feed_dict={model.x: batch_xs, model.y: batch_ys})
        if step % display_step == 0:
            summary, loss, acc = sess.run([model.merged, model.cost, model.accuracy], feed_dict={model.x: batch_xs, model.y: batch_ys})
            train_writer.add_summary(summary, step)
            print("Iter " + str(step) + ", Minibatch Loss= " + "{:.6f}".format(loss) + ", Training Accuracy= " + "{:.5f}".format(acc))
        step += 1
    print("Optimization Finished!")


def test(model, x_test, y_test, sess):
    test_data, test_label = sess.run([x_test, y_test])
    test = sess.run(model.output, feed_dict={model.x: test_data, model.y: test_label})
    error_sum = 0
    for i in range(model.batch_size):
        error_sum += abs(test[i] - test_label[i]) * 20000
        # print test[i] * 20000, test_label[i] * 20000
    print error_sum / model.batch_size
    # plt.plot(test_label * 20000, 'b-')
    # plt.plot(test * 20000, 'r-')
    # plt.legend(loc='best')
    # plt.show()

def save(sess):
    saver = tf.train.Saver()
    save_path = saver.save(sess, "./model/model.ckpt")
    print("Model saved in file: %s" % save_path)


if __name__ == "__main__":
    # mnist = input_data.read_data_sets("MNIST_data", one_hot=True)
    train_data = model.data(filename="train.tfrecord")
    test_data = model.data(filename="test.tfrecord")
    x_batch, y_batch = train_data.get_batches()
    x_test, y_test = test_data.get_batches()
    my_network = model.LSTM_layer(name="trading", learning_rate=0.001)
    init = tf.global_variables_initializer()
    with tf.Session() as sess:
        threads = tf.train.start_queue_runners(sess=sess)
        sess.run(init)
        train(my_network, x_batch, y_batch, sess)
        test(my_network, x_test, y_test, sess)
        save(sess)