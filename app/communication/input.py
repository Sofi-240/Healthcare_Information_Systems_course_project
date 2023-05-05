from app.initialization.table_obj import Table
from app.initialization.ServerInitiation import getTableCarry


class insert2DB:
    def __init__(self, panel):
        self.panel = panel

    def validUser(self, path):
        userID = self.panel.frame.logIn_frame.Entry_UserID.get()
        if not userID or userID == 'ID':
            self.panel.frame.logIn_frame.HandelFiled('ID', userID)
            return False
        userName = self.panel.frame.logIn_frame.Entry_UserName.get()
        if not userName or userName == 'Name':
            return False
        if path == 0:
            print(f'Researcher Entry, Name: {userName}, ID: {userID}')
        elif path == 1:
            print(f'Patient Entry, Name: {userName}, ID: {userID}')
        return True

    def validPatientSignInForward(self):
        index = self.panel.frame.Page_Frames.index(self.panel.frame.Page_Frames.select())
        if index == 0:
            errCache = False
            for val, item in self.panel.frame.pg0.__dict__.items():
                if len(val) > 10 and val[:10] == 'Entry_User':
                    if val[10:] != 'DOB':
                        txt = item.get()
                    else:
                        txt = item.get_date()
                    if not self.panel.frame.pg0.HandelFiled(val[10:], txt):
                        errCache = True
            if errCache:
                print(errCache)
                self.panel.frame.Page_Frames.select(1)
                return
            self.panel.frame.Page_Frames.select(1)
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
            print(f'column {colName}: {val}')
            NewPatientValues[col] = val
        symptoms = []
        for i in self.panel.frame.pg1.Listbox_UserSelectSymptoms.curselection():
            symptoms.append(self.panel.frame.pg1.Listbox_UserSelectSymptoms.get(i))
        NewPatientValues['symptoms'] = symptoms
        # self.panel.app_queries.insertNewUser('p', **NewPatientValues)
        return True
