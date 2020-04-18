from __future__ import print_function

import numpy as np
import cv2

import os
import sys
import shutil
import argparse
import time
import logging
import random


def parse_args():
    # hyper-parameters are from ResNet paper
    parser = argparse.ArgumentParser(
        description='Split Video')
    parser.add_argument('--path_file', type=str, default=None,
                        help='path to video file')
    parser.add_argument('--path_dir', type=str, default=None,
                        help='path to video dir')
    parser.add_argument('--save_path', type=str, default='split',
                        help='save dir')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    test_i = 0
    train_i = 0
    args = parse_args()

    video_list = []
    times = []
    frames = []
    print(args.path_dir)
    if args.path_dir:
        for root, dirs, files in os.walk(args.path_dir):
            for file in files:
                if '.mp4' in file:
                    video_list.append(os.path.join(root, file))
    else:
        assert args.path_file is not None
        video_list.append(args.path_file)

    print(video_list)

    if not os.path.exists(args.save_path):
        os.makedirs(args.save_path)
    if not os.path.exists(os.path.join(args.save_path, 'writing')):
        os.makedirs(os.path.join(args.save_path, 'writing'))
    if not os.path.exists(os.path.join(args.save_path, 'no')):
        os.makedirs(os.path.join(args.save_path, 'no'))

    frames_index = 0
    
    print('start loading data')
    t_start = time.time()
    for video in video_list:
        cap = cv2.VideoCapture(video)
        if 'writing' in video:
            folder = "writing"
        else:
            folder = "no"
        count_index = 0
        while True:
            success, frame = cap.read()
            if not success:
                break
            count_index += 1
            if count_index == 10:
                name = os.path.join(args.save_path, folder, os.path.basename(video).split('.')[0] \
                                    +"_"+ "{:04d}".format(frames_index) + ".jpg")
                cv2.imwrite(name, frame)
                count_index = 0
                frames_index += 1
    t_end = time.time()
    print('time cost', t_end - t_start, 's')
    cap.release()
    cv2.destroyAllWindows()
