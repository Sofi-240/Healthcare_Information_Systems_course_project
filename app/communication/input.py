from app.initialization.ServerInitiation import getTableCarry
import datetime


class insert2DB:
    def __init__(self, panel):
        self.panel = panel
        self.activeUser = None
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

    def ExSignIN(self):
        path = self.panel.frame.logIn_frame.Entry_UserPath.get()
        if path == 0:
            return self.panel.show_frame('ResearcherSignInPanel')
        return self.panel.show_frame('PatientSignInPanel')

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
                        self.panel.frame.raiseError(0)
                        errCache = True
                    else:
                        self.panel.frame.deleteError(0)
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
        self.activeUser = 'p'
        self.activeUserID = NewPatientValues['ID']
        self.panel.app_queries.checkForLogIn('p', self.activeUserID)
        return self.ExLogIn(afterSignIN=True)

    def ExLogIn(self, afterSignIN=False):
        if afterSignIN and self.activeUser is not None:
            if self.activeUser == 'r':
                return self.panel.show_frame('ResearcherMainPanel')
            return self.panel.show_frame('PatientMainPanel')

        path = self.panel.frame.logIn_frame.Entry_UserPath.get()
        if path == 0:
            path = 'r'
        else:
            path = 'p'

        userID = self.panel.frame.logIn_frame.Entry_UserID.get()
        if not self.HandelFiled('ID', userID):
            self.panel.frame.raiseError('ID')
            return
        if not self.HandelFiled('Name', userID):
            self.panel.frame.raiseError('Name')
            return
        userName = self.panel.frame.logIn_frame.Entry_UserName.get()
        retRow = self.panel.app_queries.checkForLogIn(path, userID)
        if not retRow:
            self.panel.frame.raiseError('ID')
            return
        if userName.lower() != retRow['Indices'].iloc[0, :]['name'].lower():
            self.panel.frame.raiseError('Name')
            return
        self.activeUser = path
        self.activeUserID = userID
        if path == 'r':
            return self.panel.show_frame('ResearcherMainPanel')
        return self.panel.show_frame('PatientMainPanel')

    def PatientUpDate(self):
        index = self.panel.frame.Page_Frames.index(self.panel.frame.Page_Frames.select())
        print(index)
        if index == 0:
            updateVals = {}
            errCache = False
            for val, item in dict(self.panel.app_queries.UserIndices['Indices'].iloc[0, :]).items():
                colName = val[0].upper() + val[1:]
                if val in ['ID', 'name', 'gender', 'DOB', 'COB']:
                    continue
                insertVal = self.panel.frame.pg0.__dict__.get(f'Entry_User{colName}').get()
                if not self.HandelFiled(colName, insertVal):
                    self.panel.frame.raiseError(0)
                    errCache = True
                    continue
                self.panel.frame.deleteError(0)
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
            self.panel.app_queries.updateUserIndices(self.activeUser, self.activeUserID, **updateVals)
            self.panel.app_queries.checkForLogIn(self.activeUser, self.activeUserID)
            return
        if index == 1:
            selected = []
            for each in self.panel.frame.pg1.Table_UserSymptoms.get_children():
                selected.append(self.panel.frame.pg1.Table_UserSymptoms.item(each)['values'][0])
            symptomsCurr = self.panel.app_queries.UserIndices.get('symptoms')
            if not selected and not symptomsCurr:
                return
            if not selected and symptomsCurr:
                self.panel.app_queries.deletePatientSymptom(self.activeUserID, *selected)
                return
            if selected and not symptomsCurr:
                self.panel.app_queries.insertNewSymptom(self.activeUser, ID=self.activeUserID, symptom=selected)
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
                self.panel.app_queries.insertNewSymptom(self.activeUser, ID=self.activeUserID, symptom=symptomsNew)
            self.panel.app_queries.checkForLogIn(self.activeUser, self.activeUserID)
            return
        return

    def ExSignOut(self):
        if self.activeUser == 'r':
            self.panel.destroy_frame('ResearcherMainPanel')
        elif self.activeUser == 'p':
            self.panel.destroy_frame('PatientMainPanel')
        self.activeUser = None
        return self.panel.show_frame('UserLogInPanel')

    def ExDisConnect(self):
        if not self.activeUser:
            return
        self.panel.app_queries.DeleteUser(self.activeUser, self.activeUserID)
        return self.ExSignOut()


