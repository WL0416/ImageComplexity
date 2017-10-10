from pyheatmap.heatmap import HeatMap
import numpy as np
import cv2 as cv
import math, string, os, xlrd


# This is for generating the heat-map of salience map and complexity map

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

# overlap two images together
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

# this function is used to combine some data file together.
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


# calculate the range to data, if the image is grayscale, the range is 0 -> 255
def range_bytes():
    return range(256)


# Entropy calculation function, based on Shannon Information Theory
def H(data, iterator=range_bytes):
    if not data:
        return 0
    entropy = 0
    for x in iterator():
        p_x = float(data.count(x))/len(data)
        if p_x > 0:
            current = - p_x*math.log(p_x, 2)
            print(current)
            entropy += current
    return entropy

# image complexity heat-map
def calculateComplexity(method):
    pixelcount = 0
    if method == "Entropy": # Entropy
        image = cv.imread(".\\images\\30.jpg")
        container = []
        line = []
        # loop the image matrix
        for row in image:
            if len(line) != 0:
                container.append(line)
                line =[]
            for pixel in row:
                for color in pixel:
                    line.append(color)
                    pixelcount += 1
                    break # grey scale image, R,G,B have the same value
        for eachline in container:
            print(eachline)
        print(pixelcount)


def main():
    #combinedata = combine()
    # generate heat maps
    #heatmap(combinedata)
    # overlay heat maps with original images
    #overlay()
    calculateComplexity("Entropy")
    data = [216,123,216,216,216,216]
    print(H(data))

if __name__ == "__main__":
    main()

