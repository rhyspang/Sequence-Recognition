#   offline_handwritten_recognition
#   --------------------------------------
#
#   Written and maintained by Rhys Pang <rhyspang@qq.com>
#
#   Copyright 2018 rhys. All Rights Reserved.
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import argparse

import tensorflow as tf
from tensorflow.python.framework.errors_impl import OutOfRangeError, \
    InvalidArgumentError

args = argparse.ArgumentParser()
args.add_argument('-f', '--file', help="input file")
FLAGS = args.parse_args()


def main():

    filename_queue = tf.train.string_input_producer([FLAGS.file], num_epochs=1)
    reader = tf.TextLineReader()
    _, value = reader.read(filename_queue)
    default_value = [['None'], ['None']]
    path, label = tf.decode_csv(value,
                                record_defaults=default_value)
    # image_file = tf.read_file(path)
    # image = tf.image.decode_image(image_file)

    with tf.Session() as sess:
        tf.local_variables_initializer().run()

        # user global_variables_initializer, FailedPreconditionError occurred
        # tf.global_variables_initializer().run()

        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(coord=coord)
        all_cnt, err_cnt = 0, 0
        while True:
            try:
                all_cnt += 1
                path_tensor, label_tensor = sess.run([path, label])
                # path_tensor = sess.run(path)
                # image_tensor = sess.run(image)
                print(path_tensor)
                print(label_tensor)
            except InvalidArgumentError as iae:
                err_cnt += 1
                print(iae)
            except OutOfRangeError:
                print('end')
                break
            finally:
                print("%s/%s" % (err_cnt, all_cnt-1))

        coord.request_stop()
        coord.join(threads)


if __name__ == '__main__':
    main()
