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
from collections import Counter
from multiprocessing import Process, Value, Lock, Pool, Manager
import argparse
import codecs
import csv
import datetime
import os
import uuid

import cv2
import numpy as np
import pandas as pd
import tqdm

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


def csv_normalize(row, sep=','):
    normal = []
    for field in row:
        field = field.replace('"', '""')
        field = '"%s"' % field
        normal.append(field)
    return sep.join(normal)


def img2gray(path):
    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    shape_type = "line" if img.shape[1] / img.shape[0] > 2 else "square"
    counter[shape_type] += 1
    abs_base_path = os.path.abspath(FLAGS.output_directory)
    base_path = os.path.join(abs_base_path,
                             shape_type,
                             "%08d" % (counter[shape_type] // 1000))
    if not os.path.exists(base_path):
        os.makedirs(base_path)
    filename = "%s.jpg" % uuid.uuid4().hex
    full_path = os.path.join(base_path, filename)
    cv2.imwrite(full_path, img)
    return full_path


def read_csv():
    with codecs.open(FLAGS.raw_label, 'r', 'utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        for line in reader:
            yield line


def write(data):
    with codecs.open(FLAGS.output_label, 'w', 'utf-8') as f:
        for line in data:
            f.write(line+'\n')


def main():

    results = []
    i = 0
    with tqdm.tqdm(read_csv()) as t:
        for idex, (path, label) in enumerate(t, 1):

            try:
                path = os.path.join(FLAGS.raw_directory, path)
                full_path = img2gray(path)
                line = csv_normalize([full_path, label])
                results.append(line)
            except Exception as e:
                print(path)
                print(e)
                i += 1
        write(results)
        print(i)
    pass


if __name__ == '__main__':
    main()
