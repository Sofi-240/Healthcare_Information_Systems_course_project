from table_obj import Table
from sqlalchemy import create_engine
import mysql.connector
import os

user = 'root'
password = 'St240342'
ip = '127.0.0.1'
port = 3306
host = 'localhost'
db = "his_project"
tables = []
cursor = ''
con = ''
fpath = os.path.join(os.path.split(os.path.dirname(__file__))[0], "project_data\\")


def connect2server(usr=user, passwd=password, hst=host, prt=port):
    global user, password, host, port, cursor, con
    user, password, host, port = usr, passwd, hst, prt
    con = mysql.connector.connect(host=host, user=user, passwd=password)
    cursor = con.cursor()
    return cursor


def showDBs():
    global cursor
    cursor.execute("SHOW DATABASES")
    print("Databases in server:")
    for x in cursor:
        print(x)
    return


def initDB(dbname):
    global db, cursor
    db = dbname
    print(db)
    print(f"drop database if exists {db.lower()}")
    cursor.execute(f"drop database if exists {db.lower()}")
    cursor.execute(f"CREATE DATABASE {db.upper()}")
    showDBs()
    return


def connect2serverDB(database=db):
    # this function assumes existing connection to server
    global user, password, host, port, cursor, db, con
    db = database
    con = mysql.connector.connect(host=host, user=user, passwd=password, database=db)
    cursor = con.cursor()
    return cursor, con


def showTables():
    global cursor
    cursor.execute("show tables")
    print(f"Tables in DB:")
    for i in cursor:
        print(i)
    return


def createNewTable(table, headers=[], dbname=db):
    global db, cursor
    if dbname != db:
        connect2serverDB(dbname)
    if len(headers) == 0:
        headers = table.headers
    print(table.tableName.lower())
    cursor.execute(f"use {db}")
    cursor.execute(f"drop table if exists {table.tableName.lower()}")
    tbl_firs = f"CREATE TABLE {table.tableName.lower()} ("
    for i, k in enumerate(headers):
        if i == 0:
            if "Timestamp" in k:
                tbl_firs += f"{k} TIMESTAMP"
            elif "DateTime" in k:
                tbl_firs += f"{k} DATETIME"
            elif "Date" in k:
                tbl_firs += f"{k} DATE"
            else:
                tbl_firs += f"{k} VARCHAR(255)"
        else:
            if "Timestamp" in k:
                tbl_firs += f", {k} TIMESTAMP"
            elif "Date" in k:
                tbl_firs += f", {k} DATE"
            else:
                tbl_firs += f", {k} VARCHAR(255)"
    tbl_firs += f")"
    print(tbl_firs)
    cursor.execute(tbl_firs)
    return


def insertData2Table(table):
    global user, password, ip, port, db, con
    con = create_engine('mysql+pymysql://' + user + ':' + password + '@' + ip + ':' + str(port) + '/' + db)
    table.data.to_sql(name=table.tableName.lower(), con=con, index=False, if_exists="append")
    return


def addPKs(table):
    global cursor, db
    connect2serverDB(db)
    lst = table.pks
    if len(lst) == 1:
        alter_table_com = f"ALTER TABLE {table.tableName.lower()} " \
                          f"ADD PRIMARY KEY ({lst[0]})"
        print(alter_table_com)
        cursor.execute(alter_table_com)
    elif len(lst) > 1:
        alter_table_com = f"ALTER TABLE {table.tableName.lower()} ADD PRIMARY KEY ("
        for j in lst[:-1]:
            alter_table_com += f"{j},"
        alter_table_com += f"{lst[-1]})"
        print(alter_table_com)
        cursor.execute(alter_table_com)
    return


def addFKs(table):
    global cursor, db
    connect2serverDB(db)
    for i, t in enumerate(table.ref_tables):
        if len(table.fks[i]) == 1:
            alter_table_com = f"ALTER TABLE {table.tableName.lower()} " \
                              f"ADD FOREIGN KEY ({table.fks[i][0]}) " \
                              f"REFERENCES {t}({table.refs[i][0]})"
            print(alter_table_com)
            cursor.execute(alter_table_com)
        elif len(table.fks[i]) > 1:
            alter_table_com = f"ALTER TABLE {table.tableName.lower()} " \
                              f"ADD FOREIGN KEY ("
            for j in range(len(table.fks[i]) - 1):
                alter_table_com += f"{table.fks[i][j]}, "
            alter_table_com += f"{table.fks[i][-1]}) REFERENCES {t}( "
            for j in range(len(table.refs[i]) - 1):
                alter_table_com += f"{table.refs[i][j]}, "
            alter_table_com += f"{table.refs[i][-1]})"
            print(alter_table_com)
            cursor.execute(alter_table_com)
    return

