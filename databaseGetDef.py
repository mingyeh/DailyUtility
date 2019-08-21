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

    definitionFile = open('{obj}.sql'.format(obj = objectName), 'w')
    for row in definitionRows:
        definitionFile.write(row[0].replace('\n', ''))
    definitionFile.close()

databaseConnection.close()
print('Database {db} disconnected.'.format(db = databaseName))
