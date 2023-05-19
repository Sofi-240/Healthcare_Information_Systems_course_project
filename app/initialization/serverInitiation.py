from sqlalchemy import create_engine
import mysql.connector
from app.initialization.tableObj import Table
import os
import pandas as pd
import json

user, password, cursor, con = '', '', '', ''
ip, port, host, db = '127.0.0.1', 3306, 'localhost', 'his_project'


def connect2server(usr='root', passwd='St240342', hst='localhost', prt=3306):
    global user, password, host, port, cursor, con
    user = usr
    password = passwd
    host = hst
    port = prt
    con = mysql.connector.connect(host=host, user=user, passwd=password, buffered=True)
    cursor = con.cursor()
    return cursor, con


def showDBs():
    global cursor
    cursor.execute("SHOW DATABASES")
    print("Databases in SERV:")
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


def connect2serverDB(database='his_project'):
    connect2server()
    global user, password, host, port, cursor, db, con
    db = database
    con = mysql.connector.connect(host=host, user=user, passwd=password, database=db, buffered=True)
    cursor = con.cursor()
    return cursor, con


def showTables():
    global cursor
    cursor.execute("show tables")
    print(f"Tables in DB:")
    for i in cursor:
        print(i)
    return


def hasTable(name):
    global cursor
    cursor.execute("show tables")
    for x in cursor:
        if x[0] == name:
            return True
    return False


def createNewTable(table, headers=[], dbname=db):
    global db, cursor
    if dbname != db:
        connect2serverDB(dbname)
    if len(headers) == 0:
        headers = table.headers
    print(table.tableName.lower())
    cursor.execute(f"use {db}")
    dropRefFKs(table)
    cursor.execute(f"drop table if exists {table.tableName.lower()}")
    tbl_sqlStr = f"CREATE TABLE {table.tableName.lower()} ("
    for k, t in zip(table.headers, table.headers_type):
        tbl_sqlStr += f"{k} {t}, "
    tbl_sqlStr = tbl_sqlStr[:-2]
    tbl_sqlStr += f")"
    print(tbl_sqlStr)
    cursor.execute(tbl_sqlStr)
    return


def insertData2Table(table):
    global user, password, ip, port, db
    con = create_engine('mysql+pymysql://' + user + ':' + password + '@' + ip + ':' + str(port) + '/' + db)
    table.data.to_sql(name=table.tableName.lower(), con=con, index=False, if_exists="append")
    return


def dropTable(table, dbname=db):
    global db, cursor
    if dbname != db:
        connect2serverDB(dbname)
    print(table.tableName.lower())
    dropRefFKs(table.tableName.lower())
    cursor.execute(f"use {db}")
    cursor.execute(f"drop table if exists {table.tableName.lower()}")
    return


def addPKs(table):
    global cursor, db
    connect2serverDB(database=db)
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
    connect2serverDB(database=db)
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


def hasFKs(tableName, dbname=db):
    global db, cursor
    if dbname != db:
        connect2serverDB(dbname)
    has_sqlStr = f"SELECT " \
                 f"TABLE_NAME, " \
                 f"CONSTRAINT_NAME " \
                 f"FROM " \
                 f"INFORMATION_SCHEMA.KEY_COLUMN_USAGE " \
                 f"WHERE " \
                 f"REFERENCED_TABLE_SCHEMA = '{dbname}'" \
                 f"AND REFERENCED_TABLE_NAME = '{tableName}';"
    cursor.execute(has_sqlStr)
    return cursor.fetchall()


def dropRefFKs(tableName, dbname=db):
    dep = hasFKs(tableName, dbname=dbname)
    if not dep:
        return
    print(dep)
    for t, c in dep:
        dropFk(t, c, dbname=dbname)
    return


def dropFk(tableName, fpk, dbname=db):
    global cursor, db
    if db != dbname:
        connect2serverDB(database=dbname)
    alter_table_com = f"ALTER TABLE {tableName} " \
                      f"DROP FOREIGN KEY {fpk};"
    cursor.execute(alter_table_com)
    print(alter_table_com)
    return


