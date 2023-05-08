from app.initialization.ServerInitiation import getTableCarry
import datetime


class insert2DB:
    def __init__(self, panel):
        self.panel = panel
        self.activeUser = None
        self.activeUserVals = {}
        self.activeUserID = None

    @staticmethod
    def HandelFiled(EntryName, txt):
        if txt and txt == EntryName and EntryName != 'COB':
            return False
        if EntryName == 'ID':
            if not txt or (txt and (len(txt) < 9 or len(txt) > 9)):
                return False
            return True
        if EntryName == 'Name':
            if not txt or (txt and len(txt) < 2):
                return False
            return True
        if EntryName == 'Phone':
            if not txt or (txt and (len(txt) < 10 or len(txt) > 10)):
                return False
            return True
        if EntryName == 'DOB':
            today = datetime.date.today()
            if today.year - txt.year - ((today.month, today.day) < (txt.month, txt.day)) < 18:
                return False
            return True
        if EntryName == 'Weight':
            if not txt:
                return False
            try:
                digit = float(txt)
            except ValueError:
                digit = 0
            if digit <= 0:
                return False
            return True
        if EntryName == 'Height':
            if not txt:
                return False
            try:
                digit = float(txt)
            except ValueError:
                digit = 0
            if digit <= 0:
                return False
            return True
        if EntryName == 'Gender':
            if not txt:
                return False
            return True
        if EntryName == 'Area':
            if not txt:
                return False
            return True
        if EntryName == 'City':
            if not txt:
                return False
            return True
        if EntryName == 'HMO':
            if not txt:
                return False
            return True
        if EntryName == 'Support':
            if not txt:
                return False
            return True
        return True

    def validPatientSignIn(self):
        index = self.panel.frame.Page_Frames.index(self.panel.frame.Page_Frames.select())
        if index == 0:
            errCache = False
            for val, item in self.panel.frame.pg0.__dict__.items():
                if len(val) > 10 and val[:10] == 'Entry_User':
                    if val[10:] != 'DOB':
                        txt = item.get()
                    else:
                        txt = item.get_date()
                    if not self.HandelFiled(val[10:], txt):
                        self.panel.frame.pg0.raiseError(val[10:])
                        errCache = True
                    else:
                        self.panel.frame.pg0.deleteError(val[10:])
            if errCache:
                print(errCache)
                self.panel.frame.Page_Frames.tab(1, state="normal")
                self.panel.frame.Page_Frames.select(1)
                return
            self.panel.frame.Page_Frames.tab(1, state="normal")
            self.panel.frame.Page_Frames.select(1)
            return
        if index == 1:
            return self.pushNewPatient()
        return

    def PatientUpDate(self):
        index = self.panel.frame.Page_Frames.index(self.panel.frame.Page_Frames.select())
        print(index)
        if index == 0:
            updateVals = {}
            errCache = False
            for val, item in dict(self.activeUserVals['Indices'].iloc[0, :]).items():
                colName = val[0].upper() + val[1:]
                if val in ['ID', 'name', 'gender', 'DOB', 'COB']:
                    continue
                insertVal = self.panel.frame.pg0.__dict__.get(f'Entry_User{colName}').get()
                if not self.HandelFiled(colName, insertVal):
                    self.panel.frame.pg0.raiseError(colName)
                    errCache = True
                    continue
                self.panel.frame.pg0.deleteError(colName)
                if colName == 'Area':
                    insertVal = insertVal[0]
                if colName == 'Gender':
                    insertVal = insertVal[0]
                if colName == 'Phone':
                    insertVal = insertVal
                if colName == 'Support' and insertVal.lower() == 'yes':
                    insertVal = 1
                elif colName == 'Support' and insertVal.lower() == 'no':
                    insertVal = 0
                if colName == 'Height':
                    insertVal = float(insertVal)
                    if insertVal > 3:
                        insertVal /= 100
                if colName == 'Weight':
                    insertVal = float(insertVal)
                if str(insertVal) == item:
                    continue
                print(f'column {val}: {insertVal}')
                updateVals[val] = insertVal
            if errCache:
                return
            self.panel.app_queries.updateUserIndices('p', self.activeUserVals['ID'], **updateVals)
            self.activeUserVals = self.panel.app_queries.checkForLogIn('p', self.activeUserVals['ID'])
            return
        if index == 1:
            selected = []
            for each in self.panel.frame.pg1.Table_UserSymptoms.get_children():
                selected.append(self.panel.frame.pg1.Table_UserSymptoms.item(each)['values'][0])
            symptomsCurr = self.activeUserVals.get('symptoms')
            if not selected and not symptomsCurr:
                return
            if not selected and symptomsCurr:
                self.panel.app_queries.deletePatientSymptom(self.activeUserID, *selected)
                return
            if selected and not symptomsCurr:
                self.panel.app_queries.insertNewSymptom('p', ID=self.activeUserID, symptom=selected)
                return
            symptomsCurrHash = {symp: True for symp in symptomsCurr}
            symptomsNew = []
            for symp in selected:
                if symptomsCurrHash.get(symp):
                    symptomsCurrHash.pop(symp)
                    continue
                symptomsNew.append(symp)
            if symptomsCurrHash:
                self.panel.app_queries.deletePatientSymptom(self.activeUserID, *list(symptomsCurrHash.keys()))
            if symptomsNew:
                self.panel.app_queries.insertNewSymptom('p', ID=self.activeUserID, symptom=symptomsNew)
            self.activeUserVals = self.panel.app_queries.checkForLogIn('p', self.activeUserID)
            return
        return

    def pushNewPatient(self):
        columns = getTableCarry('patient').get('headers')
        NewPatientValues = {}
        for col in columns:
            colName = col[0].upper() + col[1:]
            if col != 'DOB':
                val = self.panel.frame.pg0.__dict__.get(f'Entry_User{colName}').get()
            else:
                val = self.panel.frame.pg0.__dict__.get(f'Entry_User{colName}').get_date()
            insertVal = val
            if colName == 'Area':
                insertVal = insertVal[0]
            if colName == 'Gender':
                insertVal = insertVal[0]
            if colName == 'Support' and insertVal.lower() == 'yes':
                insertVal = 1
            elif colName == 'Support' and insertVal.lower() == 'no':
                insertVal = 0
            if colName == 'Height':
                insertVal = float(insertVal)
                if insertVal > 3:
                    insertVal /= 100
            if colName == 'Weight':
                insertVal = float(insertVal)
            print(f'column {col}: {insertVal}')
            NewPatientValues[col] = insertVal
        NewPatientValues['symptoms'] = []
        for each in self.panel.frame.pg1.Table_UserSelectSymptoms.get_children():
            NewPatientValues['symptoms'].append(self.panel.frame.pg1.Table_UserSelectSymptoms.item(each)['values'][0])
        self.panel.app_queries.insertNewUser('p', **NewPatientValues)
        self.activeUser = 1
        self.activeUserID = NewPatientValues['ID']
        self.activeUserVals = self.panel.app_queries.checkForLogIn('p', NewPatientValues['ID'])
        return self.ExLogIn(afterSignIN=True, pathSignIN=1)

    def ExSignOut(self):
        if self.activeUser == 0:
            self.panel.destroy_frame('ResearcherMainPanel')
        elif self.activeUser == 1:
            self.panel.destroy_frame('PatientMainPanel')
        self.activeUser = None
        self.activeUserVals = {}
        return self.panel.show_frame('UserLogInPanel')

    def ExDisConnect(self):
        if not self.activeUserVals:
            return
        if self.activeUser == 0:
            self.panel.app_queries.DeleteUser('r', self.activeUserID)
        elif self.activeUser == 1:
            self.panel.app_queries.DeleteUser('p', self.activeUserID)
        return self.ExSignOut()

    def ExLogIn(self, afterSignIN=False, pathSignIN=None):
        if afterSignIN and pathSignIN is not None:
            if pathSignIN == 0:
                return self.panel.show_frame('ResearcherMainPanel')
            return self.panel.show_frame('PatientMainPanel')

        path = self.panel.frame.logIn_frame.Entry_UserPath.get()
        userID = self.panel.frame.logIn_frame.Entry_UserID.get()
        if not self.HandelFiled('ID', userID):
            self.panel.frame.logIn_frame.raiseError('ID')
            return
        if not self.HandelFiled('Name', userID):
            self.panel.frame.logIn_frame.raiseError('Name')
            return
        userName = self.panel.frame.logIn_frame.Entry_UserName.get()
        retRow = {}
        if path == 0:
            retRow = self.panel.app_queries.checkForLogIn('r', userID)
            print(f'Researcher Entry, Name: {userName}, ID: {userID}. {retRow}')
        elif path == 1:
            retRow = self.panel.app_queries.checkForLogIn('p', userID)
            print(f'Patient Entry, Name: {userName}, ID: {userID}. {retRow}')
        if not retRow:
            self.panel.frame.logIn_frame.raiseError('ID')
            return
        if userName.lower() != retRow['Indices'].iloc[0, :]['name'].lower():
            self.panel.frame.logIn_frame.raiseError('Name')
            return
        self.activeUser = path
        self.activeUserVals = retRow
        self.activeUserID = userID
        if path == 0:
            return self.panel.show_frame('ResearcherMainPanel')
        return self.panel.show_frame('PatientMainPanel')

    def ExSignIN(self):
        path = self.panel.frame.logIn_frame.Entry_UserPath.get()
        if path == 0:
            return self.panel.show_frame('ResearcherSignInPanel')
        return self.panel.show_frame('PatientSignInPanel')

    def dequeueUserIndices(self, call):
        if self.activeUser is None or self.activeUserID is None:
            return
        self.activeUserVals = self.panel.app_queries.checkForLogIn('p', self.activeUserID)
        if call == 'PatientMainPg1':
            ret = {'Indices': dict(self.activeUserVals['Indices'].iloc[0, :]), 'researchers': self.activeUserVals['researchers']}
            return ret
        if call == 'PatientMainPg2':
            return self.activeUserVals.get('symptoms')
        if call == 'PatientMainPg3':
            return self.activeUserVals.get('availableResearch')
        return