# DailyUtility
DailyUtility project is used to contain the scripts I use in daily work.

## How to use
Since the best way of getting usage instruction is to read the source code.
Here is some information that could be helpful for the newbies.

### checkDatabase

This is script to fetch the type of database, and useless to who does not work in DP team.

**Usage:**

```
python checkDatabase.py
```

Input name of databases (separated with comma) when prompted.

**Example:**

```
Please input database name separated by comma(,):GB00,GB20,NL564
Truck Center ID:        728
Truck Center:   UK Regional
SQL Database:   GB00
Server Name:    SOME_DB_SERVER
IP Address:     XXX.XXX.XX.XX
environment:    QA
Database Type:  Region
DMS:    Unknown


Truck Center ID:        20
Truck Center:   TC GB North&Scotland
SQL Database:   GB20
Server Name:    ANOTHER_DB_SERVER
IP Address:     XXX.XXX.XX.XXX
environment:    PROD
Database Type:  TruckCenter
DMS:    GDS


Truck Center ID:        564
Truck Center:   Netherlands QA
SQL Database:   NL564
Server Name:    NEW_DB_SERVER_NAMW
IP Address:     XXX.XXX.XX.XX
environment:    QA
Database Type:  TruckCenter
DMS:    GDS


Press any key to exit
```

The Truck Center database in Production Environment will be marked red.

### databaseExport
This is script used to export result of SQL script execution to Excel file.

**Usage**

1. Add configuration of database in AppSettings.xml if necessary.
2. Copy the SQL script to clipboard.
3. Execute script in command line with db parameter.

**Example**

```
C:\code\DailyUtility>python databaseExport.py db=GB20,GB23,GB25,GB309,GB16
Acout to execute:
select
        d.DealerID,
        d.Dealer,
        d.GDSDealerID,
        d.DealerCode,
        c.Country,
        tc.TruckCenter
from rnvwDealers as d
        left join eud.dbo.adtbCountry as c on d.CountryID = c.CountryID
        left join eud.dbo.adtbTruckCenters as tc on d.TruckCenterID = tc.TruckCenterID

Fetching data from GB20

Fetching data from GB23

Fetching data from GB25

Fetching data from GB309

Fetching data from GB16

Data saved as dataExtract.xlsx
```

If the SQL script needs to be executed in multiple databases, please separate database names with comma(,) in db parameter.

The database names in db parameter must be identical with the databaseName value in AppSettings.xml

Execution result of each database will be listed in individual sheet in Excel file.

