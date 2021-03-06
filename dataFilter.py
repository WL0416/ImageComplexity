import xlrd
import xlwt

file = ".\\Data\\IJCAI_1.xlsx"
output = ".\\Data\\NewData.xls"
columnsFilter = ['MediaName','LocalTimeStamp','GazeEventType','GazeEventDuration','GazePointIndex','GazePointX (MCSpx)','GazePointY (MCSpx)','MediaWidth','MediaHeight']

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
            if column == table.cell(0,c).value:
                for r in range(table.nrows):
                    temp.append(table.cell(r,c).value)
                if temp:
                    for value in temp:
                        datasheet.write(indexR, indexC, value)
                        indexR += 1
                    indexR = 0
                    indexC += 1
                break
    book.save(output)

excel_filter(file, columnsFilter)