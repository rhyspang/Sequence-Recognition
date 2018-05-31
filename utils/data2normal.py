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
import csv
import os
import uuid
from collections import Counter

import cv2

args = argparse.ArgumentParser()
args.add_argument('-rd',
                  '--raw_directory',
                  help="target image directory to convert")
args.add_argument('-od',
                  '--output_directory',
                  help='output directory')
args.add_argument('-rl',
                  '--raw_label',
                  help="raw label filename to read")
args.add_argument('-ol',
                  '--output_label',
                  default='new_label.csv',
                  help="output label file name")
FLAGS = args.parse_args()


counter = Counter()

def img2gray(path):
    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    shape_type = "line" if img.shape[1] / img.shape[0] > 2 else "square"
    counter[shape_type] += 1

    directory = os.path.join(FLAGS.output_directory,
                             shape_type,
                             "%08d" % (counter[shape_type] // 1000))
    if not os.path.exists(directory):
        os.makedirs(directory)
    filename = "%s.jpg" % uuid.uuid4().hex
    full_path = os.path.join(directory, filename)
    cv2.imwrite(full_path, img)
    return full_path


def main():

    with open(FLAGS.raw_label, 'r') as fr, \
            open(FLAGS.output_label, 'w') as fw:

        reader = csv.reader(fr)
        writer = csv.writer(fw, quoting=csv.QUOTE_ALL)

        for path, label in reader:
            print(reader.line_num)
            try:
                path = img2gray(path)
            except Exception as e:
                print("path: %s, e: %s" % (path, e))
                continue

            writer.writerow((path, label))


if __name__ == '__main__':
    main()
