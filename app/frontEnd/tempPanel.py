import tkinter as tk
from tkinter import ttk
from screeninfo import get_monitors


class Panel(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('App Panel')
        self.width = get_monitors()[0].width
        self.height = get_monitors()[0].height
        self.geometry(f'{int(self.width * 1)}x{int(self.height * 1)}')
        self.resizable(True, True)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)
        self.config(bg="white")
        self._initPanel()

    def _initPanel(self):
        self.frames = {}
        for F in [UserLogInPanel, PatientSingInPanel, ResearcherSingInFrame]:
            frame = F(self)
            frame.grid(column=1, row=1, padx=20, pady=20, sticky="nsew")
            self.frames[F] = frame
        return self.show_frame(UserLogInPanel)

    def show_frame(self, name):
        self.frame = self.frames[name]
        self.frame.tkraise()
        return


class UserLogInPanel(ttk.Frame):

    def __init__(self, MasterPanel):
        ttk.Frame.__init__(self, master=MasterPanel, relief=tk.RAISED, borderwidth=2)
        self.width = 0.5 * MasterPanel.width
        self.height = 0.5 * MasterPanel.height
        self.columnconfigure(list(range(1, 11)), weight=1)
        self.rowconfigure(list(range(1, 11)), weight=1)
        self._create_sub_frames(MasterPanel)

    def _create_sub_frames(self, MasterPanel):
        self.style = ttk.Style(self)
        self.style.configure('TFrame', background='white')
        self.logIn_frame = LogInFrame(self)
        self.logIn_frame.grid(column=5, row=5, padx=50, pady=50)
        return


