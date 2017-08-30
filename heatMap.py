from pyheatmap.heatmap import HeatMap
import xlrd
import os
import numpy as np
import cv2 as cv

outputpath = ".\\heatmaps\\"
file = ".\\Data\\NewData.xls"
imagespath = ".\\images\\"
overlaypath = ".\\overlay\\"
combinedpath = ".\\combine"

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
    Resolutions = []
    Resolution = []

    MapData = []
    MediaNames = []
    GazeEventDuration = []
    GazePointsX = []
    GazePointsY = []
    for row in range(1,nrows-1):
        gpx = table.cell(row, 7).value
        eventType = table.cell(row, 4).value
        if gpx and eventType == 'Fixation':
            Resolution.append(int(table.cell(row,1).value))
            Resolution.append(int(table.cell(row,2).value))
            Resolutions.append(Resolution)
            Resolution = []
            GazePointsX.append(int(gpx))
            GazePointsY.append(int(table.cell(row, 8).value))
            MediaNames.append(table.cell(row, 0).value)
            GazeEventDuration.append(int(table.cell(row,5).value))

    MapData.append(MediaNames)
    MapData.append(Resolutions)
    MapData.append(GazePointsX)
    MapData.append(GazePointsY)
    MapData.append(GazeEventDuration)

    return MapData

def heatmap(combinedata):
    MapData = excel_table_index(file)
    MediaNames = MapData[0]
    Resolution = MapData[1]
    GazePointsX = MapData[2]
    GazePointsY = MapData[3]
    GazeEventDuration = MapData[4]

    checkName = MediaNames[0]

    imagesize = [[0, 0], [Resolution[0][0], Resolution[0][1]]]

    index = 0
    point = []
    pointslist = []
    for name in MediaNames:
        if checkName is not name:
            print(checkName)
            pointslist.extend(imagesize)
            imagesize.remove(imagesize[1])
            imagesize.append([Resolution[index][0], Resolution[index][1]])

            if combinedata:
                for cindex in range(len(combinedata[0])):
                    if combinedata[0][cindex] == checkName:
                        pointslist.append([int(combinedata[1][cindex]),int(combinedata[2][cindex])])

            hm = HeatMap(pointslist)
            hmnames = checkName.split(".")
            hmname = hmnames[0]
            #hm.clickmap(save_as=outputpath + hmname + "_hit.png")
            hm.heatmap(save_as=outputpath + hmname + "_heat.png")
            pointslist = []
            checkName = name

        point.append(GazePointsX[index])
        point.append(GazePointsY[index])
        pointslist.append(point)
        point = []

        if index == len(MediaNames) - 1:
            print(checkName)
            pointslist.extend(imagesize)

            if combinedata:
                for cindex in range(len(combinedata[0])):
                    if combinedata[0][cindex] == checkName:
                        pointslist.append([int(combinedata[1][cindex]),int(combinedata[2][cindex])])

            hm = HeatMap(pointslist)
            hmnames = name.split(".")
            hmname = hmnames[0]
            #hm.clickmap(save_as=outputpath + hmname + "_hit.png")
            hm.heatmap(save_as=outputpath + hmname + "_heat.png")
            break

        index += 1

def overlay():
    for root, folders, files in os.walk(imagespath):
        # loop the images
        for file in files:
            image = cv.imread(root + "\\" + file)
            imagenames = file.split(".")
            imagename = imagenames[0]
            map = cv.imread(outputpath + imagename + "_heat.png")
            imagemap = cv.addWeighted(map,0.5,image,0.5,0)
            cv.imwrite(overlaypath + imagename + ".jpg",imagemap)

def combine():
    combineddata = []
    name = []
    gazeX = []
    gazeY = []
    for root, folders, files in os.walk(combinedpath):
        if files:
            for file in files:
                print(file)
                data = open_excel(root + "\\" + file)
                table = data.sheet_by_name("Data")
                nrows = table.nrows
                for row in range(1, nrows - 1):
                    if table.cell(row,10).value:
                        if table.cell(row, 43).value == 'Fixation':
                            if table.cell(row,54).value and table.cell(row,55).value:
                                gazeX.append(table.cell(row,54).value)
                                gazeY.append(table.cell(row,55).value)
                                name.append(table.cell(row, 10).value)
    combineddata.append(name)
    combineddata.append(gazeX)
    combineddata.append(gazeY)
    return combineddata

def main():
    combinedata = combine()
    # generate heat maps
    heatmap(combinedata)
    # overlay heat maps with original images
    overlay()

if __name__ == "__main__":
    main()