def createFullTable(table, dbname=db):
    global db, cursor
    if dbname != db:
        connect2serverDB(dbname)
    print(table.tableName.lower())
    cursor.execute(f"use {db}")
    dropRefFKs(table.tableName.lower())
    cursor.execute(f"drop table if exists {table.tableName.lower()}")
    tbl_sqlStr = f"CREATE TABLE {table.tableName.lower()} ("
    for k, t in zip(table.headers, table.headers_type):
        tbl_sqlStr += f"{k} {t}, "
    tbl_sqlStr = tbl_sqlStr[:-2]
    if table.pks:
        tbl_sqlStr += f",  PRIMARY KEY ("
        for pk in table.pks:
            tbl_sqlStr += f"{pk},"
        tbl_sqlStr = tbl_sqlStr[:-1] + f")"
    tbl_fkStr = ""
    if table.fks:
        for fk, ref, refT in zip(table.fks, table.refs, table.ref_tables):
            if not hasTable(refT):
                continue
            for i, j in zip(fk, ref):
                tbl_fkStr += f" CONSTRAINT FK_{i + table.tableName.lower() + '_' + j + refT} FOREIGN KEY(" \
                             f"{i}) REFERENCES {refT}(" \
                             f"{j}) ON DELETE NO ACTION ON UPDATE NO ACTION,"
        if tbl_fkStr:
            tbl_fkStr = "," + tbl_fkStr[:-1]
    tbl_sqlStr += tbl_fkStr + f")"
    print(tbl_sqlStr)
    cursor.execute(tbl_sqlStr)
    if table.shape[0] != 0:
        insertData2Table(table)
    return


def executedQuery(queryStr, dbname=db):
    global db, cursor
    if dbname != db:
        connect2serverDB(dbname)
    cursor.execute(queryStr)
    return cursor.fetchall()


def executedQueryCommit(queryStr, dbname=db):
    global db, cursor, con
    if dbname != db:
        connect2serverDB(dbname)
    cursor.execute(queryStr)
    con.commit()
    return


def insert2Table(tableName, values, columns=None, dbname=db):
    global cursor, db, con
    if db != dbname:
        connect2serverDB(database=dbname)
    if not hasTable(tableName.lower()):
        print('Table not EXIST!')
        return
    if not columns:
        columns = getTableCarry(tableName.lower())['headers']
    if len(columns) != len(values):
        print('Values number != Columns number')
        return
    queryStr = f"INSERT INTO {tableName.lower()} "
    if columns:
        queryStr += "("
        for col in columns:
            queryStr += f"{col}, "
        queryStr = queryStr[:-2] + f") "
    queryStr += f"VALUES("
    for val in values:
        queryStr += f"'{val}', "
    queryStr = queryStr[:-2] + f");"
    print(queryStr)
    cursor.execute(queryStr)
    con.commit()
    return


def getTableCarry(tableName):
    temp_carry = json.loads(
        open(os.path.split(os.path.dirname(__file__))[0] + '\\initialization\\' + 'tables_carry.txt',
             'r').read())
    return temp_carry.get(tableName)


def updateTableCarry(tableName, val):
    temp_carry = json.loads(
        open(os.path.split(os.path.dirname(__file__))[0] + '\\initialization\\' + 'tables_carry.txt',
             'r').read())
    temp_carry[tableName] = val
    param_file = open(os.path.split(os.path.dirname(__file__))[0] + '\\initialization\\' + 'tables_carry.txt', 'w')
    param_file.write(json.dumps(temp_carry))
    param_file.close()
    return


def updateTable(tableName):
    queryStr = f"SELECT * FROM {tableName.lower()};"
    res = executedQuery(queryStr)
    print('updateTable:\n', queryStr)
    table = Table(tableName.lower())
    colsName = table.headers
    table.data = pd.DataFrame(res, columns=colsName)
    table.save()
    return


def main():
    connect2server()
    initDB('his_project')
    connect2serverDB(database='his_project')
    tablesNames = ['diseases', 'symptomsDiseases', 'patient', 'symptomsPatient', 'researcher', 'activeresearch',
                   'patientdiagnosis']
    for tbl in tablesNames:
        createFullTable(Table(tbl))
    return


if __name__ == "__main__":
    main()
