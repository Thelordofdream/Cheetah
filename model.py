import tensorflow as tf
import pymysql
from tensorflow.contrib import rnn


class nerual_network(object):
    def __init__(self, steps=28, inputs=28, hidden=128, batch_size=128, classes=10, learning_rate=0.01):
        self.steps = steps
        self.inputs = inputs
        self.hidden = hidden
        self.batch_size = batch_size
        self.classes = classes
        self.learning_rate = learning_rate
        self.x = tf.placeholder("float", [None, self.steps, self.inputs])
        self.y = tf.placeholder("float", [None, self.classes])
        self.keep_prob = tf.placeholder(tf.float32)

    def shape_tranform(self):
        x = tf.transpose(self.x, [1, 0, 2])
        x = tf.reshape(x , [-1, self.inputs])
        x = tf.split(x, self.steps, 0)
        return x


class LSTM_layer(nerual_network):
    def __init__(self, name="N1"):
        super(LSTM_layer, self).__init__()
        self.name = name
        self.output = None
        self.cross_entropy = None
        self.optimizer = None
        self.accuracy = None
        with tf.variable_scope(self.name):
            with tf.variable_scope("inputs"):
                x = self.shape_tranform()

            with tf.variable_scope("lstm_layer"):
                lstm_cell = rnn.BasicLSTMCell(self.inputs, forget_bias=0.1, state_is_tuple=True)
                outputs, states = rnn.static_rnn(lstm_cell, x, initial_state=lstm_cell.zero_state(self.batch_size, tf.float32))

            with tf.variable_scope("dropout"):
                hidden_w = tf.Variable(tf.random_normal([self.inputs, self.classes]), name='hidden_w')
                hidden_b = tf.Variable(tf.random_normal([self.classes]), name='hidden_b')
                readout = tf.matmul(outputs[-1], hidden_w) + hidden_b
                self.output = tf.nn.dropout(readout, self.keep_prob)

            with tf.name_scope('loss'):
                self.cross_entropy= tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=self.y, logits=self.output))
            tf.summary.scalar('cross_entropy', self.cross_entropy)

            with tf.name_scope('optimizer'):
                self.optimizer = tf.train.AdamOptimizer(learning_rate=self.learning_rate).minimize(self.cross_entropy)
                correct_pred = tf.equal(tf.argmax(self.output, 1), tf.argmax(self.y, 1))
                self.accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))
            tf.summary.scalar('accuracy', self.accuracy)

            self.merged = tf.summary.merge_all()


class data(nerual_network):
    def __init__(self, stock_name="AAPL"):
        super(data, self).__init__()
        connection = pymysql.connect(user='root', password='root',
                                     database='tickets')
        cursor = connection.cursor()
        commit = "select * from $%s;" % stock_name
        cursor.execute(commit)
        self.data = cursor.fetchall()
        self.number = len(self.data)
        self.start_point = -self.batch_size

    def next_batch(self):
        self.start_point += self.batch_size





