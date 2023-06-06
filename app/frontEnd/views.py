import tkinter as tk
from tkinter import ttk, HORIZONTAL, VERTICAL
from app.frontEnd.roundButton import RoundedButton
from tkcalendar import DateEntry
from app.frontEnd.autoComplete import AUTO_complete


class UserLogInPanel(ttk.Frame):

    def __init__(self, MasterPanel):
        ttk.Frame.__init__(self, master=MasterPanel, relief=tk.RAISED, borderwidth=2)
        self.width = 0.5 * MasterPanel.width
        self.height = 0.5 * MasterPanel.height
        self.columnconfigure(list(range(1, 8)), weight=1)
        self.rowconfigure(list(range(1, 8)), weight=1)
        self.style = ttk.Style(self)
        self.style.configure('Frame1.TFrame', background='LightSkyBlue4', borderwidth=10, relief='RAISED')
        self._logInFrame(self, style='Frame1.TFrame')
        self.logIn_frame.grid(column=4, row=2, rowspan=4, padx=50, pady=50, sticky="nsew")

    def _logInFrame(self, MasterPanel, *args, **kwargs):
        self.logIn_frame = ttk.Frame(master=MasterPanel, *args, **kwargs)
        self.logIn_frame.columnconfigure(list(range(1, 6)), weight=1)
        self.logIn_frame.rowconfigure(list(range(1, 9)), weight=1)

        self.logIn_frame.style = ttk.Style(self.logIn_frame)
        self.logIn_frame.style.configure('TRadiobutton', font=("Helvetica", 18, "bold"), background="LightSkyBlue4",
                                         foreground='black', weight=40)
        self.logIn_frame.style.configure('TEntry', weight=100)
        labelConfigure = {'font': ("Helvetica", 18, "bold"), 'background': 'LightSkyBlue4'}
        entryConfigure = {'font': ("Helvetica", 16, "bold"), 'background': 'white'}
        gridTEntryConfigure = {'padx': 10, 'pady': 0, 'sticky': tk.W, 'ipady': 0, 'ipadx': 0}
        gridConfigure = {'padx': 5, 'pady': 0, 'sticky': tk.W}

        app_insert2DB = self.master.__dict__.get('app_insert2DB')
        if not app_insert2DB:
            print('Master have not Insert2DB instance')
            return

        def entryFocusOut(entryName):
            entry = self.logIn_frame.__dict__.get(f'Entry_User{entryName}')
            if not entry:
                return
            if not entry.get():
                entry.insert(0, entryName)
            return

        def entryButton1(entryName):
            entry = self.logIn_frame.__dict__.get(f'Entry_User{entryName}')
            if not entry:
                return
            if entry.get() == entryName:
                entry.delete(0, "end")
            return

        Label_title = ttk.Label(self.logIn_frame, text='Log In', font=("Helvetica", 60, "bold", 'underline'),
                                background="LightSkyBlue4", foreground='white')
        Label_title.grid(column=2, row=1, sticky="nsew")

        ttk.Separator(self.logIn_frame, orient=HORIZONTAL).grid(row=2, column=0, columnspan=6, ipadx=150,
                                                                sticky=tk.W + tk.E)

        # User Path researcher or patient
        self.logIn_frame.Label_UserPath = ttk.Label(self.logIn_frame, text='User', **labelConfigure)
        self.logIn_frame.Label_UserPath.grid(column=1, row=3, **gridConfigure)
        self.logIn_frame.Entry_UserPath = tk.IntVar()
        self.logIn_frame.Entry_UserPath.set(1)
        self.logIn_frame.RB_UserPath_Patient = ttk.Radiobutton(self.logIn_frame, text='Patient',
                                                               variable=self.logIn_frame.Entry_UserPath, value=1)
        self.logIn_frame.RB_UserPath_Patient.grid(column=2, row=3, **gridConfigure)

        self.logIn_frame.RB_UserPath_Researcher = ttk.Radiobutton(self.logIn_frame, text='Researcher',
                                                                  variable=self.logIn_frame.Entry_UserPath, value=0)
        self.logIn_frame.RB_UserPath_Researcher.grid(column=2, row=4, **gridConfigure)

        # User, researcher or patient Insert ID
        self.logIn_frame.Label_UserID = ttk.Label(self.logIn_frame, text='User ID:', **labelConfigure)
        self.logIn_frame.Label_UserID.grid(column=1, row=5, **gridConfigure)
        self.logIn_frame.Entry_UserID = ttk.Entry(self.logIn_frame, **entryConfigure)
        self.logIn_frame.Entry_UserID.insert(0, "ID")
        self.logIn_frame.Entry_UserID.grid(column=2, row=5, **gridTEntryConfigure)
        self.logIn_frame.Entry_UserID.bind("<FocusOut>", lambda e: entryFocusOut('ID'))
        self.logIn_frame.Entry_UserID.bind("<Button-1>", lambda e: entryButton1('ID'))

        # User researcher or patient Insert Name
        self.logIn_frame.Label_UserName = ttk.Label(self.logIn_frame, text='User Name:', **labelConfigure)
        self.logIn_frame.Label_UserName.grid(column=1, row=6, **gridConfigure)
        self.logIn_frame.Entry_UserName = ttk.Entry(self.logIn_frame, **entryConfigure)
        self.logIn_frame.Entry_UserName.insert(0, "Name")
        self.logIn_frame.Entry_UserName.grid(column=2, row=6, **gridTEntryConfigure)
        self.logIn_frame.Entry_UserName.bind("<FocusOut>", lambda e: entryFocusOut('Name'))
        self.logIn_frame.Entry_UserName.bind("<Button-1>", lambda e: entryButton1('Name'))

        # LOGIN button
        self.logIn_frame.Button_LogIn = RoundedButton(master=self.logIn_frame, text="Log In", radius=25,
                                                      btnbackground="DarkGoldenrod3",
                                                      btnforeground="black", width=250, height=60, highlightthickness=0,
                                                      font=("Helvetica", 18, "bold"), masterBackground='LightSkyBlue4')
        self.logIn_frame.Button_LogIn.grid(column=2, row=7, **gridConfigure)
        self.logIn_frame.Button_LogIn.bind("<Button-1>", lambda e: app_insert2DB.exLogIn())

        # SingIN button
        self.logIn_frame.Button_SignIN = RoundedButton(master=self.logIn_frame, text="Sign IN", radius=25,
                                                       btnbackground="DarkGoldenrod3",
                                                       btnforeground="black", width=250, height=60,
                                                       highlightthickness=0,
                                                       font=("Helvetica", 18, "bold"), masterBackground='LightSkyBlue4')
        self.logIn_frame.Button_SignIN.grid(column=2, row=8, **gridConfigure)
        self.logIn_frame.Button_SignIN.bind("<Button-1>", lambda e: app_insert2DB.exSignIN())
        return

    def raiseError(self, labelName):
        label = self.logIn_frame.__dict__.get(f'Label_User{labelName}')
        if not label:
            return
        label.config(foreground="red")
        return

    def deleteError(self, labelName):
        label = self.logIn_frame.__dict__.get(f'Label_User{labelName}')
        if not label:
            return
        label.config(foreground="black")
        return


