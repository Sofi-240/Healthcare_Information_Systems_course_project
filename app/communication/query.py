import json
import os
from app.initialization.serverInitiation import *
import pandas as pd
import datetime
from app.communication.trieStruct import Trie


class DataQueries:
    def __init__(self, dbName, app):
        self.dbName = dbName
        self.panel = app
        self.cursor, self.con = connect2serverDB(database=dbName)
        self.SymptomsTrie = Trie()
        self._enqueueSymptomsTrie()
        self.UserIndices = {}
        self.activeUser = None
        self.activeUserName = None

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

    def activateLogIn(self, userPath, userID, userName):
        showFrame = True
        if userPath == 'active' and self.UserIndices:
            userPath = self.activeUser
            userID = self.UserIndices['Indices'].iloc[0, :]['ID']
            userName = self.activeUserName
            showFrame = False
        if userPath == 'active':
            return
        UserIndices = {}
        frameName = ''
        if userPath == 'patient' or userPath == 'p':
            temp = executedQuery(f"SELECT * FROM patient WHERE ID = '{userID}';")
            if not temp:
                return 'ID'
            UserIndices['Indices'] = pd.DataFrame(temp, columns=getTableCarry('patient').get('headers'))
            if userName.lower() != UserIndices['Indices'].iloc[0, :]['name'].lower():
                return 'name'
            symptoms = list(executedQuery(f"SELECT Symptom FROM symptomspatient WHERE ID = '{userID}';"))
            UserIndices['symptoms'] = []
            for symp in symptoms:
                UserIndices['symptoms'].append(symp[0])
            UserIndices['availableResearch'] = self.queryAvailableResearchValues('p', ID=userID)
            queryStr = f"SELECT d.ID, d.rID, r.Fname, r.Lname, r.phone, r.Mail FROM activeresearch AS d" \
                       f" INNER JOIN researcher AS r ON r.ID = d.rID WHERE d.pID = '{userID}';"
            researchers = pd.DataFrame(list(executedQuery(queryStr)), columns=['researchID', 'researcherID', 'Fname', 'Lname', 'Phone',
                                                'Mail'])
            UserIndices['researchers'] = researchers
            print(f'Patient Entry, ID: {userID}. Name {userName}')
            frameName = 'PatientMainPanel'
        elif userPath == 'researcher' or userPath == 'r':
            temp = executedQuery(f"SELECT * FROM researcher WHERE ID = '{userID}';")
            if not temp:
                return 'ID'
            UserIndices['Indices'] = pd.DataFrame(temp, columns=getTableCarry('researcher').get('headers'))
            if userName.lower() != UserIndices['Indices'].iloc[0, :]['Fname'].lower():
                return 'Fname'
            queryStr = f"SELECT ar.ID, d.depName, d.disName, ar.pID FROM activeresearch AS ar" \
                       f" INNER JOIN diseases AS d ON ar.disID = d.disID WHERE ar.rID = '{userID}';"
            researchers = pd.DataFrame(list(executedQuery(queryStr)),
                                       columns=['ResearchID', 'Type Of Dis', 'DisName', 'PatientID'])
            UserIndices['researchers'] = researchers
            UserIndices['availablePatients'] = self.queryAvailableResearchValues('r', ID=userID)
            print(f'Researcher Entry, ID: {userID}. Name {userName}')
            frameName = 'ResearcherMainPanel'
            self.addItem('diseases', self.get_table('diseases'))
        if not frameName:
            return False
        self.UserIndices = UserIndices
        self.activeUser = userPath[0].lower()
        self.activeUserName = userName
        if showFrame:
            self.panel.show_frame(frameName)
        return True

    def dequeueUserIndices(self, call):
        if not self.UserIndices:
            return
        if call == 'PatientMainPg0':
            return {'Indices': dict(self.UserIndices['Indices'].iloc[0, :]), 'researchers': self.UserIndices['researchers']}
        if call == 'PatientMainPg1':
            return self.UserIndices.get('symptoms')
        if call == 'PatientMainPg2':
            return self.UserIndices.get('availableResearch')
        if call == 'ResearcherMainPg0':
            return {'Indices': dict(self.UserIndices['Indices'].iloc[0, :]), 'researchers': self.UserIndices['researchers']}
        if call == 'ResearcherMainPg1':
            if self.__dict__.get('diseases') is None:
                return self.addItem('diseases', self.get_table('diseases'))
            return self.__dict__.get('diseases')
        if call == 'ResearcherMainPg2':
            return self.UserIndices.get('availablePatients')
        if call == 'ResearcherMainPg4':
            return self.UserIndices.get('symptomsDiseases')

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
        if not id_Sym[0]:
            return
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

        Returns:
            table (pd.DataFrame): patient table. .
        """
        where_limits = {}
        join = []
        colsName = getTableCarry('patient').get('headers')
        for key, val in kwargs.items():
            if key in ['ID', 'gender', 'support', 'phone', 'area', 'HMO', 'COB']:
                if (type(val) == set or type(val) == tuple or type(val) == list) and len(val) > 1:
                    temp = f" {key} IN {tuple(val)} "
                else:
                    if type(val) == set or type(val) == tuple or type(val) == list:
                        temp = f" {key} = '{val[0]}' "
                    else:
                        temp = f" {key} = '{val}' "
                where_limits[key] = temp
            if key in ['height', 'weight', 'age']:
                tempKey = key
                if key == 'age':
                    tempKey = 'TIMESTAMPDIFF(YEAR, DOB, CURDATE())'
                eq = ('>=', '<=')
                if val[0] is not None and val[1] is not None:
                    temp = f" {tempKey} {eq[0]} {val[0]} AND {tempKey} {eq[1]} {val[1]} "
                elif val[0] is not None:
                    temp = f" {tempKey} {eq[0]} {val[0]} "
                elif val[1] is not None:
                    temp = f" {tempKey} {eq[1]} {val[1]} "
                else:
                    temp = None
                if temp is not None:
                    where_limits[key] = temp
            if key == 'symptoms' and val:
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
            if key == 'disName':
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
        return pd.DataFrame(executedQuery(queryStr), columns=colsName)

    def queryAvailableResearchValues(self, userPath, **kwargs):
        ID = kwargs.get('ID')
        if not ID:
            print("Missing ID column")
            return
        if userPath == 'r' or userPath == 'researcher':
            if kwargs.get('researchers'):
                researchers = kwargs.get('researchers')
            else:
                queryStr = f"SELECT ar.ID, d.depName, d.disName, ar.pID FROM activeresearch AS ar" \
                           f" INNER JOIN diseases AS d ON ar.disID = d.disID WHERE ar.rID = '{ID}';"
                researchers = pd.DataFrame(list(executedQuery(queryStr)),
                                           columns=['ResearchID', 'Type Of Dis', 'DisName', 'PatientID'])
            if researchers.empty:
                return pd.DataFrame(columns=['patientID', 'patientName', 'patientPhone', 'researchID'])
            path = os.path.join(
                os.path.split(os.path.dirname(__file__))[0], 'initialization', 'searchHashFile.txt'
            )
            fileDict = json.loads(
                open(
                    path, 'r'
                ).read()
            )
            availablePatients = []
            for i in list(researchers['ResearchID'].unique()):
                researchHash = fileDict.get(str(i))
                if not researchHash:
                    continue
                avlPatient = self.queryPatientIndices(**researchHash)
                if avlPatient.empty:
                    continue
                avlPatient = avlPatient.loc[:, ['ID', 'name', 'phone']]
                avlPatient['researchID'] = i
                availablePatients.append(avlPatient)

            if not availablePatients:
                return pd.DataFrame(columns=['patientID', 'patientName', 'patientPhone', 'researchID'])
            availablePatients = pd.concat(availablePatients, axis=0)
            availablePatients.columns = ['patientID', 'patientName', 'patientPhone', 'researchID']
            return availablePatients
        elif userPath == 'p' or userPath == 'patient':
            queryStr = f"SELECT d.ID, d.rID, r.Fname, r.Lname, r.phone, r.Mail FROM activeresearch AS d" \
                       f" INNER JOIN researcher AS r ON r.ID = d.rID WHERE " \
                       f"d.disID = (SELECT FdisID FROM patientdiagnosis WHERE ID = '{ID}') OR " \
                       f"d.disID = (SELECT SdisID FROM patientdiagnosis WHERE ID = '{ID}'); "
            researchers = list(executedQuery(queryStr))
            availableResearch = pd.DataFrame(researchers,
                                             columns=['researchID', 'researcherID', 'Fname', 'Lname', 'Phone', 'Mail'])
            return availableResearch
        return

    def querySymptomsDiseases(self, disName):
        disName = disName
        if not disName:
            print("Missing disName column")
            return
        queryStr = f"SELECT s.Symptom FROM symptomsdiseases AS s" \
                   f" INNER JOIN diseases AS d ON s.disID = d.disID" \
                   f" WHERE d.disName = '{disName}';"

        symptoms = list(executedQuery(queryStr))
        return symptoms

    def insertResearch(self, researcherID, **researchHash):
        if researcherID == 'active' and self.UserIndices:
            researcherID = self.UserIndices['Indices'].iloc[0, :]['ID']
        if researcherID == 'active':
            return
        disName = researchHash.get('disName')
        newID = int(executedQuery(f'SELECT MAX(ID) FROM activeresearch;')[0][0]) + 1
        if not disName:
            disID = None
        else:
            queryStr = f"SELECT disID FROM diseases WHERE disName = '{disName}';"
            print(queryStr)
            disID = executedQuery(queryStr)[0][0]
        path = os.path.join(
            os.path.split(os.path.dirname(__file__))[0], 'initialization', 'searchHashFile.txt'
        )
        fileDict = json.loads(
            open(
                path, 'r'
            ).read()
        )
        fileDict[str(newID)] = researchHash

        open(
            path, 'w'
        ).write(
            json.dumps(fileDict)
        )
        insert2Table('activeresearch', [newID, disID, researcherID, None])
        return

    def insertPatientToResearch(self, researchID, *patientID):
        queryStr = f'SELECT disID, rID FROM activeresearch WHERE ID = {researchID} LIMIT 1;'
        disID, rID = executedQuery(queryStr)
        while patientID:
            insert2Table(
                'activeresearch', [
                    researchID, disID, rID, patientID.pop()
                ]
            )
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
        if symptomPath == 'active' and self.UserIndices:
            symptomPath = self.activeUser
            kwargs['ID'] = self.UserIndices['Indices'].iloc[0, :]['ID']
        if symptomPath == 'active':
            return
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
            disID, symptoms, disName = kwargs.get('disID'), kwargs.get('symptom'), kwargs.get('disName')
            print(f'The {disID} disease {symptoms} is ')
            if symptoms is None:
                print("No symptoms where given")
                return
            if disID is None:
                if not disName:
                    print('No disease ID entered')
                    return
                disName = disName[0]
                disID = str(int(executedQuery(f"SELECT disID FROM diseases WHERE disName = '{disName}';")[-1][0]))
                if not disID:
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
            return False
        values = []
        for col in cols:
            val = kwargs.get(col)
            if val is None and val != 'support':
                print(f"column named {col} is missing")
                return False
            if col == 'support' and val is None:
                val = 0
            if col == 'ID':
                if executedQuery(f"SELECT * FROM {tableName} WHERE ID = '{val}';"):
                    print(f"The user with {val} ID exists in the system")
                    return True
            if col == 'USRname':
                if executedQuery(f"SELECT * FROM {tableName} WHERE USRname = '{val}';"):
                    print(f"The username {val} exists in the system")
                    return True
            values.append(val)
        insert2Table(tableName, values)
        if tableName == 'patient' and kwargs.get('symptoms'):
            self.insertNewSymptom('p', ID=kwargs.get('ID'), symptom=kwargs.get('symptoms'))
        if tableName == 'patient' and kwargs.get('ExLogIn'):
            return self.activateLogIn(userPath, kwargs.get('ID'), kwargs.get('name'))
        if tableName == 'researcher' and kwargs.get('ExLogIn'):
            return self.activateLogIn(userPath, kwargs.get('ID'), kwargs.get('Fname'))
        return True

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
        depID = str(
            int(
                executedQuery(f"SELECT depID FROM diseases WHERE depName = '{depName}';")[-1][0]
            )
        )
        disID = str(int(
            executedQuery(
                f"SELECT disID FROM diseases WHERE depName = '{depName}' ORDER BY disID;")[-1][0]
            ) + 1)
        insert2Table('diseases', [disID, disName, depID, depName])
        for syp in disSymptoms:
            self.insertNewSymptom('d', disID=disID, symptom=syp)
        return

    def deleteUser(self, userPath, ID):
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
        if userPath == 'active' and self.UserIndices:
            userPath = self.activeUser
            ID = self.UserIndices['Indices'].iloc[0, :]['ID']
        if userPath == 'active':
            return
        if userPath == 'patient' or userPath == 'p':
            tables = [('symptomsPatient', 'ID'),
                      ('patientdiagnosis', 'ID'),
                      ('activeresearch', 'pID'),
                      ('patient', 'ID')]
        elif userPath == 'researcher' or userPath == 'r':
            tables = [('activeresearch', 'rID'),
                      ('researcher', 'ID')]
            queryStr = f"SELECT ID FROM activeresearch WHERE rID = {ID}"
            researchers = list(executedQuery(queryStr))
            path = os.path.join(
                os.path.split(os.path.dirname(__file__))[0], 'initialization', 'searchHashFile.txt'
            )
            fileDict = json.loads(
                open(
                    path, 'r'
                ).read()
            )
            for rID in researchers:
                if fileDict.get(str(rID[0])):
                    fileDict.pop(str(rID[0]))
            open(
                path, 'w'
            ).write(
                json.dumps(fileDict)
            )

        else:
            print(f"User Path {userPath} is not valid")
            return
        for t, v in tables:
            queryStr = f"DELETE FROM {t} WHERE {v} = '{ID}';"
            print(queryStr)
            executedQueryCommit(queryStr)
        return

    def updateUserIndices(self, userPath, ID, **kwargs):
        if userPath == 'active' and self.UserIndices:
            userPath = self.activeUser
            ID = self.UserIndices['Indices'].iloc[0, :]['ID']
        if userPath == 'active':
            return False
        if userPath == 'patient' or userPath == 'p':
            cols = getTableCarry('patient').get('headers')
            tableName = 'patient'
        elif userPath == 'researcher' or userPath == 'r':
            cols = getTableCarry('researcher').get('headers')
            tableName = 'researcher'
        else:
            print(f"User Path {userPath} is not valid")
            return False
        queryStr = f"UPDATE {tableName} SET"
        newSet = False
        for key, val in kwargs.items():
            if key in cols:
                newSet = True
                queryStr += f" {key} = '{val}',"
        if not newSet:
            return True
        queryStr = queryStr[:-1]
        queryStr += f' WHERE ID = {ID};'
        print(queryStr)
        executedQueryCommit(queryStr)
        return True

    def deletePatientSymptom(self, ID, *symptoms):
        if ID == 'active' and self.UserIndices:
            ID = self.UserIndices['Indices'].iloc[0, :]['ID']
        if ID == 'active':
            return
        if not symptoms:
            return
        for symp in symptoms:
            queryStr = f"DELETE FROM symptomsPatient WHERE ID = '{ID}' AND Symptom LIKE '%{symp}%';"
            print(queryStr)
            executedQueryCommit(queryStr)
        self.queryUpdateTrigger(ID)
        return