class LogInFrame(ttk.Frame):
    def __init__(self, MasterPanel):
        ttk.Frame.__init__(self, master=MasterPanel, relief=tk.RAISED, borderwidth=20)
        self.width = 0.5 * MasterPanel.width
        self.height = 0.5 * MasterPanel.height
        self.columnconfigure(list(range(1, 5)), weight=1)
        self.rowconfigure(list(range(1, 5)), weight=1)
        self._create_widgets(MasterPanel)

    def _create_widgets(self, MasterPanel):
        self.style = ttk.Style(self)
        self.style.configure('TLabel', font=("Helvetica", 14, "bold"), background='white')
        self.style.configure('TLabelframe', bordercolor="LightSkyBlue2", background='white')
        self.style.configure('TLabelframe.Label', font=("Helvetica", 14, "bold"), background='white')
        self.style.configure('TButton', font=("Helvetica", 14, "bold"), background="LightSkyBlue2", foreground='black')
        self.style.configure('TRadiobutton', font=("Helvetica", 14, "bold"), background="white", foreground='black')
        self.style.configure('TEntry', width=20)
        entryConfigure = {'font': ("Helvetica", 16, "bold"), 'background': 'white'}
        gridTEntryConfigure = {'padx': 10, 'pady': 0, 'sticky': tk.W, 'ipady': 5, 'ipadx': 0}
        gridConfigure = {'padx': 5, 'pady': 5, 'sticky': tk.W}

        # User Path researcher or patient
        self.Label_UserPath = ttk.LabelFrame(self, text='User')
        self.Label_UserPath.grid(column=1, row=1, columnspan=2, **gridConfigure)
        self.Entry_UserPath = tk.IntVar()
        self.Entry_UserPath.set(1)
        self.RB_UserPath_Patient = ttk.Radiobutton(self.Label_UserPath, text='Patient', variable=self.Entry_UserPath,
                                                   value=1)
        self.RB_UserPath_Patient.grid(column=1, row=2, **gridConfigure)

        self.RB_UserPath_Researcher = ttk.Radiobutton(self.Label_UserPath, text='Researcher',
                                                      variable=self.Entry_UserPath, value=0)
        self.RB_UserPath_Researcher.grid(column=2, row=2, **gridConfigure)

        # User, researcher or patient Insert ID
        self.Label_UserID = ttk.Label(self, text='User ID:')
        self.Label_UserID.grid(column=1, row=3, **gridConfigure)
        self.Entry_UserID = ttk.Entry(self, **entryConfigure)
        self.Entry_UserID.insert(0, "ID")
        self.Entry_UserID.grid(column=2, row=3, **gridTEntryConfigure)
        self.Entry_UserID.bind("<FocusOut>", lambda e: self.EntryFocusOut('ID'))
        self.Entry_UserID.bind("<Button-1>", lambda e: self.EntryButton1('ID'))
        self.EntryError_UserID = ttk.Label(self)

        # User researcher or patient Insert Name
        self.Label_UserName = ttk.Label(self, text='User Name:')
        self.Label_UserName.grid(column=1, row=4, **gridConfigure)
        self.Entry_UserName = ttk.Entry(self, **entryConfigure)
        self.Entry_UserName.insert(0, "Name")
        self.Entry_UserName.grid(column=2, row=4, **gridTEntryConfigure)
        self.Entry_UserName.bind("<FocusOut>", lambda e: self.EntryFocusOut('Name'))
        self.Entry_UserName.bind("<Button-1>", lambda e: self.EntryButton1('Name'))
        self.EntryError_UserName = ttk.Label(self)

        # LOGIN button
        self.Button_LogIn = ttk.Button(self, text="Log In", command=lambda: self.ExLogIn(MasterPanel))
        self.Button_LogIn.grid(column=4, row=3, **gridConfigure)

        # SingIN button
        self.Button_SingIN = ttk.Button(self, text="Sing IN", command=lambda: self.ExSingIN(MasterPanel))
        self.Button_SingIN.grid(column=4, row=4, **gridConfigure)

        return

    def EntryFocusOut(self, EntryName):
        txt = self.__dict__[f'Entry_User{EntryName}'].get()
        if not txt:
            self.__dict__[f'Entry_User{EntryName}'].insert(0, EntryName)
            return
        if self.__dict__.get(f'EntryError_User{EntryName}'):
            return self.HandelFiled(EntryName, txt)
        return

    def EntryButton1(self, EntryName):
        txt = self.__dict__[f'Entry_User{EntryName}'].get()
        if txt == EntryName:
            self.__dict__[f'Entry_User{EntryName}'].delete(0, "end")
        return

    def HandelFiled(self, EntryName, txt):
        if EntryName == 'ID':
            if not txt:
                self.Entry_UserID.insert(0, "ID")
                return
            if len(txt) < 9 or len(txt) > 9:
                self.Entry_UserID.config(foreground="red")
                self.EntryError_UserID.configure(text='*The ID is not valid', foreground='red',
                                                 font=("Helvetica", 10, "bold"))
                self.EntryError_UserID.grid(column=3, row=3, padx=0, pady=0)
                return
            self.Entry_UserID.config(foreground="black")
            self.EntryError_UserID.configure(text='')
        return

    def validUser(self, path):
        userID = self.Entry_UserID.get()
        if not userID or userID == 'ID':
            return False
        userName = self.Entry_UserName.get()
        if not userName or userName == 'Name':
            return False
        if path == 0:
            print(f'Researcher Entry, Name: {userName}, ID: {userID}')
        elif path == 1:
            print(f'Patient Entry, Name: {userName}, ID: {userID}')
        return True

    def ExLogIn(self, MasterPanel):
        selected = self.Entry_UserPath.get()
        if not self.validUser(selected):
            print('error')
            return
        if selected == 0:
            return
        return

    def ExSingIN(self, MasterPanel):
        selected = self.Entry_UserPath.get()
        if selected == 0:
            return MasterPanel.master.show_frame(ResearcherSingInFrame)
        return MasterPanel.master.show_frame(PatientSingInPanel)


