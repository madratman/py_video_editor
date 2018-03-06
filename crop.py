import cv2
from argparse import ArgumentParser
import os
import numpy as np
from joblib import Parallel, delayed

print_every_nth = 200

parser = ArgumentParser()
parser.add_argument('--orig_video_fname', type=str)
parser.add_argument('--cropped_video_fname', type=str)
parser.add_argument('--crop_top', type=int, default=0)
parser.add_argument('--crop_left', type=int, default=0)
parser.add_argument('--crop_bottom', type=int, default=0)
parser.add_argument('--crop_right', type=int, default=0)
args = parser.parse_args()

def crop_video(args):
    orig_capture = cv2.VideoCapture(args.orig_video_fname)

    orig_fps = int(orig_capture.get(cv2.cv.CV_CAP_PROP_FPS))
    orig_width = int(orig_capture.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH))   
    orig_height = int(orig_capture.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT))
    orig_num_frames = int(orig_capture.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))

    crop_width = orig_width - (args.crop_left + args.crop_right)
    crop_height = orig_height - (args.crop_top + args.crop_bottom)
    fourcc = cv2.cv.CV_FOURCC(*'XVID')
    video_crop = cv2.VideoWriter(args.cropped_video_fname, fourcc, orig_fps, (crop_width, crop_height))
    ctr = 0
 
    while(orig_capture.isOpened()):
        ret, frame = orig_capture.read()
        if ret==True:
            frame_crop = frame[args.crop_top:args.crop_top+crop_height, args.crop_left:args.crop_left+crop_width]
            # print frame.shape, frame_crop.shape, (crop_height, crop_width)
            video_crop.write(frame_crop)
            ctr+=1
            if not (ctr%print_every_nth):
                print "{} of {} done".format(ctr, orig_num_frames)
        else:
            break

crop_video(args)
