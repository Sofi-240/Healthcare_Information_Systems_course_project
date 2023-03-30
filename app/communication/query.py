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
        return

    def queryPatientResearch(self, order=2, *patientIDs):
        def DiagnosisDecision(data, n=order):
            index = data.loc[:, ['disID']].value_counts()
            index = index.index[:min([n, index.shape[0]])].values.tolist()
            data = data.groupby(['disID'])
            curr_ord = 1
            dec = []
            while index:
                dec += [[curr_ord] + list(data.get_group(index.pop(0)[0]).iloc[0, :][['disID', 'disName', 'depID']])]
                curr_ord += 1
            return dec

        queryStr = f"SELECT t1.* FROM symptomspatient t1 " \
                   f"INNER JOIN patient t2 " \
                   f"ON t1.ID = t2.ID"
        if not patientIDs:
            queryStr += f";"
        elif len(patientIDs) == 1:
            queryStr += f" WHERE t2.ID = {patientIDs[0]};"
        else:
            queryStr += f" WHERE t2.ID IN {patientIDs};"
        print('queryPatientDiagnosis:\n', queryStr)
        SymptomsPatient_table = pd.DataFrame(executedQuery(queryStr), columns=['ID', 'symptom'])
        ret_table = pd.DataFrame(columns=['ID', 'order', 'disID', 'disName', 'depID'])
        p, r, prevID = 0, 0, ''
        diseases_table = Queries.queryTable('diseases').groupby(['disID'])
        stack = pd.DataFrame(columns=['symptom', 'disID', 'disName', 'depID'])
        for i in SymptomsPatient_table.index:
            curr_ID = SymptomsPatient_table.loc[i, 'ID']
            if not prevID:
                prevID = curr_ID
            if prevID and curr_ID != prevID:
                temp = DiagnosisDecision(stack)
                while temp:
                    ret_table.loc[p, :] = [prevID] + temp.pop(0)
                    p += 1
                stack = pd.DataFrame(columns=['symptom', 'disID', 'disName', 'depID'])
                r = 0
                prevID = curr_ID

            full_dig = Queries.getDiagnosis(SymptomsPatient_table.loc[i, 'symptom'])
            for d in full_dig:
                stack.loc[r, 'symptom'] = SymptomsPatient_table.loc[i, 'symptom']
                stack.loc[r, 'disID'] = d
                stack.loc[r, ['disName', 'depID']] = diseases_table.get_group(d).iloc[0][['disName', 'depID']]
                r += 1
        temp = DiagnosisDecision(stack)
        while temp:
            ret_table.loc[p, :] = [prevID] + temp.pop(0)
            p += 1
        self.addItem('PatientResearch', ret_table)
        return ret_table

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
        queryStr = queryStr[:-1] + ";"
        print(queryStr)
        table = pd.DataFrame(executedQuery(queryStr))
        return table


def main():
    q = DataQueries("his_project")
    q.enqueueSymptomsTree()
    if q.LastUpdate.days >= 1:
        pass
    return q


if __name__ == "__main__":
    Queries = main()

# PatientWith_weak = Queries.queryPatientSymptoms('fatigue')
# PatientDiagnosis = Queries.queryPatientResearch(1, *list(PatientWith_weak['ID'].unique()))

Qpi = Queries.queryPatientIndices(gender='M', age=(50, 70), weight=[70, 90])
