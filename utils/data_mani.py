# coding: utf8
# Copyright (c) 2018 Didichuxing Inc.
# Author: Sheng Pang (pangsheng_i@didichuxing.com)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import argparse
import os

import pandas as pd
import numpy as np

args = argparse.ArgumentParser()
args.add_argument('-f', '--filename', required=True, help="filename")
args.add_argument('-s', '--sep', default=',', help="separated by")
args.add_argument('-p', '--percent', default=10, type=int, help="percentage")
args.add_argument('-ws', '--write_sep', default='^', help="write separator")
FLAGS = args.parse_args()


def main():
    data = pd.read_csv(FLAGS.filename, sep=FLAGS.sep)
    data['path'] = os.path.abspath('.') + os.sep + data['path'].astype(str)
    data.to_csv("label_full_path.csv", FLAGS.write_sep,
                index=False, header=False)
    data_arr = data.as_matrix()
    np.random.shuffle(data_arr)
    data_len = len(data_arr)
    sep_point = data_len * FLAGS.percent // 100
    eval_set, train_set = pd.DataFrame(data_arr[:sep_point]), \
                          pd.DataFrame(data_arr[sep_point:])
    print(eval_set.shape, train_set.shape)
    eval_set.to_csv('eval.csv', FLAGS.write_sep, index=False, header=False)
    train_set.to_csv('train.csv', FLAGS.write_sep, index=False, header=False)


if __name__ == '__main__':
    main()