class PatientSignInPanel(ttk.Frame):

    def __init__(self, MasterPanel):
        ttk.Frame.__init__(self, master=MasterPanel, relief=tk.RAISED, borderwidth=2)
        self.width = 0.5 * MasterPanel.width
        self.height = 0.5 * MasterPanel.height
        self.columnconfigure(list(range(1, 6)), weight=1)
        self.rowconfigure(list(range(1, 11)), weight=1)
        self._create_sub_frames(MasterPanel)

    def _create_sub_frames(self, MasterPanel):
        self.style = ttk.Style(self)
        self.style.configure('TFrame', background='white', borderwidth=10, relief='RAISED')
        self.style.configure('TNotebook', background="LightSkyBlue4", weight=50, tabmargins=[5, 5, 0, 0])
        self.style.configure('TNotebook.Tab', background="tomato3", compound=tk.LEFT,
                             font=("Helvetica", 18, "bold"), weight=50, padding=[50, 20])

        app_insert2DB = MasterPanel.__dict__.get('app_insert2DB')
        if not app_insert2DB:
            print('Master have not Insert2DB instance')
            return

        app_queries = MasterPanel.__dict__.get('app_queries')
        if not app_queries:
            print('Master have not queries instance')
            return

        def back():
            index = self.Page_Frames.index(self.Page_Frames.select())
            if index == 1:
                self.Page_Frames.select(0)
            return

        Label_title = ttk.Label(self, text='                                            Sign In',
                                font=("Helvetica", 50, "bold"),
                                background="DarkGoldenrod2", foreground='black')
        Label_title.grid(row=1, column=0, columnspan=6, ipadx=150, sticky=tk.W + tk.E)

        ttk.Separator(self, orient=HORIZONTAL).grid(row=2, column=0, columnspan=6, ipadx=150, sticky=tk.W + tk.E)

        # Back button
        self.Button_Back = RoundedButton(master=self, text="Back", radius=10, btnbackground="LightSkyBlue4",
                                         btnforeground="white", width=150, height=60, highlightthickness=0,
                                         font=("Helvetica", 18, "bold"), masterBackground='DarkGoldenrod2')
        self.Button_Back.grid(column=2, row=1, padx=5, pady=5, sticky=tk.W)
        self.Button_Back.bind("<Button-1>", lambda e: back())

        # Next button
        self.Button_Next = RoundedButton(master=self, text="Next", radius=10, btnbackground="LightSkyBlue4",
                                         btnforeground="white", width=150, height=60, highlightthickness=0,
                                         font=("Helvetica", 18, "bold"), masterBackground='DarkGoldenrod2')
        self.Button_Next.grid(column=4, row=1, padx=5, pady=5, sticky=tk.E)
        self.Button_Next.bind("<Button-1>", lambda e: app_insert2DB.validUserSignIn())

        # Return button
        self.Button_Return = RoundedButton(master=self, text="Return", radius=10, btnbackground="LightSkyBlue4",
                                           btnforeground="white", width=150, height=60, highlightthickness=0,
                                           font=("Helvetica", 18, "bold"), masterBackground='white')
        self.Button_Return.grid(column=2, row=10, padx=5, pady=5, sticky=tk.W)
        self.Button_Return.bind("<Button-1>", lambda e: app_insert2DB.exSignOut())

        self.Page_Frames = ttk.Notebook(self, width=700, height=600)
        self.Page_Frames.grid(column=2, row=3, padx=10, pady=10, sticky="nsew", columnspan=3, rowspan=2)

        self._initPatientSignInPg0(self.Page_Frames, style='TFrame')
        self.pg0.grid(column=2, row=3, padx=10, pady=10, sticky="nsew", columnspan=3, rowspan=2)

        self._initPatientSignInPg1(self.Page_Frames, style='TFrame')
        self.pg1.grid(column=2, row=3, padx=10, pady=10, sticky="nsew", columnspan=3, rowspan=2)

        self.Page_Frames.add(self.pg0, text='                Step 1                ', )
        self.Page_Frames.add(self.pg1, text='                Step 2                ')
        self.Page_Frames.select(0)
        self.Page_Frames.tab(1, state="disabled")
        return

    def _initPatientSignInPg0(self, MasterPanel, *args, **kwargs):
        self.pg0 = ttk.Frame(master=MasterPanel, *args, **kwargs)
        self.pg0.columnconfigure(list(range(1, 5)), weight=1)
        self.pg0.rowconfigure(list(range(1, 14)), weight=1)

        gridConfigure = {'padx': 20, 'pady': 0, 'sticky': tk.W}
        gridTEntryConfigure = {'padx': 20, 'pady': 0, 'sticky': tk.W, 'ipady': 5, 'ipadx': 0}
        entryConfigure = {'font': ("Helvetica", 18), 'background': 'white'}
        labelConfigure = {'font': ("Helvetica", 18, "bold"), 'background': 'white', 'borderwidth': 0}

        # ------------------------- ID ------------------------------------------
        self.pg0.Label_UserID = ttk.Label(self.pg0, text='ID: *', **labelConfigure)
        self.pg0.Label_UserID.grid(column=1, row=1, **gridConfigure)

        self.pg0.Entry_UserID = ttk.Entry(self.pg0, **entryConfigure)
        self.pg0.Entry_UserID.grid(column=1, row=2, **gridTEntryConfigure)

        # ------------------------- Name ------------------------------------------
        self.pg0.Label_UserName = ttk.Label(self.pg0, text='Name: *', **labelConfigure)
        self.pg0.Label_UserName.grid(column=1, row=3, **gridConfigure)

        self.pg0.Entry_UserName = ttk.Entry(self.pg0, **entryConfigure)
        self.pg0.Entry_UserName.grid(column=1, row=4, columnspan=2, **gridTEntryConfigure)

        # ------------------------- Gender ------------------------------------------
        self.pg0.Label_UserGender = ttk.Label(self.pg0, text='Gender: *', **labelConfigure)
        self.pg0.Label_UserGender.grid(column=1, row=5, **gridConfigure)

        self.pg0.textVariable_UserGender = tk.StringVar()
        self.pg0.Entry_UserGender = ttk.Combobox(self.pg0, textvariable=self.pg0.textVariable_UserGender,
                                                 **entryConfigure)
        self.pg0.Entry_UserGender['values'] = ('Female', 'Male')
        self.pg0.Entry_UserGender.grid(column=1, row=6, **gridTEntryConfigure)

        # ------------------------- Area ------------------------------------------
        self.pg0.Label_UserArea = ttk.Label(self.pg0, text='Area: *', **labelConfigure)
        self.pg0.Label_UserArea.grid(column=1, row=7, **gridConfigure)

        self.pg0.textVariable_UserArea = tk.StringVar()
        self.pg0.Entry_UserArea = ttk.Combobox(self.pg0, textvariable=self.pg0.textVariable_UserArea, **entryConfigure)
        self.pg0.Entry_UserArea['values'] = ('North', 'Center', 'South')
        self.pg0.Entry_UserArea.grid(column=1, row=8, **gridTEntryConfigure)

        # ------------------------- City ------------------------------------------
        self.pg0.Label_UserCity = ttk.Label(self.pg0, text='City: *', **labelConfigure)
        self.pg0.Label_UserCity.grid(column=1, row=9, **gridConfigure)

        self.pg0.Entry_UserCity = ttk.Entry(self.pg0, **entryConfigure)
        self.pg0.Entry_UserCity.grid(column=1, row=10, columnspan=2, **gridTEntryConfigure)

        # ------------------------- Phone ------------------------------------------
        self.pg0.Label_UserPhone = ttk.Label(self.pg0, text='Phone: *', **labelConfigure)
        self.pg0.Label_UserPhone.grid(column=1, row=11, **gridConfigure)

        self.pg0.Entry_UserPhone = ttk.Entry(self.pg0, **entryConfigure)
        self.pg0.Entry_UserPhone.grid(column=1, row=12, columnspan=2, **gridTEntryConfigure)

        # ------------------------- Separator ------------------------------------------
        ttk.Separator(self.pg0, orient=VERTICAL).grid(row=1, column=2, rowspan=13, ipady=150, sticky=tk.N + tk.S + tk.E)

        # ------------------------- DOB ------------------------------------------
        self.pg0.Label_UserDOB = ttk.Label(self.pg0, text='Date of Birth: *', **labelConfigure)
        self.pg0.Label_UserDOB.grid(column=3, row=1, **gridConfigure)

        self.pg0.Entry_UserDOB = DateEntry(self.pg0, selectmode='day', date_pattern='MM-dd-yyyy',
                                           font=("Helvetica", 18, "bold"),
                                           firstweekday='sunday', weekenddays=[6, 7], background='LightSkyBlue4',
                                           foreground='white')
        self.pg0.Entry_UserDOB.grid(column=3, row=2, **gridConfigure)

        # ------------------------- HMO ------------------------------------------
        self.pg0.Label_UserHMO = ttk.Label(self.pg0, text='HMO: *', **labelConfigure)
        self.pg0.Label_UserHMO.grid(column=3, row=3, **gridConfigure)

        self.pg0.textVariable_UserHMO = tk.StringVar()
        self.pg0.Entry_UserHMO = ttk.Combobox(self.pg0, textvariable=self.pg0.textVariable_UserHMO, **entryConfigure)
        self.pg0.Entry_UserHMO['values'] = ('Clalit', 'Maccabi', 'Meuhedet', 'Leumit')
        self.pg0.Entry_UserHMO.grid(column=3, row=4, **gridTEntryConfigure)

        # ------------------------- COB ------------------------------------------
        self.pg0.Label_UserCOB = ttk.Label(self.pg0, text='Country Of Birth:', **labelConfigure)
        self.pg0.Label_UserCOB.grid(column=3, row=5, **gridConfigure)

        self.pg0.Entry_UserCOB = ttk.Entry(self.pg0, **entryConfigure)
        self.pg0.Entry_UserCOB.insert(0, 'Israel')
        self.pg0.Entry_UserCOB.grid(column=3, row=6, **gridTEntryConfigure)
        self.pg0.Entry_UserCOB.bind("<Button-1>", lambda e: self.entryButton1('COB'))
        self.pg0.Entry_UserCOB.bind("<FocusOut>", lambda e: self.entryFocusOut('COB'))

        # ------------------------- Height ------------------------------------------
        self.pg0.Label_UserHeight = ttk.Label(self.pg0, text='Height: *', **labelConfigure)
        self.pg0.Label_UserHeight.grid(column=3, row=7, **gridConfigure)

        self.pg0.Entry_UserHeight = tk.Entry(self.pg0, **entryConfigure)
        self.pg0.Entry_UserHeight.grid(column=3, row=8, **gridTEntryConfigure)

        # ------------------------- Weight ------------------------------------------
        self.pg0.Label_UserWeight = ttk.Label(self.pg0, text='Weight: *', **labelConfigure)
        self.pg0.Label_UserWeight.grid(column=3, row=9, **gridConfigure)

        self.pg0.Entry_UserWeight = ttk.Entry(self.pg0, **entryConfigure)
        self.pg0.Entry_UserWeight.grid(column=3, row=10, **gridTEntryConfigure)

        # ------------------------- Support ------------------------------------------
        self.pg0.Label_UserSupport = ttk.Label(self.pg0, text='Support: *', **labelConfigure)
        self.pg0.Label_UserSupport.grid(column=3, row=11, **gridConfigure)

        self.pg0.textVariable_UserSupport = tk.StringVar()
        self.pg0.Entry_UserSupport = ttk.Combobox(self.pg0, textvariable=self.pg0.textVariable_UserSupport,
                                                  **entryConfigure)
        self.pg0.Entry_UserSupport['values'] = ('Yes', 'No')
        self.pg0.Entry_UserSupport.grid(column=3, row=12, **gridTEntryConfigure)
        return

    def _initPatientSignInPg1(self, MasterPanel, *args, **kwargs):
        self.pg1 = ttk.Frame(master=MasterPanel, *args, **kwargs)
        self.pg1.columnconfigure(list(range(1, 7)), weight=1)
        self.pg1.rowconfigure(list(range(1, 9)), weight=1)

        entryConfigure = {'font': ("Helvetica", 18), 'background': 'white'}
        labelConfigure = {'font': ("Helvetica", 18, "bold"), 'background': 'white', 'borderwidth': 0}
        s = ttk.Style()
        s.configure('Custom.Treeview', rowheight=30, highlightthickness=2, bd=0, font=('Helvetica', 18))
        s.map("Custom.Treeview", background=[("selected", "ivory4")])

        # ------------------------- Enter Symptoms ------------------------------------------
        self.pg1.Label_UserSymptoms = ttk.Label(self.pg1, text='Symptoms:', **labelConfigure)
        self.pg1.Label_UserSymptoms.grid(column=1, row=1, columnspan=2, sticky=tk.W + tk.N, padx=5, pady=10)

        self.pg1.Entry_UserSymptoms = ttk.Entry(self.pg1, textvariable=tk.StringVar(), width=40, **entryConfigure)
        self.pg1.Entry_UserSymptoms.grid(column=1, row=2, columnspan=2, sticky=tk.W + tk.N + tk.E, padx=5)

        self.pg1.Listbox_UserSymptoms = tk.Listbox(self.pg1, selectmode=tk.EXTENDED, font=("Helvetica", 18),
                                                   bg='white', highlightcolor='white', highlightthickness=0,
                                                   relief='flat', width=40)
        self.pg1.Listbox_UserSymptoms.grid(column=1, row=3, columnspan=2, rowspan=3, sticky=tk.W + tk.N + tk.E, padx=5,
                                           pady=10)

        self.pg1.Button_select = RoundedButton(master=self.pg1, text="Select", radius=10,
                                               btnbackground="seashell3",
                                               btnforeground="black", width=80, height=60, highlightthickness=0,
                                               font=("Helvetica", 18, "bold"), masterBackground='white')
        self.pg1.Button_select.grid(column=1, row=7, sticky=tk.W + tk.N + tk.E)

        # ------------------------- Separator ------------------------------------------
        ttk.Separator(self.pg1, orient=VERTICAL).grid(row=2, column=3, rowspan=7, ipady=150, sticky=tk.N + tk.S)

        # ------------------------- Selected Symptoms ------------------------------------------

        self.pg1.Label_UserSelectSymptoms = ttk.Label(self.pg1, text='Selected Symptoms:', **labelConfigure)
        self.pg1.Label_UserSelectSymptoms.grid(column=4, row=1, columnspan=2, sticky=tk.W + tk.N, pady=10, padx=10)

        self.pg1.Table_UserSelectSymptoms = ttk.Treeview(self.pg1, selectmode='browse', style='Custom.Treeview')
        self.pg1.Table_UserSelectSymptoms['columns'] = ['Symptoms']
        self.pg1.Table_UserSelectSymptoms.column("#0", width=0, stretch=tk.NO)
        self.pg1.Table_UserSelectSymptoms.column('Symptoms', anchor=tk.W, width=400)

        self.pg1.Table_UserSelectSymptoms.grid(column=4, row=3, columnspan=3, rowspan=3, sticky=tk.W + tk.N + tk.E)
        self.pg1.Table_UserSelectSymptoms.tag_configure('odd', background='snow2')
        self.pg1.Table_UserSelectSymptoms.tag_configure('even', background='white')

        self.pg1.Button_deleteSelect = RoundedButton(master=self.pg1, text="Delete Selected", radius=10,
                                                     btnbackground="seashell3",
                                                     btnforeground="black", width=80, height=60, highlightthickness=0,
                                                     font=("Helvetica", 18, "bold"), masterBackground='white')
        self.pg1.Button_deleteSelect.grid(column=4, row=7, sticky=tk.W + tk.N + tk.E)

        temp = self.master.__dict__.get('symptomsTrie')
        if temp:
            self.AutoComplete = AUTO_complete(temp, self.pg1.Entry_UserSymptoms, self.pg1.Listbox_UserSymptoms,
                                              treeview=self.pg1.Table_UserSelectSymptoms,
                                              select=self.pg1.Button_select, deleteSelect=self.pg1.Button_deleteSelect)

        # ------------------------- SignIN ------------------------------------------
        self.pg1.Button_SignIN = RoundedButton(master=self.pg1, text="Sign In", radius=10,
                                               btnbackground="LightSkyBlue4",
                                               btnforeground="white", width=150, height=60, highlightthickness=0,
                                               font=("Helvetica", 18, "bold"), masterBackground='white')
        self.pg1.Button_SignIN.grid(column=6, row=8, sticky=tk.E + tk.S + tk.W)
        app_insert2DB = self.master.__dict__.get('app_insert2DB')
        self.pg1.Button_SignIN.bind("<Button-1>", lambda e: app_insert2DB.validUserSignIn())
        self.pg1.Var_conifer = tk.IntVar()
        self.pg1.Entry_conifer = tk.Checkbutton(self.pg1, text="I agree to the terms",
                                                variable=self.pg1.Var_conifer,
                                                onvalue=1, offvalue=0, width=20, background="white",
                                                font=("Helvetica", 12), foreground='black')
        self.pg1.Entry_conifer.grid(column=6, row=9, sticky=tk.E + tk.S + tk.W)
        return

    def raiseError(self, pgIndex, labelName=None):
        pg = self.__dict__.get(f'pg{pgIndex}')
        if not pg:
            return
        if pgIndex == 0 and labelName is not None:
            label = pg.__dict__.get(f'Label_User{labelName}')
            if not label:
                return
            label.config(foreground="red")
            return
        entry = pg.__dict__.get('Entry_conifer')
        if not entry:
            return
        entry.configure(foreground='red', font=("Helvetica", 12, "bold", 'underline'))
        return

    def deleteError(self, pgIndex, labelName=None):
        pg = self.__dict__.get(f'pg{pgIndex}')
        if not pg:
            return
        if pgIndex == 0 and labelName is not None:
            label = pg.__dict__.get(f'Label_User{labelName}')
            if not label:
                return
            label.config(foreground="black")
            return
        entry = pg.__dict__.get('Entry_conifer')
        if not entry:
            return
        entry.configure(foreground='black', font=("Helvetica", 12))
        return

    def entryButton1(self, EntryName):
        index = self.Page_Frames.index(self.Page_Frames.select())
        entry = self.__dict__[f'pg{index}'].__dict__.get(f'Entry_User{EntryName}')
        if not entry:
            return
        if EntryName == 'COB' and entry.get() == 'Israel':
            entry.delete(0, "end")
            return
        return

    def entryFocusOut(self, EntryName):
        index = self.Page_Frames.index(self.Page_Frames.select())
        entry = self.__dict__[f'pg{index}'].__dict__.get(f'Entry_User{EntryName}')
        if not entry:
            return
        if not entry.get() and EntryName == 'COB':
            entry.insert(0, 'Israel')
            return
        return


