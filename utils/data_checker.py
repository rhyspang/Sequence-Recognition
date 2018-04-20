from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import argparse
import codecs

from PIL import Image
import tensorflow as tf
import tqdm


args = argparse.ArgumentParser()
args.add_argument('-f', '--file', help='filename')
args.add_argument('-d', '--directory', help='directory')
FLAGS = args.parse_args()


def tf_read(path, label):
    try:

        image_content = tf.read_file(path)
        image = tf.image.decode_image(image_content, )
        print(image.eval().shape)

        return True
    except Exception as e:
        print("exception: %s. path: %s. label:%s" % (e, path, label))
        return False


def pil_read(path, label):

    try:
        img = Image.open(path)
        print(img.size)
    except IOError as ioe:
        print(ioe)


def write(filename, batch):
    with codecs.open(filename, 'a', 'utf-8') as f:
        for item in batch:
            f.write("%s^%s" % (item[0], item[1]))


def main():
    all_cnt = 0
    cnt = 0
    err_list = []
    with tf.Session().as_default():
        with codecs.open(FLAGS.file, 'r', 'utf-8') as f:
            with tqdm.tqdm(f, postfix={'no': cnt}) as t:
                for idx, line in enumerate(f.readlines(), 1):
                    print(idx)
                    all_cnt += 1
                    path, label = line.split('^')
                    if not tf_read(path, label):
                        cnt += 1
                        print(cnt)
                        err_list.append((path, label))
                        if len(err_list) == 100:
                            write('err.csv', err_list)
                            err_list = []
                        t.set_postfix({'no': cnt})
                    # pil_read(path, label)


if __name__ == '__main__':
    main()