class PatientSingInPanel(ttk.Frame):

    def __init__(self, MasterPanel):
        ttk.Frame.__init__(self, master=MasterPanel, relief=tk.RAISED, borderwidth=2)
        self.width = 0.5 * MasterPanel.width
        self.height = 0.5 * MasterPanel.height
        self.columnconfigure(list(range(1, 5)), weight=1)
        self.rowconfigure(list(range(1, 11)), weight=1)
        self._create_sub_frames(MasterPanel)

    def _create_sub_frames(self, MasterPanel):
        self.style = ttk.Style(self)
        self.style.configure('TFrame', background='white')
        self.style.configure('TNotebook', background='LightSkyBlue2')
        self.style.configure('TNotebook.Tab', background="LightSkyBlue2", compound=tk.LEFT,
                             font=("Helvetica", 14, "bold"))
        self.style.configure('TButton', font=("Helvetica", 14, "bold"), background="LightSkyBlue2", foreground='black')

        # Back button
        self.Button_LogIn = ttk.Button(self, text="Back", command=lambda: self.back())
        self.Button_LogIn.grid(column=1, row=1, padx=5, pady=5, sticky=tk.W)

        # Next button
        self.Button_SingIN = ttk.Button(self, text="Next", command=lambda: self.forward())
        self.Button_SingIN.grid(column=2, row=1, padx=5, pady=5, sticky=tk.E)

        self.Page_Frames = ttk.Notebook(self, width=500, height=500)
        self.Page_Frames.grid(column=1, row=2, padx=10, pady=10, sticky="nsew", columnspan=2, rowspan=2)

        pg0 = PatientSingInPg1(self)
        pg1 = PatientSingInPg2(self)
        self.frames = {}
        self.Page_Frames.add(pg0, text='                Step 1                ')
        self.Page_Frames.add(pg1, text='                Step 2                ')
        self.Page_Frames.select(0)
        return

    def back(self):
        index = self.Page_Frames.index(self.Page_Frames.select())
        if index == 1:
            self.Page_Frames.select(0)

    def forward(self):
        index = self.Page_Frames.index(self.Page_Frames.select())
        if index == 0:
            self.Page_Frames.select(1)


