import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui
import numpy as np
import cv2
from datetime import datetime

# from embedding import EmbeddingThread

class CaptureThread(QtCore.QThread):
    change_pixmap_signal = QtCore.Signal(np.ndarray)
    capture_stopped = QtCore.Signal()
    
    def __init__(self):
        super().__init__()
        self._run_flag = True
        self._is_capturing = False
        self._is_secret = False
        self._is_stopped = False
        self._cover_capture_frames = []
        self._secret_capture_frames = []

    def run(self):
        # capture from web cam
        cap = cv2.VideoCapture(0)
        while self._run_flag:
            ret, cv_img = cap.read()
            if ret:
                self.change_pixmap_signal.emit(cv_img)

            if self._is_capturing:
                pass
                # if self._is_secret:
                #     if self._is_stopped:
                #         self._is_capturing = False
                #         self._cover_capture_frames.clear()
                #         self._secret_capture_frames.clear()
                #     else:
                #         self._secret_capture_frames.append(cv_img)
                        
                #         if len(self._secret_capture_frames) == len(self._cover_capture_frames):
                #             self.stop_capture()
                # else:
                #     if self._is_stopped:
                #         self._is_capturing = False
                #     else:
                #         self._cover_capture_frames.append(cv_img)
                        
        cap.release()

    @QtCore.Slot(bool)
    def toggle_capture(self, on):
        if on:
            self.start_capture()
        else:
            self.stop_capture()
    
    def toggle_secret_capture(self, on):
        if on:
            self.start_capture(True)
            # self.embedding_thread = EmbeddingThread()
            # self.embedding_thread._cover_capture_frames = self._cover_capture_frames
            # self.change_pixmap_signal.connect(self.embedding_thread.add_secret_frame)
            # self.capture_stopped.connect(self.embedding_thread.on_secret_capture_stopped)
            # self.embedding_thread.start()
        else:
            self.stop_capture()
            
    def start_capture(self, secret_mode = False):
        self._is_capturing = True
        self._is_secret = secret_mode
        self._is_stopped = False
    
    def stop_capture(self):
        self._is_stopped = True
        self.capture_stopped.emit()
        
    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()
