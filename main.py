import numpy as np
import math
import msvcrt
import tkinter
import cv2
import PIL.Image
import PIL.ImageTk


class App:
    def __init__(self, window, video_path=0):
        # Create window
        self.window = window
        self.window.title('Video Recognition')

        # Load video
        self.vid = VideoPlayer(video_path)

        # Show video in window
        self.canvas = tkinter.Canvas(
            window, width=self.vid.width, height=self.vid.height)
        self.canvas.pack()

        # Render, process frames and update
        self.delay = 30  # 1000
        self.update()

        self.window.mainloop()

    def update(self):
        ret, frame = self.vid.get_frame()
        if ret:
            self.process_frame(frame)
            self.render_frame(frame)

        self.window.after(self.delay, self.update)

    def process_frame(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        features = cv2.goodFeaturesToTrack(
            gray, maxCorners=3000, qualityLevel=0.01, minDistance=3)

        for c, i in enumerate(features):
            x, y = i.ravel()
            cv2.circle(frame, (x, y), radius=3, color=255, thickness=1)

    def render_frame(self, frame):
        self.img = PIL.ImageTk.PhotoImage(
            image=PIL.Image.fromarray(frame))
        self.canvas.create_image(0, 0, image=self.img, anchor=tkinter.NW)


class VideoPlayer:
    def __init__(self, path=0):
        self.vid = cv2.VideoCapture(path)
        if not self.vid.isOpened():
            raise ValueError('Unable to open video path', path)

        self.width = math.floor(self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)//1.5)
        self.height = math.floor(self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)//1.5)

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                return (ret, cv2.cvtColor(cv2.resize(frame, (self.width, self.height)), cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)


App(tkinter.Tk(), 'video.mp4')
