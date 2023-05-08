import tkinter as tk
from tkinter import ttk, HORIZONTAL, VERTICAL
from app.frontEnd.RoundButton import RoundedButton
from tkcalendar import DateEntry


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
        self.Button_Back.bind("<Button-1>", lambda e: self.back())

        # Next button
        self.Button_Next = RoundedButton(master=self, text="Next", radius=10, btnbackground="LightSkyBlue4",
                                         btnforeground="white", width=150, height=60, highlightthickness=0,
                                         font=("Helvetica", 18, "bold"), masterBackground='DarkGoldenrod2')
        self.Button_Next.grid(column=4, row=1, padx=5, pady=5, sticky=tk.E)
        self.Button_Next.bind("<Button-1>", lambda e: MasterPanel.app_insert2DB.validPatientSignIn())

        # Return button
        self.Button_Return = RoundedButton(master=self, text="Return", radius=10, btnbackground="LightSkyBlue4",
                                           btnforeground="white", width=150, height=60, highlightthickness=0,
                                           font=("Helvetica", 18, "bold"), masterBackground='white')
        self.Button_Return.grid(column=2, row=10, padx=5, pady=5, sticky=tk.W)
        self.Button_Return.bind("<Button-1>", lambda e: MasterPanel.app_insert2DB.ExSignOut())

        self.Page_Frames = ttk.Notebook(self, width=700, height=600)
        self.Page_Frames.grid(column=2, row=3, padx=10, pady=10, sticky="nsew", columnspan=3, rowspan=2)

        self.pg0 = PatientSignInPg1(self.Page_Frames, style='TFrame')
        self.pg0.grid(column=2, row=3, padx=10, pady=10, sticky="nsew", columnspan=3, rowspan=2)
        self.pg1 = PatientSignInPg2(self.Page_Frames, style='TFrame')
        self.pg1.grid(column=2, row=3, padx=10, pady=10, sticky="nsew", columnspan=3, rowspan=2)
        self.Page_Frames.add(self.pg0, text='                Step 1                ', )
        self.Page_Frames.add(self.pg1, text='                Step 2                ')
        self.Page_Frames.select(0)
        self.Page_Frames.tab(1, state="disabled")
        return

    def back(self):
        index = self.Page_Frames.index(self.Page_Frames.select())
        if index == 1:
            self.Page_Frames.select(0)
        return


