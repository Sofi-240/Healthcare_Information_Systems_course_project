import pandas as pd
import datetime
import os


class Table:
    def __init__(self, tableName, **kwargs):
        self.headers = []
        self.headers_type = []
        if not kwargs.get('csvFileName'):
            self.csvFileName = os.path.split(os.path.dirname(__file__))[0] + '\\initialization\\' + tableName + '.csv'
        else:
            self.csvFileName = os.path.split(os.path.dirname(__file__))[0] + '\\initialization\\' + kwargs.get(
                'csvFileName') + '.csv'
        self.tableName = tableName
        self.pks = kwargs.get('pks')
        self.fks = kwargs.get('fks')
        self.ref_tables = kwargs.get('ref_tables')
        self.refs = kwargs.get('refs')
        self.data = kwargs.get('data')
        if self.pks is None:
            self.pks = []
        if self.fks is None:
            self.fks = []
        if self.ref_tables is None:
            self.ref_tables = []
        if self.refs is None:
            self.refs = []
        try:
            if self.data is None:
                self.data = pd.read_csv(self.csvFileName)
        except FileNotFoundError:
            print("Error: Incorrect File Name")
        except:
            print("Error: Table Importing Went Wrong")
        finally:
            self.headers = self.data.columns.values
            for h in self.headers:
                catch = type(self.data[h].iloc[0])
                self.headers_type.append(catch)
                if catch == str:
                    catch = self.catch_data(self.data[h].iloc[0])
                if type(catch) != str and self.headers_type[-1] == str:
                    self.transform_datetime(h, catch)
                    self.headers_type.append(catch)
            self.data = self.data.where(pd.notnull(self.data), None)

    @staticmethod
    def datetime_format(val, dataformat):
        if dataformat == 'Timestamp':
            return datetime.datetime.strptime(val[:-6], '%Y/%m/%d %I:%M:%S %phone_ptr')
        elif dataformat == 'DateTime':
            return datetime.datetime.strptime(val, '%m/%d/%Y %H:%M')
        elif dataformat == 'Date':
            return datetime.datetime.strptime(val, "%Y-%m-%d")
        return

    @staticmethod
    def catch_data(str_val):
        fmts = ('%Y', '%b %d, %Y', '%b %d, %Y', '%B %d, %Y', '%B %d %Y', '%m/%d/%Y', '%m/%d/%y', '%b %Y', '%B%Y', '%b %d,%Y')
        dataformat = None
        for fmt in fmts:
            try:
                t = datetime.datetime.strptime(str_val, fmt)
                dataformat = type(t)
                break
            except ValueError:
                pass
        if not dataformat:
            return str
        return dataformat

    def save(self):
        if os.path.exists(self.csvFileName):
            os.remove(self.csvFileName)
        self.data.to_csv(self.csvFileName, index=False)
        print('Save Data in: ', self.csvFileName)
        return

    def transform_datetime(self, col, dataformat):
        for i in self.data.index:
            self.data.loc[i, col] = self.datetime_format(self.data.loc[i, col], dataformat)
        return
