import tensorflow as tf
from tensorflow.contrib import rnn


class nerual_network(object):
    def __init__(self, name="N1", steps=28, inputs=28, hidden=128, batch_size=128, classes=10, learning_rate=0.01):
        self.name = name
        self.steps = steps
        self.inputs = inputs
        self.hidden = hidden
        self.batch_size = batch_size
        self.classes = classes
        self.x = tf.placeholder("float", [None, self.steps, self.inputs])
        self.y = tf.placeholder("float", [None, self.classes])
        self.keep_prob = tf.placeholder(tf.float32)
        self.learning_rate = learning_rate
        self.output = None
        self.cost = None
        self.optimizer = None
        self.accuracy = None
        self.biases = {
            'hidden': tf.Variable(tf.random_normal([self.classes]), name='hidden_b'),
        }
        self.weights = {
            'hidden': tf.Variable(tf.random_normal([self.inputs, self.classes]), name='hidden_w'),
        }

    def shape_tranform(self):
        x = tf.transpose(self.x, [1, 0, 2])
        x = tf.reshape(x , [-1, self.inputs])
        x = tf.split(x, self.steps, 0)
        return x

    def LSTM_layer(self):
        with tf.variable_scope(self.name):
            x = self.shape_tranform()
            lstm_cell = rnn.BasicLSTMCell(self.inputs, forget_bias=0.1, state_is_tuple=True)
            outputs, states = rnn.static_rnn(lstm_cell, x, initial_state=lstm_cell.zero_state(self.batch_size, tf.float32))
            readout = tf.matmul(outputs[-1], self.weights['hidden']) + self.biases['hidden']
            self.output = tf.nn.dropout(readout, self.keep_prob)

    def set_optimizer(self):
        self.cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(labels=self.y, logits=self.output))
        self.optimizer = tf.train.AdamOptimizer(learning_rate=self.learning_rate).minimize(self.cost)
        correct_pred = tf.equal(tf.argmax(self.output, 1), tf.argmax(self.y, 1))
        self.accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))


