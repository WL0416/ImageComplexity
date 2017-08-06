import tkinter as tk
import os
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image
from PIL import ImageTk
from itertools import count
import xlrd
import xlwt
import threading

inputpath = "./data"
output = "./new/NewData.xls"
columnsFilter = ['MediaName',
                 'LocalTimeStamp',
                 'GazeEventType',
                 'GazeEventDuration',
                 'GazePointIndex',
                 'GazePointX (MCSpx)',
                 'GazePointY (MCSpx)']
subjects = {'architecture':4,
            'engineering':0,
            'fashion':1,
            'finance':3,
            'science':2}

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
                if result == '011.jpg'\
                        or result=='012.jpg'\
                        or result=='013.jpg'\
                        or result=='014.jpg':
                    self.config(image=self.frames[subjects['architecture']])
                elif result == '015.jpg'\
                        or result=='016.jpg'\
                        or result=='017.jpg'\
                        or result=='018.jpg':
                    self.config(image=self.frames[subjects['engineering']])
                elif result == '019.jpg'\
                        or result=='020.jpg'\
                        or result=='021.jpg'\
                        or result=='022.jpg':
                    self.config(image=self.frames[subjects['fashion']])
                elif result == '023.jpg'\
                        or result=='024.jpg'\
                        or result=='025.jpg'\
                        or result=='026.jpg':
                    self.config(image=self.frames[subjects['finance']])
                else:
                    self.config(image=self.frames[subjects['science']])

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
    table = data.sheet_by_name("Shivy_Wei_Data_Export")
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
        file = "./data/" + str(users['value'][users.current()])
        excel_filter(file, columnsFilter)
    except IndexError:
        messagebox.showinfo("Error", "Invalid file!")
        start = False

    if start:
        data = open_excel(output)
        table = data.sheet_by_name("NewData")
        nrows = table.nrows
        # dictionary which can store the pupil dilation values of all images
        interest = {}
        dilationsum = 0
        count = 0
        MediaName = []
        testdata = 0
        for row in range(1, nrows):
            if table.cell(row, 0).value and table.cell(row, 2).value == "Fixation":
                # run only one time
                if not MediaName:
                    MediaName.append(table.cell(row, 0).value)

                if MediaName and table.cell(row, 0).value != MediaName[0]:
                    # this variable means one image has been through
                    testdata += 1
                    if testdata>11:
                        average = dilationsum / count
                        interest[MediaName[0]] = average
                    if testdata<=30:
                        MediaName.insert(0, table.cell(row, 0).value)
                    if testdata<12:
                        del MediaName[1]
                    count = 0
                    dilationsum = 0

                if testdata > 10 and testdata <= 30:
                    count += 1
                    # sum the pupil dilation values for each image
                    dilationsum += int(table.cell(row,3).value)
            '''
            if row == nrows - 1:
                average = dilationsum / count
                interest[MediaName[0]] = average
                count = 0
                dilationsum = 0
                testdata += 1
            '''
            if testdata == 31:
                for key in interest.iteritems():
                    print key
                break

        # find out which image's pupil dilation value is the greatest
        max_item = max(interest.items(), key=lambda x: x[1])
        #sort_item = sorted(interest.items(), key=lambda  x: x[1])
        global result
        result = max_item[0]
        print result

    global play
    play = False


# calculate the prediction result, two threads will be created to handle two processes
def calculation():
    global play
    play = True
    lbl.unload()
    t2 = threading.Thread(target=file_process)
    t2.start()

    t1 = threading.Thread(target=lbl.load, args=('slider.gif', play))
    t1.start()

# locating the window in the center of screen
def center(win):
    win.update_idletasks()
    width = win.winfo_width()
    height = win.winfo_height()
    x = (win.winfo_screenwidth() // 2) - (width // 2)
    y = (win.winfo_screenheight() // 2) - (height // 2)
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))

# main stage of the app
stage = tk.Tk()
# remove the toolbar on the top of window
#stage.wm_attributes('-type','splash')
#stage.wm_attributes('-fullscreen','true')
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
#users.bind("<<ComboboxSelected>>", getUsers)
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

center(stage)

stage.mainloop()