from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import argparse
import csv
import os


args = argparse.ArgumentParser()
args.add_argument('-f', '--file', help="file to read")
args.add_argument('-p', '--percent', type=float, default=10,
                  help="train set percentage")
args.add_argument('-t', '--train', default='train.csv',
                  help="train set file name")
args.add_argument('-e', '--eval', default='eval.csv',
                  help="eval set file name")
FLAGS = args.parse_args()


def main():
    pwd = os.path.dirname(os.path.abspath(FLAGS.file))

    with open(FLAGS.file, 'r') as fr,\
            open(FLAGS.train, 'w') as ft, open(FLAGS.eval, 'w') as fe:
        line_count = sum(1 for _ in fr)
        fr.seek(0)
        reader = csv.reader(fr)
        ft_writer = csv.writer(ft, quoting=csv.QUOTE_ALL)
        fe_writer = csv.writer(fe, quoting=csv.QUOTE_ALL)

        for path, label in reader:
            path = os.path.join(pwd, path)
            if reader.line_num / line_count < FLAGS.percent:
                ft_writer.writerow((path, label))
            else:
                fe_writer.writerow((path, label))


if __name__ == '__main__':
    main()
