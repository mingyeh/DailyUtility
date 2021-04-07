from bs4 import BeautifulSoup
import pyodbc

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

def getDatabaseConnectionFromParam(server, userName, password, database, trustedConnection, driver = 'SQL Server Native Client 11.0'):
    if trustedConnection == 'true':
        return pyodbc.connect('Driver={driver};'
                'Server={server};'
                'Database={database};Trusted_Connection=yes'.format(driver = driver, server = server,
                                                                    database = database))
    else:
        return pyodbc.connect('Driver={driver};'
                'Server={server};'
                'Database={database};'
                'UID={username};'
                'PWD={password}'.format(driver = driver, server = server, database = database,
                                        username = userName, password = password))

def getDatabaseConnectionFromEUD(databaseName):
    sqlGetDatabaseInfo = """select
    s.IPAddress
from adtbTruckCenters as tc
    left join adtbServers as s on tc.ServerName = s.ServerName
where
    tc.SqlDb = '{db}'""".format(db = databaseName)

    eudConnection = getDatabaseConnection('EUD')
    eudCursor = eudConnection.cursor()
    eudCursor.execute(sqlGetDatabaseInfo)
    ipAddress = eudCursor.fetchval()
    if ipAddress is not None and ipAddress != '':
        return getDatabaseConnectionFromParam(ipAddress, '', '', databaseName, 'true')
    else:
        return None

def getDatabaseConnection(databaseName):
    configuration = getDatabaseConfiguration(databaseName)
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
    else:
        getDatabaseConnectionFromEUD(databaseName)

if __name__ == '__main__':
    print('Begin function verification... \n\nGetting EUD configuration...\n')
    eudConfiguration = getDatabaseConfiguration('EUD')
    print(eudConfiguration)
    print('\nConnecting to EUD database...\n')
    eudDatabaseConnection = getDatabaseConnection('EUD')
    print('Fetching record from EUD database...\n')
    eudCursor = eudDatabaseConnection.cursor()
    eudCursor.execute('select getdate()')
    print(eudCursor.fetchone()[0])
    print('\nClosing EUD connection...\n')
    eudDatabaseConnection.close()
    print('\nTesting get connection via EUD...\n')
    tcConnection = getDatabaseConnectionFromEUD('JP385')
    tcCursor = tcConnection.cursor()
    tcCursor.execute('select getdate()')
    print(tcCursor.fetchval())
    print('\nClosing connection created via EUD...\n')
    tcConnection.close()
    print('Verification completed.')
    
