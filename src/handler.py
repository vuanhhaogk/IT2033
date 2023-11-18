import cv2
import math
import sys
import random
import numpy as np
from time import sleep
from PySide6 import QtCore
from keras.models import load_model
from constants import BASE_SIZE
from utils import load_video_to_frames, save_frames_to_video
from hide import run_hide

class SaveHandlerThread(QtCore.QThread):
  def __init__(self, filename):
    super().__init__()
    self._run_flag = True    
    self._queue = []

    self._filename = filename
    self._fourcc = cv2.VideoWriter_fourcc(*'XVID')
    self._out = None

  def process(self, frame):
    return frame
    
  def run(self):
    while self._run_flag:
      while len(self._queue) > 0:
        if self._out == None:
          self._out = cv2.VideoWriter(self._filename, self._fourcc, 20.0, (BASE_SIZE, BASE_SIZE))

        inp_frame = self._queue.pop(0)
        out_frame = self.process(inp_frame)
        self._out.write(out_frame)
      sleep(1)

    self._out.release()
  
  @QtCore.Slot(np.ndarray)
  def add_frame(self, frame):
    frame = cv2.resize(frame, (BASE_SIZE, BASE_SIZE), interpolation=cv2.INTER_AREA)
    self._queue.append(frame)

  def stop(self):
    """Sets run flag to False and waits for thread to finish"""
    self._run_flag = False
    self.wait()

class HideHandlerThread(SaveHandlerThread):
  def __init__(self, filename):
    super().__init__(filename)

  def process(self, frame):
    w = frame.shape[1]
    h = frame.shape[0]
    r, g, b = cv2.split(frame)
    br = -100
    for i in range(h):
      for j in range(w):
        r[i][j] = max(min(r[i][j] + br, 255), 0)
        g[i][j] = max(min(g[i][j] + br, 255), 0)
        b[i][j] = max(min(b[i][j] + br, 255), 0)

    return cv2.merge([b, g, r])
  
  def run(self):
    while self._run_flag:
      sleep(1)

    cover_all = load_video_to_frames(self._filename)
    container_frames = run_hide(cover_all, self._queue)
    save_frames_to_video(container_frames, self._filename)

