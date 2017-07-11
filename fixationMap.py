import xlrd
import numpy as np
import cv2 as cv

outputpath = ".\\fixationMap"
file = ".\\Data\\NewData.xls"

def open_excel(file):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception as e:
        print(str(e))

def excel_table_index(file):
    data = open_excel(file)
    table = data.sheet_by_name("NewData")
    nrows = table.nrows
    Resolution = [1920,1080]

    MapData = []
    MediaNames = []
    GazeEventDuration = []
    GazePointsX = []
    GazePointsY = []
    for row in range(1,nrows-1):
        gpx = table.cell(row, 5).value
        eventType = table.cell(row, 2).value
        if gpx and eventType == 'Fixation':
            GazePointsX.append(int(gpx))
            GazePointsY.append(int(table.cell(row, 6).value))
            MediaNames.append(table.cell(row, 0).value)
            GazeEventDuration.append(int(table.cell(row,3).value))

    MapData.append(MediaNames)
    MapData.append(Resolution)
    MapData.append(GazePointsX)
    MapData.append(GazePointsY)
    MapData.append(GazeEventDuration)

    return MapData

def canvas_draw(file):
    MapData = excel_table_index(file)
    MediaNames = MapData[0]
    Resolution = MapData[1]
    GazePointsX = MapData[2]
    GazePointsY = MapData[3]
    GazeEventDuration = MapData[4]

    white = (255, 255, 255)
    black = (0, 0, 0)

    canvas = np.zeros((Resolution[1],Resolution[0]))

    checkName = MediaNames[0]
    checkDuration = GazeEventDuration[0]

    index = 0
    point = []
    pointslist = []
    for name in MediaNames:
        if checkName is not name:
            draw_convex_hull(pointslist, canvas)
            cv.imwrite(outputpath+"\\"+checkName,canvas)
            print(checkName)
            pointslist = []
            checkName = name
            checkDuration = GazeEventDuration[index]
            # initial the background into black
            cv.rectangle(canvas, (0, 0), (Resolution[0]-1,Resolution[1]-1), black, -1)

        cv.rectangle(canvas, (GazePointsX[index], GazePointsY[index]),
                     (GazePointsX[index], GazePointsY[index]), white)

        if checkDuration != GazeEventDuration[index]:
            draw_convex_hull(pointslist, canvas)
            pointslist = []

        point.append(GazePointsX[index])
        point.append(GazePointsY[index])
        pointslist.append(point)
        point = []

        if index == len(MediaNames)-1:
            draw_convex_hull(pointslist, canvas)
            cv.imwrite(outputpath + "\\" + checkName, canvas)
            print(checkName)
            break

        checkDuration = GazeEventDuration[index]
        index += 1

def draw_convex_hull(pointslist,canvas):
    inputpoints = np.array(pointslist)
    outpoints = cv.convexHull(inputpoints)
    for i in range(len(outpoints)):
        if i != len(outpoints) - 1:
            cv.line(canvas, (outpoints[i][0][0], outpoints[i][0][1]),
                    (outpoints[i + 1][0][0], outpoints[i + 1][0][1]), 255, 1)
        else:
            cv.line(canvas, (outpoints[i][0][0], outpoints[i][0][1]),
                    (outpoints[0][0][0], outpoints[0][0][1]), 255, 1)

canvas_draw(file)