class PatientSignInPg1(ttk.Frame):
    def __init__(self, MasterPanel, *args, **kwargs):
        ttk.Frame.__init__(self, master=MasterPanel, *args, **kwargs)
        self.columnconfigure(list(range(1, 5)), weight=1)
        self.rowconfigure(list(range(1, 14)), weight=1)
        self._create_widgets(MasterPanel)

    def _create_widgets(self, MasterPanel):
        gridConfigure = {'padx': 20, 'pady': 0, 'sticky': tk.W}
        gridTEntryConfigure = {'padx': 20, 'pady': 0, 'sticky': tk.W, 'ipady': 5, 'ipadx': 0}
        entryConfigure = {'font': ("Helvetica", 18), 'background': 'white'}
        labelConfigure = {'font': ("Helvetica", 18, "bold"), 'background': 'white', 'borderwidth': 0}

        # ------------------------- ID ------------------------------------------
        self.Label_UserID = ttk.Label(self, text='ID: *', **labelConfigure)
        self.Label_UserID.grid(column=1, row=1, **gridConfigure)

        self.Entry_UserID = ttk.Entry(self, **entryConfigure)
        self.Entry_UserID.grid(column=1, row=2, **gridTEntryConfigure)

        # ------------------------- Name ------------------------------------------
        self.Label_UserName = ttk.Label(self, text='Name: *', **labelConfigure)
        self.Label_UserName.grid(column=1, row=3, **gridConfigure)

        self.Entry_UserName = ttk.Entry(self, **entryConfigure)
        self.Entry_UserName.grid(column=1, row=4, columnspan=2, **gridTEntryConfigure)

        # ------------------------- Gender ------------------------------------------
        self.Label_UserGender = ttk.Label(self, text='Gender: *', **labelConfigure)
        self.Label_UserGender.grid(column=1, row=5, **gridConfigure)

        self.textVariable_UserGender = tk.StringVar()
        self.Entry_UserGender = ttk.Combobox(self, textvariable=self.textVariable_UserGender, **entryConfigure)
        self.Entry_UserGender['values'] = ('Female', 'Male')
        self.Entry_UserGender.grid(column=1, row=6, **gridTEntryConfigure)

        # ------------------------- Area ------------------------------------------
        self.Label_UserArea = ttk.Label(self, text='Area: *', **labelConfigure)
        self.Label_UserArea.grid(column=1, row=7, **gridConfigure)

        self.textVariable_UserArea = tk.StringVar()
        self.Entry_UserArea = ttk.Combobox(self, textvariable=self.textVariable_UserArea, **entryConfigure)
        self.Entry_UserArea['values'] = ('North', 'Center', 'South')
        self.Entry_UserArea.grid(column=1, row=8, **gridTEntryConfigure)

        # ------------------------- City ------------------------------------------
        self.Label_UserCity = ttk.Label(self, text='City: *', **labelConfigure)
        self.Label_UserCity.grid(column=1, row=9, **gridConfigure)

        self.Entry_UserCity = ttk.Entry(self, **entryConfigure)
        self.Entry_UserCity.grid(column=1, row=10, columnspan=2, **gridTEntryConfigure)

        # ------------------------- Phone ------------------------------------------
        self.Label_UserPhone = ttk.Label(self, text='Phone: *', **labelConfigure)
        self.Label_UserPhone.grid(column=1, row=11, **gridConfigure)

        self.Entry_UserPhone = ttk.Entry(self, **entryConfigure)
        self.Entry_UserPhone.grid(column=1, row=12, columnspan=2, **gridTEntryConfigure)

        # ------------------------- Separator ------------------------------------------
        ttk.Separator(self, orient=VERTICAL).grid(row=1, column=2, rowspan=13, ipady=150, sticky=tk.N + tk.S + tk.E)

        # ------------------------- DOB ------------------------------------------
        self.Label_UserDOB = ttk.Label(self, text='Date of Birth: *', **labelConfigure)
        self.Label_UserDOB.grid(column=3, row=1, **gridConfigure)

        self.Entry_UserDOB = DateEntry(self, selectmode='day', date_pattern='MM-dd-yyyy',
                                       font=("Helvetica", 18, "bold"),
                                       firstweekday='sunday', weekenddays=[6, 7], background='LightSkyBlue4',
                                       foreground='white')
        self.Entry_UserDOB.grid(column=3, row=2, **gridConfigure)

        # ------------------------- HMO ------------------------------------------
        self.Label_UserHMO = ttk.Label(self, text='HMO: *', **labelConfigure)
        self.Label_UserHMO.grid(column=3, row=3, **gridConfigure)

        self.textVariable_UserHMO = tk.StringVar()
        self.Entry_UserHMO = ttk.Combobox(self, textvariable=self.textVariable_UserHMO, **entryConfigure)
        self.Entry_UserHMO['values'] = ('Clalit', 'Maccabi', 'Meuhedet', 'Leumit')
        self.Entry_UserHMO.grid(column=3, row=4, **gridTEntryConfigure)

        # ------------------------- COB ------------------------------------------
        self.Label_UserCOB = ttk.Label(self, text='Country Of Birth:', **labelConfigure)
        self.Label_UserCOB.grid(column=3, row=5, **gridConfigure)

        self.Entry_UserCOB = ttk.Entry(self, **entryConfigure)
        self.Entry_UserCOB.insert(0, 'Israel')
        self.Entry_UserCOB.grid(column=3, row=6, **gridTEntryConfigure)
        self.Entry_UserCOB.bind("<Button-1>", lambda e: self.EntryButton1('COB'))
        self.Entry_UserCOB.bind("<FocusOut>", lambda e: self.EntryFocusOut('COB'))

        # ------------------------- Height ------------------------------------------
        self.Label_UserHeight = ttk.Label(self, text='Height: *', **labelConfigure)
        self.Label_UserHeight.grid(column=3, row=7, **gridConfigure)

        self.Entry_UserHeight = tk.Entry(self, **entryConfigure)
        self.Entry_UserHeight.grid(column=3, row=8, **gridTEntryConfigure)

        # ------------------------- Weight ------------------------------------------
        self.Label_UserWeight = ttk.Label(self, text='Weight: *', **labelConfigure)
        self.Label_UserWeight.grid(column=3, row=9, **gridConfigure)

        self.Entry_UserWeight = ttk.Entry(self, **entryConfigure)
        self.Entry_UserWeight.grid(column=3, row=10, **gridTEntryConfigure)

        # ------------------------- Support ------------------------------------------
        self.Label_UserSupport = ttk.Label(self, text='Support: *', **labelConfigure)
        self.Label_UserSupport.grid(column=3, row=11, **gridConfigure)

        self.textVariable_UserSupport = tk.StringVar()
        self.Entry_UserSupport = ttk.Combobox(self, textvariable=self.textVariable_UserSupport, **entryConfigure)
        self.Entry_UserSupport['values'] = ('Yes', 'No')
        self.Entry_UserSupport.grid(column=3, row=12, **gridTEntryConfigure)

    def EntryFocusOut(self, EntryName):
        if not self.__dict__[f'Entry_User{EntryName}'].get() and EntryName == 'COB':
            self.Entry_UserCOB.insert(0, 'Israel')
        return

    def EntryButton1(self, EntryName):
        if EntryName == 'COB' and self.__dict__[f'Entry_User{EntryName}'].get() == 'Israel':
            self.__dict__[f'Entry_User{EntryName}'].delete(0, "end")
        return

    def raiseError(self, EntryName):
        self.__dict__[f'Label_User{EntryName}'].config(foreground="red")
        return

    def deleteError(self, EntryName):
        self.__dict__[f'Label_User{EntryName}'].config(foreground="black")
        return


