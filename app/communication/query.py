from app.initialization.ServerInitiation import *
import pandas as pd
import datetime
from app.communication.strNode import node


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
        queryStr = f"SELECT * FROM symptomsDiseases;"
        id_Sym = executedQuery(queryStr)
        for tip, txt in id_Sym:
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

    def queryUpdateTrigger(self, *IDs):
        def DiagnosisDecision(dataList):
            dataList = pd.DataFrame(dataList, columns=['disID'])
            index = dataList.loc[:, ['disID']].value_counts()
            data = dataList.groupby(['disID'])
            dec = [data.get_group(index.index[0][0])['disID'].iloc[0], index.iloc[0]]
            if index.shape[0] == 1:
                return dec + ['', 0]
            dec += [data.get_group(index.index[1][0])['disID'].iloc[0], index.iloc[1]]
            return dec

        print('UPDATE Trigger table')
        queryStr = f"SELECT * FROM symptomspatient"
        if IDs:
            if len(IDs) == 1:
                queryStr += f" WHERE ID = {IDs[0]}"
            else:
                queryStr += f" WHERE ID IN {IDs}"
        queryStr += " ORDER BY ID;"
        print(queryStr)
        id_Sym = executedQuery(queryStr)
        prev_id = ''
        stack = []
        counter = 0
        queryStr = f"INSERT INTO patientdiagnosis (ID, FdisID, Fconf, SdisID, Sconf) VALUES "
        for ID, sym in id_Sym:
            counter += 1
            if ID != prev_id or counter == len(id_Sym):
                if counter == len(id_Sym):
                    stack += self.getDiagnosis(sym)
                if stack:
                    curr_dec = [ID] + DiagnosisDecision(stack)
                    curr_dec[2] /= len(stack)
                    curr_dec[-1] /= len(stack)
                    queryStr += f"{tuple(curr_dec)}, "
                    stack = []
                prev_id = ID
            if ID == prev_id:
                stack += self.getDiagnosis(sym)
        queryStr = queryStr[:-2] + f" ON DUPLICATE KEY UPDATE " \
                                   f" FdisID = FdisID, " \
                                   f"Fconf = Fconf, " \
                                   f"SdisID = SdisID, " \
                                   f"Sconf = Sconf;"
        print(queryStr)
        executedQueryCommit(queryStr)
        updateTable('patientdiagnosis')
        if not IDs:
            updateTableCarry('trigger', datetime.datetime.now().strftime('%m/%d/%Y %H:%M'))
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

    def insertNewSymptom(self, symptomPath, **kwargs):
        if symptomPath == 'patient' or symptomPath == 'p':
            ID, symptoms = kwargs.get('ID'), kwargs.get('symptom')
            if ID:
                print("Missing ID column")
                return
            if not symptoms:
                print("No symptoms where given")
                return
            for syp in symptoms:
                insert2Table('symptomsPatient', [ID, syp])
            self.queryUpdateTrigger(ID)
            return
        if symptomPath == 'diseases' or symptomPath == 'd':
            disID, symptoms = kwargs.get('disID'), kwargs.get('symptom')
            if symptoms:
                print("No symptoms where given")
                return
            if not disID:
                disName = kwargs.get('disName')
                if not disName:
                    print('No disease ID entered')
                    return
                disID = executedQuery(f"SELECT disID FROM diseases WHERE disName = '{disName}';")
                if disID:
                    disID = disID[0]
                else:
                    print(f'The {disName} disease is not registered in the database')
                    return
            for syp in symptoms:
                insert2Table('symptomsdiseases', [disID, syp])
        self.enqueueSymptomsTree()
        return

    def insertNewUser(self, userPath, **kwargs):
        if userPath == 'patient' or userPath == 'p':
            cols = getTableCarry('patient').get('headers')
            tableName = 'patient'
        elif userPath == 'researcher' or userPath == 'r':
            cols = getTableCarry('researcher').get('headers')
            tableName = 'researcher'
        else:
            print(f"User Path {userPath} is not valid")
            return
        values = []
        for col in cols:
            val = kwargs.get(col)
            if val is None and val != 'support':
                print(f"column named {col} is missing")
                return
            if col == 'support' and val is None:
                val = 0
            if col == 'ID':
                if executedQuery(f"SELECT * FROM {tableName} WHERE ID = '{val}';"):
                    print(f"The user with {val} ID exists in the system")
                    return
            if col == 'USRname':
                if executedQuery(f"SELECT * FROM {tableName} WHERE USRname = '{val}';"):
                    print(f"The username {val} exists in the system")
                    return
            values.append(val)
        insert2Table(tableName, values)
        if tableName == 'patient' and kwargs.get('symptoms'):
            self.insertNewPatienSymptoms('p', ID=kwargs.get('ID'), symptom=kwargs.get('symptoms'))
        return

    def DeleteUser(self, userPath, ID):
        if userPath == 'patient' or userPath == 'p':
            tables = [('symptomsPatient', 'ID'),
                      ('patientdiagnosis', 'ID'),
                      ('activeresearch', 'pID'),
                      ('patient', 'ID')]
        elif userPath == 'researcher' or userPath == 'r':
            tables = [('activeresearch', 'rID'),
                      ('researcher', 'ID')]
        else:
            print(f"User Path {userPath} is not valid")
            return
        for t, v in tables:
            queryStr = f"DELETE FROM {t} WHERE {v} = '{ID}';"
            print(queryStr)
            executedQueryCommit(queryStr)
        return

    def insertNewDisease(self, depName, disName, disSymptoms=None):
        if disSymptoms is None:
            disSymptoms = []
        depID = executedQuery(f"SELECT depID FROM diseases WHERE depName = '{depName}' LIMIT 1;")
        if not depID:
            depID = str(int(executedQuery(f"SELECT depID FROM diseases ORDER BY depID;")[-1][0]) + 10)
            disID = depID + '00001'
            insert2Table('diseases', [disID, disName, depID, depName])
        else:
            depID = depID[0]
            disID = str(int(executedQuery(f"SELECT disID FROM diseases WHERE depName = '{depName}' ORDER BY disID;")[-1][0]) + 1)
            insert2Table('diseases', [disID, disName, depID, depName])
        for syp in disSymptoms:
            self.insertNewSymptom('d', disID=disID, symptom=syp)
        return


def main():
    q = DataQueries("his_project")
    q.enqueueSymptomsTree()
    print(f"Last update for patient diagnosis (trigger) Table: {q.LastUpdate}")
    if q.LastUpdate.days >= 1:
        q.queryUpdateTrigger()
    return q


if __name__ == "__main__":
    Queries = main()


# Queries.insertNewDisease('dd', 'e', [])


# Qpi = Queries.queryPatientIndices(gender='F',
#                                   symptom='pain',
#                                   diseases=('Bone cancer', 'Skin cancer'),
#                                   conf=[0.3, None],
#                                   age=[42, None])

# Queries.getDiagnosis('in')
# Queries.queryUpdateTrigger()

# Queries.DeletePatient('320465461')
# ret = Queries.insertNewPatient('320465461', 'M', 'Nicki', datetime.date(1999, 5, 20), 'C',
#                          'Yavne', '0502226474', 'Clalit', 'Israel', 2.1, 90, 1, ['lower back pain'])
# Qpi = Queries.queryPatientIndices(ID=113910790)
# ret = Queries.insertNewUser('p', ID='113910790')
