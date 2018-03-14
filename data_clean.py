import IO
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np

bitcoin = IO.grab("bitcoin_2000hours.pkl")[1:-1]
bitcoin.reverse()
features = []

for each_hour in bitcoin:
    # extract open, high, low, close price and volume
    features.append([each_hour['open']/20000, each_hour['high']/20000, each_hour['low']/20000, each_hour['close']/20000, each_hour['vol']/40000000])
features = np.array(features)
list = range(len(features))

writer = tf.python_io.TFRecordWriter("train.tfrecord")
for sample_point in list[:-510]:
    each_feature = features[sample_point:sample_point+10]
    each_feature = each_feature.astype(np.float)
    feature = each_feature.tostring()
    label = features[sample_point+10][3]
    example = tf.train.Example(
        features=tf.train.Features(
            feature={'label': tf.train.Feature(float_list=tf.train.FloatList(value=[label])),
                     'sequence': tf.train.Feature(bytes_list=tf.train.BytesList(value=[feature]))
    }))
    writer.write(example.SerializeToString())
writer.close()


writer = tf.python_io.TFRecordWriter("test.tfrecord")
for sample_point in list[-510:-10]:
    each_feature = features[sample_point:sample_point+10]
    each_feature = each_feature.astype(np.float)
    feature = each_feature.tostring()
    label = features[sample_point+10][3]
    example = tf.train.Example(
        features=tf.train.Features(
            feature={'label': tf.train.Feature(float_list=tf.train.FloatList(value=[label])),
                     'sequence': tf.train.Feature(bytes_list=tf.train.BytesList(value=[feature]))
    }))
    writer.write(example.SerializeToString())
writer.close()