class PatientSignInPg2(ttk.Frame):
    def __init__(self, MasterPanel, *args, **kwargs):
        ttk.Frame.__init__(self, master=MasterPanel, *args, **kwargs)
        self.columnconfigure(list(range(1, 7)), weight=1)
        self.rowconfigure(list(range(1, 9)), weight=1)
        self._create_widgets(MasterPanel)
        self.keyRelBool = True
        self.TableIndex = 0

    def _create_widgets(self, MasterPanel):
        entryConfigure = {'font': ("Helvetica", 18), 'background': 'white'}
        labelConfigure = {'font': ("Helvetica", 18, "bold"), 'background': 'white', 'borderwidth': 0}
        s = ttk.Style()
        s.configure('Custom.Treeview', rowheight=30, highlightthickness=2, bd=0, font=('Helvetica', 18))
        s.map("Custom.Treeview", background=[("selected", "ivory4")])

        # ------------------------- Enter Symptoms ------------------------------------------
        self.Label_UserSymptoms = ttk.Label(self, text='Symptoms:', **labelConfigure)
        self.Label_UserSymptoms.grid(column=1, row=1, columnspan=2, sticky=tk.W + tk.N, padx=5, pady=10)

        self.symptomText = tk.StringVar()
        self.Entry_UserSymptoms = ttk.Entry(self, textvariable=self.symptomText, width=40, **entryConfigure)
        self.Entry_UserSymptoms.insert(0, 'Enter your common symptoms...')
        self.Entry_UserSymptoms.grid(column=1, row=2, columnspan=2, sticky=tk.W + tk.N + tk.E, padx=5)
        self.Entry_UserSymptoms.bind("<Button-1>", lambda e: self.EntryButton1('Symptoms'))
        self.Entry_UserSymptoms.bind("<FocusOut>", lambda e: self.EntryFocusOut('Symptoms'))
        self.Entry_UserSymptoms.bind("<space>", lambda e: MasterPanel.master.master.symptomsTrie.space())
        self.Entry_UserSymptoms.bind("<BackSpace>", lambda e: MasterPanel.master.master.symptomsTrie.backSpace())
        self.Entry_UserSymptoms.bind("<KeyRelease>", lambda e: self._KeyRelease(MasterPanel))

        self.Listbox_UserSymptoms = tk.Listbox(self, selectmode=tk.EXTENDED, font=("Helvetica", 18),
                                               bg='white', highlightcolor='white', highlightthickness=0,
                                               relief='flat', width=40)
        self.Listbox_UserSymptoms.grid(column=1, row=3, columnspan=2, rowspan=3, sticky=tk.W + tk.N + tk.E, padx=5,
                                       pady=10)
        var = tk.Variable(value=MasterPanel.master.master.symptomsTrie.initValues())
        self.Listbox_UserSymptoms.config(listvariable=var)

        self.Button_select = RoundedButton(master=self, text="Select", radius=10,
                                           btnbackground="seashell3",
                                           btnforeground="black", width=80, height=60, highlightthickness=0,
                                           font=("Helvetica", 18, "bold"), masterBackground='white')
        self.Button_select.grid(column=1, row=7, sticky=tk.W + tk.N + tk.E)
        self.Button_select.bind('<Button-1>', lambda e: self.updateSelectSymptoms())

        # ------------------------- Separator ------------------------------------------
        ttk.Separator(self, orient=VERTICAL).grid(row=2, column=3, rowspan=7, ipady=150, sticky=tk.N + tk.S)

        # ------------------------- Selected Symptoms ------------------------------------------

        self.Label_UserSelectSymptoms = ttk.Label(self, text='Selected Symptoms:', **labelConfigure)
        self.Label_UserSelectSymptoms.grid(column=4, row=1, columnspan=2, sticky=tk.W + tk.N, pady=10, padx=10)

        self.Table_UserSelectSymptoms = ttk.Treeview(self, selectmode='browse', style='Custom.Treeview')
        self.Table_UserSelectSymptoms['columns'] = ['Symptoms']
        self.Table_UserSelectSymptoms.column("#0", width=0, stretch=tk.NO)
        self.Table_UserSelectSymptoms.column('Symptoms', anchor=tk.W, width=400)

        self.Table_UserSelectSymptoms.grid(column=4, row=3, columnspan=3, rowspan=3, sticky=tk.W + tk.N + tk.E)
        self.Table_UserSelectSymptoms.tag_configure('odd', background='snow2')
        self.Table_UserSelectSymptoms.tag_configure('even', background='white')

        self.Button_deleteSelect = RoundedButton(master=self, text="Delete Selected", radius=10,
                                                 btnbackground="seashell3",
                                                 btnforeground="black", width=80, height=60, highlightthickness=0,
                                                 font=("Helvetica", 18, "bold"), masterBackground='white')
        self.Button_deleteSelect.grid(column=4, row=7, sticky=tk.W + tk.N + tk.E)
        self.Button_deleteSelect.bind('<Button-1>', lambda e: self.deleteSelectSymptoms())

        # ------------------------- SignIN ------------------------------------------
        self.Button_SignIN = RoundedButton(master=self, text="Sign In", radius=10, btnbackground="LightSkyBlue4",
                                           btnforeground="white", width=150, height=60, highlightthickness=0,
                                           font=("Helvetica", 18, "bold"), masterBackground='white')
        self.Button_SignIN.grid(column=6, row=8, sticky=tk.E + tk.S + tk.W)
        self.Button_SignIN.bind("<Button-1>", lambda e: self.SignINButton(MasterPanel))
        self.Entry_coniferVar = tk.IntVar()
        self.Entry_conifer = tk.Checkbutton(self, text="I agree to the terms", variable=self.Entry_coniferVar,
                                            onvalue=1, offvalue=0, width=20, background="white",
                                            font=("Helvetica", 12), foreground='black')
        self.Entry_conifer.grid(column=6, row=9, sticky=tk.E + tk.S + tk.W)

    def SignINButton(self, MasterPanel):
        var = self.Entry_coniferVar.get()
        if var == 0:
            self.Entry_conifer.configure(foreground='red', font=("Helvetica", 12, "bold", 'underline'))
            return
        return MasterPanel.master.master.app_insert2DB.validPatientSignIn()

    def updateSelectSymptoms(self):
        selected = self.Listbox_UserSymptoms.curselection()
        if not selected:
            return
        txt = self.Listbox_UserSymptoms.get(selected[0])
        for each in self.Table_UserSelectSymptoms.get_children():
            if self.Table_UserSelectSymptoms.item(each)['values'][0] == txt:
                return
        if int(self.TableIndex) % 2:
            self.Table_UserSelectSymptoms.insert(parent='', index='end', iid=int(self.TableIndex), text='',
                                                 values=[txt], tags=('even',))
        else:
            self.Table_UserSelectSymptoms.insert(parent='', index='end', iid=int(self.TableIndex), text='',
                                                 values=[txt], tags=('odd',))
        self.TableIndex += 1
        return print(txt)

    def deleteSelectSymptoms(self):
        textList = self.Table_UserSelectSymptoms.item(self.Table_UserSelectSymptoms.focus())["values"]
        if not textList:
            return
        self.Table_UserSelectSymptoms.delete(self.Table_UserSelectSymptoms.selection()[0])
        self.TableIndex -= 1
        return

    def EntryButton1(self, EntryName):
        if EntryName == 'Symptoms' and self.__dict__[f'Entry_User{EntryName}'].get() == 'Enter your common symptoms...':
            self.__dict__[f'Entry_User{EntryName}'].delete(0, "end")
        return

    def EntryFocusOut(self, EntryName):
        if not self.__dict__[f'Entry_User{EntryName}'].get() and EntryName == 'Symptoms':
            self.Entry_UserSymptoms.insert(0, 'Enter your common symptoms...')
        return

    def _KeyRelease(self, MasterPanel):
        sentence = self.Entry_UserSymptoms.get()
        sentence_list = MasterPanel.master.master.symptomsTrie.keyRelease(sentence)
        var = tk.Variable(value=sentence_list)
        self.Listbox_UserSymptoms.config(listvariable=var)
        return


