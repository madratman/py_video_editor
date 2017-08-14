import cv2
from argparse import ArgumentParser
import os
import numpy as np
from joblib import Parallel, delayed

print_every_nth = 200

parser = ArgumentParser()
parser.add_argument('--frames_dir', type=str)
parser.add_argument('--write_every_nth_frame', type=int)
# parser.add_argument('--width', type=int, default=1280)
# parser.add_argument('--height', type=int, default=720)
args = parser.parse_args()

def extract_frames(video_file):
    video_file_name, extension = os.path.splitext(os.path.basename(video_file))
    print video_file_name
    capture = cv2.VideoCapture(video_file)
    n_frames = int(capture.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))
    if not os.path.exists(args.frames_dir):
        os.makedirs(args.frames_dir)
    ctr = 0
    while(capture.isOpened()):
        ret, frame = capture.read()
        if not (ctr%print_every_nth):
            print "{} of {} done".format(ctr, n_frames)
        if ret==True:
            ctr+=1
            if (ctr%args.write_every_nth_frame==0):
                # height_orig, width_orig, channels = frame.shape
                # frame_resized = cv2.resize(frame, (args.width, args.height))
                cv2.imwrite(os.path.join(args.frames_dir, video_file_name+ "_" + str(ctr).zfill(5)+".png"), frame) 
        else:
            break

vid_directory = "/home/madratman/Videos/every_neighbourhood/DCIM/videos/"
list_of_videos = sorted(os.listdir(vid_directory))
list_of_videos = [os.path.join(vid_directory, vid_file) for vid_file in list_of_videos]
Parallel(n_jobs=8, verbose=100)(delayed(extract_frames)(video_file) for video_file in list_of_videos)
