from app.initialization.ServerInitiation import *
import pandas as pd
import datetime
from app.communication.strNode import node
from app.initialization.table_obj import Table


class DataQueries:
    def __init__(self, dbName):
        self.dbName = dbName
        self.cursor, self.con = connect2serverDB(database=dbName)
        self.SymptomsRoot = {}

    @property
    def LastUpdate(self):
        return datetime.datetime.now() - datetime.datetime.strptime(getTableCarry('trigger'), '%m/%d/%Y %H:%M')

    def addItem(self, key, itm):
        self.__dict__[key] = itm
        return itm

    def enqueueSymptomsTree(self):
        table = self.queryTable('symptomsDiseases')
        for tip, txt in table[['disID', 'Symptom']].values:
            currTxt = txt + ' ' + str(tip)
            splitTxt = currTxt.split()
            splitTxt.reverse()
            headName = splitTxt.pop()
            head_node = self.SymptomsRoot.get(headName)
            if not head_node:
                head_node = node(headName)
                self.SymptomsRoot[headName] = head_node
            curr_node = head_node
            while splitTxt:
                curr_node = curr_node.append(node(splitTxt.pop()))
        print('LOAD Symptoms Tree')
        return

    def getDiagnosis(self, symTxt):
        if type(symTxt) is not str:
            print(f"symTxt need to by of type srt not {type(symTxt)}")
            return
        if not self.SymptomsRoot:
            self.enqueueSymptomsTree()
        splitTxt = symTxt.split()
        splitTxt.reverse()
        curr_node = self.SymptomsRoot.get(splitTxt.pop())
        while splitTxt and curr_node:
            curr_node = curr_node.getChild(splitTxt.pop())
        if not curr_node:
            print(f"{symTxt} is not found")
            return
        dig = []
        for key, child in curr_node.children.items():
            if not child.children:
                dig.append(key)
        return dig

    def queryTrigger(self):
        def DiagnosisDecision(dataList):
            dataList = pd.DataFrame(dataList, columns=['disID'])
            index = dataList.loc[:, ['disID']].value_counts()
            data = dataList.groupby(['disID'])
            dec = [data.get_group(index.index[0][0])['disID'].iloc[0], index.iloc[0]]
            if index.shape[0] == 1:
                return dec + [None, 0]
            dec += [data.get_group(index.index[1][0])['disID'].iloc[0], index.iloc[1]]
            return dec

        queryStr = f"SELECT t1.* FROM symptomspatient t1 " \
                   f"INNER JOIN patient t2 " \
                   f"ON t1.ID = t2.ID;"
        print('queryPatientDiagnosis:\n', queryStr)
        trigger_table = []
        SymptomsPatient_table = pd.DataFrame(executedQuery(queryStr), columns=['ID', 'symptom']).groupby(['ID'])
        for key, df in SymptomsPatient_table:
            stack = []
            for i in df.index:
                stack += self.getDiagnosis(df.loc[i, 'symptom'])
            trigger_table.append([df.loc[i, 'ID']] + DiagnosisDecision(stack))
            trigger_table[-1][2] /= df.shape[0]
            trigger_table[-1][-1] /= df.shape[0]
        trigger_table = pd.DataFrame(trigger_table,
                                     columns=["ID", "FdisID", "Fconf", "SdisID", "Sconf"])
        trigger_table = Table('patientdiagnosis', data=trigger_table,
                              pks=['ID'],
                              fks=[['ID'], ['FdisID'], ['SdisID']],
                              refs=[['ID'], ['disID'], ['disID']],
                              ref_tables=['patient', 'diseases', 'diseases'])
        trigger_table.save()
        createFullTable(trigger_table)
        return

    def queryTable(self, tableName):
        queryStr = f"SELECT * FROM {tableName.lower()};"
        res = executedQuery(queryStr)
        print('getTable:\n', queryStr)
        colsName = getTableCarry(tableName.lower())
        if colsName:
            colsName = colsName.get('headers')
        else:
            colsName = list(range(len(res[0])))
        table = pd.DataFrame(res, columns=colsName)
        self.addItem(tableName, table)
        return table

    def queryPatientResearch(self, order=0, *patientIDs):
        cols = []
        slc = None
        queryStr = f"SELECT "
        if order == 1:
            slc = 3

        for c in getTableCarry('patient').get('headers'):
            cols.append(c)
            queryStr += f"t1.{c}, "
            if c == 'DOB':
                queryStr += 'TIMESTAMPDIFF(YEAR, t1.DOB, CURDATE()), '
                cols.append('age')

        for c in getTableCarry('patientdiagnosis').get('headers')[1:slc]:
            queryStr += f"t2.{c}, "
            cols.append(c)
        queryStr = queryStr[:-2]
        queryStr += f" FROM patient AS t1 " \
                    f"INNER JOIN patientdiagnosis AS t2 " \
                    f"ON t1.ID = t2.ID"
        if not patientIDs:
            queryStr += f";"
        elif len(patientIDs) == 1:
            queryStr += f" WHERE t2.ID = {patientIDs[0]};"
        else:
            queryStr += f" WHERE t2.ID IN {patientIDs};"
        print('queryPatientResearch:\n', queryStr)
        table = pd.DataFrame(executedQuery(queryStr), columns=cols)

        self.addItem('PatientResearch', table)
        return table

    def queryPatientSymptoms(self, symptom):
        colsName = getTableCarry('patient').get('headers')
        queryStr = f"SELECT "
        for col in colsName:
            queryStr += f"t1.{col}, "
        queryStr += f"t2.Symptom " \
                    f"FROM patient as t1 " \
                    f"INNER JOIN " \
                    f"symptomspatient as t2 " \
                    f"WHERE t1.ID = t2.ID " \
                    f"AND t2.Symptom LIKE '%{symptom}%';"
        print('queryPatientSymptoms:\n', queryStr)
        table = pd.DataFrame(executedQuery(queryStr), columns=colsName + ['symptom'])
        self.addItem('PatientSymptoms', table)
        return table

    def queryPatientIndices(self, **kwargs):
        limits = {}
        colsName = getTableCarry('patient').get('headers')
        for key, val in kwargs.items():
            if key in ['ID', 'gender', 'support', 'phone', 'area', 'city', 'HMO', 'COB']:
                if type(val) == set or type(val) == tuple or type(val) == list:
                    temp = f" {key} IN {val} "
                else:
                    temp = f" {key} = '{val}' "
            if key in ['height', 'weight', 'age']:
                tempKey = key
                if key == 'age':
                    tempKey = 'TIMESTAMPDIFF(YEAR, DOB, CURDATE())'
                if type(val) == list:
                    eq = ('>=', '<=')
                else:
                    eq = ('>', '<')
                if val[0] is not None and val[1] is not None:
                    temp = f" {tempKey} {eq[0]} {val[0]} AND {tempKey} {eq[1]} {val[1]} "
                elif val[0] is None:
                    temp = f" {tempKey} {eq[0]} {val[1]} "
                else:
                    temp = f" {tempKey} {eq[1]} {val[0]} "
            if key == 'symptom':
                pass
            if key == 'diseases':
                pass
            limits[key] = temp

        queryStr = f"SELECT "
        for col in colsName:
            queryStr += f"t.{col} AS {col}, "
            if col == 'DOB' and limits.get('age'):
                queryStr += "TIMESTAMPDIFF(YEAR, DOB, CURDATE()) AS age, "
        queryStr = queryStr[:-2] + " FROM patient as t"
        stack = ['AND'] * (len(limits) - 1) + [' WHERE']
        for val in limits.values():
            queryStr += stack.pop() + val
        queryStr = queryStr[:-1]
        queryStr += ";"
        print(queryStr)
        table = pd.DataFrame(executedQuery(queryStr))
        return table


def main():
    q = DataQueries("his_project")
    q.enqueueSymptomsTree()
    print(q.LastUpdate)
    if q.LastUpdate.days >= 1:
        q.queryTrigger()
        updateTableCarry('trigger', datetime.datetime.now().strftime('%m/%d/%Y %H:%M'))

    return q


if __name__ == "__main__":
    Queries = main()

# PatientWith_weak = Queries.queryPatientSymptoms('fatigue')
# PatientDiagnosis = Queries.queryPatientResearch(1, *list(PatientWith_weak['ID'].unique()))

Qpi = Queries.queryPatientIndices(gender='M', age=(50, 70), weight=[70, 90], symptom=None)