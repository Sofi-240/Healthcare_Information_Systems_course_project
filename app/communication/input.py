from app.server.serverInitiation import getTableCarry
import datetime
from tkinter import messagebox


class DataInputs:
    def __init__(self, panel):
        self.panel = panel

    @staticmethod
    def handelFiled(EntryName, txt):
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
        if EntryName == 'Fname':
            if not txt or (txt and len(txt) < 2):
                return False
            return True
        if EntryName == 'Lname':
            if not txt or (txt and len(txt) < 2):
                return False
            return True
        if EntryName == 'Mail':
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

    def exSignIN(self):
        if self.panel.frame.getEntry('user') == 'r':
            return self.panel.show_frame('ResearcherSignInPanel')
        return self.panel.show_frame('PatientSignInPanel')

    def validUserSignIn(self):
        if str(self.panel.frame)[2:].lower() == 'PatientSignInPanel'.lower():
            index = self.panel.frame.Page_Frames.index(
                self.panel.frame.Page_Frames.select()
            )
            if index == 0:
                columns = getTableCarry('patient').get('headers')
                errCache = False
                for col in columns:
                    colName = col[0].upper() + col[1:]
                    txt = self.panel.frame.getEntry(colName)
                    if not self.handelFiled(colName, txt):
                        self.panel.frame.raiseError(
                            labelName=colName
                        )
                        errCache = True
                    else:
                        self.panel.frame.deleteError(
                            labelName=colName
                        )
                if errCache:
                    return
                self.panel.frame.Page_Frames.tab(
                    1, state="normal"
                )
                self.panel.frame.Page_Frames.select(1)
            if index == 1:
                var = self.panel.frame.getEntry('Conifer')
                if var == 0:
                    return self.panel.frame.raiseError('Conifer')
                return self.pushNewUser()
            return
        elif str(self.panel.frame)[2:].lower() == 'ResearcherSignInPanel'.lower():
            errCache = False
            columns = getTableCarry('researcher').get('headers')
            for col in columns:
                colName = col[0].upper() + col[1:]
                txt = self.panel.frame.getEntry(colName)
                if not self.handelFiled(colName, txt):
                    self.panel.frame.raiseError(
                        labelName=colName
                    )
                    errCache = True
                else:
                    self.panel.frame.deleteError(
                        labelName=colName
                    )
            if errCache:
                return
            var = self.panel.frame.getEntry('Conifer')
            if var == 0:
                return self.panel.frame.raiseError('Conifer')
            return self.pushNewUser()
        return

    def pushNewUser(self):
        if str(self.panel.frame)[2:].lower() == 'PatientSignInPanel'.lower():
            columns = getTableCarry('patient').get('headers')
            NewPatientValues = {}
            for col in columns:
                colName = col[0].upper() + col[1:]
                insertVal = self.panel.frame.getEntry(colName)
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
                NewPatientValues[col] = insertVal
            NewPatientValues['symptoms'] = []
            tableSymptoms = self.panel.frame.getEntry('Symptoms')
            for each in tableSymptoms.get_children():
                NewPatientValues['symptoms'].append(
                    tableSymptoms.item(each)['values'][0]
                )
            NewPatientValues['ExLogIn'] = True
            self.panel.app_queries.insertNewUser(
                'p', **NewPatientValues
            )
        elif str(self.panel.frame)[2:].lower() == 'ResearcherSignInPanel'.lower():
            columns = getTableCarry('researcher').get('headers')
            NewResearcherValues = {}
            for col in columns:
                colName = col[0].upper() + col[1:]
                insertVal = self.panel.frame.getEntry(colName)
                if colName == 'Gender':
                    insertVal = insertVal[0]
                NewResearcherValues[col] = insertVal
            NewResearcherValues['ExLogIn'] = True
            self.panel.app_queries.insertNewUser(
                'r', **NewResearcherValues
            )
        return

    def pushNewResearch(self):
        NewResearch = {}
        for val, item in self.panel.frame.pg1.__dict__.items():
            temp = val.split('_')
            if temp[0] == 'Entry' and temp[1] == 'Research':
                colName = temp[-1]
                if type(item) is list and item:
                    insertVal = []
                    for x in item:
                        txt = x.get()
                        if txt == '':
                            insertVal.append(None)
                        else:
                            try:
                                digit = int(txt)
                            except ValueError:
                                digit = txt
                            insertVal.append(digit)
                elif colName == 'symptoms':
                    insertVal = []
                    for each in item.get_children():
                        insertVal.append(
                            item.item(each)['values'][0]
                        )
                elif colName in ['disName', 'depName']:
                    insertVal = item.get()
                else:
                    try:
                        insertValTemp = item.optionList
                    except AttributeError:
                        continue
                    insertVal = []
                    for widg, opt in insertValTemp:
                        if widg.get() == 0:
                            continue
                        if colName == 'support' and opt.lower() == 'no':
                            insertVal.append(0)
                        elif colName == 'support' and opt.lower() == 'yes':
                            insertVal.append(1)
                        elif colName == 'area' or colName == 'gender':
                            insertVal.append(opt[0])
                        else:
                            insertVal.append(opt)
                NewResearch[colName] = insertVal
        self.panel.app_queries.insertResearch(
            'active', **NewResearch
        )
        messagebox.showinfo(
            "", "The research inserted into the db"
        )
        return

    def addPatientToResearch(self):
        treeview = self.panel.frame.pg2.__dict__.get('Table_AvailablePatients')
        if not treeview:
            return
        textList = treeview.item(treeview.focus())["values"]
        if not textList:
            return
        res = messagebox.askquestion(
            'Agreement', f"Did you have {textList[2]} agreement?"
        )
        if res == 'yes':
            self.panel.app_queries.insertPatientToResearch(
                textList[0], textList[1]
            )
            messagebox.showinfo(
                "", f"{textList[2]} now in the research"
            )
        return

    def pushNewDiseases(self):
        columns = getTableCarry('diseases').get('headers')
        NewDiseasesValues = {}
        for col in columns:
            if col in ['disName', 'depName']:
                colName = col[0].upper() + col[1:]
                insertVal = self.panel.frame.pg3.__dict__.get(f'Entry_Disease{colName}').get()
                NewDiseasesValues[col] = insertVal
        NewDiseasesValues['disSymptoms'] = []
        for each in self.panel.frame.pg3.Table_DiseaseSelectSymptoms.get_children():
            NewDiseasesValues['disSymptoms'].append(
                [self.panel.frame.pg3.Table_DiseaseSelectSymptoms.item(each)['values'][0]]
            )
        self.panel.app_queries.insertNewDisease(
            **NewDiseasesValues
        )
        return

    def pushNewSymptoms(self):
        NewSymptomValues = {'disName': [
            self.panel.frame.pg4.__dict__.get(f'Entry_DiseaseDisName').get()
        ], 'symptom': [
            self.panel.frame.pg4.__dict__.get(f'Entry_DiseaseSymptom').get()
        ]}
        self.panel.app_queries.insertNewSymptom(
            'd', **NewSymptomValues
        )
        return

    def exLogIn(self):
        path = self.panel.frame.getEntry('user')
        userID = self.panel.frame.getEntry('ID')
        userName = self.panel.frame.getEntry('name')
        if not self.handelFiled('ID', userID):
            self.panel.frame.raiseError('ID')
            return
        if not self.handelFiled('Name', userName):
            self.panel.frame.raiseError('name')
            return
        retBool = self.panel.app_queries.activateLogIn(
            path, userID, userName
        )
        if type(retBool) is bool and retBool:
            return
        if type(retBool) is str:
            retBool = retBool[0].upper() + retBool[1:]
            self.panel.frame.raiseError(retBool)
            return
        return

    def userUpDate(self):
        if str(self.panel.frame)[2:].lower() == 'PatientMainPanel'.lower():
            index = self.panel.frame.Page_Frames.index(
                self.panel.frame.Page_Frames.select()
            )
            if index == 0:
                updateVals = {}
                errCache = False
                for val, item in dict(self.panel.app_queries.UserIndices['Indices'].iloc[0, :]).items():
                    colName = val[0].upper() + val[1:]
                    if val in ['ID', 'name', 'gender', 'DOB', 'COB']:
                        continue
                    insertVal = self.panel.frame.pg0.__dict__.get(f'Entry_{colName}').get()
                    if not self.handelFiled(colName, insertVal):
                        self.panel.frame.raiseError(0, colName)
                        errCache = True
                        continue
                    self.panel.frame.deleteError(0, colName)
                    if colName == 'Area':
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
                    updateVals[val] = insertVal
                if errCache:
                    return False
                return self.panel.app_queries.updateUserIndices('active', None, **updateVals)
            if index == 1:
                selected = []
                for each in self.panel.frame.pg1.Table_UserSymptoms.get_children():
                    selected.append(
                        self.panel.frame.pg1.Table_UserSymptoms.item(each)['values'][0]
                    )
                symptomsCurr = self.panel.app_queries.UserIndices.get('symptoms')
                if not selected and not symptomsCurr:
                    return True
                if selected and not symptomsCurr:
                    self.panel.app_queries.insertNewSymptom('active', symptom=selected)
                    return True
                symptomsCurrHash = {symp: True for symp in symptomsCurr}
                symptomsNew = []
                for symp in selected:
                    if symptomsCurrHash.get(symp):
                        symptomsCurrHash.pop(symp)
                        continue
                    symptomsNew.append(symp)
                if symptomsCurrHash:
                    self.panel.app_queries.deletePatientSymptom('active', *list(symptomsCurrHash.keys()))
                if symptomsNew:
                    self.panel.app_queries.insertNewSymptom('active', symptom=symptomsNew)
                return True
        elif str(self.panel.frame)[2:].lower() == 'ResearcherMainPanel'.lower():
            index = self.panel.frame.Page_Frames.index(
                self.panel.frame.Page_Frames.select()
            )
            if index == 0:
                updateVals = {}
                errCache = False
                for val, item in dict(self.panel.app_queries.UserIndices['Indices'].iloc[0, :]).items():
                    colName = val[0].upper() + val[1:]
                    if val in ['ID', 'Fname', 'gender', 'Lname']:
                        continue
                    insertVal = self.panel.frame.pg0.__dict__.get(f'Entry_{colName}').get()
                    if not self.handelFiled(colName, insertVal):
                        self.panel.frame.raiseError(0, colName)
                        errCache = True
                        continue
                    self.panel.frame.deleteError(0, colName)
                    updateVals[val] = insertVal
                if errCache:
                    return False
                return self.panel.app_queries.updateUserIndices('active', None, **updateVals)
        return False

    def exSignOut(self):

        self.panel.destroy_frame('active')
        self.panel.app_queries.activeUser = None
        self.panel.app_queries.activeUserName = None
        self.panel.app_queries.UserIndices = {}
        return

    def exDisConnect(self):
        self.panel.app_queries.deleteUser('active', None)
        return self.exSignOut()


