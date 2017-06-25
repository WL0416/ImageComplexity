import xlrd
import numpy as np
import cv2 as cv

outputpath = ".\\saliencyMap"

def open_excel(file = ".\\Data\\Shivy_Wei_Eye_Tracking_Data_12APR17.xlsx"):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception as e:
        print(str(e))

def excel_table_index(file= ".\\Data\\Shivy_Wei_Eye_Tracking_Data_12APR17.xlsx",
                        colnameindex=0,by_index=0):
    data = open_excel(file)
    table = data.sheet_by_name("Data")
    nrows = table.nrows
    ncols = table.ncols
    list = []
    list.append(nrows)
    list.append(ncols)
    RecordingResolution = table.cell(1,8).value

    Resolution = []
    if RecordingResolution == "1280 x 1024":
        Resolution.append(1920)
        Resolution.append(1080)
    else:
        Resolution.append(100)
        Resolution.append(100)

    MapData = []
    MediaNames = []
    GazePointsX = []
    GazePointsY = []
    for row in range(1,nrows-1):
        gpx = table.cell(row, 54).value
        if gpx:
            GazePointsX.append(int(gpx))
            GazePointsY.append(int(table.cell(row, 55).value))
            MediaName = table.cell(row, 10).value
            MediaNames.append(MediaName)

    MapData.append(MediaNames)
    MapData.append(Resolution)
    MapData.append(GazePointsX)
    MapData.append(GazePointsY)

    return MapData

def canvas_draw():
    MapData = excel_table_index()
    MediaNames = MapData[0]
    Resolution = MapData[1]
    GazePointsX = MapData[2]
    GazePointsY = MapData[3]

    white = (255,255,255)
    black = (0,0,0)

    canvas = np.zeros((Resolution[1],Resolution[0]))

    checkName = MediaNames[0]

    index = 0
    point = []
    pointslist = []
    print(checkName)
    for name in MediaNames:
        if checkName is not name:
            draw_convex_hull(pointslist, canvas)
            cv.imwrite(outputpath+"\\"+checkName,canvas)
            pointslist = []
            checkName = name
            print(checkName)
            # initial the background into black
            cv.rectangle(canvas, (0, 0), (Resolution[0]-1,Resolution[1]-1), black, -1)

        cv.rectangle(canvas, (GazePointsX[index], GazePointsY[index]),
                     (GazePointsX[index], GazePointsY[index]), white)
        point.append(GazePointsX[index])
        point.append(GazePointsY[index])
        pointslist.append(point)
        point = []

        if index == len(MediaNames)-1:
            draw_convex_hull(pointslist, canvas)
            cv.imwrite(outputpath + "\\" + checkName, canvas)
        index += 1

def draw_convex_hull(pointslist,canvas):
    inputpoints = np.array(pointslist)
    outpoints = cv.convexHull(inputpoints)
    for i in range(len(outpoints)):
        if (i != len(outpoints) - 1):
            cv.line(canvas, (outpoints[i][0][0], outpoints[i][0][1]),
                    (outpoints[i + 1][0][0], outpoints[i + 1][0][1]), 255, 1)
        else:
            cv.line(canvas, (outpoints[i][0][0], outpoints[i][0][1]),
                    (outpoints[0][0][0], outpoints[0][0][1]), 255, 1)

canvas_draw()