class PatientSingInPg1(ttk.Frame):
    def __init__(self, MasterPanel):
        ttk.Frame.__init__(self, master=MasterPanel, relief=tk.RAISED)
        self.columnconfigure(list(range(1, 5)), weight=1)
        self.rowconfigure(list(range(1, 13)), weight=1)
        self._create_widgets(MasterPanel)

    def _create_widgets(self, MasterPanel):
        self.style = ttk.Style(self)
        self.style.configure('TLabel', font=("Helvetica", 14, "bold"), background='white')
        self.style.configure('TCombobox', font=("Helvetica", 14, "bold"), background='white',
                             arrowcolor="LightSkyBlue2", arrowsize=5)
        self.style.configure('TButton', font=("Helvetica", 14, "bold"), background="LightSkyBlue2", foreground='black')
        self.style.configure('TLabelframe', bordercolor="LightSkyBlue2", background='white', borderwidth=5)
        self.style.configure('TLabelframe.Label', font=("Helvetica", 14, "bold"), background='white')
        self.style.configure('TEntry', weight=100)
        gridConfigure = {'padx': 10, 'pady': 0, 'sticky': tk.W}
        gridTEntryConfigure = {'padx': 10, 'pady': 0, 'sticky': tk.W, 'ipady': 5, 'ipadx': 0}
        entryConfigure = {'font': ("Helvetica", 16), 'background': 'white'}

        self.Label_UserID = ttk.Label(self, text='ID', borderwidth=0)
        self.Label_UserID.grid(column=1, row=1,  **gridConfigure)
        self.Entry_UserID = ttk.Entry(self, **entryConfigure)
        self.Entry_UserID.grid(column=1, row=2, **gridTEntryConfigure)
        self.EntryError_UserID = ttk.Label(self, font=("Helvetica", 10), background='white',
                                           foreground='red')
        self.EntryError_UserID.grid(column=2, row=2, padx=0, pady=0, sticky=tk.W)
        self.Entry_UserID.bind("<Button-1>", lambda e: self.EntryButton1('ID'))
        self.Entry_UserID.bind("<FocusOut>", lambda e: self.EntryFocusOut('ID'))

        self.Label_UserName = ttk.Label(self, text='Name:')
        self.Label_UserName.grid(column=1, row=3, **gridConfigure)
        self.Entry_UserName = ttk.Entry(self, **entryConfigure)
        self.Entry_UserName.grid(column=1, row=4, columnspan=2, **gridTEntryConfigure)
        self.EntryError_UserName = ttk.Label(self)
        self.Entry_UserName.bind("<Button-1>", lambda e: self.EntryButton1('Name'))

        self.Label_UserDOB = ttk.LabelFrame(self, text='Date of Birth')
        self.Label_UserDOB.grid(column=1, row=5, columnspan=3, **gridConfigure)
        self.Entry_UserDay = ttk.Entry(self.Label_UserDOB, **entryConfigure)
        self.Entry_UserDay.insert(0, "Day")
        self.Entry_UserDay.grid(column=1, row=6, **gridTEntryConfigure)
        self.EntryError_UserDay = ttk.Label(self)
        self.Entry_UserDay.bind("<Button-1>", lambda e: self.EntryButton1('Day'))
        self.Entry_UserDay.bind("<FocusOut>", lambda e: self.EntryFocusOut('Day'))

        self.Entry_UserMonth = ttk.Entry(self.Label_UserDOB, **entryConfigure)
        self.Entry_UserMonth.insert(0, "Month")
        self.Entry_UserMonth.grid(column=2, row=6, **gridTEntryConfigure)
        self.EntryError_UserMonth = ttk.Label(self)
        self.Entry_UserMonth.bind("<Button-1>", lambda e: self.EntryButton1('Month'))
        self.Entry_UserMonth.bind("<FocusOut>", lambda e: self.EntryFocusOut('Month'))

        self.Entry_UserYear = ttk.Entry(self.Label_UserDOB, **entryConfigure)
        self.Entry_UserYear.insert(0, "Year")
        self.Entry_UserYear.grid(column=3, row=6, **gridTEntryConfigure)
        self.EntryError_UserYear = ttk.Label(self)
        self.Entry_UserYear.bind("<Button-1>", lambda e: self.EntryButton1('Year'))
        self.Entry_UserYear.bind("<FocusOut>", lambda e: self.EntryFocusOut('Year'))

        self.Label_UserArea = ttk.Label(self, text='Area:')
        self.Label_UserArea.grid(column=1, row=7, **gridConfigure)
        self.textVariable_UserArea = tk.StringVar()
        self.Entry_UserArea = ttk.Combobox(self, textvariable=self.textVariable_UserArea, **entryConfigure)
        self.Entry_UserArea['values'] = ('N', 'C', 'S')
        self.Entry_UserArea.grid(column=1, row=8, **gridTEntryConfigure)

        self.Label_UserCity = ttk.Label(self, text='City:')
        self.Label_UserCity.grid(column=1, row=9, **gridConfigure)
        self.Entry_UserCity = ttk.Entry(self, **entryConfigure)
        self.Entry_UserCity.grid(column=1, row=10, columnspan=2, **gridTEntryConfigure)
        self.EntryError_UserCity = ttk.Label(self)
        self.Entry_UserCity.bind("<Button-1>", lambda e: self.EntryButton1('City'))

        self.Label_UserPhone = ttk.Label(self, text='Phone:')
        self.Label_UserPhone.grid(column=1, row=11, **gridConfigure)
        self.Entry_UserPhone = ttk.Entry(self, **entryConfigure)
        self.Entry_UserPhone.grid(column=1, row=12, columnspan=2, **gridTEntryConfigure)
        self.EntryError_UserPhone = ttk.Label(self)
        self.Entry_UserPhone.bind("<Button-1>", lambda e: self.EntryButton1('Phone'))

    def EntryFocusOut(self, EntryName):
        txt = self.__dict__[f'Entry_User{EntryName}'].get()
        if not txt and EntryName in ["Day", "Month", "Year"]:
            self.__dict__[f'Entry_User{EntryName}'].insert(0, EntryName)
            return
        if not txt:
            return
        if self.__dict__.get(f'EntryError_User{EntryName}'):
            return self.HandelFiled(EntryName, txt)
        return

    def EntryButton1(self, EntryName):
        txt = self.__dict__[f'Entry_User{EntryName}'].get()
        if txt == EntryName:
            self.__dict__[f'Entry_User{EntryName}'].delete(0, "end")
        return

    def HandelFiled(self, EntryName, txt):
        if EntryName == 'ID':
            if len(txt) < 9 or len(txt) > 9:
                self.Entry_UserID.config(foreground="red")
                self.EntryError_UserID.configure(text='The ID is not valid', foreground='red')
                return
            self.Entry_UserID.config(foreground="black")
            self.EntryError_UserID.configure(text='')
            return
        if EntryName == 'Phone':
            if len(txt) < 10 or len(txt) > 10:
                self.Entry_UserPhone.config(foreground="red")
                self.EntryError_UserPhone.configure(text='The Phone number is not valid', foreground='red')
                return
            self.Entry_UserPhone.config(foreground="black")
            self.EntryError_UserPhone.configure(text='')
            return
        return


