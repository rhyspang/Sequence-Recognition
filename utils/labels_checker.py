from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from collections import Counter
import argparse
import csv


args = argparse.ArgumentParser()
args.add_argument('-f', '--file', help="label filename")
args.add_argument('-o', '--output',
                  default="format.csv", help="output filename")
args.add_argument('-m', '--mode', help="mode. check or replace")
FLAGS = args.parse_args()


CONVERT_MAP = {
    "—": "-",
    "，、": ",",
    "）": ")",
    "（": "(",
    "“”":  "\"",
    "‘’": "'",
    "？": "?",
    "·": ".",
    "：": ":",
    "、": "",
    "分良言一句三冬暖恶语伤人六月寒°": "",
    "！": "!",
    "…": "...",
    "。": ".",
    "；": ";",
    "①": "1",
    "＊": "*",
    "②": "2"
}


def main():
    counter = Counter()
    invalid_cnt = 0
    with open(FLAGS.file, 'r') as f:
        reader = csv.reader(f)
        # writer = csv.writer(fw, quoting=csv.QUOTE_ALL)
        for idx, (path, label) in enumerate(reader, 1):
            print(idx)
            valid = True
            for char in label:
                if not 0 < ord(char) < 128:
                    counter[char] += 1
                    valid = False

            if not valid:
                invalid_cnt += 1
                print(label)

            # writer.writerow((path, label))

    for item in counter.most_common():
        print(item)
    print(invalid_cnt)


if __name__ == '__main__':
    main()