class PatientMainPanel(ttk.Frame):

    def __init__(self, MasterPanel):
        ttk.Frame.__init__(self, master=MasterPanel, relief=tk.RAISED, borderwidth=2)
        self.width = 0.5 * MasterPanel.width
        self.height = 0.5 * MasterPanel.height
        self.columnconfigure(list(range(1, 5)), weight=1)
        self.rowconfigure(list(range(1, 6)), weight=1)
        self._create_widgets(MasterPanel)

    def _create_widgets(self, MasterPanel):
        self.style = ttk.Style(self)
        self.style.configure('TFrame', background='white', borderwidth=10, relief='RAISED')
        self.style.configure('TNotebook', background="LightSkyBlue4", weight=50, tabmargins=[5, 5, 0, 0])
        self.style.configure('TNotebook.Tab', background="tomato3", compound=tk.LEFT,
                             font=("Helvetica", 18, "bold"), weight=50, padding=[50, 20])

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
        self.Button_SignOut.bind("<Button-1>", lambda e: MasterPanel.app_insert2DB.ExSignOut())

        self.Button_DisConnect = RoundedButton(master=self, text="DisConnect", radius=10, btnbackground="LightSkyBlue4",
                                               btnforeground="white", width=150, height=60, highlightthickness=0,
                                               font=("Helvetica", 18, "bold"), masterBackground='DarkGoldenrod2')
        self.Button_DisConnect.grid(column=5, row=0, padx=5, pady=5, sticky=tk.E)
        self.Button_DisConnect.bind("<Button-1>", lambda e: MasterPanel.app_insert2DB.ExDisConnect())

        self.Page_Frames = ttk.Notebook(self, width=800, height=600)
        self.Page_Frames.grid(column=1, row=2, padx=1, pady=1, sticky="nsew", columnspan=3, rowspan=3)

        self.pg0 = PatientMainPg1(self.Page_Frames, style='TFrame')
        self.pg0.grid(column=2, row=3, padx=10, pady=10, sticky="nsew", columnspan=3, rowspan=2)
        self.pg1 = PatientMainPg2(self.Page_Frames, style='TFrame')
        self.pg1.grid(column=2, row=3, padx=10, pady=10, sticky="nsew", columnspan=3, rowspan=2)
        self.pg2 = PatientMainPg3(self.Page_Frames, style='TFrame')
        self.pg2.grid(column=2, row=3, padx=10, pady=10, sticky="nsew", columnspan=3, rowspan=2)
        self.Page_Frames.add(self.pg0, text='                Profile                ', )
        self.Page_Frames.add(self.pg1, text='                Symptoms                ')
        self.Page_Frames.add(self.pg2, text='                Available Researches                ')
        self.Page_Frames.select(0)

        return


