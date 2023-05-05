from app.initialization.table_obj import Table
from app.initialization.ServerInitiation import getTableCarry


class insert2DB:
    def __init__(self, panel):
        self.panel = panel
        self.activeUser = None
        self.activeUserVals = []

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
                    if not self.panel.frame.pg0.HandelFiled(val[10:], txt, appCall=True):
                        errCache = True
            if errCache:
                print(errCache)
                self.panel.frame.Page_Frames.tab(1, state="normal")
                self.panel.frame.Page_Frames.select(1)
                return
            self.panel.frame.Page_Frames.tab(1, state="normal")
            self.panel.frame.Page_Frames.select(1)
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
                insertVal = True
            if colName == 'Support' and insertVal.lower() == 'no':
                insertVal = False
            if colName == 'Height':
                insertVal = float(insertVal)
                if insertVal > 3:
                    insertVal /= 100
            if colName == 'Weight':
                insertVal = float(insertVal)
            print(f'column {col}: {insertVal}')
            NewPatientValues[col] = insertVal
        symptoms = []
        for i in self.panel.frame.pg1.Listbox_UserSelectSymptoms.curselection():
            symptoms.append(self.panel.frame.pg1.Listbox_UserSelectSymptoms.get(i))
        NewPatientValues['symptoms'] = symptoms
        # self.panel.app_queries.insertNewUser('p', **NewPatientValues)
        self.activeUser = 1
        self.activeUserVals = list(NewPatientValues.values())
        return self.ExLogIn(afterSignIN=True, pathSignIN=1)

    def ExSignOut(self):
        if self.activeUser == 0:
            self.panel.destroy_frame('ResearcherMainPanel')
        elif self.activeUser == 1:
            self.panel.destroy_frame('PatientMainPanel')
        self.activeUser = None
        self.activeUserVals = None
        return self.panel.show_frame('UserLogInPanel')

    def ExLogIn(self, afterSignIN=False, pathSignIN=None):
        if afterSignIN and pathSignIN is not None:
            if pathSignIN == 0:
                return self.panel.show_frame('ResearcherMainPanel')
            return self.panel.show_frame('PatientMainPanel')

        path = self.panel.frame.logIn_frame.Entry_UserPath.get()
        userID = self.panel.frame.logIn_frame.Entry_UserID.get()
        userName = self.panel.frame.logIn_frame.Entry_UserName.get()
        retRow = []
        if path == 0:
            retRow = self.panel.app_queries.checkForLogIn('r', userID)
            print(f'Researcher Entry, Name: {userName}, ID: {userID}. {retRow}')
        elif path == 1:
            retRow = self.panel.app_queries.checkForLogIn('p', userID)
            print(f'Patient Entry, Name: {userName}, ID: {userID}. {retRow}')
        if not retRow:
            self.panel.frame.logIn_frame.HandelFiled('ID', userID, appCall=True)
            return
        if userName.lower() != retRow[2].lower():
            self.panel.frame.logIn_frame.HandelFiled('Name', userID, appCall=True)
            return
        self.activeUser = path
        self.activeUserVals = retRow
        if path == 0:
            return self.panel.show_frame('ResearcherMainPanel')
        return self.panel.show_frame('PatientMainPanel')

    def ExSignIN(self):
        path = self.panel.frame.logIn_frame.Entry_UserPath.get()
        if path == 0:
            return self.panel.show_frame('ResearcherSignInPanel')
        return self.panel.show_frame('PatientSignInPanel')

    def dequeueIndices(self):
        if self.activeUser is None:
            return
        if not self.activeUserVals:
            return
        if self.activeUser == 1:
            columns = getTableCarry('patient').get('headers')
        else:
            columns = getTableCarry('researcher').get('headers')
        Indices = {}
        for i, col in enumerate(columns):
            Indices[col] = self.activeUserVals[i]
        if self.activeUser == 0:
            return Indices
        if len(self.activeUserVals) > len(columns):
            Indices['symptoms'] = self.activeUserVals[len(columns):]
        return Indices
