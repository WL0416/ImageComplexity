import tkinter as tk
import os
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from itertools import count
import xlrd
import xlwt
import threading
import time

inputpath = ".\\data"
output = ".\\new\\NewData.xls"
columnsFilter = ['MediaName', 'LocalTimeStamp', 'GazeEventType', 'GazeEventDuration', 'GazePointIndex',
                 'GazePointX (MCSpx)', 'GazePointY (MCSpx)']


class ImageLabel(ttk.Label):
    """a label that displays images, and plays them if they are GIFs"""

    def load(self, im, play):
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

        if len(self.frames) == 1 or play == False:
            self.config(image=self.frames[0])
        else:
            self.next_frame()

    def unload(self):
        self.config(image=None)
        self.frames = None

    def next_frame(self):
        global play
        global result
        if self.frames:
            self.loc += 1
            self.loc %= len(self.frames)
            self.config(image=self.frames[self.loc])
            if play:
                self.after(self.delay, self.next_frame)
            else:
                if result == '049.jpg':
                    self.config(image=self.frames[len(self.frames) - 1])


# a method can get the user data which we want to calculate
def getUsers():
    global play
    play = False
    global result
    result = ""
    filelist = []
    for root, folders, files in os.walk(inputpath):
        for file in files:
            filelist.append(file.title())
    users['value'] = tuple(filelist)


def open_excel(file):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception as e:
        print(str(e))


def excel_filter(file, columnsFilter):
    data = open_excel(file)
    table = data.sheet_by_name("Data")
    book = xlwt.Workbook()
    datasheet = book.add_sheet("NewData", cell_overwrite_ok=True)

    indexR = 0
    indexC = 0
    for c in range(table.ncols):
        temp = []
        for column in columnsFilter:
            if column == table.cell(0, c).value:
                for r in range(table.nrows):
                    temp.append(table.cell(r, c).value)
                if temp:
                    for value in temp:
                        datasheet.write(indexR, indexC, value)
                        indexR += 1
                    indexR = 0
                    indexC += 1
                break
    book.save(output)


def file_process():
    start = True
    try:
        file = ".\\data\\" + str(users['value'][users.current()])
        excel_filter(file, columnsFilter)
    except IndexError:
        messagebox.showinfo("Error", "Invalid file!")
        start = False

    if start:
        data = open_excel(output)
        table = data.sheet_by_name("NewData")
        nrows = table.nrows
        interest = {}
        count = 0
        MediaName = []
        for row in range(1, nrows):
            if table.cell(row, 0).value and table.cell(row, 2).value == "Fixation":
                # run only one time
                if not MediaName:
                    MediaName.append(table.cell(row, 0).value)

                if MediaName and table.cell(row, 0).value != MediaName[0]:
                    interest[MediaName[0]] = count
                    MediaName.insert(0, table.cell(row, 0).value)
                    count = 0
                count += 1
            if row == nrows - 1:
                interest[MediaName[0]] = count
                count = 0

        # find out which image has most fixations
        max_item = max(interest.items(), key=lambda x: x[1])
        global result
        result = max_item[0]

    global play
    play = False


# calculate the prediction result, two threads will be created to handle two processes
def calculation():
    global play
    play = True
    lbl.unload()
    t2 = threading.Thread(target=file_process)
    t2.start()

    t1 = threading.Thread(target=lbl.load, args=('test.gif', play))
    t1.start()


# main stage of the app
stage = tk.Tk()
stage.title("Subject Prediction")

# the frame that easily to manage on the stage
mainframe = ttk.Frame(stage)
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

# option draw-down box
filename = StringVar(mainframe, value='Select a user')
users = ttk.Combobox(mainframe, textvariable=filename)
getUsers()
users.current(0)
users.bind("<<ComboboxSelected>>", getUsers)
users.grid(column=0, row=0, sticky=W)

# refresh button, scan users and initialise the app
ttk.Button(mainframe, text="Scan users", command=getUsers).grid(column=0, row=0, sticky=E)

play = False
result = ""
lbl = ImageLabel(mainframe)
lbl.load('0.jpg', play)

# calculation button
ttk.Button(mainframe, text="Calculate", command=calculation).grid(column=0, row=2, sticky=N)

# overall layout
for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

stage.mainloop()