class PatientMainPg1(ttk.Frame):
    def __init__(self, MasterPanel, *args, **kwargs):
        ttk.Frame.__init__(self, master=MasterPanel, *args, **kwargs)
        self.columnconfigure(list(range(1, 10)), weight=1)
        self.rowconfigure(list(range(1, 14)), weight=1)
        self._create_widgets(MasterPanel)

    def _create_widgets(self, MasterPanel):
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

        UserIndices = MasterPanel.master.master.app_insert2DB.dequeueUserIndices('PatientMainPg1')
        Indices = UserIndices['Indices']
        researchers = UserIndices['researchers']
        # ------------------------- ID ------------------------------------------
        self.Label_UserID = ttk.Label(self, text='ID:', **labelConfigure)
        self.Label_UserID.grid(column=1, row=1, **gridConfigure)

        self.Entry_UserID = ttk.Entry(self, **entryConfigure)
        self.Entry_UserID.grid(column=1, row=2, **gridTEntryConfigure)
        self.Entry_UserID.insert(0, Indices['ID'])
        self.Entry_UserID.config(state="disabled")

        # ------------------------- Name ------------------------------------------
        self.Label_UserName = ttk.Label(self, text='Name:', **labelConfigure)
        self.Label_UserName.grid(column=1, row=3, **gridConfigure)

        self.Entry_UserName = ttk.Entry(self, **entryConfigure)
        self.Entry_UserName.grid(column=1, row=4, columnspan=2, **gridTEntryConfigure)
        self.Entry_UserName.insert(0, Indices['name'])
        self.Entry_UserName.config(state="disabled")

        # ------------------------- Gender ------------------------------------------
        self.Label_UserGender = ttk.Label(self, text='Gender:', **labelConfigure)
        self.Label_UserGender.grid(column=1, row=5, **gridConfigure)

        self.Entry_UserGender = ttk.Entry(self, **entryConfigure)
        self.Entry_UserGender.grid(column=1, row=6, **gridTEntryConfigure)
        self.Entry_UserGender.insert(0, Indices['gender'])
        self.Entry_UserGender.config(state="disabled")

        # ------------------------- Area ------------------------------------------
        self.Label_UserArea = ttk.Label(self, text='Area:', **labelConfigure)
        self.Label_UserArea.grid(column=1, row=7, **gridConfigure)

        area = ''
        for val in ('North', 'Center', 'South'):
            if Indices['area'][0] == val[0]:
                area = val
                break
        self.textVariable_UserArea = tk.StringVar(value=area)
        self.Entry_UserArea = ttk.Combobox(self, textvariable=self.textVariable_UserArea, **entryConfigure)
        self.Entry_UserArea['values'] = ('North', 'Center', 'South')
        self.Entry_UserArea.grid(column=1, row=8, **gridTEntryConfigure)

        # ------------------------- City ------------------------------------------
        self.Label_UserCity = ttk.Label(self, text='City:', **labelConfigure)
        self.Label_UserCity.grid(column=1, row=9, **gridConfigure)

        self.Entry_UserCity = ttk.Entry(self, **entryConfigure)
        self.Entry_UserCity.grid(column=1, row=10, columnspan=2, **gridTEntryConfigure)
        self.Entry_UserCity.insert(0, Indices['city'])

        # ------------------------- Phone ------------------------------------------
        self.Label_UserPhone = ttk.Label(self, text='Phone:', **labelConfigure)
        self.Label_UserPhone.grid(column=1, row=11, **gridConfigure)

        self.Entry_UserPhone = ttk.Entry(self, **entryConfigure)
        self.Entry_UserPhone.grid(column=1, row=12, columnspan=2, **gridTEntryConfigure)
        self.Entry_UserPhone.insert(0, Indices['phone'])

        # ------------------------- Separator ------------------------------------------
        ttk.Separator(self, orient=VERTICAL).grid(row=1, column=1, rowspan=13, ipady=150, sticky=tk.N + tk.S + tk.E)

        # ------------------------- DOB ------------------------------------------
        self.Label_UserDOB = ttk.Label(self, text='Date of Birth:', **labelConfigure)
        self.Label_UserDOB.grid(column=2, row=1, **gridConfigure)

        self.Entry_UserDOB = ttk.Entry(self, **entryConfigure)
        self.Entry_UserDOB.grid(column=2, row=2, **gridConfigure)
        self.Entry_UserDOB.insert(0, Indices['DOB'])
        self.Entry_UserDOB.config(state="disabled")

        # ------------------------- HMO ------------------------------------------
        self.Label_UserHMO = ttk.Label(self, text='HMO:', **labelConfigure)
        self.Label_UserHMO.grid(column=2, row=3, **gridConfigure)

        self.textVariable_UserHMO = tk.StringVar(value=Indices['HMO'])
        self.Entry_UserHMO = ttk.Combobox(self, textvariable=self.textVariable_UserHMO, **entryConfigure)
        self.Entry_UserHMO['values'] = ('Clalit', 'Maccabi', 'Meuhedet', 'Leumit')
        self.Entry_UserHMO.grid(column=2, row=4, **gridTEntryConfigure)

        # ------------------------- COB ------------------------------------------
        self.Label_UserCOB = ttk.Label(self, text='Country Of Birth:', **labelConfigure)
        self.Label_UserCOB.grid(column=2, row=5, **gridConfigure)

        self.Entry_UserCOB = ttk.Entry(self, **entryConfigure)
        self.Entry_UserCOB.insert(0, Indices['COB'])
        self.Entry_UserCOB.grid(column=2, row=6, **gridTEntryConfigure)
        self.Entry_UserCOB.config(state="disabled")

        # ------------------------- Height ------------------------------------------
        self.Label_UserHeight = ttk.Label(self, text='Height:', **labelConfigure)
        self.Label_UserHeight.grid(column=2, row=7, **gridConfigure)

        self.Entry_UserHeight = tk.Entry(self, **entryConfigure)
        self.Entry_UserHeight.grid(column=2, row=8, **gridTEntryConfigure)
        self.Entry_UserHeight.insert(0, Indices['height'])

        # ------------------------- Weight ------------------------------------------
        self.Label_UserWeight = ttk.Label(self, text='Weight:', **labelConfigure)
        self.Label_UserWeight.grid(column=2, row=9, **gridConfigure)

        self.Entry_UserWeight = ttk.Entry(self, **entryConfigure)
        self.Entry_UserWeight.grid(column=2, row=10, **gridTEntryConfigure)
        self.Entry_UserWeight.insert(0, Indices['weight'])

        # ------------------------- Support ------------------------------------------
        self.Label_UserSupport = ttk.Label(self, text='Support:', **labelConfigure)
        self.Label_UserSupport.grid(column=2, row=11, **gridConfigure)

        sup = Indices['support']
        if sup == '1':
            sup = 'Yes'
        else:
            sup = 'No'
        self.textVariable_UserSupport = tk.StringVar(value=sup)
        self.Entry_UserSupport = ttk.Combobox(self, textvariable=self.textVariable_UserSupport, **entryConfigure)
        self.Entry_UserSupport['values'] = ('Yes', 'No')
        self.Entry_UserSupport.grid(column=2, row=12, **gridTEntryConfigure)

        # ------------------------- Separator ------------------------------------------
        ttk.Separator(self, orient=VERTICAL).grid(row=1, column=3, rowspan=13, ipady=150, sticky=tk.N + tk.S)

        # ------------------------- Researchers ------------------------------------------

        self.Label_Researchers = ttk.Label(self, text='Researchers in which you participate:', **labelConfigure)
        self.Label_Researchers.grid(column=5, row=1, columnspan=3, sticky=tk.N + tk.W + tk.E, pady=5, padx=5)

        self.Table_Researchers = ttk.Treeview(self, style='Custom.Treeview')
        self.Table_Researchers['columns'] = list(researchers.columns)
        self.Table_Researchers.column("#0", width=0, stretch=tk.NO)
        for col in list(researchers.columns):
            w = 100
            if col == 'Mail':
                w = 200
            self.Table_Researchers.column(col, anchor=tk.CENTER, width=w, stretch=True)
            self.Table_Researchers.heading(col, text=col, anchor=tk.CENTER)
        for row in researchers.index:
            vals = list(researchers.loc[row, :])
            if row % 2:
                self.Table_Researchers.insert(parent='', index='end', iid=int(row), text='', values=vals,
                                              tags=('even',))
            else:
                self.Table_Researchers.insert(parent='', index='end', iid=int(row), text='', values=vals, tags=('odd',))

        self.Table_Researchers.tag_configure('odd', background='snow2')
        self.Table_Researchers.tag_configure('even', background='white')
        self.Table_Researchers.grid(column=5, row=3, columnspan=5, rowspan=9, sticky=tk.N + tk.W + tk.E, pady=5)

        self.Button_UpDate = RoundedButton(master=self, text="UPDATE", radius=10, btnbackground="LightSkyBlue4",
                                           btnforeground="white", width=150, height=60, highlightthickness=0,
                                           font=("Helvetica", 18, "bold"), masterBackground='white')
        self.Button_UpDate.grid(column=9, row=14, padx=5, pady=5, sticky=tk.W)
        self.Button_UpDate.bind('<Button-1>', lambda e: MasterPanel.master.master.app_insert2DB.PatientUpDate())

        return

    def raiseError(self, EntryName):
        self.__dict__[f'Label_User{EntryName}'].config(foreground="red")
        return

    def deleteError(self, EntryName):
        self.__dict__[f'Label_User{EntryName}'].config(foreground="LightSkyBlue4")
        return


