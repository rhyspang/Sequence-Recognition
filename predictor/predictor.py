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


class Predictor(object):

    def __init__(self, model_dir=None, sess=None):
        self.session = sess or tf.get_default_session()
        self.model = tf.saved_model.loader.load(self.session,
                                                ['serve'],
                                                model_dir)
        self._input_dict, self._output_dict = \
            Predictor._signature_def_to_tensor(
                self.model.signature_def['predictions']
            )

    def predict(self, image):
        return self.session.run(
            self._output_dict,
            feed_dict={self._input_dict['images']: image}
        )

    def predict_image(self, image_path: str):
        image_contents = tf.read_file(image_path)
        image = tf.image.decode_image(image_contents)
        image = tf.image.rgb_to_grayscale(image)
        return self.predict(self.session.run(image))

    @staticmethod
    def _signature_def_to_tensor(signature_def):
        def get_items(sd_dict):
            return {
                key: graph.get_tensor_by_name(value.name)
                for key, value in sd_dict.items()
            }

        graph = tf.get_default_graph()
        return get_items(signature_def.inputs), get_items(signature_def.outputs)


def main():
    tf.Session().as_default()
    p = Predictor('model_dir/1525577622')
    print(p.predict('1.png')['words'])


if __name__ == '__main__':
    main()
