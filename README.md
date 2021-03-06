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

