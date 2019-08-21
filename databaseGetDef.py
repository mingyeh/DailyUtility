import pyodbc
from bs4 import BeautifulSoup
import databaseUtility

databaseName = input('Please input database from where to get the defination:')

databaseConnection = databaseUtility.getDatabaseConnection(databaseName)
if databaseConnection is not None:
    print('Database connected.')
else:
    print('Cannot connect to database specified.')
    exit()

while(True):
    objectName = input('Please input object name:')
    if objectName.lower() == 'exit':
        break
    getObjectTypeSql = "select type as objectType from sys.objects where name = '{obj}'".format(obj = objectName)

    cursor = databaseConnection.cursor()
    cursor.execute(getObjectTypeSql)

    objectTypeRow = cursor.fetchone()

    objectType = ''
    if objectTypeRow is None:
        print('Object not found.')
        continue
    else:
        objectType = str(objectTypeRow.objectType).strip()
        if objectType not in ['FN', 'F', 'P', 'TF', 'V']:
            print('The object does not support definition script.')
            continue

    cursor.execute('sp_helptext {obj}'.format(obj = objectName))
    definitionRows = cursor.fetchall()

    scriptHeader = """SET XACT_ABORT ON

BEGIN TRANSACTION
-- Check Database object is exists or not 
IF EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[{obj}]') 
AND type in (N'{objType}'))

-- if object exists then drop object first
DROP PROCEDURE [dbo].[{obj}]
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO\n""".format(obj = objectName, objType = objectType)
    scriptFooter = '''GO

if @@TRANCOUNT > 0 
	COMMIT
GO'''
    comment = '''
/**********************************************************************************************************************
Release      SP Version        Date             Name    			Remarks
-----------------------------------------------------------------------------------------------------------------------
XXWXX			1.0				XX-XX-20XX		Ming Ye				PBI XXXX:
**********************************************************************************************************************/
'''
    
    definitionFile = open('{obj}.sql'.format(obj = objectName), 'w')
    definitionFile.write(scriptHeader)
    withComment = str(definitionRows[0][0]).startswith('/***')
    if not withComment:
        definitionFile.write(comment)
    for row in definitionRows:
        definitionFile.write(row[0].replace('\n', ''))
    
    definitionFile.write(scriptFooter)
    definitionFile.close()
    print('Object saved as {obj}.sql'.format(obj = objectName))

databaseConnection.close()
print('Database {db} disconnected.'.format(db = databaseName))
