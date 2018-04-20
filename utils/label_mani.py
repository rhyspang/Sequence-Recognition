# coding: utf8
# Copyright (c) 2018 Didichuxing Inc.
# Author: Sheng Pang (pangsheng_i@didichuxing.com)

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import argparse

args = argparse.ArgumentParser()
args.add_argument('-f', '--file', help="file to read")
args.add_argument('-o', '--out', help="output file")
FLAGS = args.parse_args()


def main():
    with open(FLAGS.file, 'r') as fr, open(FLAGS.out, 'w') as fw:
        for line in fr:
            if line.isspace():
                continue
            path, label = line.split('^')
            path = path.strip().replace('"', '""')
            label = label.strip().replace('"', '""')

            fw.write('"%s","%s"\n' % (path, label))

    pass


if __name__ == '__main__':
    main()
