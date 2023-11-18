from PySide6 import QtCore, QtWidgets, QtGui
import numpy as np
import cv2
from capture import CaptureThread

COVER_MODE = 1
SECRET_MODE = 2

class AppUI(QtWidgets.QWidget):
    capture_button_clicked = QtCore.Signal(bool)
    # secret_capture_button_clicked = QtCore.Signal(bool)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Camera")
        self.disply_width = 640
        self.display_height = 480
        self._is_capturing = False

        # Capture mode: Cover (1), Secret (2)
        self._capture_mode = COVER_MODE

        # create icons
        self.rec_icon = QtGui.QIcon("assets/icons/rec-button.png")
        self.secret_rec_icon = QtGui.QIcon("assets/icons/secret-rec-button.png")
        self.stop_icon = QtGui.QIcon("assets/icons/stop-button.png")
        
        # create the label that holds the image
        self.image_label = QtWidgets.QLabel(self)
        self.image_label.resize(self.disply_width, self.display_height)
        # create buttons
        self.capture_button = QtWidgets.QPushButton()
        self.capture_button.setIcon(self.rec_icon)
        self.capture_button.setIconSize(QtCore.QSize(65, 65))
        self.capture_button.clicked.connect(self.on_capture_button_clicked)
        
        # self.secret_capture_button = QtWidgets.QPushButton()
        # self.secret_capture_button.setIcon(self.secret_rec_icon)
        # self.secret_capture_button.setIconSize(QtCore.QSize(65, 65))
        # self.secret_capture_button.setVisible(False)
        # self.secret_capture_button.clicked.connect(self.on_secret_capture_button_clicked)

        # create a vertical box layout and add the two labels
        vbox = QtWidgets.QVBoxLayout()
        hbox = QtWidgets.QHBoxLayout()
        vbox.addWidget(self.image_label)
        vbox.addLayout(hbox)
        
        hbox.addStretch()
        hbox.addWidget(self.capture_button)
        # hbox.addWidget(self.secret_capture_button)
        hbox.addStretch()
        
        # set the vbox layout as the widgets layout
        self.setLayout(vbox)

        # events
        self._events = {
            'capture': [],
            'stop': []
        }
        self.handler_thread = None

        # create the video capture thread
        self.video_thread = CaptureThread()

        # connect its signal to the update_image slot
        self.video_thread.change_pixmap_signal.connect(self.update_image)
        # self.video_thread.capture_stopped.connect(self.on_capture_stopped)

        # start the thread
        self.video_thread.start()

    def start_handler(self, handler):
        self.handler_thread = handler
        self.video_thread.change_pixmap_signal.connect(self.handler_thread.add_frame)
        self.handler_thread.start()

    def stop_handler(self):
        if self.handler_thread != None:
            self.video_thread.change_pixmap_signal.disconnect(self.handler_thread.add_frame)
            self.handler_thread.stop()
            self.handler_thread = None

    def closeEvent(self, event):
        self.video_thread.stop()
        self.stop_handler()
        event.accept()

    def on(self, name, fn):
        self._events[name].append(fn)

    def emit(self, name, value):
        res = []
        for fn in self._events[name]:
            res.append(fn(value))
        return res


    @QtCore.Slot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.image_label.setPixmap(qt_img)
    
    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, QtCore.Qt.KeepAspectRatio)
        return QtGui.QPixmap.fromImage(p)
    
    @QtCore.Slot()
    def on_capture_button_clicked(self):
        self._is_capturing = (not self._is_capturing)
        
        # self.secret_capture_button.setVisible((not self._is_capturing))
        # self.video_thread.toggle_capture(self._is_capturing)
        
        if self._is_capturing:
            self.capture_button.setIcon(self.stop_icon)

            res = self.emit('capture', self._capture_mode == SECRET_MODE)
            if len(res) > 0 and res[0] != None:
                self.start_handler(res[0])
        else:
            self.capture_button.setIcon(self.rec_icon)

            self.stop_handler()
            self._capture_mode = SECRET_MODE if self._capture_mode == COVER_MODE else COVER_MODE

    # @QtCore.Slot()
    # def on_secret_capture_button_clicked(self):
    #     self._is_capturing = (not self._is_capturing)
        
    #     self.capture_button.setVisible((not self._is_capturing))
        
    #     # self.video_thread.toggle_secret_capture(self._is_capturing)
        
    #     if self._is_capturing:
    #         self.secret_capture_button.setIcon(self.stop_icon)
    #     else:
    #         self.secret_capture_button.setIcon(self.secret_rec_icon)
            
    # @QtCore.Slot()
    # def on_capture_stopped(self):
    #     self._is_capturing = False
        
    #     if self._capture_mode == 1: #cover mode
    #         self.capture_button.setIcon(self.rec_icon)
    #         self.capture_button.setVisible(False)
    #         self.secret_capture_button.setVisible(True)
    #     elif self._capture_mode == 2: #secret mode
    #         self.secret_capture_button.setIcon(self.secret_rec_icon)
    #         self.secret_capture_button.setVisible(False)
    #         self.capture_button.setVisible(True)
        
    #     self._capture_mode = SECRET_MODE if self._capture_mode == COVER_MODE else COVER_MODE
    