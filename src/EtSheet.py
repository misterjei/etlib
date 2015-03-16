from xlwt import *
from xlrd import *

def write_multiple(sheet, rowIndex, colIndex, dataList, style):
    for cellData in dataList:
        sheet.write(rowIndex, colIndex, cellData, style)
        colIndex = colIndex + 1