class PatientMainPanel(ttk.Frame):

    def __init__(self, MasterPanel):
        ttk.Frame.__init__(self, master=MasterPanel, relief=tk.RAISED, borderwidth=2)
        self.width = 0.5 * MasterPanel.width
        self.height = 0.5 * MasterPanel.height
        self.columnconfigure(list(range(1, 5)), weight=1)
        self.rowconfigure(list(range(1, 6)), weight=1)
        self._create_sub_frames(MasterPanel)

    def _create_sub_frames(self, MasterPanel):
        self.style = ttk.Style(self)
        self.style.configure('TFrame', background='white', borderwidth=10, relief='RAISED')
        self.style.configure('TNotebook', background="LightSkyBlue4", weight=50, tabmargins=[5, 5, 0, 0])
        self.style.configure('TNotebook.Tab', background="tomato3", compound=tk.LEFT,
                             font=("Helvetica", 18, "bold"), weight=50, padding=[50, 20])

        app_insert2DB = MasterPanel.__dict__.get('app_insert2DB')
        if not app_insert2DB:
            print('Master have not Insert2DB instance')
            return

        app_queries = MasterPanel.__dict__.get('app_queries')
        if not app_queries:
            print('Master have not queries instance')
            return

        Label_title = ttk.Label(self, text=' ',
                                font=("Helvetica", 50, "bold"),
                                background="DarkGoldenrod2", foreground='black')
        Label_title.grid(row=0, column=0, columnspan=11, ipadx=150, sticky=tk.W + tk.E)

        ttk.Separator(self, orient=HORIZONTAL).grid(row=1, column=0, columnspan=11, ipadx=150,
                                                    sticky=tk.W + tk.E + tk.N)
        self.Button_SignOut = RoundedButton(master=self, text="Sign Out", radius=10, btnbackground="LightSkyBlue4",
                                            btnforeground="white", width=150, height=60, highlightthickness=0,
                                            font=("Helvetica", 18, "bold"), masterBackground='DarkGoldenrod2')
        self.Button_SignOut.grid(column=0, row=0, padx=5, pady=5, sticky=tk.W)
        self.Button_SignOut.bind("<Button-1>", lambda e: app_insert2DB.exSignOut())

        self.Button_Refresh = RoundedButton(master=self, text="Refresh", radius=10,
                                            btnbackground="LightSkyBlue4",
                                            btnforeground="white", width=150, height=60, highlightthickness=0,
                                            font=("Helvetica", 18, "bold"), masterBackground='DarkGoldenrod2')
        self.Button_Refresh.grid(column=1, row=0, padx=5, pady=5, sticky=tk.W)
        self.Button_Refresh.bind('<Button-1>', lambda e: self.buttonRefresh())

        self.Button_DisConnect = RoundedButton(master=self, text="DisConnect", radius=10, btnbackground="LightSkyBlue4",
                                               btnforeground="white", width=150, height=60, highlightthickness=0,
                                               font=("Helvetica", 18, "bold"), masterBackground='DarkGoldenrod2')
        self.Button_DisConnect.grid(column=5, row=0, padx=5, pady=5, sticky=tk.E)
        self.Button_DisConnect.bind("<Button-1>", lambda e: app_insert2DB.exDisConnect())
        return self._initNoteBook()

    def _initNoteBook(self):
        index = 0
        if self.__dict__.get('Page_Frames'):
            Page_Frames = self.__dict__.get('Page_Frames')
            index = Page_Frames.index(Page_Frames.select())
            Page_Frames.destroy()
        self.Page_Frames = ttk.Notebook(self, width=800, height=600)
        self.Page_Frames.grid(column=1, row=2, padx=1, pady=1, sticky="nsew", columnspan=3, rowspan=3)

        self._initPatientMainPg0(self.Page_Frames, style='TFrame')
        self.pg0.grid(column=2, row=3, padx=10, pady=10, sticky="nsew", columnspan=3, rowspan=2)
        self._initPatientMainPg1(self.Page_Frames, style='TFrame')
        self.pg1.grid(column=2, row=3, padx=10, pady=10, sticky="nsew", columnspan=3, rowspan=2)
        self._initPatientMainPg2(self.Page_Frames, style='TFrame')
        self.pg2.grid(column=2, row=3, padx=10, pady=10, sticky="nsew", columnspan=3, rowspan=2)
        self.Page_Frames.add(self.pg0, text='                Profile                ', )
        self.Page_Frames.add(self.pg1, text='                Symptoms                ')
        self.Page_Frames.add(self.pg2, text='                Available Researches                ')
        self.Page_Frames.select(index)
        return

    def _initPatientMainPg0(self, MasterPanel, *args, **kwargs):
        UserIndices = self.master.__dict__.get('app_queries').dequeueUserIndices('PatientMainPg0')
        self.pg0 = ttk.Frame(master=MasterPanel, *args, **kwargs)
        self.pg0.columnconfigure(list(range(1, 10)), weight=1)
        self.pg0.rowconfigure(list(range(1, 14)), weight=1)
        self.pg0.UserIndices = UserIndices

        gridConfigure = {'padx': 5, 'pady': 5, 'sticky': tk.W}
        gridTEntryConfigure = {'padx': 5, 'pady': 0, 'sticky': tk.W, 'ipady': 0, 'ipadx': 0}
        entryConfigure = {'font': ("Helvetica", 18), 'background': 'white'}
        labelConfigure = {'font': ("Helvetica", 18, "bold"), 'background': 'white', 'borderwidth': 0,
                          'foreground': 'LightSkyBlue4'}
        s = ttk.Style()
        s.configure('Custom.Treeview', rowheight=30, highlightthickness=2, bd=0, font=('Helvetica', 18))
        s.configure('Custom.Treeview.Heading', background='seashell3', foreground='black',
                    font=('Helvetica', 18, 'bold'))
        s.map("Custom.Treeview", background=[("selected", "ivory4")])

        Indices = self.pg0.UserIndices['Indices']
        researchers = self.pg0.UserIndices['researchers']
        # ------------------------- ID ------------------------------------------
        self.pg0.Label_UserID = ttk.Label(self.pg0, text='ID:', **labelConfigure)
        self.pg0.Label_UserID.grid(column=1, row=1, **gridConfigure)

        self.pg0.Entry_UserID = ttk.Entry(self.pg0, **entryConfigure)
        self.pg0.Entry_UserID.grid(column=1, row=2, **gridTEntryConfigure)
        self.pg0.Entry_UserID.insert(0, Indices['ID'])
        self.pg0.Entry_UserID.config(state="disabled")

        # ------------------------- Name ------------------------------------------
        self.pg0.Label_UserName = ttk.Label(self.pg0, text='Name:', **labelConfigure)
        self.pg0.Label_UserName.grid(column=1, row=3, **gridConfigure)

        self.pg0.Entry_UserName = ttk.Entry(self.pg0, **entryConfigure)
        self.pg0.Entry_UserName.grid(column=1, row=4, columnspan=2, **gridTEntryConfigure)
        self.pg0.Entry_UserName.insert(0, Indices['name'])
        self.pg0.Entry_UserName.config(state="disabled")

        # ------------------------- Gender ------------------------------------------
        self.pg0.Label_UserGender = ttk.Label(self.pg0, text='Gender:', **labelConfigure)
        self.pg0.Label_UserGender.grid(column=1, row=5, **gridConfigure)

        self.pg0.Entry_UserGender = ttk.Entry(self.pg0, **entryConfigure)
        self.pg0.Entry_UserGender.grid(column=1, row=6, **gridTEntryConfigure)
        self.pg0.Entry_UserGender.insert(0, Indices['gender'])
        self.pg0.Entry_UserGender.config(state="disabled")

        # ------------------------- Area ------------------------------------------
        self.pg0.Label_UserArea = ttk.Label(self.pg0, text='Area:', **labelConfigure)
        self.pg0.Label_UserArea.grid(column=1, row=7, **gridConfigure)

        area = ''
        for val in ('North', 'Center', 'South'):
            if Indices['area'][0] == val[0]:
                area = val
                break
        self.pg0.textVariable_UserArea = tk.StringVar(value=area)
        self.pg0.Entry_UserArea = ttk.Combobox(self.pg0, textvariable=self.pg0.textVariable_UserArea, **entryConfigure)
        self.pg0.Entry_UserArea['values'] = ('North', 'Center', 'South')
        self.pg0.Entry_UserArea.grid(column=1, row=8, **gridTEntryConfigure)

        # ------------------------- City ------------------------------------------
        self.pg0.Label_UserCity = ttk.Label(self.pg0, text='City:', **labelConfigure)
        self.pg0.Label_UserCity.grid(column=1, row=9, **gridConfigure)

        self.pg0.Entry_UserCity = ttk.Entry(self.pg0, **entryConfigure)
        self.pg0.Entry_UserCity.grid(column=1, row=10, columnspan=2, **gridTEntryConfigure)
        self.pg0.Entry_UserCity.insert(0, Indices['city'])

        # ------------------------- Phone ------------------------------------------
        self.pg0.Label_UserPhone = ttk.Label(self.pg0, text='Phone:', **labelConfigure)
        self.pg0.Label_UserPhone.grid(column=1, row=11, **gridConfigure)

        self.pg0.Entry_UserPhone = ttk.Entry(self.pg0, **entryConfigure)
        self.pg0.Entry_UserPhone.grid(column=1, row=12, columnspan=2, **gridTEntryConfigure)
        self.pg0.Entry_UserPhone.insert(0, Indices['phone'])

        # ------------------------- Separator ------------------------------------------
        ttk.Separator(self.pg0, orient=VERTICAL).grid(row=1, column=1, rowspan=13, ipady=150, sticky=tk.N + tk.S + tk.E)

        # ------------------------- DOB ------------------------------------------
        self.pg0.Label_UserDOB = ttk.Label(self.pg0, text='Date of Birth:', **labelConfigure)
        self.pg0.Label_UserDOB.grid(column=2, row=1, **gridConfigure)

        self.pg0.Entry_UserDOB = ttk.Entry(self.pg0, **entryConfigure)
        self.pg0.Entry_UserDOB.grid(column=2, row=2, **gridConfigure)
        self.pg0.Entry_UserDOB.insert(0, Indices['DOB'])
        self.pg0.Entry_UserDOB.config(state="disabled")

        # ------------------------- HMO ------------------------------------------
        self.pg0.Label_UserHMO = ttk.Label(self.pg0, text='HMO:', **labelConfigure)
        self.pg0.Label_UserHMO.grid(column=2, row=3, **gridConfigure)

        self.pg0.textVariable_UserHMO = tk.StringVar(value=Indices['HMO'])
        self.pg0.Entry_UserHMO = ttk.Combobox(self.pg0, textvariable=self.pg0.textVariable_UserHMO, **entryConfigure)
        self.pg0.Entry_UserHMO['values'] = ('Clalit', 'Maccabi', 'Meuhedet', 'Leumit')
        self.pg0.Entry_UserHMO.grid(column=2, row=4, **gridTEntryConfigure)

        # ------------------------- COB ------------------------------------------
        self.pg0.Label_UserCOB = ttk.Label(self.pg0, text='Country Of Birth:', **labelConfigure)
        self.pg0.Label_UserCOB.grid(column=2, row=5, **gridConfigure)

        self.pg0.Entry_UserCOB = ttk.Entry(self.pg0, **entryConfigure)
        self.pg0.Entry_UserCOB.insert(0, Indices['COB'])
        self.pg0.Entry_UserCOB.grid(column=2, row=6, **gridTEntryConfigure)
        self.pg0.Entry_UserCOB.config(state="disabled")

        # ------------------------- Height ------------------------------------------
        self.pg0.Label_UserHeight = ttk.Label(self.pg0, text='Height:', **labelConfigure)
        self.pg0.Label_UserHeight.grid(column=2, row=7, **gridConfigure)

        self.pg0.Entry_UserHeight = tk.Entry(self.pg0, **entryConfigure)
        self.pg0.Entry_UserHeight.grid(column=2, row=8, **gridTEntryConfigure)
        self.pg0.Entry_UserHeight.insert(0, Indices['height'])

        # ------------------------- Weight ------------------------------------------
        self.pg0.Label_UserWeight = ttk.Label(self.pg0, text='Weight:', **labelConfigure)
        self.pg0.Label_UserWeight.grid(column=2, row=9, **gridConfigure)

        self.pg0.Entry_UserWeight = ttk.Entry(self.pg0, **entryConfigure)
        self.pg0.Entry_UserWeight.grid(column=2, row=10, **gridTEntryConfigure)
        self.pg0.Entry_UserWeight.insert(0, Indices['weight'])

        # ------------------------- Support ------------------------------------------
        self.pg0.Label_UserSupport = ttk.Label(self.pg0, text='Support:', **labelConfigure)
        self.pg0.Label_UserSupport.grid(column=2, row=11, **gridConfigure)

        sup = Indices['support']
        if sup == '1':
            sup = 'Yes'
        else:
            sup = 'No'
        self.pg0.textVariable_UserSupport = tk.StringVar(value=sup)
        self.pg0.Entry_UserSupport = ttk.Combobox(self.pg0, textvariable=self.pg0.textVariable_UserSupport,
                                                  **entryConfigure)
        self.pg0.Entry_UserSupport['values'] = ('Yes', 'No')
        self.pg0.Entry_UserSupport.grid(column=2, row=12, **gridTEntryConfigure)

        # ------------------------- Separator ------------------------------------------
        ttk.Separator(self.pg0, orient=VERTICAL).grid(row=1, column=3, rowspan=13, ipady=150, sticky=tk.N + tk.S)

        # ------------------------- Researchers ------------------------------------------

        self.pg0.Label_Researchers = ttk.Label(self.pg0, text='Researchers in which you participate:', **labelConfigure)
        self.pg0.Label_Researchers.grid(column=5, row=1, columnspan=3, sticky=tk.N + tk.W + tk.E, pady=5, padx=5)

        self.pg0.Table_Researchers = ttk.Treeview(self.pg0, style='Custom.Treeview')
        self.pg0.Table_Researchers['columns'] = list(researchers.columns)
        self.pg0.Table_Researchers.column("#0", width=0, stretch=tk.NO)
        for col in list(researchers.columns):
            w = 100
            if col == 'Mail':
                w = 200
            self.pg0.Table_Researchers.column(col, anchor=tk.CENTER, width=w, stretch=True)
            self.pg0.Table_Researchers.heading(col, text=col, anchor=tk.CENTER)
        for row in researchers.index:
            vals = list(researchers.loc[row, :])
            if row % 2:
                self.pg0.Table_Researchers.insert(parent='', index='end', iid=int(row), text='', values=vals,
                                                  tags=('even',))
            else:
                self.pg0.Table_Researchers.insert(parent='', index='end', iid=int(row), text='', values=vals,
                                                  tags=('odd',))

        self.pg0.Table_Researchers.tag_configure('odd', background='snow2')
        self.pg0.Table_Researchers.tag_configure('even', background='white')
        self.pg0.Table_Researchers.grid(column=5, row=3, columnspan=5, rowspan=9, sticky=tk.N + tk.W + tk.E, pady=5)

        self.pg0.Button_UpDate = RoundedButton(master=self.pg0, text="UPDATE", radius=10, btnbackground="LightSkyBlue4",
                                               btnforeground="white", width=150, height=60, highlightthickness=0,
                                               font=("Helvetica", 18, "bold"), masterBackground='white')
        self.pg0.Button_UpDate.grid(column=9, row=14, padx=5, pady=5, sticky=tk.W)
        self.pg0.Button_UpDate.bind('<Button-1>', lambda e: self.buttonUpDate())
        return

    def _initPatientMainPg1(self, MasterPanel, *args, **kwargs):
        UserSymptoms = self.master.__dict__.get('app_queries').dequeueUserIndices('PatientMainPg1')
        self.pg1 = ttk.Frame(master=MasterPanel, *args, **kwargs)
        self.pg1.columnconfigure(list(range(1, 9)), weight=1)
        self.pg1.rowconfigure(list(range(1, 14)), weight=1)

        entryConfigure = {'font': ("Helvetica", 18), 'background': 'white'}
        labelConfigure = {'font': ("Helvetica", 18, "bold"), 'background': 'white', 'borderwidth': 0,
                          'foreground': 'LightSkyBlue4'}
        s = ttk.Style()
        s.configure('Custom.Treeview', rowheight=30, highlightthickness=2, bd=0, font=('Helvetica', 18))
        s.map("Custom.Treeview", background=[("selected", "ivory4")])

        # ------------------------- Symptoms ------------------------------------------

        self.pg1.Label_UserSymptoms = ttk.Label(self.pg1, text='Your Symptoms:', **labelConfigure)
        self.pg1.Label_UserSymptoms.grid(column=1, row=1, columnspan=3, sticky=tk.W + tk.N, padx=10, pady=10)

        self.pg1.Table_UserSymptoms = ttk.Treeview(self.pg1, style='Custom.Treeview')
        self.pg1.Table_UserSymptoms['columns'] = ['Symptoms']
        self.pg1.Table_UserSymptoms.column("#0", width=0, stretch=tk.NO)
        self.pg1.Table_UserSymptoms.column('Symptoms', anchor=tk.W, width=400)

        self.pg1.Table_UserSymptoms.tag_configure('odd', background='snow2')
        self.pg1.Table_UserSymptoms.tag_configure('even', background='white')

        self.pg1.Table_UserSymptoms.grid(column=1, row=2, columnspan=3, rowspan=4, sticky=tk.W + tk.E, padx=10)

        self.pg1.Button_deleteSelect = RoundedButton(master=self.pg1, text="Delete Selected", radius=10,
                                                     btnbackground="LightSkyBlue4",
                                                     btnforeground="white", width=80, height=60, highlightthickness=0,
                                                     font=("Helvetica", 18, "bold"), masterBackground='white')
        self.pg1.Button_deleteSelect.grid(column=1, row=6, sticky=tk.W + tk.E)

        # ------------------------- Separator ------------------------------------------
        ttk.Separator(self.pg1, orient=VERTICAL).grid(row=1, column=4, rowspan=13, ipady=150, sticky=tk.N + tk.S)

        # ------------------------- New Symptoms ------------------------------------------

        self.pg1.Label_NewUserSymptoms = ttk.Label(self.pg1, text='Search for Symptoms:', **labelConfigure)
        self.pg1.Label_NewUserSymptoms.grid(column=5, row=1, columnspan=2, sticky=tk.W + tk.N, pady=10, padx=10)

        self.pg1.Entry_UserSymptomsNew = ttk.Entry(self.pg1, textvariable=tk.StringVar(), width=40,
                                                   **entryConfigure)
        self.pg1.Entry_UserSymptomsNew.grid(column=5, row=2, columnspan=2, rowspan=2, sticky=tk.W + tk.N + tk.E)

        self.pg1.Listbox_NewUserSymptoms = tk.Listbox(self.pg1, selectmode=tk.EXTENDED, font=("Helvetica", 18),
                                                      bg='white', highlightcolor='LightSkyBlue4', highlightthickness=1,
                                                      relief='flat', width=40)
        self.pg1.Listbox_NewUserSymptoms.grid(column=5, row=3, columnspan=2, rowspan=3, sticky=tk.W + tk.E, padx=10)

        self.pg1.Button_select = RoundedButton(master=self.pg1, text="Select", radius=10,
                                               btnbackground="LightSkyBlue4",
                                               btnforeground="white", width=80, height=60, highlightthickness=0,
                                               font=("Helvetica", 18, "bold"), masterBackground='white')
        self.pg1.Button_select.grid(column=5, row=6, sticky=tk.W + tk.E)

        temp = self.master.__dict__.get('symptomsTrie')
        if temp:
            self.AutoComplete = AUTO_complete(temp, self.pg1.Entry_UserSymptomsNew, self.pg1.Listbox_NewUserSymptoms,
                                              treeview=self.pg1.Table_UserSymptoms,
                                              select=self.pg1.Button_select, deleteSelect=self.pg1.Button_deleteSelect,
                                              initSymptoms=UserSymptoms)

        self.pg1.Button_UpDate = RoundedButton(master=self.pg1, text="UPDATE", radius=10, btnbackground="LightSkyBlue4",
                                               btnforeground="white", width=150, height=60, highlightthickness=0,
                                               font=("Helvetica", 18, "bold"), masterBackground='white')
        self.pg1.Button_UpDate.grid(column=9, row=14, padx=5, pady=5, sticky=tk.W)
        self.pg1.Button_UpDate.bind('<Button-1>', lambda e: self.buttonUpDate())
        return

    def _initPatientMainPg2(self, MasterPanel, *args, **kwargs):
        availableResearch = self.master.__dict__.get('app_queries').dequeueUserIndices('PatientMainPg2')
        self.pg2 = ttk.Frame(master=MasterPanel, *args, **kwargs)
        self.pg2.columnconfigure(list(range(1, 5)), weight=1)
        self.pg2.rowconfigure(list(range(1, 7)), weight=1)
        self.pg2.availableResearch = availableResearch

        labelConfigure = {'font': ("Helvetica", 18, "bold"), 'background': 'white', 'borderwidth': 0,
                          'foreground': 'LightSkyBlue4'}
        s = ttk.Style()
        s.configure('Custom.Treeview', rowheight=30, highlightthickness=2, bd=0, font=('Helvetica', 18))
        s.configure('Custom.Treeview.Heading', background='seashell3', foreground='black',
                    font=('Helvetica', 18, 'bold'))
        s.map("Custom.Treeview", background=[("selected", "ivory4")])
        # ------------------------- Researchers ------------------------------------------

        self.pg2.Label_Researchers = ttk.Label(self.pg2, text='Available Researchers for you:', **labelConfigure)
        self.pg2.Label_Researchers.grid(column=1, row=1, columnspan=3, sticky=tk.W, pady=5, padx=5)

        self.pg2.Table_AvailableResearch = ttk.Treeview(self.pg2, style='Custom.Treeview')
        self.pg2.Table_AvailableResearch['columns'] = list(availableResearch.columns)
        self.pg2.Table_AvailableResearch.column("#0", width=0, stretch=tk.NO)
        for col in list(availableResearch.columns):
            w = 100
            if col == 'Mail':
                w = 200
            self.pg2.Table_AvailableResearch.column(col, anchor=tk.CENTER, width=w)
            self.pg2.Table_AvailableResearch.heading(col, text=col, anchor=tk.CENTER)

        for row in availableResearch.index:
            vals = list(availableResearch.loc[row, :])
            if row % 2:
                self.pg2.Table_AvailableResearch.insert(parent='', index='end', iid=int(row), text='',
                                                        values=vals, tags=('even',))
            else:
                self.pg2.Table_AvailableResearch.insert(parent='', index='end', iid=int(row), text='',
                                                        values=vals, tags=('odd',))

        self.pg2.Table_AvailableResearch.tag_configure('odd', background='snow2')
        self.pg2.Table_AvailableResearch.tag_configure('even', background='white')

        self.pg2.Table_AvailableResearch.grid(column=1, row=2, columnspan=4, rowspan=3, sticky=tk.W + tk.E, padx=5)
        return

    def buttonUpDate(self):
        app_insert2DB = self.master.__dict__.get('app_insert2DB')
        if not app_insert2DB:
            return
        if app_insert2DB.updateUserIndices():
            return self.buttonRefresh()
        return

    def buttonRefresh(self):
        app_queries = self.master.__dict__.get('app_queries')
        app_queries.activateLogIn('active', None, None)
        return self._initNoteBook()

    def raiseError(self, pgIndex, labelName=None):
        pg = self.__dict__.get(f'pg{pgIndex}')
        if not pg:
            return
        label = pg.__dict__.get(f'Label_User{labelName}')
        if not label:
            return
        label.config(foreground="red")
        return

    def deleteError(self, pgIndex, labelName=None):
        pg = self.__dict__.get(f'pg{pgIndex}')
        if not pg:
            return
        label = pg.__dict__.get(f'Label_User{labelName}')
        if not label:
            return
        label.config(foreground="black")
        return


