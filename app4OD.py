import tkinter as tk
import os
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from itertools import count

inputpath = ".\\data"

class ImageLabel(ttk.Label):
    """a label that displays images, and plays them if they are gifs"""
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        self.loc = 0
        self.frames = []
        self.grid(column=0, row=1, sticky=N)

        try:
            for i in count(1):
                self.frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100

        if len(self.frames) == 1:
            self.config(image=self.frames[0])
        else:
            self.next_frame()

    def unload(self):
        self.config(image=None)
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.loc += 1
            self.loc %= len(self.frames)
            self.config(image=self.frames[self.loc])
            self.after(self.delay, self.next_frame)

filelist = []

for root,folders,files in os.walk(inputpath):
    for file in files:
       filelist.append(file.title())

stage = tk.Tk()
stage.title("Subject Prediction")
mainframe = ttk.Frame(stage, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)
filenamevar = StringVar(mainframe, value='Select user')
users = ttk.Combobox(mainframe, textvariable=filenamevar)
users['value'] = tuple(filelist)
users.grid(column=0, row=0, sticky=N)
lbl = ImageLabel(mainframe)
lbl.load('giphy.gif')
ttk.Button(mainframe, text="Calculate").grid(column=0, row=2, sticky=N)

for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

stage.mainloop()