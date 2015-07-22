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