class PatientMainPg2(ttk.Frame):
    def __init__(self, MasterPanel, *args, **kwargs):
        ttk.Frame.__init__(self, master=MasterPanel, *args, **kwargs)
        self.columnconfigure(list(range(1, 9)), weight=1)
        self.rowconfigure(list(range(1, 14)), weight=1)
        self.TableIndex = 0
        self._create_widgets(MasterPanel)

    def _create_widgets(self, MasterPanel):
        entryConfigure = {'font': ("Helvetica", 18), 'background': 'white'}
        labelConfigure = {'font': ("Helvetica", 18, "bold"), 'background': 'white', 'borderwidth': 0,
                          'foreground': 'LightSkyBlue4'}
        Indices = MasterPanel.master.master.app_insert2DB.dequeueUserIndices('PatientMainPg2')
        s = ttk.Style()
        s.configure('Custom.Treeview', rowheight=30, highlightthickness=2, bd=0, font=('Helvetica', 18))
        s.map("Custom.Treeview", background=[("selected", "ivory4")])
        # ------------------------- Symptoms ------------------------------------------

        self.Label_UserSymptoms = ttk.Label(self, text='Your Symptoms:', **labelConfigure)
        self.Label_UserSymptoms.grid(column=1, row=1, columnspan=3, sticky=tk.W + tk.N, padx=10, pady=10)

        self.Table_UserSymptoms = ttk.Treeview(self, style='Custom.Treeview')
        self.Table_UserSymptoms['columns'] = ['Symptoms']
        self.Table_UserSymptoms.column("#0", width=0, stretch=tk.NO)
        self.Table_UserSymptoms.column('Symptoms', anchor=tk.W, width=400)

        if Indices:
            for row, symp in enumerate(Indices):
                self.TableIndex += 1
                if row % 2:
                    self.Table_UserSymptoms.insert(parent='', index='end', iid=int(row), text='',
                                                   values=[symp], tags=('even',))
                else:
                    self.Table_UserSymptoms.insert(parent='', index='end', iid=int(row), text='',
                                                   values=[symp], tags=('odd',))

        self.Table_UserSymptoms.tag_configure('odd', background='snow2')
        self.Table_UserSymptoms.tag_configure('even', background='white')

        self.Table_UserSymptoms.grid(column=1, row=2, columnspan=3, rowspan=4, sticky=tk.W + tk.E, padx=10)

        self.Button_deleteSelect = RoundedButton(master=self, text="Delete Selected", radius=10,
                                                 btnbackground="LightSkyBlue4",
                                                 btnforeground="white", width=80, height=60, highlightthickness=0,
                                                 font=("Helvetica", 18, "bold"), masterBackground='white')
        self.Button_deleteSelect.grid(column=1, row=6, sticky=tk.W + tk.E)
        self.Button_deleteSelect.bind('<Button-1>', lambda e: self.deleteSelectSymptoms())

        # ------------------------- Separator ------------------------------------------
        ttk.Separator(self, orient=VERTICAL).grid(row=1, column=4, rowspan=13, ipady=150, sticky=tk.N + tk.S)

        # ------------------------- New Symptoms ------------------------------------------

        self.Label_NewUserSymptoms = ttk.Label(self, text='Search for Symptoms:', **labelConfigure)
        self.Label_NewUserSymptoms.grid(column=5, row=1, columnspan=2, sticky=tk.W + tk.N, pady=10, padx=10)

        self.symptomText = tk.StringVar()
        self.Entry_UserSymptomsNew = ttk.Entry(self, textvariable=self.symptomText, width=40, **entryConfigure)
        self.Entry_UserSymptomsNew.insert(0, 'Enter your common symptoms...')
        self.Entry_UserSymptomsNew.grid(column=5, row=2, columnspan=2, rowspan=2, sticky=tk.W + tk.N + tk.E)

        self.Listbox_NewUserSymptoms = tk.Listbox(self, selectmode=tk.EXTENDED, font=("Helvetica", 18),
                                                  bg='white', highlightcolor='LightSkyBlue4', highlightthickness=1,
                                                  relief='flat', width=40)
        self.Listbox_NewUserSymptoms.grid(column=5, row=3, columnspan=2, rowspan=3, sticky=tk.W + tk.E, padx=10)
        var = tk.Variable(value=MasterPanel.master.master.symptomsTrie.initValues())
        self.Listbox_NewUserSymptoms.config(listvariable=var)
        self.Entry_UserSymptomsNew.bind("<space>", lambda e: MasterPanel.master.master.symptomsTrie.space())
        self.Entry_UserSymptomsNew.bind("<BackSpace>", lambda e: MasterPanel.master.master.symptomsTrie.backSpace())
        self.Entry_UserSymptomsNew.bind("<Key>", lambda e: self._KeyRelease(MasterPanel))
        self.Entry_UserSymptomsNew.bind("<Button-1>", lambda e: self.EntryButton1('SymptomsNew'))
        self.Entry_UserSymptomsNew.bind("<FocusOut>", lambda e: self.EntryFocusOut('SymptomsNew'))

        self.Button_select = RoundedButton(master=self, text="Select", radius=10,
                                           btnbackground="LightSkyBlue4",
                                           btnforeground="white", width=80, height=60, highlightthickness=0,
                                           font=("Helvetica", 18, "bold"), masterBackground='white')
        self.Button_select.grid(column=5, row=6, sticky=tk.W + tk.E)
        self.Button_select.bind('<Button-1>', lambda e: self.updateSelectSymptoms())

        self.Button_UpDate = RoundedButton(master=self, text="UPDATE", radius=10, btnbackground="LightSkyBlue4",
                                           btnforeground="white", width=150, height=60, highlightthickness=0,
                                           font=("Helvetica", 18, "bold"), masterBackground='white')
        self.Button_UpDate.grid(column=9, row=14, padx=5, pady=5, sticky=tk.W)
        self.Button_UpDate.bind('<Button-1>', lambda e: MasterPanel.master.master.app_insert2DB.PatientUpDate())

        return

    def _KeyRelease(self, MasterPanel):
        sentence = self.Entry_UserSymptomsNew.get()
        sentence_list = MasterPanel.master.master.symptomsTrie.keyRelease(sentence)
        var = tk.Variable(value=sentence_list)
        self.Listbox_NewUserSymptoms.config(listvariable=var)
        return

    def EntryButton1(self, EntryName):
        txt = self.__dict__[f'Entry_User{EntryName}'].get()
        if EntryName == 'SymptomsNew' and txt == 'Enter your common symptoms...':
            self.__dict__[f'Entry_User{EntryName}'].delete(0, "end")
        return

    def EntryFocusOut(self, EntryName):
        txt = self.__dict__[f'Entry_User{EntryName}'].get()
        if not txt and EntryName == 'SymptomsNew':
            self.Entry_UserSymptomsNew.insert(0, 'Enter your common symptoms...')
        return

    def updateSelectSymptoms(self):
        selected = self.Listbox_NewUserSymptoms.curselection()
        if not selected:
            return
        txt = self.Listbox_NewUserSymptoms.get(selected[0])
        for each in self.Table_UserSymptoms.get_children():
            if self.Table_UserSymptoms.item(each)['values'][0] == txt:
                return
        if int(self.TableIndex) % 2:
            self.Table_UserSymptoms.insert(parent='', index='end', iid=int(self.TableIndex), text='',
                                           values=[txt], tags=('even',))
        else:
            self.Table_UserSymptoms.insert(parent='', index='end', iid=int(self.TableIndex), text='',
                                           values=[txt], tags=('odd',))
        self.TableIndex += 1
        return

    def deleteSelectSymptoms(self):
        textList = self.Table_UserSymptoms.item(self.Table_UserSymptoms.focus())["values"]
        if not textList:
            return
        self.Table_UserSymptoms.delete(self.Table_UserSymptoms.selection()[0])
        self.TableIndex -= 1
        return


