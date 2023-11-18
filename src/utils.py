import random
import cv2
import math
import sys
import numpy as np
from constants import BASE_SIZE

def shuffle(message, key):
  random.seed(key)
  l = list(range(len(message)))
  random.shuffle(l)
  return [message[x] for x in l]

def unshuffle(shuffled_message, key):
  random.seed(key)
  l = list(range(len(shuffled_message)))
  random.shuffle(l)
  out = [None] * len(shuffled_message)
  for i, x in enumerate(l):
      out[x] = shuffled_message[i]
  return out

def load_video_to_frames(video_path):
  video = cv2.VideoCapture(video_path)
  frames = []
  while True:
    (success, frame) = video.read()

    if not success:
      break

    frames.append(frame)
  return frames

def save_frames_to_video(frames, video_path, codec = 'HFYU'):
  video = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*(codec)), 30, (BASE_SIZE,BASE_SIZE))
  for i in range(len(frames)):
    video.write(frames[i])
  video.release()

def normalize_batch(imgs):
  return (imgs -  np.array([0.485, 0.456, 0.406])) /np.array([0.229, 0.224, 0.225])

def denormalize_batch(imgs,should_clip=True):
  imgs= (imgs * np.array([0.229, 0.224, 0.225])) + np.array([0.485, 0.456, 0.406])
  if should_clip:
    imgs= np.clip(imgs,0,1)
  return imgs

def update_progress(current_frame, total_frames):
  progress=math.ceil((current_frame/total_frames)*100)
  sys.stdout.write('\rProgress: [{0}] {1}%'.format('>'*math.ceil(progress/10), progress))
