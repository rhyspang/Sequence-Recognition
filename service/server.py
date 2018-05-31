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

import flask
import numpy as np
import tensorflow as tf

from predictor import predictor


app = flask.Flask(__name__)
sess = tf.Session()
sequence_predictor = predictor.Predictor("model_dir/1525577622", sess)


@app.route("/api/sr", methods=["POST"])
def sequence_recognize():
    image_data = np.array(flask.request.json, dtype=np.int16)
    image_data = image_data[..., np.newaxis]
    result = sequence_predictor.predict(image_data)
    print(str(result['words'][0]))
    return flask.jsonify(result['words'][0].decode('utf-8'))


@app.route("/")
def index():
    return flask.render_template("index.html")


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
