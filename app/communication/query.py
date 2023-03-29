from app.initialization.ServerInitiation import *
import pandas as pd
from app.initialization.strNode import node


class DataQueries:
    def __init__(self, dbName):
        self.dbName = dbName
        self.cursor, self.con = connect2serverDB(database=dbName)
        self.SymptomsRoot = {}

    def addItem(self, key, itm):
        self.__dict__[key] = itm
        return itm

    def queryPatientDiagnosis(self, order=2, *patientIDs):
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
        self.cursor.execute(queryStr)
        SymptomsPatient_table = pd.DataFrame(self.cursor.fetchall(), columns=['ID', 'symptom'])
        ret_table = pd.DataFrame(columns=['ID', 'order', 'disID', 'disName', 'depID'])
        p, r, prevID = 0, 0, ''
        diseases_table = Queries.getTable('diseases').groupby(['disID'])
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
        return ret_table

    def getTable(self, tableName):
        queryStr = f"SELECT * FROM {tableName.lower()};"
        self.cursor.execute(queryStr)
        res = self.cursor.fetchall()
        print('getTable:\n', queryStr)
        colslStr = f"SELECT " \
                   f"COLUMN_NAME " \
                   f"FROM " \
                   f"INFORMATION_SCHEMA.COLUMNS " \
                   f"WHERE " \
                   f"TABLE_SCHEMA = '{self.dbName}'" \
                   f"AND TABLE_NAME = '{tableName.lower()}';"
        self.cursor.execute(colslStr)
        temp = self.cursor.fetchall()
        colsName = [t[0] for t in temp]
        table = pd.DataFrame(res, columns=colsName)
        return table

    def enqueueSymptomsTree(self):
        table = self.getTable('symptomsDiseases')
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
            return
        dig = []
        for key, child in curr_node.children.items():
            if not child.children:
                dig.append(key)
        return dig

    def queryPatientSymptoms(self, symptom):
        collStr = f"SELECT " \
                   f"COLUMN_NAME " \
                   f"FROM " \
                   f"INFORMATION_SCHEMA.COLUMNS " \
                   f"WHERE " \
                   f"TABLE_SCHEMA = '{self.dbName}'" \
                   f"AND TABLE_NAME = '{'patient'}';"
        self.cursor.execute(collStr)
        temp = self.cursor.fetchall()
        colsName = [t[0] for t in temp]
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
        self.cursor.execute(queryStr)
        table = pd.DataFrame(self.cursor.fetchall(), columns=colsName + ['symptom'])
        return table


def main():
    q = DataQueries("his_project")
    return q


if __name__ == "__main__":
    Queries = main()

PatientWithPain = Queries.queryPatientSymptoms('pain')
PatientDiagnosis = Queries.queryPatientDiagnosis(1, *list(PatientWithPain['ID'].unique()))
