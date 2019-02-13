import os.path
import pyodbc
from bs4 import BeautifulSoup
import openpyxl
from openpyxl.styles import PatternFill, colors, Font
import pyperclip
import sys
import re

def printUsage():
    print(Fore.BLUE + 'Usage:\nCopy the SQL script needs to run, and execute "exportFromDB db=db_name_in_config" or "exportFromDB tc=truck_centerID"')
    exit()

def getDatabaseConfiguration(databaseName):
    result = {'driver':'','server':'', 'database':databaseName, 'userName':'', 'password':'', 'trustedConnection':''}
    
    configurationContent = '\n'.join(open('AppSettings.xml').readlines())
    configurationDocument = BeautifulSoup(configurationContent, features='xml')
    databaseSettingsNode = configurationDocument.find('databaseSettings')
    if databaseSettingsNode is not None:
        databaseConfigurationNode = databaseSettingsNode.find('database', databaseName=databaseName)
        if databaseConfigurationNode is not None:
            if databaseConfigurationNode.get('driver') is not None:
                result['driver'] = databaseConfigurationNode.get('driver')
            if databaseConfigurationNode.get('server') is not None:
                result['server'] = databaseConfigurationNode.get('server')
            if databaseConfigurationNode.get('userName') is not None:
                result['userName'] = databaseConfigurationNode.get('userName')
            if databaseConfigurationNode.get('password') is not None:
                result['password'] = databaseConfigurationNode.get('password')
            if databaseConfigurationNode.get('trustedConnection') is not None:
                result['trustedConnection'] = databaseConfigurationNode.get('trustedConnection')
        else:
            return None

    return result

def getDatabaseConnection(configuration):
    if configuration is not None:
        if configuration['trustedConnection'] == 'true':
            return pyodbc.connect('Driver={driver};'
                'Server={server};'
                'Database={database};Trusted_Connection=yes'.format(driver = configuration['driver'], server = configuration['server'],
                                                                    database = configuration['database']))
        else:
            return pyodbc.connect('Driver={driver};'
                'Server={server};'
                'Database={database};'
                'UID={username};'
                'PWD={password}'.format(driver = configuration['driver'], server = configuration['server'], database = configuration['database'],
                                        username = configuration['userName'], password = configuration['password']))

#Read configuration info
if not os.path.exists('AppSettings.xml'):
    print("ERROR: Cannot find configuration file.")
    exit()

dbConnection = None

#Check argument
databaseNames = ''
if len(sys.argv) < 2:
    printUsage()
else:
    dbNameRe = re.compile(r'^db=(?P<dbName>.+)$')
    dbNameMatch = dbNameRe.match(sys.argv[1])
    if dbNameMatch is not None:
        databaseNames = dbNameMatch.group('dbName').split(',')
    else:
        printUsage()

#Check SQL script
sql = pyperclip.paste()
if len(sql) == 0:
    print('ERROR: Please copy SQL script to clipboard before execution.')
    exit()

print('Acout to execute:\n{sql}\n'.format(sql = sql))

#Create Excel file
fileName = 'dataExtract.xlsx'
wb = openpyxl.workbook.Workbook()

#Read Style configuration
headerRowDisplayStyle = {'fontColor':'FFFFFF', 'backgroundColor':'000080'}
highLightRowDisplayStyle = {'fontColor':'FFFFFF', 'backgroundColor':'FFFF00'}

configurationContent = '\n'.join(open('AppSettings.xml').readlines())
configurationDocument = BeautifulSoup(configurationContent, features='xml')
uiConfiguration = configurationDocument.find('uiSettings')
if uiConfiguration is not None:
    headerRowConfiguration = uiConfiguration.find('headerRow')
    if headerRowConfiguration is not None:
        if headerRowConfiguration.get('fontColor') is not None:
            headerRowDisplayStyle['fontColor'] = headerRowConfiguration.get('fontColor')
        if headerRowConfiguration.get('backgroundColor') is not None:
            headerRowDisplayStyle['backgroundColor'] = headerRowConfiguration.get('backgroundColor')
    highLightRowConfiguration = uiConfiguration.find('highLightRow')
    if highLightRowConfiguration is not None:
        if highLightRowConfiguration.get('fontColor') is not None:
            highLightRowDisplayStyle['fontColor'] = highLightRowConfiguration.get('fontColor')
        if highLightRowConfiguration.get('backgroundColor') is not None:
            highLightRowDisplayStyle['backgroundColor'] = highLightRowConfiguration.get('backgroundColor')

headerRowFill = PatternFill(start_color=headerRowDisplayStyle['backgroundColor'],
                    end_color=headerRowDisplayStyle['backgroundColor'],
                    fill_type='solid')
highLightRowFill = PatternFill(start_color=highLightRowDisplayStyle['backgroundColor'],
                    end_color=highLightRowDisplayStyle['backgroundColor'],
                    fill_type='solid')
headerRowFont = Font(color=headerRowDisplayStyle['fontColor'])
highLightRowFont = Font(color=highLightRowDisplayStyle['fontColor'])

for databaseName in databaseNames:
    print('Fetching data from {db}\n'.format(db = databaseName))
    dbConfig = getDatabaseConfiguration(databaseName)
    if dbConfig is None:
        print('ERROR: Cannot find database configuration for {db}\n'.format(db = databaseName))
        continue
    
    dbConnection = getDatabaseConnection(dbConfig)
    dbCursor = dbConnection.cursor()
    dbCursor.execute(sql)

    dataSheet = wb.create_sheet(title = databaseName, index = 0)

    #Write Header row
    columnCount = len(dbCursor.description)
    headerIndex = 1
    for header in dbCursor.description:
        headerCell = dataSheet.cell(row = 1, column = headerIndex)
        headerCell.value = header[0]
        headerCell.fill = headerRowFill
        headerCell.font = headerRowFont
        headerIndex += 1

    rowIndex = 2
    for row in dbCursor.fetchall():
        for i in range(0, columnCount):
            dataSheet.cell(row = rowIndex, column = i + 1).value = row[i]
        rowIndex += 1

    cornerCell = dataSheet['A2']
    dataSheet.freeze_panes = cornerCell
    
    dbConnection.close()

#Save SQL script
sqlSheet = wb.create_sheet(title='SQL', index=len(wb.worksheets)-1)
sqlSheet['A1'].value = sql

wb.save(fileName)
print('Data saved as ' + fileName)
