import pandas as pd
from datetime import datetime
import numpy as np
import os


class Table:
    data_path = os.path.join(os.path.split(os.path.dirname(__file__))[0], "project_data\\")

    def __init__(self, tableName, csvFileName, pks=None, fks=None, ref_tables=None, refs=None):
        if refs is None:
            refs = []
        if ref_tables is None:
            ref_tables = []
        if fks is None:
            fks = []
        if pks is None:
            pks = []
        self.headers = []
        self.csvFileName = self.data_path + csvFileName + '.csv'
        self.tableName = tableName
        self.data = pd.DataFrame()
        self.pks = pks
        self.fks = fks
        self.ref_tables = ref_tables
        self.refs = refs
        try:
            self.data = pd.read_csv(self.csvFileName)
            self.headers = self.data.columns.values
        except FileNotFoundError:
            print("Error: Incorrect File Name")
        except:
            print("Error: Table Importing Went Wrong")
        finally:
            if "Timestamp" in self.data.columns:
                for i in range(self.data.shape[0]):
                    self.data.loc[i, "Timestamp"] = datetime.strptime(self.data.loc[i, "Timestamp"][:-6],
                                                                      '%Y/%m/%d %I:%M:%S %phone_ptr')
            if "DateTime" in self.data.columns:
                for i in range(self.data.shape[0]):
                    print(self.data.loc[i, "DateTime"])
                    self.data.loc[i, "DateTime"] = datetime.strptime(self.data.loc[i, "DateTime"], '%m/%d/%Y %H:%M')
            for i in self.data.columns:
                if i in ['DOB', 'Date']:
                    for j in range(self.data.shape[0]):
                        if isinstance(self.data.loc[j, i], str):
                            self.data.loc[j, i] = datetime.strptime(self.data.loc[j, i], '%m/%d/%Y').strftime(
                                "%Y-%m-%d")
            self.data = self.data.where(pd.notnull(self.data), None)
        return
