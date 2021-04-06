import pyodbc
import databaseUtility

objectToCheck = 'trvwCustomers'

sqlGetTruckCenters = """select
	tc.TruckCenter,
	tc.SqlDb,
	tc.ServerName,
	s.IPAddress
from adtbTruckCenters as tc
	left join adtbServers as s on tc.ServerName = s.ServerName
where 
	tc.Environment = 'Prod' and tc.SqlDb is not null
	and tc.DatabaseType = 'T'
order by tc.ServerName, tc.SqlDb"""

eudConnection = databaseUtility.getDatabaseConnection('EUD')
eudCursor = eudConnection.cursor()
eudCursor.execute(sqlGetTruckCenters)

result = {}

indicator = 1
for tc in eudCursor.fetchall():  
    print('Checking Truck Center {i}: {tc}({db})...'.format(tc = tc.TruckCenter, db = tc.SqlDb, i = indicator))
    print('Server: {server}'.format(server = tc.IPAddress))
    print('Database: {db}'.format(db = tc.SqlDb))

    if tc.ServerName is None or tc.ServerName == '' or tc.SqlDb is None or tc.SqlDb == '':
        continue
    try:
        testSql = "select count(*) as objCount from sys.objects where name = '{obj}'".format(obj = objectToCheck)
        tcConnection = databaseUtility.getDatabaseConnectionFromParam(tc.IPAddress, '', '', tc.SqlDb, 'true')
        tcCursor = tcConnection.cursor()
        tcCursor.execute(testSql)
        
        matchCount = tcCursor.fetchval()
        if matchCount == 0:
            continue
        else:
            objDefinition = []
            
            sqlGetDefinition = 'sp_helptext {obj}'.format(obj = objectToCheck)
            tcCursor.execute(sqlGetDefinition)
                        
            for line in tcCursor.fetchall():
                objDefinition.append(line)
                            
            hashCode = hash(str(objDefinition))
            print('\tObject Hash Code: {h}'.format(h = hashCode))

            if hashCode not in result.keys():
                result[hashCode] = tc.SqlDb
            else:
                result[hashCode] = '{currentValue}, {db}'.format(currentValue = result[hashCode], db = tc.SqlDb)        
            
        tcConnection.close()
        indicator += 1
    except:
            print('\tCannot get definition.')
            continue
resultFile = open('compareResult.txt', 'w')
resultFile.write('HashCode\t\tDatabases\n')
resultFile.write('-'*100 + '\n')
for k in result.keys():
    resultFile.write('{h}\t\t{db}\n'.format(h = k, db = result[k]))

resultFile.close()
eudConnection.close()
