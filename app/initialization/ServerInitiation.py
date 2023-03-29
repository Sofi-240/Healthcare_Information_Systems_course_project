from sqlalchemy import create_engine
import mysql.connector
from app.initialization.table_obj import Table

user = ''
password = ''
ip = '127.0.0.1'
port = 3306
host = "localhost"
db = 'his_project'
tables = []
cursor = ''
con = ''


def connect2server(usr='root', passwd='St240342', hst='localhost', prt=3306):
    global user, password, host, port, cursor, con
    user = usr
    password = passwd
    host = hst
    port = prt
    con = mysql.connector.connect(host=host, user=user, passwd=password, buffered=True)
    cursor = con.cursor()
    return cursor


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


def connect2serverDB(database=db):
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
    for i, k, t in zip(range(len(headers)), headers, table.headers_type):
        if i != 0:
            tbl_sqlStr += f", "
        if t == 'TIMESTAMP':
            tbl_sqlStr += f"{k} TIMESTAMP"
        elif t == 'DATETIME':
            tbl_sqlStr += f"{k} DATETIME"
        elif t == 'DATE':
            tbl_sqlStr += f"{k} DATE"
        else:
            tbl_sqlStr += f"{k} VARCHAR(255)"
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
    for i, k, t in zip(range(len(table.headers)), table.headers, table.headers_type):
        if i != 0:
            tbl_sqlStr += f", "
        if t == 'TIMESTAMP':
            tbl_sqlStr += f"{k} TIMESTAMP"
        elif t == 'DATETIME':
            tbl_sqlStr += f"{k} DATETIME"
        elif t == 'DATE':
            tbl_sqlStr += f"{k} DATE"
        else:
            tbl_sqlStr += f"{k} VARCHAR(255)"
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


def main():
    connect2server(usr='root', passwd='St240342', hst="localhost", prt=3306)
    table_lst = [Table('department', pks=['depID'])]
    table_lst += [Table('diseases', pks=['disID'], fks=[['depID']], refs=[['depID']], ref_tables=['department'])]
    table_lst += [Table('symptomsDiseases', fks=[['disID']], refs=[['disID']], ref_tables=['diseases'])]
    table_lst += [Table('patient', pks=['ID'])]
    table_lst += [Table('symptomsPatient', fks=[['ID']], refs=[['ID']], ref_tables=['patient'])]
    for tbl in table_lst:
        createFullTable(tbl)
    return


if __name__ == "__main__":
    main()
