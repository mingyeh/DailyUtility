import pyodbc
from bs4 import BeautifulSoup
from colorama import init, Fore, Style
import databaseUtility

init()

databases = input('Please input database name separated by comma(,):').replace(' ', '')

conn = databaseUtility.getDatabaseConnection('EUD')
cursor = conn.cursor()

for database in databases.split(','):
    sql = """select 
	tc.TruckCenterID,
	tc.TruckCenter,
	tc.SqlDb,
	tc.ServerName,
	s.IPAddress,
	tc.Environment,
	case when tc.DatabaseType = 'T' then 'TruckCenter' else 'Region' end as DatabaseType,
	case when tc.DMSID = 1 then 'GDS' 
	when tc.DMSID = 2 then 'LDS'
	when tc.DMSID = 3 then 'RTMDS'
	else 'Unknown' end as DMS
from adtbTruckCenters as tc
	left join adtbServers as s on tc.ServerName = s.ServerName
where SqlDb = '{db}'""".format(db = database)
    
    truckCenterID = truckCenter = sqlDb = serverName = ipAddress = environment = databaseType = dms = ''
     
    cursor.execute(sql)
    row = cursor.fetchone()

    if row is None:
        continue

    truckCenterID = row[0]
    truckCenter = row[1]
    sqlDb = row[2]
    serverName = row[3]
    ipAddress = row[4]
    environment = row[5]
    databaseType = row[6]
    dms = row[7]

    print((Fore.RED if environment == 'PROD' and databaseType == 'TruckCenter' else Fore.GREEN) + '''Truck Center ID: \t{tcID}
Truck Center: \t{tc}
SQL Database: \t{db}
Server Name: \t{server}
IP Address: \t{ip}
environment: \t{env}
Database Type: \t{dbType}
DMS: \t{dms}\n'''.format(tcID = truckCenterID, tc = truckCenter, db = sqlDb, server = serverName, ip = ipAddress, env = environment, dbType = databaseType, dms = dms))    
    print(Style.RESET_ALL)

conn.close()

input('Press any key to exit')
