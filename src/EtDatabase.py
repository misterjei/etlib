import xlrd
import sqlite3
import sys, os
import csv, codecs

def loadCsv(filename, dialect = None):
    # Determine if the file exists. If not, raise an exception.
    if not os.path.isfile(filename):
        raise Exception("Error: " + filename + " not found.")
    
    # Determine the csv file dialect (if not provided)
    csvFile = open(filename, 'rU')
    
    # Read file into list of lists
    if dialect != None:
        reader = csv.reader(csvFile, dialect)
    else:
        reader = csv.reader(csvFile)

    rowData = list()
    for row in reader:
        rowData.append(row)
    
    csvFile.close()
    return rowData

def openExcel(filename):
    # Determine if the file exists. If not, raise an exception.
    if not os.path.isfile(filename):
        raise Exception("Error: " + filename + " not found.")
    
    # Load the workbook.
    try: workbook = xlrd.open_workbook(filename)
    except: pass

    return workbook

def getExcelSheetAsCsv(workbook, sheetName = None):
    if sheetName != None:
        sheet = workbook.sheet_by_name(sheetName)
    else:
        sheet = workbook.sheet_by_index(0)

    # Get the row data
    rowData = list()
    for row in range(sheet.nrows):
        values = list()
        for col in range(sheet.ncols):
            values.append(sheet.cell(row, col).value)
        rowData.append(values)

    return rowData

def loadExcelSheetAsCsv(filename, sheetName = None):
    return getExcelSheetAsCsv(openExcel(filename), sheetName)

def saveCsv(filename, rowData, insertKey = False):
    # Open file for writing
    csvFile = codecs.open(filename, 'w+', encoding='utf-8')
    writer = csv.writer(csvFile, quotechar='"', delimiter=',')

    # Write the data
    if insertKey:
        for key, row in rowData.iteritems():
            print "Key: " + key + " Value: " + row
            writer.writerow([ key ] + row)
    else:
        for row in rowData:
            writer.writerow(row)

    # Close the file
    csvFile.close()

def getSheetDataColumn(rowData, number):
    columnData = list()
    
    for row in rowData:
        columnData.append(row[number])

    return columnData

def getNumColumns(rowData):
    columns = 0
    
    for row in rowData:
        if len(row) > columns:
            columns = len(row)
    
    return columns
#===============================================================================
# def dbFromCsv(filename, schema = None, table = "data", hasHeaderRow = True, hasPrimaryKey = False):
#     # Load the row data from the CSV file
#     rowData = loadCsv(filename)
#     headerRow = rowData.pop(0) if hasHeaderRow else None
#     dataSample = rowData.pop(0)
#     rowData.insert(0, dataSample)
# 
#     # If there's no header row, create one (just in case we need it.)
#     if headerRow == None:
#         headerRow = list()
#         for index in range(0, len(dataSample)):
#             headerRow.append("Column" + index)
# 
#     # open database
#     try:
#         database = sqlite3.connect(":memory:")
#     except:
#         raise Exception("Error: could not connect to RAM database")
#         return None
# 
#     with database:
#         # Create the database for storage
#         if schema == None:
#             headerSchema = "CREATE TABLE header ( " + "__key__ VARCHAR(255), " if hasPrimaryKey else ""
#             dataSchema = "CREATE TABLE " + table + " ( " + "__key__ INTEGER PRIMARY KEY, " if hasPrimaryKey else ""
#             for header in headerRow:
#                 headerSchema += header + " VARCHAR(255), "
#                 dataSchema += header + " DOUBLE, " if isinstance(dataSample.pop(0), float) else  " TEXT, "
#             schema = headerSchema[:-2] + " ); " + dataSchema[:-2] + " );"
# 
#         cursor = database.cursor()
#         cursor.executescript(schema)
#         
#         # Process headers
#         query = "INSERT INTO header VALUES ("
#         for i in range(0, len(headerRow)):
#             query += "?, "
#         query = query[:-2] + ")" # drop trailing comma & space
#         cursor.execute(query, headerRow)
# 
#         # Add data to database
#         numrows = 0
#         for row in rowData:
#             # row contains more data than table can hold
#             if len(row) > len(headerRow):
#                 print "Error: more columns in critique data than schema can hold, even after massaging data. Bad data? Update schema?"
#                 sys.exit()
# 
#             # row contains less data than table can hold - fill as empty strings, which become nulls in the db
#             if len(row) < len(headerRow):
#                 for i in range(0, len(headerRow) - len(row)):
#                     row.append("");
# 
#             # insert critique row
#             query = "INSERT INTO " + table + " VALUES ("
#             for i in range(0, len(row)):
#                 if not row[i]:
#                     row[i] = "None"
#                 query += "?,"
#             query = query[:-1] # drop trailing comma
#             query += ")"
#             try:
#                 cursor.execute(query, row)
#             except:
#                 print "Error: this critique row could not be inserted into the database:"
#                 print row
#             numrows = numrows + 1
#===============================================================================

def getColumn(theDb, tableName, columnName, condition = None, conditionValues=(), isDistinct=False, suffix=""):
    return getColumns(theDb, tableName, (columnName, ), condition, conditionValues, isDistinct, suffix)

def getColumns(theDb, tableName, columnNames, condition = None, conditionValues=(), isDistinct=False, suffix=""):
    query = "SELECT " + ("DISTINCT " if isDistinct else "") + toQueryList(columnNames) + " FROM " + tableName
    query += ("" if condition == None or condition == "" else (" WHERE " + condition)) + " " + suffix

    cursor = theDb.cursor()
    cursor.execute(query, conditionValues)
    return cursor.fetchall()

def toQueryList(listItems):
    queryList = ""
    
    for listItem in listItems:
        queryList += listItem + ", "
        
    if len(listItems) != 0:
        queryList = queryList[:-2]  # drop trailing comma and space

    return queryList