from server.serverInitiation import showTables, showDBs, connect2server, connect2serverDB, main as serverMain
from frontEnd.appPanel import AppPanel

"""
Run this file in order to initialize the database and load the application
NOTE: Change the values for the connection to the workbench to your values!!!
"""


if __name__ == '__main__':
    usr = 'root'
    passwd = 'St240342'
    hst = 'localhost'
    prt = 3306

    try:
        connect2server(usr=usr, passwd=passwd, hst=hst, prt=prt)
    except Exception as e:
        print('MySql error: ', e)
        print('set-up the sql connection values')
    finally:
        if 'his_project' not in showDBs():
            serverMain()
        connect2serverDB(database="his_project")
        if not showTables():
            serverMain()
        App = AppPanel()
        App.mainloop()
