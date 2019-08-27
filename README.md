# DailyUtility
DailyUtility project is used to contain the scripts I use in daily work.

## How to use
Since the best way of getting usage instruction is to read the source code.
Here is some information that could be helpful for the newbies.

### checkDatabase

This is script to fetch the type of database, and useless who does not work in DP team.

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

The Truck Center database in Production Environment will be mark red.