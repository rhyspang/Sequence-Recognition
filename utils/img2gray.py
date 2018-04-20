# coding: utf8
# Copyright (c) 2018 Didichuxing Inc.
# Author: Sheng Pang (pangsheng_i@didichuxing.com)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from collections import Counter
from multiprocessing import Pool, Value
import argparse
import uuid
import os

import cv2
import pandas as pd

args = argparse.ArgumentParser()
args.add_argument('-f', '--file', help='file to read')
args.add_argument('-s', '--sep', default=',', help="separated by")
args.add_argument('-ws', '--write_sep', default='^', help="write separator")
args.add_argument('-d', '--output', default='data_all')
FLAGS = args.parse_args()

counter = Counter()
new_label = pd.DataFrame(columns=['path', 'label'])


def save(param):
    path, label = param
    try:
        img = cv2.imread(path)
        base = "line" if img.shape[1] / img.shape[0] > 2 else "square"
        base = os.path.join(FLAGS.output, base)
        dir_name = os.path.join(base, '%08d' % (counter[base] // 250))
        filename = uuid.uuid4().hex + ".png"
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        fullname = os.path.join(dir_name, filename)
        cv2.imwrite(fullname, img)
        print(fullname)
        counter[base] += 1
        return fullname, label
    except Exception as e:
        print(e)
        # print('err path: %s' % fullname)
        return None


def main():
    value_list = []
    data_set = pd.read_csv(FLAGS.file, FLAGS.sep)
    for _, row in data_set.iterrows():
        value_list.append(row.tolist())
    print('read data completed')

    pool = Pool(5)
    result = pool.map(save, value_list)
    print(len(result))

    with open('new_labels.csv', 'w') as f:
        for item in result:
            try:
                if item is None:
                    continue
                key, value = item
                key = str(key)
                value = str(value)
                f.write("%s^%s\n" % (key.strip(), value.strip()))
            except Exception as e:
                print(e)


if __name__ == '__main__':
    main()
