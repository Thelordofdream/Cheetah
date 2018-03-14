import tensorflow as tf
from tensorflow.contrib import rnn


class nerual_network(object):
    def __init__(self, steps=10, inputs=5, hidden=5, batch_size=500, classes=1):
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
    def __init__(self, filename):
        super(data, self).__init__()
        filename_queue = tf.train.string_input_producer([filename])
        reader = tf.TFRecordReader()
        _, serialized_example = reader.read(filename_queue)
        features = tf.parse_single_example(serialized_example,
                                           features={
                                               'label': tf.FixedLenFeature([1], tf.float32),
                                               'sequence': tf.FixedLenFeature([], tf.string),
                                           })
        self.sequence = tf.decode_raw(features['sequence'], tf.float64)
        self.sequence = tf.reshape(self.sequence, shape=[self.steps, self.inputs])
        self.label = tf.cast(features['label'], tf.float32)

    def get_batches(self):
        x_batch, y_batch = tf.train.shuffle_batch([self.sequence, self.label], batch_size=self.batch_size,
                               capacity=1000, min_after_dequeue=200, num_threads=4)
        return x_batch, y_batch