class PatientSingInPg2(ttk.Frame):
    def __init__(self, MasterPanel):
        ttk.Frame.__init__(self, master=MasterPanel, relief=tk.RAISED)
        self.columnconfigure(list(range(1, 6)), weight=1)
        self.rowconfigure(list(range(1, 16)), weight=1)
        self._create_widgets(MasterPanel)

    def _create_widgets(self, MasterPanel):
        self.style = ttk.Style(self)
        self.style.configure('TLabel', font=("Helvetica", 14, "bold"), background='white')
        self.style.configure('TCombobox', font=("Helvetica", 14, "bold"), background='white',
                             arrowcolor="LightSkyBlue2", arrowsize=5)
        self.style.configure('TButton', font=("Helvetica", 14, "bold"), background="LightSkyBlue2", foreground='black')
        self.style.configure('TLabelframe', bordercolor="LightSkyBlue2", background='white', borderwidth=5)
        self.style.configure('TLabelframe.Label', font=("Helvetica", 14, "bold"), background='white')
        self.style.configure('TEntry', weight=100)
        gridConfigure = {'padx': 10, 'pady': 0, 'sticky': tk.W}
        gridTEntryConfigure = {'padx': 10, 'pady': 0, 'sticky': tk.W, 'ipady': 5, 'ipadx': 0}
        entryConfigure = {'font': ("Helvetica", 16), 'background': 'white'}

        self.Label_UserGender = ttk.Label(self, text='Gender:')
        self.Label_UserGender.grid(column=1, row=1, **gridConfigure)
        self.textVariable_UserGender = tk.StringVar(value='Gender')
        self.Entry_UserGender = ttk.Combobox(self, textvariable=self.textVariable_UserGender, **entryConfigure)
        self.Entry_UserGender['values'] = ('Female', 'Male')
        self.Entry_UserGender.grid(column=1, row=2, **gridTEntryConfigure)

        self.Label_UserHMO = ttk.Label(self, text='HMO:')
        self.Label_UserHMO.grid(column=1, row=3, **gridConfigure)
        self.textVariable_UserHMO = tk.StringVar(value='HMO')
        self.Entry_UserHMO = ttk.Combobox(self, textvariable=self.textVariable_UserHMO, **entryConfigure)
        # self.Entry_UserHMO['values'] = ('Meuhedet', 'C', 'S')
        self.Entry_UserHMO.grid(column=1, row=4, **gridTEntryConfigure)

        self.Label_UserCOB = ttk.Label(self, text='COB:')
        self.Label_UserCOB.grid(column=1, row=5, **gridConfigure)
        self.Entry_UserCOB = ttk.Entry(self)
        self.Entry_UserCOB.grid(column=1, row=6, **gridTEntryConfigure)
        self.EntryError_UserCOB = ttk.Label(self, **entryConfigure)
        self.Entry_UserCOB.bind("<Button-1>", lambda e: self.EntryButton1('COB'))
        self.Entry_UserCOB.bind("<FocusOut>", lambda e: self.EntryFocusOut('COB'))

        self.Label_UserHeight = ttk.Label(self, text='Height:')
        self.Label_UserHeight.grid(column=1, row=7, **gridConfigure)
        self.Entry_UserHeight = tk.Entry(self, **entryConfigure)
        self.Entry_UserHeight.grid(column=1, row=8, **gridTEntryConfigure)
        self.EntryError_UserHeight = ttk.Label(self, **entryConfigure)
        self.Entry_UserHeight.bind("<Button-1>", lambda e: self.EntryButton1('Height'))
        self.Entry_UserHeight.bind("<FocusOut>", lambda e: self.EntryFocusOut('Height'))

        self.Label_UserWeight = ttk.Label(self, text='Weight:')
        self.Label_UserWeight.grid(column=1, row=9, **gridConfigure)
        self.Entry_UserWeight = ttk.Entry(self, **entryConfigure)
        self.Entry_UserWeight.grid(column=1, row=10, **gridTEntryConfigure)
        self.EntryError_UserWeight = ttk.Label(self)
        self.Entry_UserWeight.bind("<Button-1>", lambda e: self.EntryButton1('Weight'))
        self.Entry_UserWeight.bind("<FocusOut>", lambda e: self.EntryFocusOut('Weight'))

        self.Label_UserSupport = ttk.Label(self, text='support:')
        self.Label_UserSupport.grid(column=1, row=11, **gridConfigure)
        self.textVariable_UserSupport = tk.StringVar(value='Support')
        self.Entry_UserSupport = ttk.Combobox(self, textvariable=self.textVariable_UserSupport, **entryConfigure)
        self.Entry_UserSupport['values'] = ('Yes', 'No')
        self.Entry_UserSupport.grid(column=1, row=12, **gridTEntryConfigure)

        self.Label_UserSymptoms = ttk.Label(self, text='Symptoms:')
        self.Label_UserSymptoms.grid(column=4, row=3, **gridConfigure)
        self.symptomText = tk.StringVar()
        self.Entry_UserSymptoms = ttk.Entry(self, textvariable=self.symptomText, **entryConfigure)
        self.Entry_UserSymptoms.grid(column=4, row=4, columnspan=3, rowspan=3, **gridTEntryConfigure)
        self.Entry_UserSymptoms.bind("<Button-1>", lambda e: self.EntryButton1('Symptoms'))
        self.Entry_UserSymptoms.bind("<FocusOut>", lambda e: self.EntryFocusOut('Symptoms'))
        self.Entry_UserSymptoms.bind("<space>", lambda e: self.autoComplete())
        self.Listbox_UserSymptoms = tk.Listbox(self)
        # self.Listbox_UserSymptoms.grid(column=2, row=14, padx=0, pady=0)

        self.Button_SingIN = ttk.Button(self, text="SingIN", command=self.SingINButton(MasterPanel))
        self.Button_SingIN.grid(column=3, row=15, **gridConfigure)

    def SingINButton(self, MasterPanel):

        return

    def EntryFocusOut(self, EntryName):
        if EntryName == 'Symptoms':
            return
        txt = self.__dict__[f'Entry_User{EntryName}'].get()
        if not txt:
            return
        if self.__dict__.get(f'EntryError_User{EntryName}'):
            return self.HandelFiled(EntryName, txt)
        return

    def EntryButton1(self, EntryName):
        txt = self.__dict__[f'Entry_User{EntryName}'].get()
        if txt == EntryName:
            self.__dict__[f'Entry_User{EntryName}'].delete(0, "end")
        return

    def HandelFiled(self, EntryName, txt):
        return

    def autoComplete(self):
        txt = self.Entry_UserSymptoms.get()
        print(txt)
        return


class ResearcherSingInFrame(ttk.Frame):

    def __init__(self, MasterPanel):
        ttk.Frame.__init__(self, master=MasterPanel, relief=tk.RAISED, borderwidth=2)
        self.width = 0.5 * MasterPanel.width
        self.height = 0.5 * MasterPanel.height
        self.columnconfigure(list(range(1, 11)), weight=1)
        self.rowconfigure(list(range(1, 11)), weight=1)
        self._create_sub_frames(MasterPanel)

    def _create_sub_frames(self, MasterPanel):
        return


if __name__ == '__main__':
    myPanel = Panel()
    myPanel.mainloop()
