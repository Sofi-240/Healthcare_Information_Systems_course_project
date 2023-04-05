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

    @staticmethod
    def queryTable(tableName):
        queryStr = f"SELECT * FROM {tableName.lower()};"
        res = executedQuery(queryStr)
        print('getTable:\n', queryStr)
        colsName = getTableCarry(tableName.lower())
        if colsName:
            colsName = colsName.get('headers')
        else:
            colsName = list(range(len(res[0])))
        table = pd.DataFrame(res, columns=colsName)
        return table

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
        trigger_table_stack = []
        SymptomsPatient_table = pd.DataFrame(executedQuery(queryStr), columns=['ID', 'symptom']).groupby(['ID'])
        for key, df in SymptomsPatient_table:
            stack = []
            for i in df.index:
                stack += self.getDiagnosis(df.loc[i, 'symptom'])
            trigger_table_stack.append([df.loc[0, 'ID']] + DiagnosisDecision(stack))
            trigger_table_stack[-1][2] /= df.shape[0]
            trigger_table_stack[-1][-1] /= df.shape[0]
        trigger_table = pd.DataFrame(trigger_table_stack,
                                     columns=["ID", "FdisID", "Fconf", "SdisID", "Sconf"])
        createFullTable(Table('patientdiagnosis', data=trigger_table,
                              pks=['ID'],
                              fks=[['ID'], ['FdisID'], ['SdisID']],
                              refs=[['ID'], ['disID'], ['disID']],
                              ref_tables=['patient', 'diseases', 'diseases']).save())
        self.addItem('patientdiagnosis', trigger_table)
        return

    def queryPatientIndices(self, **kwargs):
        where_limits = {}
        join = []
        colsName = getTableCarry('patient').get('headers')
        for key, val in kwargs.items():
            if key in ['ID', 'gender', 'support', 'phone', 'area', 'city', 'HMO', 'COB']:
                if type(val) == set or type(val) == tuple or type(val) == list:
                    temp = f" {key} IN {val} "
                else:
                    temp = f" {key} = '{val}' "
                where_limits[key] = temp
            if key in ['height', 'weight', 'age']:
                tempKey = key
                if key == 'age':
                    tempKey = 'TIMESTAMPDIFF(YEAR, DOB, CURDATE())'
                if type(val) == list:
                    eq = ('>=', '<=')
                elif type(val) == tuple:
                    eq = ('>', '<')
                else:
                    if val < 0:
                        eq = '<>'
                        val = abs(val)
                    else:
                        eq = '='
                if type(eq) == tuple:
                    if val[0] is not None and val[1] is not None:
                        temp = f" {tempKey} {eq[0]} {val[0]} AND {tempKey} {eq[1]} {val[1]} "
                    elif val[0] is None:
                        temp = f" {tempKey} {eq[1]} {val[1]} "
                    else:
                        temp = f" {tempKey} {eq[0]} {val[0]} "
                else:
                    temp = f" {tempKey} {eq} {val} "
                where_limits[key] = temp
            if key == 'symptom':
                colName = ['symptom']
                joinCol = f"t1.Symptom AS symptom, "
                joinStr = f"INNER JOIN (SELECT d1.Symptom, d1.ID FROM symptomspatient as d1 "
                if type(val) == set or type(val) == tuple or type(val) == list:
                    joinStr += f"WHERE d1.Symptom LIKE '%{val[0]}%' "
                    for v in val[1:]:
                        joinStr += f"OR d1.Symptom LIKE '%{v}%' "
                    joinStr = joinStr[:-1] + ") "
                else:
                    joinStr += f"WHERE d1.Symptom LIKE '%{val}%') "
                pass
                joinStr += f"AS t1 " \
                           f"ON t.ID = t1.ID "
                join.append([colName, joinCol, joinStr])
            if key == 'diseases':
                colName = ['disName', 'conf']
                joinCol = f"t2.disName AS disName, t2.conf AS conf, "
                joinStr = f"INNER JOIN (SELECT d1.disName, d2.ID, " \
                          f"CASE WHEN d2.FdisID = d1.disID THEN d2.Fconf " \
                          f"ELSE d2.Sconf END AS conf " \
                          f"FROM diseases AS d1 " \
                          f"INNER JOIN patientdiagnosis AS d2 ON d1.disID = d2.FdisID " \
                          f"OR d1.disID = d2.SdisID " \
                          f"WHERE d1.disName "
                if type(val) == set or type(val) == tuple or type(val) == list:
                    joinStr += f"IN {val}) "
                else:
                    joinStr += f"= '{val}') "
                joinStr += f"AS t2 " \
                           f"ON t.ID = t2.ID "
                join.append([colName, joinCol, joinStr])
                if kwargs.get('conf'):
                    conf = kwargs.get('conf')
                    if type(conf) == list:
                        eq = ('>=', '<=')
                    elif type(conf) == tuple:
                        eq = ('>', '<')
                    else:
                        if conf < 0:
                            eq = '<>'
                            conf = abs(conf)
                        else:
                            eq = '='
                    if type(eq) == tuple:
                        if conf[0] is not None and conf[1] is not None:
                            temp = f" conf {eq[0]} {conf[0]} AND conf {eq[1]} {conf[1]} "
                        elif val[0] is None:
                            temp = f" conf {eq[1]} {conf[1]} "
                        else:
                            temp = f" conf {eq[0]} {conf[0]} "
                    else:
                        temp = f" conf {eq} {conf} "
                    where_limits['conf'] = temp

        queryStr = f"SELECT "
        ret_cols = []
        while colsName:
            col = colsName.pop(0)
            queryStr += f"t.{col} AS {col}, "
            ret_cols.append(col)
            if col == 'DOB' and where_limits.get('age'):
                queryStr += "TIMESTAMPDIFF(YEAR, DOB, CURDATE()) AS age, "
                ret_cols.append('age')
        for curr_join in join:
            for col in curr_join[0]:
                ret_cols.append(col)
            queryStr += curr_join[1]
        colsName, ret_cols = ret_cols, colsName
        queryStr = queryStr[:-2] + " FROM patient as t "
        for curr_join in join:
            queryStr += curr_join[2]
        stack = ['AND'] * (len(where_limits) - 1) + ['WHERE']
        for val in where_limits.values():
            queryStr += stack.pop() + val
        queryStr = queryStr[:-1]
        queryStr += ";"
        print(queryStr)
        table = pd.DataFrame(executedQuery(queryStr), columns=colsName)
        return self.addItem('patientIndices', table)

    def insertNewPatienSymptoms(self, ID, symptoms):
        for syp in symptoms:
            insert2Table('symptomsPatient', [ID, syp])
        return

    def insertNewPatient(self, ID, gender, name, dob, area, city, phone, hmo, cob, height, weight, support, symptoms):
        values = [ID, gender, name, dob, area, city, phone, hmo, cob, height, weight, support]
        insert2Table('patient', values)
        self.insertNewPatienSymptoms(ID, symptoms)
        return

    def DeletePatient(self, ID):
        for t, v in [('symptomsPatient', 'ID'), ('patientdiagnosis', 'ID'), ('activeresearch', 'pID'), ('patient', 'ID')]:
            DeleteRow(t, v, ID)
        return

def main():
    q = DataQueries("his_project")
    q.enqueueSymptomsTree()
    print(f"Last update for patient diagnosis Table: {q.LastUpdate}")
    if q.LastUpdate.days >= 1:
        q.queryTrigger()
        updateTableCarry('trigger', datetime.datetime.now().strftime('%m/%d/%Y %H:%M'))

    return q


if __name__ == "__main__":
    Queries = main()

# Qpi = Queries.queryPatientIndices(gender='F',
#                                   symptom='pain',
#                                   diseases=('Bone cancer', 'Skin cancer'),
#                                   conf=[0.3, None],
#                                   age=[42, None])


# Queries.DeletePatient('320465461')
# Queries.insertNewPatient('320465461', 'M', 'Nicki', datetime.date(1999, 5, 20), 'C',
#                          'Yavne', '0502226474', 'Clalit', 'Israel', 2.1, 90, 1, ['lower back pain'])
# Qpi = Queries.queryPatientIndices(ID=320465461)