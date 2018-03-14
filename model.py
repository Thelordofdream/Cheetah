import tensorflow as tf
import pymysql
from tensorflow.contrib import rnn
import numpy as np


class nerual_network(object):
    def __init__(self, steps=10, inputs=4, hidden=4, batch_size=330, classes=1):
        self.steps = steps
        self.inputs = inputs
        self.hidden = hidden
        self.batch_size = batch_size
        self.classes = classes


class LSTM_layer(nerual_network):
    def __init__(self, name="N1", learning_rate=0.001):
        super(LSTM_layer, self).__init__()
        self.name = name
        self.learning_rate = learning_rate
        self.output = None
        self.cost = None
        self.optimizer = None
        self.accuracy = None
        with tf.variable_scope("input_layer"):
            self.x = tf.placeholder("float", [None, self.steps, self.inputs], name="x")
            x = self.shape_tranform()

        with tf.variable_scope("lstm_layer"):
            lstm_cell = rnn.BasicLSTMCell(self.inputs, forget_bias=0.1, state_is_tuple=True)
            outputs, states = rnn.static_rnn(lstm_cell, x, initial_state=lstm_cell.zero_state(self.batch_size, tf.float32))

        with tf.variable_scope("hidden_layer"):
            hidden_w = tf.Variable(tf.random_normal([self.inputs, self.classes]), name='hidden_w')
            hidden_b = tf.Variable(tf.random_normal([self.classes]), name='hidden_b')
            self.output = tf.matmul(outputs[-1], hidden_w) + hidden_b
        #
        # with tf.variable_scope("dropout"):
        #     self.keep_prob = tf.placeholder(tf.float32, name="keep_prob")
        #     self.output = tf.nn.dropout(readout, self.keep_prob)


        with tf.name_scope('loss'):
            self.y = tf.placeholder("float", [None, self.classes], name="y")
            self.cost = tf.losses.mean_squared_error(self.y, self.output)
        tf.summary.scalar('cross', self.cost)

        with tf.name_scope('optimizer'):
            self.optimizer = tf.train.AdamOptimizer(learning_rate=self.learning_rate).minimize(self.cost)
            correct_pred = tf.equal(self.output, self.y)
            self.accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))
        tf.summary.scalar('accuracy', self.accuracy)

        self.merged = tf.summary.merge_all()

    def shape_tranform(self):
        x = tf.transpose(self.x, [1, 0, 2])
        x = tf.reshape(x, [-1, self.inputs])
        x = tf.split(x, self.steps, 0)
        return x


class data(nerual_network):
    def __init__(self, stock_name):
        super(data, self).__init__()
        connection = pymysql.connect(user='root', password='root',
                                     database='tickets')
        cursor = connection.cursor()
        commit = "select * from $%s;" % stock_name
        cursor.execute(commit)
        self.data = np.array([list([float(j)/110 for j in i[2:6]]) for i in cursor.fetchall()])
        self.number = len(self.data)
        self.start_point = 0

    def next_batch(self):
        if (self.start_point + self.batch_size * self.steps) > self.number:
            self.start_point = 0
        batch_x = np.reshape(
            self.data[self.start_point: self.start_point + self.batch_size * self.steps], [self.batch_size, self.steps, self.inputs])
        batch_y = np.reshape(
            self.data[self.start_point + self.steps:self.start_point + self.batch_size * self.steps + self.steps:self.steps, -1], [self.batch_size, 1])
        self.start_point += self.steps
        return batch_x, batch_y

    def test_batch(self):
        batch_x = np.reshape(
            self.data[self.number - 1 - self.batch_size * self.steps - self.steps:self.number - 1 - self.steps],
            [self.batch_size, self.steps, self.inputs])
        batch_y = np.reshape(
            self.data[
            self.number - 1 - self.batch_size * self.steps:self.number - 1:self.steps, -1],
            [self.batch_size, 1])
        return batch_x, batch_y





