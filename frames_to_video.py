import cv2
from argparse import ArgumentParser
import os
import numpy as np
# import joblib

## usage 
## python frames_to_video.py --video_file temp.avi --frames_dir /data/datasets/ratneshm/pytorch_results/autel_flight_videos/MAX_0037.MOV --fps 8 --width 640 --height 480
print_every_nth = 200
parser = ArgumentParser()
parser.add_argument('--video_file', help='video file')
parser.add_argument('--frames_dir', type=str)
# parser.add_argument('--width', type=int)
# parser.add_argument('--height', type=int)
parser.add_argument('--fps', type=int)

args = parser.parse_args()

frames_sorted = sorted(os.listdir(args.frames_dir))
#frames_indices = [int(file.split('.')[0].split('_')[-1]) for file in frames_filenames]
#frames_sorted = [fname for (idx,fname) in sorted(zip(frames_indices, frames_filenames))]

height, width, _ = cv2.imread(os.path.join(args.frames_dir, frames_sorted[0])).shape
if args.video_file is not None:
    video_file = args.video_file
else:
    video_file = "_".join(os.path.dirname(args.frames_dir).split("/")[-2:])+".avi"

print video_file
fourcc = cv2.cv.CV_FOURCC(*'XVID')
video = cv2.VideoWriter(video_file, fourcc, args.fps, (width, height))

for (ctr, fname) in enumerate(frames_sorted):
    img = cv2.imread(os.path.join(args.frames_dir, fname))
    video.write(img)
    if not(ctr%100):
        print "{} done of {}".format(ctr, len(frames_sorted))

video.release()
