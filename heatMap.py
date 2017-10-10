from pyheatmap.heatmap import HeatMap
import numpy as np
import cv2 as cv
import math, string, os, xlrd
import matplotlib.pyplot as plt


# This is for generating the heat-map of salience map and complexity map

complexitypath = ".\\imageComp\\"
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
def overlay(outputpath, per1, per2):
    for root, folders, files in os.walk(imagespath):
        # loop the images
        for file in files:
            image = cv.imread(root + "\\" + file)
            imagenames = file.split(".")
            imagename = imagenames[0]
            map = cv.imread(outputpath + imagename + "_heat.png")

            height, width, depth = image.shape
            print(height, width, depth)

            height, width, depth = map.shape
            print(height, width, depth)

            imagemap = cv.addWeighted(map,per1,image,per2,0)
            cv.imwrite(overlaypath + imagename + "_complex.jpg", imagemap)

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
#def range_bytes():
#    return range(256)


# Entropy calculation function, based on Shannon Information Theory
def H(data):
    if not data:
        return 0
    entropy = 0
    Hlist = []
    for element in data:
        p_x = float(data.count(element))/len(data)
        if p_x > 0:
            current = - p_x*math.log(p_x, 2)
            Hlist.append(current)
            # this variable entropy represents whole block's entropy value
            entropy += current
    return Hlist

# image complexity heat-map
def calculateComplexity(method, window_length, window_wide):
    # loop the target folder to get the original images' information
    for root, folders, files in os.walk(imagespath):
        # loop the images
        for file in files:
            print(file)
            if method == "Entropy":  # Entropy
                image = cv.imread(root+"\\"+file)
                # get the images row and column numbers
                row_num = len(image)
                column_num = len(image[0])
                # y (wide)
                print(row_num)
                # x (length)
                print(column_num)

                # list to store the data used to calculate the entropy value
                s = (row_num, column_num)
                final_matrix = np.zeros(s)
                counter_matrix = np.zeros(s, dtype=int)

                # print(final_matrix)
                # print (counter_matrix)

                pixel_counter = 0
                for row in range(row_num):
                    for column in range(column_num):
                        color = image[row][column][0]
                        data = [color]
                        for window_column in range(window_length):
                            length = column + window_column
                            # print('x: '+ str(length))
                            if length > column_num - 1:
                                break
                            for window_row in range(window_wide):
                                wide = row + window_row
                                # print('y: '+ str(wide))
                                if wide > row_num - 1:
                                    break
                                # grep data except the top left corner one
                                if window_column != 0 or (window_column == 0 and window_row != 0):
                                    color = image[wide][length][0]
                                    data.append(color)
                        Hlist = H(data)
                        Hindex = 0
                        final_matrix[row][column] += Hlist[Hindex]
                        counter_matrix[row][column] += 1
                        Hindex += 1
                        # here get the entropy values in the window
                        for window_column in range(window_length):
                            length = column + window_column
                            if length > column_num - 1:
                                break
                            for window_row in range(window_wide):
                                wide = row + window_row
                                if wide > row_num - 1:
                                    break
                                if window_column != 0 or (window_column == 0 and window_row != 0):
                                    final_matrix[wide][length] += Hlist[Hindex]
                                    counter_matrix[wide][length] += 1
                                    Hindex += 1
                        pixel_counter += 1
                        print(pixel_counter)

                for row in range(row_num):
                    for column in range(column_num):
                        final_matrix[row][column] = (final_matrix[row][column] / counter_matrix[row][column]) * 255
                        #if final_matrix[row][column] != 0:
                        #    print(final_matrix[row][column])
                print(final_matrix)
                print(counter_matrix)

                file_names = file.split(".")
                filename = file_names[0]
                # output the grayscale image first
                cv.imwrite(complexitypath + filename + "_heat.png", final_matrix)
                out_image = cv.imread(complexitypath + filename + "_heat.png")

                # read the grayscale image and make it to be color map
                color_final_matrix = cv.applyColorMap(out_image, cv.COLORMAP_JET)
                cv.imwrite(complexitypath + filename + "_heat.png", color_final_matrix)


def main():
    #combinedata = combine()
    # generate heat maps of fixation map
    #heatmap(combinedata)
    calculateComplexity("Entropy",10,10)
    # overlay heat maps with original images
    overlay(complexitypath, 0.3, 0.7)

if __name__ == "__main__":
    main()