class ResearcherSignInPanel(ttk.Frame):
    def __init__(self, MasterPanel):
        ttk.Frame.__init__(self, master=MasterPanel, relief=tk.RAISED, borderwidth=2)
        self.width = 0.5 * MasterPanel.width
        self.height = 0.5 * MasterPanel.height
        self.columnconfigure(list(range(1, 6)), weight=1)
        self.rowconfigure(list(range(1, 11)), weight=1)
        self._create_sub_frames(MasterPanel)

    def _create_sub_frames(self, MasterPanel):
        self.style = ttk.Style(self)
        self.style.configure('TFrame', background='white', borderwidth=10, relief='RAISED')
        self.style.configure('TNotebook', background="LightSkyBlue4", weight=50, tabmargins=[5, 5, 0, 0])
        self.style.configure('TNotebook.Tab', background="tomato3", compound=tk.LEFT,
                             font=("Helvetica", 18, "bold"), weight=50, padding=[50, 20])

        app_insert2DB = MasterPanel.__dict__.get('app_insert2DB')
        if not app_insert2DB:
            print('Master have not Insert2DB instance')
            return

        app_queries = MasterPanel.__dict__.get('app_queries')
        if not app_queries:
            print('Master have not queries instance')
            return

        def back():
            index = self.Page_Frames.index(self.Page_Frames.select())
            if index == 1:
                self.Page_Frames.select(0)
            return

        Label_title = ttk.Label(self, text='                                            Sign In',
                                font=("Helvetica", 50, "bold"),
                                background="DarkGoldenrod2", foreground='black')
        Label_title.grid(row=1, column=0, columnspan=6, ipadx=150, sticky=tk.W + tk.E)

        ttk.Separator(self, orient=HORIZONTAL).grid(row=2, column=0, columnspan=6, ipadx=150, sticky=tk.W + tk.E)

        # Back button
        self.Button_Back = RoundedButton(master=self, text="Back", radius=10, btnbackground="LightSkyBlue4",
                                         btnforeground="white", width=150, height=60, highlightthickness=0,
                                         font=("Helvetica", 18, "bold"), masterBackground='DarkGoldenrod2')
        self.Button_Back.grid(column=2, row=1, padx=5, pady=5, sticky=tk.W)
        self.Button_Back.bind("<Button-1>", lambda e: back())

        # Next button
        self.Button_Next = RoundedButton(master=self, text="Next", radius=10, btnbackground="LightSkyBlue4",
                                         btnforeground="white", width=150, height=60, highlightthickness=0,
                                         font=("Helvetica", 18, "bold"), masterBackground='DarkGoldenrod2')
        self.Button_Next.grid(column=4, row=1, padx=5, pady=5, sticky=tk.E)
        self.Button_Next.bind("<Button-1>", lambda e: app_insert2DB.validUserSignIn())

        # Return button
        self.Button_Return = RoundedButton(master=self, text="Return", radius=10, btnbackground="LightSkyBlue4",
                                           btnforeground="white", width=150, height=60, highlightthickness=0,
                                           font=("Helvetica", 18, "bold"), masterBackground='white')
        self.Button_Return.grid(column=2, row=10, padx=5, pady=5, sticky=tk.W)
        self.Button_Return.bind("<Button-1>", lambda e: app_insert2DB.exSignOut())

        self.Page_Frames = ttk.Notebook(self, width=700, height=600)
        self.Page_Frames.grid(column=2, row=3, padx=10, pady=10, sticky="nsew", columnspan=3, rowspan=2)

        self._initResearcherSignInPg0(self.Page_Frames, style='TFrame')
        self.pg0.grid(column=2, row=3, padx=10, pady=10, sticky="nsew", columnspan=3, rowspan=2)

        self.Page_Frames.add(self.pg0, text='                        Personal Details                        ', )
        self.Page_Frames.select(0)
        return

    def _initResearcherSignInPg0(self, MasterPanel, *args, **kwargs):
        self.pg0 = ttk.Frame(master=MasterPanel, *args, **kwargs)
        self.pg0.columnconfigure(list(range(1, 5)), weight=1)
        self.pg0.rowconfigure(list(range(1, 14)), weight=1)

        gridConfigure = {'padx': 20, 'pady': 0, 'sticky': tk.W}
        gridTEntryConfigure = {'padx': 20, 'pady': 0, 'sticky': tk.W, 'ipady': 5, 'ipadx': 0}
        entryConfigure = {'font': ("Helvetica", 18), 'background': 'white'}
        labelConfigure = {'font': ("Helvetica", 18, "bold"), 'background': 'white', 'borderwidth': 0}

        # ------------------------- ID ------------------------------------------
        self.pg0.Label_UserID = ttk.Label(self.pg0, text='ID: *', **labelConfigure)
        self.pg0.Label_UserID.grid(column=1, row=1, **gridConfigure)

        self.pg0.Entry_UserID = ttk.Entry(self.pg0, **entryConfigure)
        self.pg0.Entry_UserID.grid(column=1, row=2, **gridTEntryConfigure)

        # ------------------------- FName ------------------------------------------
        self.pg0.Label_UserFname = ttk.Label(self.pg0, text='First Name: *', **labelConfigure)
        self.pg0.Label_UserFname.grid(column=1, row=3, **gridConfigure)

        self.pg0.Entry_UserFname = ttk.Entry(self.pg0, **entryConfigure)
        self.pg0.Entry_UserFname.grid(column=1, row=4, columnspan=2, **gridTEntryConfigure)

        # ------------------------- LName ------------------------------------------
        self.pg0.Label_UserLname = ttk.Label(self.pg0, text='Last Name: *', **labelConfigure)
        self.pg0.Label_UserLname.grid(column=1, row=5, **gridConfigure)

        self.pg0.Entry_UserLname = ttk.Entry(self.pg0, **entryConfigure)
        self.pg0.Entry_UserLname.grid(column=1, row=6, columnspan=2, **gridTEntryConfigure)

        # ------------------------- Gender ------------------------------------------
        self.pg0.Label_UserGender = ttk.Label(self.pg0, text='Gender: *', **labelConfigure)
        self.pg0.Label_UserGender.grid(column=1, row=7, **gridConfigure)

        self.pg0.textVariable_UserGender = tk.StringVar()
        self.pg0.Entry_UserGender = ttk.Combobox(self.pg0, textvariable=self.pg0.textVariable_UserGender,
                                                 **entryConfigure)
        self.pg0.Entry_UserGender['values'] = ('Female', 'Male')
        self.pg0.Entry_UserGender.grid(column=1, row=8, **gridTEntryConfigure)

        # ------------------------- Phone ------------------------------------------
        self.pg0.Label_UserPhone = ttk.Label(self.pg0, text='Phone: *', **labelConfigure)
        self.pg0.Label_UserPhone.grid(column=3, row=1, **gridConfigure)

        self.pg0.Entry_UserPhone = ttk.Entry(self.pg0, **entryConfigure)
        self.pg0.Entry_UserPhone.grid(column=3, row=2, columnspan=2, **gridTEntryConfigure)

        # ------------------------- Mail ------------------------------------------
        self.pg0.Label_UserMail = ttk.Label(self.pg0, text='Mail: *', **labelConfigure)
        self.pg0.Label_UserMail.grid(column=3, row=3, **gridConfigure)

        self.pg0.Entry_UserMail = ttk.Entry(self.pg0, **entryConfigure)
        self.pg0.Entry_UserMail.grid(column=3, row=4, columnspan=2, **gridTEntryConfigure)

        # ------------------------- SignIN ------------------------------------------
        self.pg0.Button_SignIN = RoundedButton(master=self.pg0, text="Sign In", radius=10,
                                               btnbackground="LightSkyBlue4",
                                               btnforeground="white", width=150, height=60, highlightthickness=0,
                                               font=("Helvetica", 18, "bold"), masterBackground='white')
        self.pg0.Button_SignIN.grid(column=3, row=6, sticky=tk.E + tk.S + tk.W)
        app_insert2DB = self.master.__dict__.get('app_insert2DB')
        self.pg0.Button_SignIN.bind("<Button-1>", lambda e: app_insert2DB.validUserSignIn())
        self.pg0.Var_conifer = tk.IntVar()
        self.pg0.Entry_conifer = tk.Checkbutton(self.pg0, text="I agree to the terms",
                                                variable=self.pg0.Var_conifer,
                                                onvalue=1, offvalue=0, width=20, background="white",
                                                font=("Helvetica", 12), foreground='black')
        self.pg0.Entry_conifer.grid(column=3, row=7, sticky=tk.E + tk.S + tk.W)
        return

    def raiseError(self, pgIndex, labelName=None):
        pg = self.__dict__.get(f'pg{pgIndex}')
        if not pg:
            return
        if pgIndex == 0 and labelName is not None:
            label = pg.__dict__.get(f'Label_User{labelName}')
            if not label:
                return
            label.config(foreground="red")
            return
        entry = pg.__dict__.get('Entry_conifer')
        if not entry:
            return
        entry.configure(foreground='red', font=("Helvetica", 12, "bold", 'underline'))
        return

    def deleteError(self, pgIndex, labelName=None):
        pg = self.__dict__.get(f'pg{pgIndex}')
        if not pg:
            return
        if pgIndex == 0 and labelName is not None:
            label = pg.__dict__.get(f'Label_User{labelName}')
            if not label:
                return
            label.config(foreground="black")
            return
        entry = pg.__dict__.get('Entry_conifer')
        if not entry:
            return
        entry.configure(foreground='black', font=("Helvetica", 12))
        return

    def entryButton1(self, EntryName):
        index = self.Page_Frames.index(self.Page_Frames.select())
        entry = self.__dict__[f'pg{index}'].__dict__.get(f'Entry_User{EntryName}')
        if not entry:
            return
        if EntryName == 'COB' and entry.get() == 'Israel':
            entry.delete(0, "end")
            return
        return

    def entryFocusOut(self, EntryName):
        index = self.Page_Frames.index(self.Page_Frames.select())
        entry = self.__dict__[f'pg{index}'].__dict__.get(f'Entry_User{EntryName}')
        if not entry:
            return
        if not entry.get() and EntryName == 'COB':
            entry.insert(0, 'Israel')
            return
        return


