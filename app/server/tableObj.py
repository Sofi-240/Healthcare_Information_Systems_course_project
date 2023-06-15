import pandas as pd
import datetime
import os
import json


class Table:
    def __init__(self, tableName, **kwargs):
        self.headers = []
        self.headers_type = []
        if not kwargs.get('csvFileName'):
            self.csvFileName = os.path.split(os.path.dirname(__file__))[0] + '\\server\\' + tableName + '.csv'
        else:
            self.csvFileName = os.path.split(os.path.dirname(__file__))[0] + '\\server\\' + kwargs.get(
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
        if self.data is None:
            self.data = pd.DataFrame()
        self.load_self()

    @property
    def shape(self):
        return self.data.shape

    @staticmethod
    def datetime_format(val, dataformat):
        if dataformat == 'TIMESTAMP':
            return datetime.datetime.strptime(val[:-6], '%Y/%m/%d %I:%M:%S %phone_ptr')
        elif dataformat == 'DATETIME':
            return datetime.datetime.strptime(val, '%m/%d/%Y %H:%M')
        elif dataformat == 'DATE':
            return datetime.datetime.strptime(val[:10], "%Y-%m-%d")
        return val

    def load_self(self):
        newData = False
        try:
            if self.data.empty and not list(self.data.columns):
                self.data = pd.read_csv(self.csvFileName)
            else:
                newData = True
        except FileNotFoundError:
            self.data = pd.DataFrame()
        except:
            self.data = pd.DataFrame()
        finally:
            if newData:
                self.headers = list(self.data.columns.values)
                if not self.data.empty:
                    for h in self.headers:
                        catch = type(self.data[h].iloc[0])
                        if catch == str:
                            catch = self.catch_data(self.data[h].iloc[0])
                        else:
                            catch = 'VARCHAR(255)'
                        if catch != 'VARCHAR(255)':
                            self.transform_datetime(h, catch)
                        self.headers_type.append(catch)
                    self.data = self.data.where(pd.notnull(self.data), None)
                else:
                    self.headers_type = ['VARCHAR(255)'] * len(self.headers)
            else:
                temp_carry = json.loads(
                    open(os.path.split(os.path.dirname(__file__))[0] + '\\server\\' + 'tables_carry.txt',
                         'r').read())
                if temp_carry.get(self.tableName.lower()):
                    for key, val in temp_carry[self.tableName.lower()].items():
                        self.__dict__[key] = val

                    for col, typ in zip(self.headers, self.headers_type):
                        if typ in ['Timestamp', 'DateTime', 'Date']:
                            self.transform_datetime(col, typ)

        return

    def catch_data(self, str_val):
        fmts = ('TIMESTAMP', 'DATETIME', 'DATE')
        dataformat = None
        for fmt in fmts:
            try:
                self.datetime_format(str_val, fmt)
                dataformat = fmt
                break
            except ValueError:
                pass
        if not dataformat:
            return 'VARCHAR(255)'
        return dataformat

    def save(self):
        if os.path.exists(self.csvFileName):
            os.remove(self.csvFileName)
        self.data.to_csv(self.csvFileName, index=False)
        temp_carry = json.loads(
            open(os.path.split(os.path.dirname(__file__))[0] + '\\server\\' + 'tables_carry.txt',
                 'r').read())
        if not temp_carry.get(self.tableName.lower()):
            temp_carry[self.tableName.lower()] = {}
        for key, itm in self.__dict__.items():
            if key == 'data' or key == 'csvFileName' or key == 'tableName':
                continue
            temp_carry[self.tableName.lower()][key] = itm
        param_file = open(os.path.split(os.path.dirname(__file__))[0] + '\\server\\' + 'tables_carry.txt', 'w')
        param_file.write(json.dumps(temp_carry))
        param_file.close()
        return self

    def transform_datetime(self, col, dataformat):
        for i in self.data.index:
            self.data.loc[i, col] = self.datetime_format(self.data.loc[i, col], dataformat)
        return
