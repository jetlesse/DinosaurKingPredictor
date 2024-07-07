import cv2 as cv
import win32gui
import numpy as np
from PIL import ImageGrab

import window_capture
import time as Time


class Capture:
    """
    single interface for dealing with different types of input
    video, window, portion of screen
    """

    def next_frame(self):
        """
        get the next frame to analyze
        :return: 2-D list of BGR pixels accessed by list[y][x]
        """
        pass


class VideoCapture(Capture):
    def __init__(self, filename, fps=60):
        self.cap = cv.VideoCapture(filename)
        if not self.cap.isOpened():
            return False
        self.fps = fps

    def next_frame(self):
        return self.cap.read()[1]

    def time_to_frame(self, time):
        """
        Convert a timestamp in the form of HH:mm:ss into a frame number to find where in a video that timestamp is.
        :param time: timestamp in the form of HH:mm:ss
        :return: frame number, total number of seconds * video fps (set in general config file)
        """
        if type(time) == int:
            seconds = time
        else:
            t = Time.strptime(time, "%H:%M:%S")
            seconds = t.tm_sec + 60 * t.tm_min + 3600 * t.tm_hour
        return seconds * self.fps

    def jump_to(self, time):
        frames = self.time_to_frame(time)
        self.cap.set(cv.CAP_PROP_POS_FRAMES, frames)
        return


class WindowCapture(Capture):
    def __init__(self, window_name):
        self.game_hwnd = 0
        # gets list of all available windows
        self.windows_list = []
        win32gui.EnumWindows(self.enum_win, None)

        # search for handle of window containing expected name
        for (hwnd, win_text) in self.windows_list:
            if window_name in win_text:
                self.game_hwnd = hwnd

        # create new WindowCapture using the window handle
        self.wc = window_capture.WindowCapture(self.game_hwnd)

    def next_frame(self):
        return self.wc.get_screenshot()

    def enum_win(self, hwnd, result):
        win_text = win32gui.GetWindowText(hwnd)
        self.windows_list.append((hwnd, win_text))