class ResearcherMainPanel(ttk.Frame):

    def __init__(self, MasterPanel):
        ttk.Frame.__init__(self, master=MasterPanel, relief=tk.RAISED, borderwidth=2)
        self.width = 0.5 * MasterPanel.width
        self.height = 0.5 * MasterPanel.height
        self.columnconfigure(list(range(1, 5)), weight=1)
        self.rowconfigure(list(range(1, 6)), weight=1)
        self._create_sub_frames(MasterPanel)

    def _create_sub_frames(self, MasterPanel):
        self.style = ttk.Style(self)
        self.style.configure('TFrame', background='white', borderwidth=10, relief='RAISED')
        self.style.configure('TNotebook', background="LightSkyBlue4", weight=50, tabmargins=[5, 5, 0, 0])
        self.style.configure('TNotebook.Tab', background="tomato3", compound=tk.LEFT,
                             font=("Helvetica", 18, "bold"), weight=50, padding=[50, 20])

        app_insert2DB = MasterPanel.__dict__.get('app_insert2DB')
        if not app_insert2DB:
            print('Master have not Insert2DB instance')
            return

        app_queries = MasterPanel.__dict__.get('app_queries')
        if not app_queries:
            print('Master have not queries instance')
            return

        Label_title = ttk.Label(self, text=' ',
                                font=("Helvetica", 50, "bold"),
                                background="DarkGoldenrod2", foreground='black')
        Label_title.grid(row=0, column=0, columnspan=11, ipadx=150, sticky=tk.W + tk.E)

        ttk.Separator(self, orient=HORIZONTAL).grid(row=1, column=0, columnspan=11, ipadx=150,
                                                    sticky=tk.W + tk.E + tk.N)
        self.Button_SignOut = RoundedButton(master=self, text="Sign Out", radius=10, btnbackground="LightSkyBlue4",
                                            btnforeground="white", width=150, height=60, highlightthickness=0,
                                            font=("Helvetica", 18, "bold"), masterBackground='DarkGoldenrod2')
        self.Button_SignOut.grid(column=0, row=0, padx=5, pady=5, sticky=tk.W)
        self.Button_SignOut.bind("<Button-1>", lambda e: app_insert2DB.exSignOut())

        self.Button_Refresh = RoundedButton(master=self, text="Refresh", radius=10,
                                            btnbackground="LightSkyBlue4",
                                            btnforeground="white", width=150, height=60, highlightthickness=0,
                                            font=("Helvetica", 18, "bold"), masterBackground='DarkGoldenrod2')
        self.Button_Refresh.grid(column=1, row=0, padx=5, pady=5, sticky=tk.W)
        self.Button_Refresh.bind('<Button-1>', lambda e: self.buttonRefresh())

        self.Button_DisConnect = RoundedButton(master=self, text="DisConnect", radius=10, btnbackground="LightSkyBlue4",
                                               btnforeground="white", width=150, height=60, highlightthickness=0,
                                               font=("Helvetica", 18, "bold"), masterBackground='DarkGoldenrod2')
        self.Button_DisConnect.grid(column=5, row=0, padx=5, pady=5, sticky=tk.E)
        self.Button_DisConnect.bind("<Button-1>", lambda e: app_insert2DB.exDisConnect())
        return self._initNoteBook()

    def _initNoteBook(self):
        index = 0
        if self.__dict__.get('Page_Frames'):
            Page_Frames = self.__dict__.get('Page_Frames')
            index = Page_Frames.index(Page_Frames.select())
            Page_Frames.destroy()
        self.Page_Frames = ttk.Notebook(self, width=800, height=600)
        self.Page_Frames.grid(column=1, row=2, padx=1, pady=1, sticky="nsew", columnspan=3, rowspan=3)

        self._initResearcherMainPg0(self.Page_Frames, style='TFrame')
        self.pg0.grid(column=2, row=3, padx=10, pady=10, sticky="nsew", columnspan=3, rowspan=2)
        self._initResearcherMainPg1(self.Page_Frames, style='TFrame')
        self.pg1.grid(column=2, row=3, padx=10, pady=10, sticky="nsew", columnspan=3, rowspan=2)
        self._initResearcherMainPg2(self.Page_Frames, style='TFrame')
        self.pg2.grid(column=2, row=3, padx=10, pady=10, sticky="nsew", columnspan=3, rowspan=2)
        self._initResearcherMainPg3(self.Page_Frames, style='TFrame')
        self.pg3.grid(column=2, row=3, padx=10, pady=10, sticky="nsew", columnspan=3, rowspan=2)
        self._initResearcherMainPg4(self.Page_Frames, style='TFrame')
        self.pg4.grid(column=2, row=3, padx=10, pady=10, sticky="nsew", columnspan=3, rowspan=2)
        self.Page_Frames.add(self.pg0, text='Profile')
        self.Page_Frames.add(self.pg1, text='New Research')
        self.Page_Frames.add(self.pg2, text='Available patients')
        self.Page_Frames.add(self.pg3, text='Add New Disease')
        self.Page_Frames.add(self.pg4, text='Add New Symptom')
        self.Page_Frames.select(index)
        return

    def _initResearcherMainPg0(self, MasterPanel, *args, **kwargs):
        UserIndices = self.master.__dict__.get('app_queries').dequeueUserIndices('ResearcherMainPg0')
        self.pg0 = ttk.Frame(master=MasterPanel, *args, **kwargs)
        self.pg0.columnconfigure(list(range(1, 10)), weight=1)
        self.pg0.rowconfigure(list(range(1, 14)), weight=1)
        self.pg0.UserIndices = UserIndices

        gridConfigure = {'padx': 5, 'pady': 5, 'sticky': tk.W}
        gridTEntryConfigure = {'padx': 5, 'pady': 0, 'sticky': tk.W, 'ipady': 0, 'ipadx': 0}
        entryConfigure = {'font': ("Helvetica", 18), 'background': 'white'}
        labelConfigure = {'font': ("Helvetica", 18, "bold"), 'background': 'white', 'borderwidth': 0,
                          'foreground': 'LightSkyBlue4'}
        s = ttk.Style()
        s.configure('Custom.Treeview', rowheight=30, highlightthickness=2, bd=0, font=('Helvetica', 18))
        s.configure('Custom.Treeview.Heading', background='seashell3', foreground='black',
                    font=('Helvetica', 18, 'bold'))
        s.map("Custom.Treeview", background=[("selected", "ivory4")])

        Indices = self.pg0.UserIndices['Indices']
        researchers = self.pg0.UserIndices['researchers']
        # ------------------------- ID ------------------------------------------
        self.pg0.Label_UserID = ttk.Label(self.pg0, text='ID:', **labelConfigure)
        self.pg0.Label_UserID.grid(column=2, row=1, **gridConfigure)

        self.pg0.Entry_UserID = ttk.Entry(self.pg0, **entryConfigure)
        self.pg0.Entry_UserID.grid(column=2, row=2, **gridTEntryConfigure)
        self.pg0.Entry_UserID.insert(0, Indices['ID'])
        self.pg0.Entry_UserID.config(state="disabled")

        # ------------------------- FName ------------------------------------------
        self.pg0.Label_UserFname = ttk.Label(self.pg0, text='First Name:', **labelConfigure)
        self.pg0.Label_UserFname.grid(column=2, row=3, **gridConfigure)

        self.pg0.Entry_UserFname = ttk.Entry(self.pg0, **entryConfigure)
        self.pg0.Entry_UserFname.grid(column=2, row=4, columnspan=2, **gridTEntryConfigure)
        self.pg0.Entry_UserFname.insert(0, Indices['Fname'])
        self.pg0.Entry_UserFname.config(state="disabled")

        # ------------------------- LName ------------------------------------------
        self.pg0.Label_UserLname = ttk.Label(self.pg0, text='Last Name:', **labelConfigure)
        self.pg0.Label_UserLname.grid(column=2, row=5, **gridConfigure)

        self.pg0.Entry_UserLname = ttk.Entry(self.pg0, **entryConfigure)
        self.pg0.Entry_UserLname.grid(column=2, row=6, columnspan=2, **gridTEntryConfigure)
        self.pg0.Entry_UserLname.insert(0, Indices['Lname'])
        self.pg0.Entry_UserLname.config(state="disabled")

        # ------------------------- Gender ------------------------------------------
        self.pg0.Label_UserGender = ttk.Label(self.pg0, text='Gender:', **labelConfigure)
        self.pg0.Label_UserGender.grid(column=2, row=7, **gridConfigure)

        self.pg0.Entry_UserGender = ttk.Entry(self.pg0, **entryConfigure)
        self.pg0.Entry_UserGender.grid(column=2, row=8, **gridTEntryConfigure)
        self.pg0.Entry_UserGender.insert(0, Indices['gender'])
        self.pg0.Entry_UserGender.config(state="disabled")

        # ------------------------- Phone ------------------------------------------
        self.pg0.Label_UserPhone = ttk.Label(self.pg0, text='Phone:', **labelConfigure)
        self.pg0.Label_UserPhone.grid(column=2, row=9, **gridConfigure)

        self.pg0.Entry_UserPhone = ttk.Entry(self.pg0, **entryConfigure)
        self.pg0.Entry_UserPhone.grid(column=2, row=10, columnspan=2, **gridTEntryConfigure)
        self.pg0.Entry_UserPhone.insert(0, Indices['phone'])

        # ------------------------- Mail ------------------------------------------
        self.pg0.Label_UserMail = ttk.Label(self.pg0, text='Mail:', **labelConfigure)
        self.pg0.Label_UserMail.grid(column=2, row=11, **gridConfigure)

        self.pg0.Entry_UserMail = ttk.Entry(self.pg0, **entryConfigure)
        self.pg0.Entry_UserMail.grid(column=2, row=12, columnspan=2, **gridTEntryConfigure)
        self.pg0.Entry_UserMail.insert(0, Indices['Mail'])

        self.pg0.Button_UpDate = RoundedButton(master=self.pg0, text="UPDATE", radius=10, btnbackground="LightSkyBlue4",
                                               btnforeground="white", width=150, height=60, highlightthickness=0,
                                               font=("Helvetica", 18, "bold"), masterBackground='white')
        self.pg0.Button_UpDate.grid(column=2, row=14, padx=5, pady=5, sticky=tk.W)
        self.pg0.Button_UpDate.bind('<Button-1>', lambda e: self.buttonUpDate())

        # ------------------------- Separator ------------------------------------------
        ttk.Separator(self.pg0, orient=VERTICAL).grid(row=1, column=3, rowspan=13, ipady=150, sticky=tk.N + tk.S + tk.W)

        # ------------------------- Researchers ------------------------------------------
        self.pg0.Label_Researchers = ttk.Label(self.pg0, text='Researchers in which you participate:', **labelConfigure)
        self.pg0.Label_Researchers.grid(column=5, row=2, columnspan=3, sticky=tk.N + tk.W + tk.E, pady=5, padx=5)

        self.pg0.Table_Researchers = ttk.Treeview(self.pg0, style='Custom.Treeview')
        self.pg0.Table_Researchers['columns'] = list(researchers.columns)
        self.pg0.Table_Researchers.column("#0", width=0, stretch=tk.NO)
        for col in list(researchers.columns):
            w = 100
            if col == 'Mail':
                w = 200
            self.pg0.Table_Researchers.column(col, anchor=tk.CENTER, width=w, stretch=True)
            self.pg0.Table_Researchers.heading(col, text=col, anchor=tk.CENTER)
        for row in researchers.index:
            vals = list(researchers.loc[row, :])
            if row % 2:
                self.pg0.Table_Researchers.insert(parent='', index='end', iid=int(row), text='', values=vals,
                                                  tags=('even',))
            else:
                self.pg0.Table_Researchers.insert(parent='', index='end', iid=int(row), text='', values=vals,
                                                  tags=('odd',))

        self.pg0.Table_Researchers.tag_configure('odd', background='snow2')
        self.pg0.Table_Researchers.tag_configure('even', background='white')
        self.pg0.Table_Researchers.grid(column=5, row=3, columnspan=5, rowspan=9, sticky=tk.N + tk.W + tk.E, pady=5)

        self.pg0.Button_AddResearch = RoundedButton(master=self.pg0, text="Add Research", radius=10, btnbackground="LightSkyBlue4",
                                               btnforeground="white", width=150, height=60, highlightthickness=0,
                                               font=("Helvetica", 18, "bold"), masterBackground='white')
        self.pg0.Button_AddResearch.grid(column=5, row=10, padx=5, pady=5, sticky=tk.W+tk.E)
        self.pg0.Button_AddResearch.bind('<Button-1>', lambda e: self.buttonUpDate())

        self.pg0.Button_AvailablePatient = RoundedButton(master=self.pg0, text="Available Patient", radius=10, btnbackground="LightSkyBlue4",
                                               btnforeground="white", width=150, height=60, highlightthickness=0,
                                               font=("Helvetica", 18, "bold"), masterBackground='white')
        self.pg0.Button_AvailablePatient.grid(column=9, row=10, padx=5, pady=5, sticky=tk.W+tk.E)
        self.pg0.Button_AvailablePatient.bind('<Button-1>', lambda e: self.buttonUpDate())
        return

    def _initResearcherMainPg1(self, MasterPanel, *args, **kwargs):
        self.pg1 = ttk.Frame(master=MasterPanel, *args, **kwargs)
        self.pg1.columnconfigure(list(range(1, 9)), weight=1)
        self.pg1.rowconfigure(list(range(1, 14)), weight=1)

        gridConfigure = {'padx': 20, 'pady': 0, 'sticky': tk.W}
        gridTEntryConfigure = {'padx': 5, 'pady': 0, 'sticky': tk.W, 'ipady': 0, 'ipadx': 0}
        entryConfigure = {'font': ("Helvetica", 18), 'background': 'white'}
        labelConfigure = {'font': ("Helvetica", 18, "bold"), 'background': 'white', 'borderwidth': 0,
                          'foreground': 'LightSkyBlue4'}
        s = ttk.Style()
        s.configure('Custom.Treeview', rowheight=30, highlightthickness=2, bd=0, font=('Helvetica', 18))
        s.map("Custom.Treeview", background=[("selected", "ivory4")])

        # ------------------------- COB ------------------------------------------
        self.pg1.Label_ResearchCOB = ttk.Label(self.pg1, text='Country Of Birth:', **labelConfigure)
        self.pg1.Label_ResearchCOB.grid(column=1, row=1, **gridConfigure)

        self.pg1.Entry_ResearchCOB = ttk.Entry(self.pg1, **entryConfigure)
        self.pg1.Entry_ResearchCOB.insert(0, 'Israel')
        self.pg1.Entry_ResearchCOB.grid(column=1, row=2, **gridTEntryConfigure)
        self.pg1.Entry_ResearchCOB.bind("<Button-1>")
        self.pg1.Entry_ResearchCOB.bind("<FocusOut>")

        # ------------------------- Gender ------------------------------------------
        self.pg1.Label_ResearchGender = ttk.Label(self.pg1, text='Gender: *', **labelConfigure)
        self.pg1.Label_ResearchGender.grid(column=2, row=1, **gridConfigure)

        self.pg1.textVariable_ResearchGender = tk.StringVar()
        self.pg1.Entry_ResearchGender = ttk.Combobox(self.pg1, textvariable=self.pg1.textVariable_ResearchGender,
                                                 **entryConfigure)
        self.pg1.Entry_ResearchGender['values'] = ('Female', 'Male')
        self.pg1.Entry_ResearchGender.grid(column=2, row=2, **gridTEntryConfigure)

        # ------------------------- Age ------------------------------------------
        self.pg1.Label_ResearchDOB = ttk.Label(self.pg1, text='Age', **labelConfigure)
        self.pg1.Label_ResearchDOB.grid(column=4, row=1, **gridConfigure)

        self.pg1.Entry_ResearchDOB = DateEntry(self.pg1, selectmode='day', date_pattern='MM-dd-yyyy',
                                           font=("Helvetica", 18, "bold"),
                                           firstweekday='sunday', weekenddays=[6, 7], background='LightSkyBlue4',
                                           foreground='white')
        self.pg1.Entry_ResearchDOB.grid(column=4, row=2, **gridConfigure)

        # ------------------------- Support ------------------------------------------
        self.pg1.Label_ResearchSupport = ttk.Label(self.pg1, text='Support: *', **labelConfigure)
        self.pg1.Label_ResearchSupport.grid(column=6, row=1, **gridConfigure)

        self.pg1.textVariable_ResearchSupport = tk.StringVar()
        self.pg1.Entry_ResearchSupport = ttk.Combobox(self.pg1, textvariable=self.pg1.textVariable_ResearchSupport,
                                                  **entryConfigure)
        self.pg1.Entry_ResearchSupport['values'] = ('Yes', 'No')
        self.pg1.Entry_ResearchSupport.grid(column=6, row=2, **gridTEntryConfigure)

        # ------------------------- Height ------------------------------------------
        self.pg1.Label_ResearchHeight = ttk.Label(self.pg1, text='Height: *', **labelConfigure)
        self.pg1.Label_ResearchHeight.grid(column=1, row=3, **gridConfigure)

        self.pg1.Entry_ResearchHeight = tk.Entry(self.pg1, **entryConfigure)
        self.pg1.Entry_ResearchHeight.grid(column=1, row=4, **gridTEntryConfigure)

        # ------------------------- Weight ------------------------------------------
        self.pg1.Label_ResearchWeight = ttk.Label(self.pg1, text='Weight: *', **labelConfigure)
        self.pg1.Label_ResearchWeight.grid(column=2, row=3, **gridConfigure)

        self.pg1.Entry_ResearchWeight = ttk.Entry(self.pg1, **entryConfigure)
        self.pg1.Entry_ResearchWeight.grid(column=2, row=4, **gridTEntryConfigure)

        # ------------------------- HMO ------------------------------------------
        self.pg1.Label_ResearchHMO = ttk.Label(self.pg1, text='HMO: *', **labelConfigure)
        self.pg1.Label_ResearchHMO.grid(column=4, row=3, **gridConfigure)

        self.pg1.textVariable_ResearchHMO = tk.StringVar()
        self.pg1.Entry_ResearchHMO = ttk.Combobox(self.pg1, textvariable=self.pg1.textVariable_ResearchHMO, **entryConfigure)
        self.pg1.Entry_ResearchHMO['values'] = ('Clalit', 'Maccabi', 'Meuhedet', 'Leumit')
        self.pg1.Entry_ResearchHMO.grid(column=4, row=4, **gridTEntryConfigure)

        # ------------------------- Area ------------------------------------------
        self.pg1.Label_ResearchArea = ttk.Label(self.pg1, text='Area: *', **labelConfigure)
        self.pg1.Label_ResearchArea.grid(column=6, row=3, **gridConfigure)

        self.pg1.textVariable_ResearchArea = tk.StringVar()
        self.pg1.Entry_ResearchArea = ttk.Combobox(self.pg1, textvariable=self.pg1.textVariable_ResearchArea, **entryConfigure)
        self.pg1.Entry_ResearchArea['values'] = ('North', 'Center', 'South')
        self.pg1.Entry_ResearchArea.grid(column=6, row=4, **gridTEntryConfigure)

        # ------------------------- Separator ------------------------------------------
        ttk.Separator(self.pg1, orient=HORIZONTAL).grid(row=5, column=0, columnspan=11, ipadx=150,
                                                    sticky=tk.W + tk.E + tk.S)

        # ------------------------- Disease Department ------------------------------------------
        self.pg1.Label_ResearchDisDep = ttk.Label(self.pg1, text='Department:', **labelConfigure)
        self.pg1.Label_ResearchDisDep.grid(column=1, row=6, **gridConfigure)

        self.pg1.textVariable_ResearchDisDep = tk.StringVar()
        self.pg1.Entry_ResearchDisDep = ttk.Combobox(self.pg1, textvariable=self.pg1.textVariable_ResearchDisDep, **entryConfigure)
        self.pg1.Entry_ResearchDisDep['values'] = ('Oncology', 'Neurological', 'Vascular')
        self.pg1.Entry_ResearchDisDep.grid(column=1, row=7, **gridTEntryConfigure)

        # ------------------------- Disease Name ------------------------------------------
        self.pg1.Label_ResearchDisName = ttk.Label(self.pg1, text='Name:', **labelConfigure)
        self.pg1.Label_ResearchDisName.grid(column=2, row=6, **gridConfigure)

        self.pg1.textVariable_ResearchDisName = tk.StringVar()
        self.pg1.Entry_ResearchDisName = ttk.Combobox(self.pg1, textvariable=self.pg1.textVariable_ResearchDisDep, **entryConfigure)
        self.pg1.Entry_ResearchDisName['values'] = ('Oncology', 'Neurological', 'Vascular')
        self.pg1.Entry_ResearchDisName.grid(column=2, row=7, **gridTEntryConfigure)

        # ------------------------- Symptoms ------------------------------------------
        self.pg1.Label_ResearchSymptoms = ttk.Label(self.pg1, text='Symptoms:', **labelConfigure)
        self.pg1.Label_ResearchSymptoms.grid(column=1, row=9, columnspan=2, sticky=tk.W + tk.N, pady=10, padx=10)

        self.pg1.Entry_ResearchSymptoms = ttk.Entry(self.pg1, textvariable=tk.StringVar(), width=40,
                                                   **entryConfigure)
        self.pg1.Entry_ResearchSymptoms.grid(column=1, row=10, columnspan=2, rowspan=2, sticky=tk.W + tk.N + tk.E)

        self.pg1.Listbox_ResearchSymptoms = tk.Listbox(self.pg1, selectmode=tk.EXTENDED, font=("Helvetica", 18),
                                                      bg='white', highlightcolor='LightSkyBlue4', highlightthickness=1,
                                                      relief='flat', width=40)
        self.pg1.Listbox_ResearchSymptoms.grid(column=1, row=11, columnspan=2, rowspan=3, sticky=tk.W + tk.E, padx=10)

        self.pg1.Button_select = RoundedButton(master=self.pg1, text="Select", radius=10,
                                               btnbackground="LightSkyBlue4",
                                               btnforeground="white", width=80, height=60, highlightthickness=0,
                                               font=("Helvetica", 18, "bold"), masterBackground='white')
        self.pg1.Button_select.grid(column=2, row=14, sticky=tk.W + tk.E)

        # ------------------------- Selected Symptoms ------------------------------------------

        self.pg1.Label_ResearchSelectSymptoms = ttk.Label(self.pg1, text='Selected Symptoms:', **labelConfigure)
        self.pg1.Label_ResearchSelectSymptoms.grid(column=4, row=9, columnspan=3, sticky=tk.W + tk.N, padx=10, pady=10)

        self.pg1.Table_ResearchSelectSymptoms = ttk.Treeview(self.pg1, style='Custom.Treeview')
        self.pg1.Table_ResearchSelectSymptoms['columns'] = ['Symptoms']
        self.pg1.Table_ResearchSelectSymptoms.column("#0", width=0, stretch=tk.NO)
        self.pg1.Table_ResearchSelectSymptoms.column('Symptoms', anchor=tk.W, width=400)

        self.pg1.Table_ResearchSelectSymptoms.tag_configure('odd', background='snow2')
        self.pg1.Table_ResearchSelectSymptoms.tag_configure('even', background='white')

        self.pg1.Table_ResearchSelectSymptoms.grid(column=4, row=10, columnspan=3, rowspan=4, sticky=tk.W + tk.E, padx=10)

        self.pg1.Button_deleteSelect = RoundedButton(master=self.pg1, text="Delete Selected", radius=10,
                                                     btnbackground="LightSkyBlue4",
                                                     btnforeground="white", width=80, height=60, highlightthickness=0,
                                                     font=("Helvetica", 18, "bold"), masterBackground='white')
        self.pg1.Button_deleteSelect.grid(column=4, row=14, sticky=tk.W + tk.E)
        temp = self.master.__dict__.get('symptomsTrie')
        if temp:
            self.AutoComplete = AUTO_complete(temp, self.pg1.Entry_ResearchSymptoms,
                                              self.pg1.Listbox_ResearchSymptoms,
                                              treeview=self.pg1.Table_ResearchSelectSymptoms,
                                              select=self.pg1.Button_select, deleteSelect=self.pg1.Button_deleteSelect)

        # ------------------------- Create New Research ------------------------------------------
        self.pg1.Button_createResearch = RoundedButton(master=self.pg1, text="Create Research", radius=10,
                                                     btnbackground="LightSkyBlue4",
                                                     btnforeground="white", width=80, height=60, highlightthickness=0,
                                                     font=("Helvetica", 18, "bold"), masterBackground='white')
        self.pg1.Button_createResearch.grid(column=6, row=14, sticky=tk.W + tk.E)
        app_insert2DB = self.master.__dict__.get('app_insert2DB')
        self.pg1.Button_createResearch.bind("<Button-1>", lambda e: app_insert2DB.pushNewResearch())
        return

    def _initResearcherMainPg2(self, MasterPanel, *args, **kwargs):
        availablePatients = self.master.__dict__.get('app_queries').dequeueUserIndices('ResearcherMainPg2')
        self.pg2 = ttk.Frame(master=MasterPanel, *args, **kwargs)
        self.pg2.columnconfigure(list(range(1, 5)), weight=1)
        self.pg2.rowconfigure(list(range(1, 7)), weight=1)
        self.pg2.availablePatients = availablePatients

        labelConfigure = {'font': ("Helvetica", 18, "bold"), 'background': 'white', 'borderwidth': 0,
                          'foreground': 'LightSkyBlue4'}
        s = ttk.Style()
        s.configure('Custom.Treeview', rowheight=30, highlightthickness=2, bd=0, font=('Helvetica', 18))
        s.configure('Custom.Treeview.Heading', background='seashell3', foreground='black',
                    font=('Helvetica', 18, 'bold'))
        s.map("Custom.Treeview", background=[("selected", "ivory4")])

        # ------------------------- Researchers ------------------------------------------

        self.pg2.Label_Researchers = ttk.Label(self.pg2, text='Available Patients:', **labelConfigure)
        self.pg2.Label_Researchers.grid(column=1, row=1, columnspan=3, sticky=tk.W, pady=5, padx=5)

        self.pg2.Table_AvailablePatients = ttk.Treeview(self.pg2, style='Custom.Treeview')
        self.pg2.Table_AvailablePatients['columns'] = list(availablePatients.columns)
        self.pg2.Table_AvailablePatients.column("#0", width=0, stretch=tk.NO)
        for col in list(availablePatients.columns):
            w = 100
            if col == 'Mail':
                w = 200
            self.pg2.Table_AvailablePatients.column(col, anchor=tk.CENTER, width=w)
            self.pg2.Table_AvailablePatients.heading(col, text=col, anchor=tk.CENTER)

        for row in availablePatients.index:
            vals = list(availablePatients.loc[row, :])
            if row % 2:
                self.pg2.Table_AvailablePatients.insert(parent='', index='end', iid=int(row), text='',
                                                        values=vals, tags=('even',))
            else:
                self.pg2.Table_AvailablePatients.insert(parent='', index='end', iid=int(row), text='',
                                                        values=vals, tags=('odd',))

        self.pg2.Table_AvailablePatients.tag_configure('odd', background='snow2')
        self.pg2.Table_AvailablePatients.tag_configure('even', background='white')

        self.pg2.Table_AvailablePatients.grid(column=1, row=2, columnspan=4, rowspan=3, sticky=tk.W + tk.E, padx=5)
        self.pg2.Button_select = RoundedButton(master=self.pg2, text="Add patient to research", radius=10,
                                               btnbackground="LightSkyBlue4",
                                               btnforeground="white", width=80, height=60, highlightthickness=0,
                                               font=("Helvetica", 18, "bold"), masterBackground='white')
        self.pg2.Button_select.grid(column=4, row=5, sticky=tk.W + tk.E)
        return

    def _initResearcherMainPg3(self, MasterPanel, *args, **kwargs):
        UserIndices = self.master.__dict__.get('app_queries').dequeueUserIndices('ResearcherMainPg3')
        self.pg3 = ttk.Frame(master=MasterPanel, *args, **kwargs)
        self.pg3.columnconfigure(list(range(1, 10)), weight=1)
        self.pg3.rowconfigure(list(range(1, 14)), weight=1)
        self.pg3.UserIndices = UserIndices

        gridConfigure = {'padx': 5, 'pady': 5, 'sticky': tk.W}
        gridTEntryConfigure = {'padx': 5, 'pady': 0, 'sticky': tk.W, 'ipady': 0, 'ipadx': 0}
        entryConfigure = {'font': ("Helvetica", 18), 'background': 'white'}
        labelConfigure = {'font': ("Helvetica", 18, "bold"), 'background': 'white', 'borderwidth': 0,
                          'foreground': 'LightSkyBlue4'}
        s = ttk.Style()
        s.configure('Custom.Treeview', rowheight=30, highlightthickness=2, bd=0, font=('Helvetica', 18))
        s.configure('Custom.Treeview.Heading', background='seashell3', foreground='black',
                    font=('Helvetica', 18, 'bold'))
        s.map("Custom.Treeview", background=[("selected", "ivory4")])

        # ------------------------- Department ------------------------------------------
        self.pg3.Label_DiseaseDepName = ttk.Label(self.pg3, text='Department: *', **labelConfigure)
        self.pg3.Label_DiseaseDepName.grid(column=2, row=2, **gridConfigure)

        self.pg3.textVariable_DiseaseDepName = tk.StringVar()
        self.pg3.Entry_DiseaseDepName = ttk.Combobox(self.pg3, textvariable=self.pg3.textVariable_DiseaseDepName,
                                                     **entryConfigure)
        self.pg3.Entry_DiseaseDepName['values'] = ('Oncology', 'Neurological', 'Vascular')
        self.pg3.Entry_DiseaseDepName.grid(column=2, row=3, **gridTEntryConfigure)

        # ------------------------- Disease Name ------------------------------------------
        self.pg3.Label_DiseaseDisName = ttk.Label(self.pg3, text='Disease Name: *', **labelConfigure)
        self.pg3.Label_DiseaseDisName.grid(column=3, row=2, **gridConfigure)

        self.pg3.Entry_DiseaseDisName = ttk.Entry(self.pg3, **entryConfigure)
        self.pg3.Entry_DiseaseDisName.grid(column=3, row=3, **gridTEntryConfigure)

        # ------------------------- Enter Symptoms ------------------------------------------
        self.pg3.Label_DiseaseSymptoms = ttk.Label(self.pg3, text='Symptoms:', **labelConfigure)
        self.pg3.Label_DiseaseSymptoms.grid(column=2, row=6, columnspan=2, sticky=tk.W + tk.N, pady=10, padx=10)

        self.pg3.Entry_DiseaseSymptoms = ttk.Entry(self.pg3, textvariable=tk.StringVar(), width=40,
                                                   **entryConfigure)
        self.pg3.Entry_DiseaseSymptoms.grid(column=2, row=7, columnspan=2, rowspan=2, sticky=tk.W + tk.N + tk.E)

        self.pg3.Listbox_DiseaseSymptoms = tk.Listbox(self.pg3, selectmode=tk.EXTENDED, font=("Helvetica", 18),
                                                      bg='white', highlightcolor='LightSkyBlue4', highlightthickness=1,
                                                      relief='flat', width=40)
        self.pg3.Listbox_DiseaseSymptoms.grid(column=2, row=8, columnspan=2, rowspan=3, sticky=tk.W + tk.E, padx=10)

        self.pg3.Button_select = RoundedButton(master=self.pg3, text="Select", radius=10,
                                               btnbackground="LightSkyBlue4",
                                               btnforeground="white", width=80, height=60, highlightthickness=0,
                                               font=("Helvetica", 18, "bold"), masterBackground='white')
        self.pg3.Button_select.grid(column=2, row=11, sticky=tk.W + tk.E)

        # ------------------------- Selected Symptoms ------------------------------------------
        self.pg3.Label_DiseaseSelectSymptoms = ttk.Label(self.pg3, text='Selected Symptoms:', **labelConfigure)
        self.pg3.Label_DiseaseSelectSymptoms.grid(column=5, row=6, columnspan=3, sticky=tk.W + tk.N, padx=10, pady=10)

        self.pg3.Table_DiseaseSelectSymptoms = ttk.Treeview(self.pg3, style='Custom.Treeview')
        self.pg3.Table_DiseaseSelectSymptoms['columns'] = ['Symptoms']
        self.pg3.Table_DiseaseSelectSymptoms.column("#0", width=0, stretch=tk.NO)
        self.pg3.Table_DiseaseSelectSymptoms.column('Symptoms', anchor=tk.W, width=400)

        self.pg3.Table_DiseaseSelectSymptoms.tag_configure('odd', background='snow2')
        self.pg3.Table_DiseaseSelectSymptoms.tag_configure('even', background='white')

        self.pg3.Table_DiseaseSelectSymptoms.grid(column=5, row=7, columnspan=3, rowspan=4, sticky=tk.W + tk.E, padx=10)

        self.pg3.Button_deleteSelect = RoundedButton(master=self.pg3, text="Delete Selected", radius=10,
                                                     btnbackground="LightSkyBlue4",
                                                     btnforeground="white", width=80, height=60, highlightthickness=0,
                                                     font=("Helvetica", 18, "bold"), masterBackground='white')
        temp = self.master.__dict__.get('symptomsTrie')
        if temp:
            self.AutoComplete = AUTO_complete(temp, self.pg3.Entry_DiseaseSymptoms, self.pg3.Listbox_DiseaseSymptoms,
                                              treeview=self.pg3.Table_DiseaseSelectSymptoms,
                                              select=self.pg3.Button_select, deleteSelect=self.pg3.Button_deleteSelect)
        self.pg3.Button_deleteSelect.grid(column=5, row=11, sticky=tk.W + tk.E)
        self.pg3.Button_AddDisease = RoundedButton(master=self.pg3, text="Add New Disease", radius=10,
                                               btnbackground="LightSkyBlue4",
                                               btnforeground="white", width=80, height=60, highlightthickness=0,
                                               font=("Helvetica", 18, "bold"), masterBackground='white')
        self.pg3.Button_AddDisease.grid(column=7, row=13, sticky=tk.E + tk.S + tk.W)
        app_insert2DB = self.master.__dict__.get('app_insert2DB')
        self.pg3.Button_AddDisease.bind("<Button-1>", lambda e: app_insert2DB.pushNewDiseases())
        return

    def _initResearcherMainPg4(self, MasterPanel, *args, **kwargs):
        self.pg4 = ttk.Frame(master=MasterPanel, *args, **kwargs)
        self.pg4.columnconfigure(list(range(1, 10)), weight=1)
        self.pg4.rowconfigure(list(range(1, 14)), weight=1)

        gridConfigure = {'padx': 5, 'pady': 5, 'sticky': tk.W}
        gridTEntryConfigure = {'padx': 5, 'pady': 0, 'sticky': tk.W, 'ipady': 0, 'ipadx': 0}
        entryConfigure = {'font': ("Helvetica", 18), 'background': 'white'}
        labelConfigure = {'font': ("Helvetica", 18, "bold"), 'background': 'white', 'borderwidth': 0,
                          'foreground': 'LightSkyBlue4'}
        s = ttk.Style()
        s.configure('Custom.Treeview', rowheight=30, highlightthickness=2, bd=0, font=('Helvetica', 18))
        s.configure('Custom.Treeview.Heading', background='seashell3', foreground='black',
                    font=('Helvetica', 18, 'bold'))
        s.map("Custom.Treeview", background=[("selected", "ivory4")])

        # ------------------------- Disease Name ------------------------------------------
        self.pg4.Label_DiseaseDisName = ttk.Label(self.pg4, text='Disease Name: *', **labelConfigure)
        self.pg4.Label_DiseaseDisName.grid(column=2, row=2, **gridConfigure)

        self.pg4.Entry_DiseaseDisName = ttk.Entry(self.pg4, **entryConfigure)
        self.pg4.Entry_DiseaseDisName.grid(column=2, row=3, **gridTEntryConfigure)

        self.pg4.Button_ShowSymptoms = RoundedButton(master=self.pg4, text="Show Existing Symptoms", radius=10,
                                               btnbackground="LightSkyBlue4",
                                               btnforeground="white", width=80, height=60, highlightthickness=0,
                                               font=("Helvetica", 18, "bold"), masterBackground='white')
        self.pg4.Button_ShowSymptoms.grid(column=3, row=3, sticky=tk.W)
        self.pg4.Button_ShowSymptoms.bind("<Button-1>", lambda e: self.buttonShowSymptoms())
        # -------------------------Existing Symptoms ------------------------------------------

        self.pg4.Label_DiseaseExistingSymptoms = ttk.Label(self.pg4, text='Existing Symptoms:', **labelConfigure)
        self.pg4.Label_DiseaseExistingSymptoms.grid(column=2, row=6, columnspan=3, sticky=tk.W, padx=10, pady=10)

        self.pg4.Table_DiseaseExistingSymptoms = ttk.Treeview(self.pg4, style='Custom.Treeview')
        self.pg4.Table_DiseaseExistingSymptoms['columns'] = ['Symptoms']
        self.pg4.Table_DiseaseExistingSymptoms.column("#0", width=0, stretch=tk.NO)

        self.pg4.Table_DiseaseExistingSymptoms.tag_configure('odd', background='snow2')
        self.pg4.Table_DiseaseExistingSymptoms.tag_configure('even', background='white')
        self.pg4.Table_DiseaseExistingSymptoms.grid(column=2, row=7, columnspan=2, rowspan=9, sticky=tk.W + tk.E, pady=5)

        # -------------------------New Symptom Name ------------------------------------------
        self.pg4.Label_DiseaseSymptom = ttk.Label(self.pg4, text='New Symptom Name: *', **labelConfigure)
        self.pg4.Label_DiseaseSymptom.grid(column=5, row=2, **gridConfigure)

        self.pg4.Entry_DiseaseSymptom = ttk.Entry(self.pg4, **entryConfigure)
        self.pg4.Entry_DiseaseSymptom.grid(column=5, row=3, **gridTEntryConfigure)

        self.pg4.Button_AddSymptom = RoundedButton(master=self.pg4, text="Add New Symptom", radius=10,
                                               btnbackground="LightSkyBlue4",
                                               btnforeground="white", width=80, height=60, highlightthickness=0,
                                               font=("Helvetica", 18, "bold"), masterBackground='white')
        self.pg4.Button_AddSymptom.grid(column=6, row=3, sticky=tk.W)
        app_insert2DB = self.master.__dict__.get('app_insert2DB')
        self.pg4.Button_AddSymptom.bind("<Button-1>", lambda e: app_insert2DB.pushNewSymptoms())
        return

    def buttonShowSymptoms(self):
        disName = self.pg4.__dict__.get(f'Entry_DiseaseDisName').get()
        symptoms = self.master.__dict__.get('app_queries').querySymptomsDiseases(disName)
        for i, row in enumerate(symptoms):
            if i % 2:
                self.pg4.Table_DiseaseExistingSymptoms.insert(parent='', index='end', iid=int(i), text='', values=[row[0]],
                                                  tags=('even',))
            else:
                self.pg4.Table_DiseaseExistingSymptoms.insert(parent='', index='end', iid=int(i), text='', values=[row[0]],
                                                  tags=('odd',))
        return
    def buttonUpDate(self):
        app_insert2DB = self.master.__dict__.get('app_insert2DB')
        if not app_insert2DB:
            return
        if app_insert2DB.updateUserIndices():
            return self.buttonRefresh()
        return

    def buttonRefresh(self):
        app_queries = self.master.__dict__.get('app_queries')
        app_queries.activateLogIn('active', None, None)
        return self._initNoteBook()

    def raiseError(self, pgIndex, labelName=None):
        pg = self.__dict__.get(f'pg{pgIndex}')
        if not pg:
            return
        label = pg.__dict__.get(f'Label_User{labelName}')
        if not label:
            return
        label.config(foreground="red")
        return

    def deleteError(self, pgIndex, labelName=None):
        pg = self.__dict__.get(f'pg{pgIndex}')
        if not pg:
            return
        label = pg.__dict__.get(f'Label_User{labelName}')
        if not label:
            return
        label.config(foreground="black")
        return
