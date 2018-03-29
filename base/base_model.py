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

import tensorflow as tf


class BaseModel(object):

    def __init__(self, config):
        self.config = config
        self.init_global_step()
        self.init_cur_epoch()

    def save(self, sess):
        print('Saving model...')
        self.saver.save(sess, self.config.checkpoint_dir,
                        self.global_step_tensor)
        print('Model saved')

    def load(self, sess):
        latest_checkpoint = tf.train.latest_checkpoint(
            self.config.checkpoint_dir
        )
        if latest_checkpoint:
            print('Loading model checkpoint {}...\n'.format(latest_checkpoint))
            self.saver.restore(sess, latest_checkpoint)
            print('model loaded')

    def init_cur_epoch(self):
        with tf.variable_scope('cur_epoch'):
            self.cur_epoch_tensor = tf.Variable(0,
                                                trainable=False,
                                                name='cur_epoch')
            self.increment_cur_epoch_tensor = tf.assign(
                self.cur_epoch_tensor,
                self.cur_epoch_tensor+1
            )

    def init_global_step(self):
        with tf.variable_scope('global_step'):
            self.global_step_tensor = tf.Variable(0, trainable=False,
                                                  name='global_step')

    def init_saver(self):
        raise NotImplementedError

    def build_model(self):
        raise NotImplementedError
