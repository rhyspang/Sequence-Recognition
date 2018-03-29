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

from base import base_model


class CRNNModel(base_model.BaseModel):

    def __init__(self, config):
        super().__init__(config)

    def init_saver(self):
        self.saver = tf.train.Saver(max_to_keep=self.config.max_to_keep)
        pass

    def build_model(self):
        pass
