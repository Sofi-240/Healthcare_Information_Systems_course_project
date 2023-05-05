from app.initialization.ServerInitiation import *
import pandas as pd
import datetime
from app.communication.TrieStruct import Trie


class DataQueries:
    def __init__(self, dbName):
        self.dbName = dbName
        self.cursor, self.con = connect2serverDB(database=dbName)
        self.SymptomsTrie = Trie()
        self._enqueueSymptomsTrie()

    def _enqueueSymptomsTrie(self):
        """
            Builds and enqueues a tree of symptoms and diseases.
        """
        queryStr = f"SELECT * FROM symptomsDiseases ORDER BY Symptom;"
        diss_symptoms = executedQuery(queryStr)
        self.SymptomsTrie.build_trie(diss_symptoms)
        print('LOAD Symptoms Tree')
        print(f"Last update for patient diagnosis (trigger) Table: {self.LastUpdate}")
        checkNan = executedQuery(f"SELECT * FROM patientdiagnosis LIMIT 1;")[0][1]
        if self.LastUpdate.days >= 1 or not checkNan:
            self.queryUpdateTrigger()
        return

    @property
    def LastUpdate(self):
        """
        Calc. the difference between the current time and the last update of the patient diagnosis table.
        Returns:
            datetime.timedelta
        """
        return datetime.datetime.now() - datetime.datetime.strptime(getTableCarry('trigger'), '%m/%d/%Y %H:%M')

    @staticmethod
    def get_table(tableName):
        table = pd.DataFrame(executedQuery(f"SELECT * FROM {tableName.lower()};"))
        table.columns = getTableCarry(tableName.lower()).get('headers')
        return table

    @staticmethod
    def checkForLogIn(userPath, ID):
        ret = []
        if userPath == 'patient' or userPath == 'p':
            ret = executedQuery(f"SELECT * FROM patient WHERE ID = '{ID}';")
            if ret:
                ret = list(ret[0])
                ret += list(executedQuery(f"SELECT Symptom FROM symptomspatient WHERE ID = '{ID}';")[0])
        elif userPath == 'researcher' or userPath == 'r':
            ret = executedQuery(f"SELECT * FROM researcher WHERE ID = '{ID}';")
            if ret:
                ret = list(ret[0])
        if not ret:
            return
        return ret

    def addItem(self, key, itm):
        """
        Args:
            key (str): The key to use when adding the item to the dictionary.
            itm (Any): The item to add to the dictionary.

        Returns:
            Any: The added item.
        """
        self.__dict__[key] = itm
        return itm

    def queryUpdateTrigger(self, *IDs):
        """
        update the patient-diagnosis table based on symptom data.
        If given any IDs as arguments, only update rows with those IDs.
        Otherwise, update all rows.
        Args:
            *IDs (str): Patients IDs.

        Returns:
            None
        """

        def DiagnosisDecision(dataList):
            dataList = pd.DataFrame(dataList, columns=['disID'])
            index = dataList.loc[:, ['disID']].value_counts()
            data = dataList.groupby(['disID'])
            dec = [data.get_group(index.index[0][0])['disID'].iloc[0], index.iloc[0]]
            if index.shape[0] == 1:
                # Temporary solution for a bug --- > need to check the fks construction
                return dec + [data.get_group(index.index[0][0])['disID'].iloc[0], 0]
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
                    stack += self.SymptomsTrie.get_disID(sym.lower().split())
                if len(id_Sym) == 1 and not prev_id:
                    prev_id = ID
                if stack:
                    curr_dec = [prev_id] + DiagnosisDecision(stack)
                    curr_dec[2] /= len(stack)
                    curr_dec[-1] /= len(stack)
                    queryStr += f"{tuple(curr_dec)}, "
                    stack = []
                prev_id = ID
            if prev_id == ID:
                stack += self.SymptomsTrie.get_disID(sym.lower().split())
        queryStr = queryStr[:-2] + f" AS new(i, f, fc, s, sc) " \
                                   f"ON DUPLICATE KEY UPDATE " \
                                   f"FdisID = f, " \
                                   f"Fconf = fc, " \
                                   f"SdisID = s, " \
                                   f"Sconf = sc;"
        print(queryStr)
        executedQueryCommit(queryStr)
        updateTable('patientdiagnosis')
        print(queryStr)
        if not IDs:
            updateTableCarry('trigger', datetime.datetime.now().strftime('%m/%d/%Y %H:%M'))
        return

    def queryPatientIndices(self, **kwargs):
        """
        Queries the patient table with given conditions and returns the selected columns.

        Args:
            **kwargs: A variable-length keyword argument list, where each argument corresponds to
            a search criterion. The following search criteria are supported:
            - ID: The patient's ID
            - gender: The patient's gender
            - support: The patient's support status
            - phone: The patient's phone number
            - area: The patient's area
            - city: The patient's city
            - HMO: The patient's HMO
            - COB: The patient's country of birth
            - height: The patient's height
            - weight: The patient's weight
            - age: The patient's age (calc. from DOB)
            - symptom: The patient's symptom
            - diseases: The patient's disease
            - conf: The confidence level associated with the patient's disease diagnosis

            The values of the search criteria can be:
            - including strings (=)
            - integers (=)
            - list (>=, <=) or [iter]
            - tuple (>, <) or [iter]
            - set [iter]

        Returns:
            table (pd.DataFrame): patient table. .
        """
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

    def queryAvailableResearch(self, userPath, **kwargs):
        where_limits = {}
        join = []
        if userPath == 'r' or userPath == 'researcher':
            pass
        elif userPath == 'p' or userPath == 'patient':
            pass
        queryStr = f"SELECT "
        return

    def InsertResearch(self, researcherID, disease, *patientID):
        queryStr = f'SELECT MAX(ID) FROM activeresearch'
        newID = executedQuery(queryStr) + 1
        if type(disease) == str:
            queryStr = f'SELECT disID FROM diseases WHERE disName = {disease}'
            disID = executedQuery(queryStr)
        else:
            disID = disease
        if not patientID:
            insert2Table('activeresearch', [newID, disID, researcherID, None])
            return
        while patientID:
            insert2Table('activeresearch', [newID, disID, researcherID, patientID.pop()])
        return

    def InsertPatientToResearch(self, researchID, *patientID):
        queryStr = f'SELECT disID, rID FROM activeresearch WHERE ID = {researchID} LIMIT 1;'
        disID, rID = executedQuery(queryStr)
        while patientID:
            insert2Table('activeresearch', [researchID, disID, rID, patientID.pop()])
        return

    def insertNewSymptom(self, symptomPath, **kwargs):
        """
        Inserts a new symptom into the database.

        Args:
            symptomPath (str): A string indicating the path where the symptom should be inserted.
                Valid values are 'patient' or 'p' to insert symptom to the symptoms-patient table.,
                and 'diseases' or 'd' to insert symptom to the diseases-symptoms table.
            **kwargs:
        Returns:
            None.
        """
        if symptomPath == 'patient' or symptomPath == 'p':
            ID, symptoms = kwargs.get('ID'), kwargs.get('symptom')
            if not ID:
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
        self._enqueueSymptomsTrie()
        return

    def insertNewUser(self, userPath, **kwargs):
        """
        Inserts a new user into the database.

        Args:
            userPath (str): The type of user to add.
                    Valid values are 'patient' or 'p' for patient,
                    and 'researcher' or 'r' for researchers.
            **kwargs: A dictionary containing the column names and values for the new user record.

        Returns:
            None.
        """
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
            self.insertNewSymptom('p', ID=kwargs.get('ID'), symptom=kwargs.get('symptoms'))
        return

    def insertNewDisease(self, depName, disName, disSymptoms=None):
        """
            Inserts a new diseases into the database.

            Args:
                depName (str): The diseases department name.
                disName (str): The diseases name.
                disSymptoms (optional[list]): The diseases symptom list.
            Returns:
                None.
            """
        if disSymptoms is None:
            disSymptoms = []
        depID = executedQuery(f"SELECT depID FROM diseases WHERE depName = '{depName}' LIMIT 1;")
        if not depID:
            depID = str(int(executedQuery(f"SELECT depID FROM diseases ORDER BY depID;")[-1][0]) + 10)
            disID = depID + '00001'
            insert2Table('diseases', [disID, disName, depID, depName])
        else:
            depID = depID[0]
            disID = str(int(
                executedQuery(f"SELECT disID FROM diseases WHERE depName = '{depName}' ORDER BY disID;")[-1][0]) + 1)
            insert2Table('diseases', [disID, disName, depID, depName])
        for syp in disSymptoms:
            self.insertNewSymptom('d', disID=disID, symptom=syp)
        return

    def DeleteUser(self, userPath, ID):
        """
        Delete a new from the database.

        Args:
            userPath (str): The type of user.
                    Valid values are 'patient' or 'p' for patient,
                    and 'researcher' or 'r' for researchers.
            ID (str): User ID.

        Returns:
            None.
        """
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


def main():
    q = DataQueries("his_project")
    return q


if __name__ == "__main__":
    Queries = main()
    # patient_diagnosis = Queries.get_table('patientdiagnosis')
    # Qpi1 = Queries.queryPatientIndices(symptom='pain',
    #                                    diseases=('Bone cancer', 'Skin cancer', 'Breast cancer'),
    #                                    conf=[0.3, None],
    #                                    age=(37, None),
    #                                    weight=[60, 100])

    # Queries.insertNewUser('p', ID='320468461', gender='M', name='Nicki',
    #                       DOB=datetime.date(1999, 5, 20), area='C', city='Yavne',
    #                       phone='0502226474', HMO='Clalit', COB='Israel', height=2.1,
    #                       weight=90, support=1, symptoms=['Abdominal mass or swelling',
    #                                                       'Fatigue', 'Weight loss'])
    # Qpi2 = Queries.queryPatientIndices(ID=320468461)
    # Queries.DeleteUser('p', '320468461')

# Qpi1 = Queries.get_table('activeresearch')