import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(os.path.join(parent, 'src'))

from utils import load_video_to_frames, save_frames_to_video
from reveal import run_reveal

frames = load_video_to_frames('outputs/container_video.avi')

for codec in ['HFYU', 'RGBA', 'XVID', 'PIM1', 'MJPG', 'MP42', 'DIV3', 'DIVX', 'U263', 'I263', 'FLV1']:
  filename = 'outputs/codec/container_%s.avi' % (codec.lower())
  save_frames_to_video(frames, filename, codec)

  container_frames = load_video_to_frames(filename)
  secret_frames = run_reveal(container_frames)

  save_frames_to_video(secret_frames, 'outputs/codec/secret_%s.avi' % (codec.lower()))