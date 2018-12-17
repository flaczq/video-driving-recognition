import tkinter


class VideoPlayer(object):
    def __init__(self, path):
        self.path = path
        self.window = tkinter.Tk()

    def play(self):
        print(self.path)
        self.window.mainloop()


vp = VideoPlayer('video.mp4')
vp.play()