class PatientMainPg3(ttk.Frame):
    def __init__(self, MasterPanel, *args, **kwargs):
        ttk.Frame.__init__(self, master=MasterPanel, *args, **kwargs)
        self.columnconfigure(list(range(1, 5)), weight=1)
        self.rowconfigure(list(range(1, 7)), weight=1)
        self._create_widgets(MasterPanel)

    def _create_widgets(self, MasterPanel):
        labelConfigure = {'font': ("Helvetica", 18, "bold"), 'background': 'white', 'borderwidth': 0,
                          'foreground': 'LightSkyBlue4'}
        Indices = MasterPanel.master.master.app_insert2DB.dequeueUserIndices('PatientMainPg3')
        s = ttk.Style()
        s.configure('Custom.Treeview', rowheight=30, highlightthickness=2, bd=0, font=('Helvetica', 18))
        s.configure('Custom.Treeview.Heading', background='seashell3', foreground='black',
                    font=('Helvetica', 18, 'bold'))
        s.map("Custom.Treeview", background=[("selected", "ivory4")])
        # ------------------------- Researchers ------------------------------------------

        self.Label_Researchers = ttk.Label(self, text='Available Researchers for you:', **labelConfigure)
        self.Label_Researchers.grid(column=1, row=1, columnspan=3, sticky=tk.W, pady=5, padx=5)

        self.Table_AvailableResearch = ttk.Treeview(self, style='Custom.Treeview')
        self.Table_AvailableResearch['columns'] = list(Indices.columns)
        self.Table_AvailableResearch.column("#0", width=0, stretch=tk.NO)
        for col in list(Indices.columns):
            w = 100
            if col == 'Mail':
                w = 200
            self.Table_AvailableResearch.column(col, anchor=tk.CENTER, width=w)
            self.Table_AvailableResearch.heading(col, text=col, anchor=tk.CENTER)

        for row in Indices.index:
            vals = list(Indices.loc[row, :])
            if row % 2:
                self.Table_AvailableResearch.insert(parent='', index='end', iid=int(row), text='',
                                                    values=vals, tags=('even',))
            else:
                self.Table_AvailableResearch.insert(parent='', index='end', iid=int(row), text='',
                                                    values=vals, tags=('odd',))

        self.Table_AvailableResearch.tag_configure('odd', background='snow2')
        self.Table_AvailableResearch.tag_configure('even', background='white')

        self.Table_AvailableResearch.grid(column=1, row=2, columnspan=4, rowspan=3, sticky=tk.W + tk.E, padx=5)

        self.Button_Refresh = RoundedButton(master=self, text="Refresh", radius=10, btnbackground="LightSkyBlue4",
                                            btnforeground="white", width=100, height=60, highlightthickness=0,
                                            font=("Helvetica", 18, "bold"), masterBackground='white')
        self.Button_Refresh.grid(column=1, row=6, sticky=tk.W + tk.E, padx=5)
        self.Button_Refresh.bind('<Button-1>', lambda e: self.ButtonRefresh(MasterPanel))

        return

    def ButtonRefresh(self, MasterPanel):
        Indices = MasterPanel.master.master.app_insert2DB.dequeueUserIndices('PatientMainPg3')
        for each in self.Table_AvailableResearch.get_children():
            self.Table_AvailableResearch.delete(each)

        for row in Indices.index:
            vals = list(Indices.loc[row, :])
            if row % 2:
                self.Table_AvailableResearch.insert(parent='', index='end', iid=int(row), text='',
                                                    values=vals, tags=('even',))
            else:
                self.Table_AvailableResearch.insert(parent='', index='end', iid=int(row), text='',
                                                    values=vals, tags=('odd',))
        return
