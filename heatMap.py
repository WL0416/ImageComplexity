import matplotlib.pyplot as plt
import matplotlib.tri as tri
import numpy as np
import xlrd
import math

file = ".\\Data\\NewData.xls"
MediaName = 0
GazeEventType = 2
GazeEventDuration = 3
GazePointIndex = 4
GazePointX = 5
GazePointY = 6
x = []
y = []
heat_value = []

def open_excel(file):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception as e:
        print(str(e))

def data_analysis(file):
    data = open_excel(file)
    table = data.sheet_by_name("NewData")
    rows = table.nrows
    gazeX = []
    gazeY = []
    tempX = []
    tempY = []
    tempH = []
    mark = 0

    for row in range(1, rows-1):
        image = table.cell(row, MediaName).value
        type = table.cell(row, GazeEventType).value
        gpindex = table.cell(row, GazePointIndex).value
        gpx = table.cell(row, GazePointX).value
        gpy = table.cell(row, GazePointY).value
        duration = table.cell(row-1, GazeEventDuration).value

        if image:
            if not gpindex:
                if mark == 0:
                    mark = 1
                    continue
                else:
                    mark = 0

            if mark == 0:
                x.append(tempX)
                y.append(tempY)
                heat_value.append(tempH)
                tempX = []
                tempY = []
                tempH = []

            if type == "Fixation":
                if gpx:
                    if duration != table.cell(row, GazeEventDuration).value:
                        try:
                            if len(gazeX) != 0:
                                tempX.append(int(sum(gazeX) / len(gazeX)))
                                tempY.append(int(sum(gazeY) / len(gazeY)))
                                tempH.append(duration)
                                gazeX = []
                                gazeY = []
                        except Exception as e:
                            print(str(e))
                    else:
                        gazeX.append(gpx)
                        gazeY.append(gpy)
            else:
                try:
                    if len(gazeX) != 0:
                        tempX.append(int(sum(gazeX)/len(gazeX)))
                        tempY.append(int(sum(gazeY)/len(gazeY)))
                        tempH.append(duration)
                        gazeX = []
                        gazeY = []
                except Exception as e:
                    print(str(e))

    for im in range(len(x)):
        print('Pic' + str(im+1) + str(x[im]))

def draw_heat_map(x, y, heat_value):
    levels = []
    for l in range(11):
        levels.append(l / 10)
    print(levels)

    for i in range(len(x)):
        imageH = []
        imageX = x[i]
        print(imageX)
        imageY = y[i]
        print(imageY)
        for h in range(len(heat_value[i])):
            if heat_value[i][h] == max(heat_value[i]):
                imageH.append(1)
            else:
                imageH.append(heat_value[i][h]/max(heat_value[i]))
        print(imageH)
        plt.figure()
        ax = plt.gca()
        ax.set_aspect('equal')
        CS = ax.tricontourf(imageX, imageY, imageH, levels, cmap=plt.get_cmap('jet'))
        cbar = plt.colorbar(CS, ticks=np.sort(np.array(levels)), ax=ax, orientation='horizontal', shrink=.75, pad=.09,
                            aspect=40, fraction=0.05)
        cbar.ax.set_xticklabels(list(map(str, np.sort(np.array(levels)))))  # horizontal colorbar
        cbar.ax.tick_params(labelsize=8)
        plt.title('Heat Map')
        plt.savefig('test'+str(i)+'.png', dpi=600)

data_analysis(file)
#draw_heat_map(x, y, heat_value)