![Data Export](https://raw.githubusercontent.com/mingyeh/DailyUtility/master/screendumps/data_export.jpg)

The SQL script will be listed in *"SQL"* Sheet in Excel file.

![SQL Script](https://raw.githubusercontent.com/mingyeh/DailyUtility/master/screendumps/sql.jpg)

The header style in Excel file can be set in AppSettings.xml

```XML
<uiSettings>
	<headerRow fontColor="FFFFFF" backgroundColor="34495E" />
	<highLightRow fontColor="FFFFFF" backgroundColor="D35400" />
</uiSettings>
```

### databaseGetDef

This script is used to generate creating script of database objects.

The script supports following object types:

- Function
- Stored procedure
- View

**Usage**

```
python databaseGetDef.py
```

Input database name when prompted (Add corresponding configuration in AppSettings.xml before execution)

Input the name of object when prompted, as the screen dump listed underneath.

![Fetch object definition](https://raw.githubusercontent.com/mingyeh/DailyUtility/master/screendumps/get_def.jpg)

Input *exit* to quit the script.

### excel2MarkDownTable

This script is used to convert table in Excel file to MarkDown table snippet.

**Usage:**

1. Create table in Excel file and save as "sample_data.xls" in current directory.

   ![Table in Excel](https://raw.githubusercontent.com/mingyeh/DailyUtility/master/screendumps/excel_table.jpg)

2. Execute the script.

   ![Table in Excel](https://raw.githubusercontent.com/mingyeh/DailyUtility/master/screendumps/convert_markdown.jpg)
3. The MarkDown snippet will be output in console, and copied to clipboard as well.

   ![MarkDown Table](https://raw.githubusercontent.com/mingyeh/DailyUtility/master/screendumps/mark_down.jpg)

## stringConcat

This script is used to concatenate the data parsed from Clipboard based on parameters. It can be helpful when you need to create SQL script or source code based on data in Excel spreadsheet.

**Usage:**

1. Select the data cells in Excel spreadsheet you'd like to concatenate and copy the data to Clipboard (either by contect menu or shortcut key).

   ![Table in Excel](https://raw.githubusercontent.com/mingyeh/DailyUtility/master/screendumps/data_to_concat.jpg)

2. Execute the script.

3. Copy the SQL script file or source code file, and paste the concatenation result.

```
'10XA036ST004', '10XD036TAG04', '10XJ036ST004', '10XM036MS004', '11MA016CIT06', '11MA016LW004', 
'11MA016ST004', '11MA016XLW04', '11MA036ST004', '11MJ016ST004', '11MJ036ST004', '11MM016GV014', 
'11MM016MS004', '11MM036MS004', '20DA016PVT10', '20DA016PVT11', '20DA016STD10', '20DA016STD11', 
'20DA086STA00', '20DA086STA01', '20DA086STD10', '20DA086STD11', '20DJ016LOW00', '20DJ016LOW01', 
'20DJ016LOW10', '20DJ016LOW11', '20DJ016PVT10', '20DJ016PVT11', '20DJ016PVU10', '20DJ016PVU11', 
'20DJ016REF10', '20DJ016REF11', '20DJ016STD10', '20DJ016STD11', '20DJ086CIT10', '20DJ086CIT11', 
'20DJ086CIT12', '20DJ086GAZB9', '20DJ086GNVB9', '20DJ086GNVD9', '20DJ086GNVS9', '20DJ086LOW00', 
'20DJ086LOW01', '20DJ086LOW02', '20DJ086LOW10', '20DJ086LOW11', '20DJ086LOW12', '20DJ086REF10', 
'20DJ086REF11', '20DJ086REF12', '20DJ086ST9OF', '20DJ086STD10', '20DJ086STD11', '20DJ086STD12', 
'20DJ086STD20', '20DJ086STD21', '20DJ086STD22', '20DJ0G6REF03', '20DJ0G6STD03', '20DM016LOW00', 
'20DM016LOW01', '20DM016LOW10', '20DM016LOW11', '20DM016REF00', '20DM016REF01', '20DM016STD00', 
'20DM016STD01', '20DM086CIT00', '20DM086CIT01', '20DM086CIT02', '20DM086LOW00', '20DM086LOW01', 
'20DM086LOW02', '20DM086LOW10', '20DM086LOW11', '20DM086LOW12', '20DM086REF00', '20DM086REF01', 
'20DM086REF02', '20DM086STD00', '20DM086STD01', '20DM086STD02', '20DM086STDOF', '20DM0G6REF03', 
'20DM0G6STD03', '21DA016STD00', '21DJ016STD00', '21DJ086STD02', '21DM016STD00', '21DM086STD02', 
'30CA016STD00', '30CA036STD00', '30CJ016K0000', '30CJ016STD00', '30CJ036STD00', '30CM016STD00', 
'30CM036STD00', '30CN016K0000', '30CN016STD00', '30CN016TRI00', '30CN016TRI01', '30CN016TRI02', 
'30CN036K0000', '30CN036STD00', '30CN036TRI00', '30CN036TRI01', '30CN036TRI02', '30CR016TRI01', 
'30CR036TRI02', '30CS016K0000', '30CS016STD00', '30CS036K0000', '30CS036STD00', '40J20560LD00', 
'40J20560LD01', '40J20562LD00', '40J20562LD01', '40J20562MD00', '40J20562MD01', '40J20567LD00', 
'40J20567LD01', '40J20862MD00', '40J20862MD01', '40J40563HD00', '40J40563HD01', '40J40563HK00', 
'40J40563HK01', '40J40563MD00', '40J40563MD01', '40J40564HD00', '40J40564HD01', '40J40564HK00', 
'40J40564HK01', '40J40564MD00', '40J40564MD01', '40J40863HD00', '40J40863HD01', '40J40863HK00', 
'40J40863HK01', '40J40863MD00', '40J40863MD01', '40J40864HD00', '40J40864HD01', '40J40864HK00', 
'40J40864HK01', '40J40864MD00', '40J40864MD01', '40J60566HD00', '40J60566HD01', '40J60566HK00', 
'40J60566HK01', '40J60566MD00', '40J60566MD01', '40J60866HD00', '40J60866HD01', '40J60866HK00', 
'40J60866HK01', '40J60866MC00', '40J60866MC01', '40J60866MD00', '40J60866MD01', '40J60866MR00', 
'40J60866MR01', '40J80868HC00', '40J80868HC01', '40J80868HD00', '40J80868HD01', '40J80868HK00', 
```