import tkinter as tk
from tkinter import ttk, HORIZONTAL, VERTICAL
import tkcalendar
from tkcalendar import DateEntry
from app.frontEnd.widgets import AUTO_complete, RoundedButton
from app.frontEnd.panels import MainPanel, SignInPanel


class UserLogInPanel(ttk.Frame):

    def __init__(self, MasterPanel):
        ttk.Frame.__init__(self, master=MasterPanel, relief=tk.RAISED, borderwidth=2)
        self.width = 0.5 * MasterPanel.width
        self.height = 0.5 * MasterPanel.height
        self.columnconfigure(list(range(1, 10)), weight=1)
        self.rowconfigure(list(range(1, 8)), weight=1)
        self.style = ttk.Style(self)
        self.style.configure(
            'Frame1.TFrame', background='LightSkyBlue4', borderwidth=10, relief='RAISED'
        )
        self._logInFrame(
            self, style='Frame1.TFrame'
        )
        self.logIn_frame.grid(
            column=5, row=2, rowspan=4, padx=50, pady=50, sticky="nsew"
        )

    def _logInFrame(self, MasterPanel, *args, **kwargs):
        cols = 3
        self.logIn_frame = ttk.Frame(
            master=MasterPanel, *args, **kwargs
        )
        self.logIn_frame.columnconfigure(
            list(range(1, cols)), weight=1
        )
        self.logIn_frame.rowconfigure(
            list(range(1, 9)), weight=1
        )

        self.logIn_frame.style = ttk.Style(self.logIn_frame)
        self.logIn_frame.style.configure(
            'TRadiobutton', font=("Helvetica", 25, "bold"), background="LightSkyBlue4", foreground='black'
        )
        labelConfigure = {
            'font': ("Helvetica", 30, "bold"), 'background': 'LightSkyBlue4'
        }
        entryConfigure = {
            'font': ("Helvetica", 25, "bold"), 'background': 'white'
        }
        gridTEntryConfigure = {
            'padx': 0, 'pady': 0, 'sticky': tk.W, 'ipady': 0, 'ipadx': 0
        }
        gridConfigure = {
            'padx': 0, 'pady': 0, 'ipady': 0, 'ipadx': 0, 'sticky': tk.W
        }

        app_inputs = self.master.__dict__.get('app_inputs')
        if not app_inputs:
            return

        def entryFocusOut(entryName):
            entry = self.__dict__.get(f'Entry_{entryName}')
            if not entry:
                return
            if not entry.get():
                entry.insert(0, entryName)
            return

        def entryButton1(entryName):
            entry = self.__dict__.get(f'Entry_{entryName}')
            if not entry:
                return
            if entry.get() == entryName:
                entry.delete(0, "end")
            return

        self.Label_title = ttk.Label(
            self.logIn_frame, text='Log In', font=("Helvetica", 80, "bold", 'underline'),
            background="LightSkyBlue4", foreground='white'
        )
        self.Label_title.grid(
            column=1, row=1, columnspan=cols, sticky="nsew"
        )
        self.Label_title.configure(anchor='center')

        self.separator = ttk.Separator(
            self.logIn_frame, orient=HORIZONTAL
        )
        self.separator.grid(
            row=2, column=1, columnspan=cols, ipadx=150,
            sticky=tk.W + tk.E
        )
        # User Path researcher or patient
        self.Label_User = ttk.Label(
            self.logIn_frame, text='User', **labelConfigure
        )
        self.Label_User.grid(
            column=1, row=3, padx=5, pady=0, sticky=tk.W
        )
        self.Entry_User = tk.IntVar()
        self.Entry_User.set(1)
        self.RB_UserPath_Patient = ttk.Radiobutton(
            self.logIn_frame, text='Patient',
            variable=self.Entry_User, value=1
        )
        self.RB_UserPath_Patient.grid(
            column=2, row=3, **gridConfigure
        )

        self.RB_UserPath_Researcher = ttk.Radiobutton(
            self.logIn_frame, text='Researcher',
            variable=self.Entry_User, value=0
        )
        self.RB_UserPath_Researcher.grid(
            column=2, row=4, **gridConfigure
        )

        # User, researcher or patient Insert ID
        self.Label_ID = ttk.Label(
            self.logIn_frame, text='User ID:', **labelConfigure
        )
        self.Label_ID.grid(
            column=1, row=5, padx=5, pady=0, sticky=tk.W
        )
        self.Entry_ID = ttk.Entry(
            self.logIn_frame, **entryConfigure
        )
        self.Entry_ID.insert(
            0, "ID"
        )
        self.Entry_ID.grid(
            column=2, row=5, **gridTEntryConfigure
        )
        self.Entry_ID.bind(
            "<FocusOut>", lambda e: entryFocusOut('ID')
        )
        self.Entry_ID.bind(
            "<Button-1>", lambda e: entryButton1('ID')
        )

        # User researcher or patient Insert Name
        self.Label_Name = ttk.Label(
            self.logIn_frame, text='User Name:', **labelConfigure
        )
        self.Label_Name.grid(
            column=1, row=6, padx=5, pady=0, sticky=tk.W
        )
        self.Entry_Name = ttk.Entry(
            self.logIn_frame, **entryConfigure
        )
        self.Entry_Name.insert(0, "Name")
        self.Entry_Name.grid(
            column=2, row=6, **gridTEntryConfigure
        )
        self.Entry_Name.bind(
            "<FocusOut>", lambda e: entryFocusOut('Name')
        )
        self.Entry_Name.bind(
            "<Button-1>", lambda e: entryButton1('Name')
        )

        # LOGIN button
        self.Button_LogIn = RoundedButton(
            master=self.logIn_frame, text="Log In", radius=25,
            btnbackground="DarkGoldenrod3", btnforeground="black",
            width=250, height=80, highlightthickness=0, font=("Helvetica", 25, "bold"),
            masterBackground='LightSkyBlue4'
        )
        self.Button_LogIn.grid(
            column=1, row=7, columnspan=cols
        )
        self.Button_LogIn.bind(
            "<Button-1>", lambda e: app_inputs.exLogIn()
        )

        # SingIN button
        self.Button_SignIN = RoundedButton(
            master=self.logIn_frame, text="Sign IN", radius=25,
            btnbackground="DarkGoldenrod3", btnforeground="black",
            width=250, height=80, highlightthickness=0, font=("Helvetica", 25, "bold"),
            masterBackground='LightSkyBlue4'
        )
        self.Button_SignIN.grid(
            column=1, row=8, columnspan=cols
        )
        self.Button_SignIN.bind(
            "<Button-1>", lambda e: app_inputs.exSignIN()
        )

    def raiseError(self, labelName):
        label = self.__dict__.get(f'Label_{labelName[0].upper()}{labelName[1:]}')
        if not label:
            return
        label.config(
            foreground="red"
        )
        return

    def deleteError(self, labelName):
        label = self.__dict__.get(f'Label_{labelName[0].upper()}{labelName[1:]}')
        if not label:
            return
        label.config(
            foreground="black"
        )
        return

    def getEntry(self, key):
        entry = self.__dict__.get(f'Entry_{key[0].upper()}{key[1:]}')
        if not entry:
            return
        if key == 'user':
            if entry.get() == 0:
                path = 'r'
            else:
                path = 'p'
            return path
        if isinstance(entry, tk.ttk.Entry):
            return entry.get()
        return


class PatientSignInPanel(SignInPanel):

    def __init__(self, MasterPanel):
        super().__init__(MasterPanel)
        self._create_sub_frames(MasterPanel)

    def _create_sub_frames(self, MasterPanel):
        def back():
            index = self.Page_Frames.index(
                self.Page_Frames.select()
            )
            if index == 1:
                self.Page_Frames.select(0)
            return

        # Back button
        self.Button_Back = RoundedButton(
            master=self, text="Back", radius=10, btnbackground="LightSkyBlue4", btnforeground="white",
            width=150, height=60, highlightthickness=0, font=("Helvetica", 18, "bold"),
            masterBackground='DarkGoldenrod2'
        )
        self.Button_Back.grid(
            column=2, row=1, padx=5, pady=5, sticky=tk.W
        )
        self.Button_Back.bind(
            "<Button-1>", lambda e: back()
        )
        # Next button
        self.Button_Next = RoundedButton(
            master=self, text="Next", radius=10, btnbackground="LightSkyBlue4", btnforeground="white", width=150,
            height=60, highlightthickness=0, font=("Helvetica", 18, "bold"), masterBackground='DarkGoldenrod2'
        )
        self.Button_Next.grid(
            column=4, row=1, padx=5, pady=5, sticky=tk.E
        )
        self.Button_Next.bind(
            "<Button-1>", lambda e: self.app_inputs.validUserSignIn()
        )
        self.Page_Frames = ttk.Notebook(
            self, width=700, height=600
        )
        self.Page_Frames.grid(
            column=2, row=3, padx=10, pady=10, sticky="nsew", columnspan=3, rowspan=2
        )
        self._initPatientSignInPg0(
            self.Page_Frames, style='TFrame'
        )
        self.pg0.grid(
            column=2, row=3, padx=10, pady=10, sticky="nsew", columnspan=3, rowspan=2
        )
        self._initPatientSignInPg1(
            self.Page_Frames, style='TFrame'
        )
        self.pg1.grid(
            column=2, row=3, padx=10, pady=10, sticky="nsew", columnspan=3, rowspan=2
        )
        self.Page_Frames.add(
            self.pg0, text='                Step 1                ',
        )
        self.Page_Frames.add(
            self.pg1, text='                Step 2                '
        )
        self.Page_Frames.select(0)
        self.Page_Frames.tab(1, state="disabled")
        return

    def _initPatientSignInPg0(self, MasterPanel, *args, **kwargs):
        self.pg0 = ttk.Frame(
            master=MasterPanel, *args, **kwargs
        )
        self.pg0.columnconfigure(
            list(range(1, 5)), weight=1
        )
        self.pg0.rowconfigure(
            list(range(1, 14)), weight=1
        )
        gridConfigure = {
            'padx': 20, 'pady': 0, 'sticky': tk.W
        }
        gridTEntryConfigure = {
            'padx': 20, 'pady': 0, 'sticky': tk.W, 'ipady': 5, 'ipadx': 0
        }
        entryConfigure = {
            'font': ("Helvetica", 18), 'background': 'white'
        }
        labelConfigure = {
            'font': ("Helvetica", 18, "bold"), 'background': 'white', 'borderwidth': 0
        }
        s = ttk.Style()
        s.configure(
            'Custom.TCombobox', background='white', foreground='black', font=('Helvetica', 18)
        )
        self.option_add(
            "*TCombobox*Listbox*font", ('Helvetica', 18)
        )
        # ------------------------- ID ------------------------------------------
        self.Label_ID = ttk.Label(
            self.pg0, text='ID: *', **labelConfigure
        )
        self.Label_ID.grid(
            column=1, row=1, **gridConfigure
        )
        self.Entry_ID = ttk.Entry(
            self.pg0, **entryConfigure
        )
        self.Entry_ID.grid(
            column=1, row=2, **gridTEntryConfigure
        )
        # ------------------------- Name ------------------------------------------
        self.Label_Name = ttk.Label(
            self.pg0, text='Name: *', **labelConfigure
        )
        self.Label_Name.grid(
            column=1, row=3, **gridConfigure
        )
        self.Entry_Name = ttk.Entry(
            self.pg0, **entryConfigure
        )
        self.Entry_Name.grid(
            column=1, row=4, columnspan=2, **gridTEntryConfigure
        )
        # ------------------------- Gender ------------------------------------------
        self.Label_Gender = ttk.Label(
            self.pg0, text='Gender: *', **labelConfigure
        )
        self.Label_Gender.grid(
            column=1, row=5, **gridConfigure
        )
        self.textVariable_Gender = tk.StringVar()
        self.Entry_Gender = ttk.Combobox(
            self.pg0, textvariable=self.textVariable_Gender, style='Custom.TCombobox', **entryConfigure
        )
        self.Entry_Gender['values'] = ('Female', 'Male')
        self.Entry_Gender.grid(
            column=1, row=6, **gridTEntryConfigure
        )
        # ------------------------- Area ------------------------------------------
        self.Label_Area = ttk.Label(
            self.pg0, text='Area: *', **labelConfigure
        )
        self.Label_Area.grid(
            column=1, row=7, **gridConfigure
        )
        self.textVariable_Area = tk.StringVar()
        self.Entry_Area = ttk.Combobox(
            self.pg0, textvariable=self.textVariable_Area, style='Custom.TCombobox', **entryConfigure
        )
        self.Entry_Area['values'] = ('North', 'Center', 'South')
        self.Entry_Area.grid(
            column=1, row=8, **gridTEntryConfigure
        )
        # ------------------------- City ------------------------------------------
        self.Label_City = ttk.Label(
            self.pg0, text='City: *', **labelConfigure
        )
        self.Label_City.grid(
            column=1, row=9, **gridConfigure
        )
        self.Entry_City = ttk.Entry(
            self.pg0, **entryConfigure
        )
        self.Entry_City.grid(
            column=1, row=10, columnspan=2, **gridTEntryConfigure
        )
        # ------------------------- Phone ------------------------------------------
        self.Label_Phone = ttk.Label(
            self.pg0, text='Phone: *', **labelConfigure
        )
        self.Label_Phone.grid(
            column=1, row=11, **gridConfigure
        )
        self.Entry_Phone = ttk.Entry(
            self.pg0, **entryConfigure
        )
        self.Entry_Phone.grid(
            column=1, row=12, columnspan=2, **gridTEntryConfigure
        )
        # ------------------------- Separator ------------------------------------------
        ttk.Separator(self.pg0, orient=VERTICAL).grid(
            row=1, column=2, rowspan=13, ipady=150, sticky=tk.N + tk.S + tk.E
        )
        # ------------------------- DOB ------------------------------------------
        self.Label_DOB = ttk.Label(
            self.pg0, text='Date of Birth: *', **labelConfigure
        )
        self.Label_DOB.grid(
            column=3, row=1, **gridConfigure
        )
        self.Entry_DOB = DateEntry(
            self.pg0, selectmode='day', date_pattern='MM-dd-yyyy', font=("Helvetica", 18, "bold"),
            firstweekday='sunday', weekenddays=[6, 7], background='LightSkyBlue4', foreground='white'
        )
        self.Entry_DOB.grid(
            column=3, row=2, **gridConfigure
        )
        # ------------------------- HMO ------------------------------------------
        self.Label_HMO = ttk.Label(
            self.pg0, text='HMO: *', **labelConfigure
        )
        self.Label_HMO.grid(
            column=3, row=3, **gridConfigure
        )
        self.textVariable_HMO = tk.StringVar()
        self.Entry_HMO = ttk.Combobox(
            self.pg0, textvariable=self.textVariable_HMO,
            style='Custom.TCombobox', **entryConfigure
        )
        self.Entry_HMO['values'] = ('Clalit', 'Maccabi', 'Meuhedet', 'Leumit')
        self.Entry_HMO.grid(
            column=3, row=4, **gridTEntryConfigure
        )
        # ------------------------- COB ------------------------------------------
        self.Label_COB = ttk.Label(
            self.pg0, text='Country Of Birth:', **labelConfigure
        )
        self.Label_COB.grid(
            column=3, row=5, **gridConfigure
        )
        self.Entry_COB = ttk.Entry(
            self.pg0, **entryConfigure
        )
        self.Entry_COB.insert(
            0, 'Israel'
        )
        self.Entry_COB.grid(
            column=3, row=6, **gridTEntryConfigure
        )

        def entryButton1(EntryName):
            entry = self.__dict__.get(f'Entry_{EntryName}')
            if not entry:
                return
            if EntryName == 'COB' and entry.get() == 'Israel':
                entry.delete(0, "end")
                return
            return

        def entryFocusOut(EntryName):
            entry = self.__dict__.get(f'Entry_{EntryName}')
            if not entry:
                return
            if not entry.get() and EntryName == 'COB':
                entry.insert(0, 'Israel')
                return
            return

        self.Entry_COB.bind(
            "<Button-1>", lambda e: entryButton1('COB')
        )
        self.Entry_COB.bind(
            "<FocusOut>", lambda e: entryFocusOut('COB')
        )
        # ------------------------- Height ------------------------------------------
        self.Label_Height = ttk.Label(
            self.pg0, text='Height: *', **labelConfigure
        )
        self.Label_Height.grid(
            column=3, row=7, **gridConfigure
        )
        self.Entry_Height = ttk.Entry(
            self.pg0, **entryConfigure
        )
        self.Entry_Height.grid(
            column=3, row=8, **gridTEntryConfigure
        )
        # ------------------------- Weight ------------------------------------------
        self.Label_Weight = ttk.Label(
            self.pg0, text='Weight: *', **labelConfigure
        )
        self.Label_Weight.grid(
            column=3, row=9, **gridConfigure
        )
        self.Entry_Weight = ttk.Entry(
            self.pg0, **entryConfigure
        )
        self.Entry_Weight.grid(
            column=3, row=10, **gridTEntryConfigure
        )
        # ------------------------- Support ------------------------------------------
        self.Label_Support = ttk.Label(
            self.pg0, text='Support: *', **labelConfigure
        )
        self.Label_Support.grid(
            column=3, row=11, **gridConfigure
        )
        self.textVariable_Support = tk.StringVar()
        self.Entry_Support = ttk.Combobox(
            self.pg0, textvariable=self.textVariable_Support, style='Custom.TCombobox', **entryConfigure
        )
        self.Entry_Support['values'] = ('Yes', 'No')
        self.Entry_Support.grid(
            column=3, row=12, **gridTEntryConfigure
        )
        return

    def _initPatientSignInPg1(self, MasterPanel, *args, **kwargs):
        self.pg1 = ttk.Frame(
            master=MasterPanel, *args, **kwargs
        )
        self.pg1.columnconfigure(
            list(range(1, 7)), weight=1
        )
        self.pg1.rowconfigure(
            list(range(1, 9)), weight=1
        )

        entryConfigure = {
            'font': ("Helvetica", 18), 'background': 'white'
        }
        labelConfigure = {
            'font': ("Helvetica", 18, "bold"), 'background': 'white', 'borderwidth': 0
        }
        s = ttk.Style()
        s.configure(
            'Custom.Treeview', rowheight=30, highlightthickness=2, bd=0, font=('Helvetica', 18)
        )
        s.map(
            "Custom.Treeview", background=[("selected", "ivory4")]
        )
        # ------------------------- Enter Symptoms ------------------------------------------
        self.Label_Symptoms = ttk.Label(
            self.pg1, text='Symptoms:', **labelConfigure
        )
        self.Label_Symptoms.grid(
            column=1, row=1, columnspan=2, sticky=tk.W + tk.N, padx=5, pady=10
        )
        self.Entry_InputSymptoms = ttk.Entry(
            self.pg1, textvariable=tk.StringVar(), width=40, **entryConfigure
        )
        self.Entry_InputSymptoms.grid(
            column=1, row=2, columnspan=2, sticky=tk.W + tk.N + tk.E, padx=5
        )
        self.Listbox_Symptoms = tk.Listbox(
            self.pg1, selectmode=tk.EXTENDED, font=("Helvetica", 18), bg='white',
            highlightcolor='white', highlightthickness=0, relief='flat', width=40
        )
        self.Listbox_Symptoms.grid(
            column=1, row=3, columnspan=2, rowspan=3, sticky=tk.W + tk.N + tk.E, padx=5, pady=10
        )
        self.Button_select = RoundedButton(
            master=self.pg1, text="Select", radius=10, btnbackground="seashell3", btnforeground="black",
            width=80, height=60, highlightthickness=0, font=("Helvetica", 18, "bold"), masterBackground='white'
        )
        self.Button_select.grid(
            column=1, row=7, sticky=tk.W + tk.N + tk.E
        )
        # ------------------------- Separator ------------------------------------------
        ttk.Separator(
            self.pg1, orient=VERTICAL).grid(row=2, column=3, rowspan=7, ipady=150, sticky=tk.N + tk.S
                                            )
        # ------------------------- Selected Symptoms ------------------------------------------
        self.Label_SelectSymptoms = ttk.Label(
            self.pg1, text='Selected Symptoms:', **labelConfigure
        )
        self.Label_SelectSymptoms.grid(
            column=4, row=1, columnspan=2, sticky=tk.W + tk.N, pady=10, padx=10
        )
        self.Entry_Symptoms = ttk.Treeview(
            self.pg1, selectmode='browse', style='Custom.Treeview'
        )
        self.Entry_Symptoms['columns'] = ['Symptoms']
        self.Entry_Symptoms.column(
            "#0", width=0, stretch=tk.NO
        )
        self.Entry_Symptoms.column(
            'Symptoms', anchor=tk.W, width=400
        )
        self.Entry_Symptoms.grid(
            column=4, row=3, columnspan=3, rowspan=3, sticky=tk.W + tk.N + tk.E
        )
        self.Entry_Symptoms.tag_configure(
            'odd', background='snow2'
        )
        self.Entry_Symptoms.tag_configure(
            'even', background='white'
        )
        self.Button_deleteSelect = RoundedButton(
            master=self.pg1, text="Delete Selected", radius=10, btnbackground="seashell3", btnforeground="black",
            width=80, height=60, highlightthickness=0, font=("Helvetica", 18, "bold"), masterBackground='white'
        )
        self.Button_deleteSelect.grid(
            column=4, row=7, sticky=tk.W + tk.N + tk.E
        )
        temp = self.master.__dict__.get('symptomsTrie')
        if temp:
            self.AutoComplete = AUTO_complete(
                temp, self.Entry_InputSymptoms, self.Listbox_Symptoms,
                treeview=self.Entry_Symptoms,
                select=self.Button_select, deleteSelect=self.Button_deleteSelect
            )
        # ------------------------- SignIN ------------------------------------------
        self.Button_SignIN = RoundedButton(
            master=self.pg1, text="Sign In", radius=10, btnbackground="LightSkyBlue4", btnforeground="white",
            width=150, height=60, highlightthickness=0, font=("Helvetica", 18, "bold"), masterBackground='white'
        )
        self.Button_SignIN.grid(
            column=6, row=8, sticky=tk.E + tk.S + tk.W
        )
        self.Button_SignIN.bind(
            "<Button-1>", lambda e: self.app_inputs.validUserSignIn()
        )
        self.Entry_Conifer = tk.IntVar()
        self.Check_conifer = tk.Checkbutton(
            self.pg1, text="I agree to the terms", variable=self.Entry_Conifer, onvalue=1, offvalue=0, width=20,
            background="white", font=("Helvetica", 12), foreground='black'
        )
        self.Check_conifer.grid(
            column=6, row=9, sticky=tk.E + tk.S + tk.W
        )
        return


class PatientMainPanel(MainPanel):

    def __init__(self, MasterPanel):
        super().__init__(MasterPanel)
        self._initNoteBook()

    def _initNoteBook(self):
        index = 0
        if self.__dict__.get('Page_Frames'):
            Page_Frames = self.__dict__.get('Page_Frames')
            index = Page_Frames.index(
                Page_Frames.select()
            )
            Page_Frames.destroy()
        self.Page_Frames = ttk.Notebook(
            self, width=800, height=600
        )
        self.Page_Frames.grid(
            column=1, row=2, padx=1, pady=1, sticky="nsew", columnspan=3, rowspan=3
        )
        self._initPatientMainPg0(
            self.Page_Frames, style='TFrame'
        )
        self.pg0.grid(
            column=2, row=3, padx=10, pady=10, sticky="nsew", columnspan=3, rowspan=2
        )
        self._initPatientMainPg1(
            self.Page_Frames, style='TFrame'
        )
        self.pg1.grid(
            column=2, row=3, padx=10, pady=10, sticky="nsew", columnspan=3, rowspan=2
        )
        self._initPatientMainPg2(
            self.Page_Frames, style='TFrame'
        )
        self.pg2.grid(
            column=2, row=3, padx=10, pady=10, sticky="nsew", columnspan=3, rowspan=2
        )
        self.Page_Frames.add(
            self.pg0, text='                Profile                ',
        )
        self.Page_Frames.add(
            self.pg1, text='                Symptoms                '
        )
        self.Page_Frames.add(
            self.pg2, text='                Available Researches                '
        )
        self.Page_Frames.select(index)
        return

    def _initPatientMainPg0(self, MasterPanel, *args, **kwargs):
        UserIndices = self.app_queries.dequeueUserIndices('PatientMainPg0')
        self.pg0 = ttk.Frame(
            master=MasterPanel, *args, **kwargs
        )
        self.pg0.columnconfigure(
            list(range(1, 10)), weight=1
        )
        self.pg0.rowconfigure(
            list(range(1, 14)), weight=1
        )
        self.pg0.UserIndices = UserIndices
        gridConfigure = {
            'padx': 5, 'pady': 5, 'sticky': tk.W
        }
        gridTEntryConfigure = {
            'padx': 5, 'pady': 0, 'sticky': tk.W, 'ipady': 0, 'ipadx': 0
        }
        entryConfigure = {
            'font': ("Helvetica", 18), 'background': 'white'
        }
        labelConfigure = {
            'font': ("Helvetica", 18, "bold"), 'background': 'white', 'borderwidth': 0,
            'foreground': 'LightSkyBlue4'
        }
        s = ttk.Style()
        s.configure(
            'Custom.Treeview', rowheight=30, highlightthickness=2, bd=0, font=('Helvetica', 18)
        )
        s.configure(
            'Custom.Treeview.Heading', background='seashell3', foreground='black', font=('Helvetica', 18, 'bold')
        )
        s.configure(
            'Custom.TCombobox', background='white', foreground='black', font=('Helvetica', 18)
        )
        self.option_add(
            "*TCombobox*Listbox*font", ('Helvetica', 18)
        )
        s.map(
            "Custom.Treeview", background=[("selected", "ivory4")]
        )
        Indices = self.pg0.UserIndices['Indices']
        researchers = self.pg0.UserIndices['researchers']
        # ------------------------- ID ------------------------------------------
        self.pg0.Label_ID = ttk.Label(
            self.pg0, text='ID:', **labelConfigure
        )
        self.pg0.Label_ID.grid(
            column=1, row=1, **gridConfigure
        )
        self.pg0.Entry_ID = ttk.Entry(
            self.pg0, **entryConfigure
        )
        self.pg0.Entry_ID.grid(
            column=1, row=2, **gridTEntryConfigure
        )
        self.pg0.Entry_ID.insert(
            0, Indices['ID']
        )
        self.pg0.Entry_ID.config(
            state="disabled"
        )
        # ------------------------- Name ------------------------------------------
        self.pg0.Label_Name = ttk.Label(
            self.pg0, text='Name:', **labelConfigure
        )
        self.pg0.Label_Name.grid(
            column=1, row=3, **gridConfigure
        )
        self.pg0.Entry_Name = ttk.Entry(
            self.pg0, **entryConfigure
        )
        self.pg0.Entry_Name.grid(
            column=1, row=4, columnspan=2, **gridTEntryConfigure
        )
        self.pg0.Entry_Name.insert(
            0, Indices['name']
        )
        self.pg0.Entry_Name.config(
            state="disabled"
        )
        # ------------------------- Gender ------------------------------------------
        self.pg0.Label_Gender = ttk.Label(
            self.pg0, text='Gender:', **labelConfigure
        )
        self.pg0.Label_Gender.grid(
            column=1, row=5, **gridConfigure
        )
        self.pg0.Entry_Gender = ttk.Entry(
            self.pg0, **entryConfigure
        )
        self.pg0.Entry_Gender.grid(
            column=1, row=6, **gridTEntryConfigure
        )
        self.pg0.Entry_Gender.insert(
            0, Indices['gender']
        )
        self.pg0.Entry_Gender.config(
            state="disabled"
        )
        # ------------------------- Area ------------------------------------------
        self.pg0.Label_Area = ttk.Label(
            self.pg0, text='Area:', **labelConfigure
        )
        self.pg0.Label_Area.grid(
            column=1, row=7, **gridConfigure
        )
        area = ''
        for val in ('North', 'Center', 'South'):
            if Indices['area'][0] == val[0]:
                area = val
                break
        self.pg0.textVariable_Area = tk.StringVar(value=area)
        self.pg0.Entry_Area = ttk.Combobox(
            self.pg0, textvariable=self.pg0.textVariable_Area,
            style='Custom.TCombobox', **entryConfigure
        )
        self.pg0.Entry_Area['values'] = (
            'North', 'Center', 'South'
        )
        self.pg0.Entry_Area.grid(
            column=1, row=8, **gridTEntryConfigure
        )
        # ------------------------- City ------------------------------------------
        self.pg0.Label_City = ttk.Label(
            self.pg0, text='City:', **labelConfigure
        )
        self.pg0.Label_City.grid(
            column=1, row=9, **gridConfigure
        )
        self.pg0.Entry_City = ttk.Entry(
            self.pg0, **entryConfigure
        )
        self.pg0.Entry_City.grid(
            column=1, row=10, columnspan=2, **gridTEntryConfigure
        )
        self.pg0.Entry_City.insert(
            0, Indices['city']
        )
        # ------------------------- Phone ------------------------------------------
        self.pg0.Label_Phone = ttk.Label(
            self.pg0, text='Phone:', **labelConfigure
        )
        self.pg0.Label_Phone.grid(
            column=1, row=11, **gridConfigure
        )
        self.pg0.Entry_Phone = ttk.Entry(
            self.pg0, **entryConfigure
        )
        self.pg0.Entry_Phone.grid(
            column=1, row=12, columnspan=2, **gridTEntryConfigure
        )
        self.pg0.Entry_Phone.insert(
            0, Indices['phone']
        )
        # ------------------------- Separator ------------------------------------------
        ttk.Separator(self.pg0, orient=VERTICAL).grid(
            row=1, column=1, rowspan=13, ipady=150, sticky=tk.N + tk.S + tk.E
        )
        # ------------------------- DOB ------------------------------------------
        self.pg0.Label_DOB = ttk.Label(
            self.pg0, text='Date of Birth:', **labelConfigure
        )
        self.pg0.Label_DOB.grid(
            column=2, row=1, **gridConfigure
        )
        self.pg0.Entry_DOB = ttk.Entry(
            self.pg0, **entryConfigure
        )
        self.pg0.Entry_DOB.grid(
            column=2, row=2, **gridConfigure
        )
        self.pg0.Entry_DOB.insert(
            0, Indices['DOB']
        )
        self.pg0.Entry_DOB.config(
            state="disabled"
        )
        # ------------------------- HMO ------------------------------------------
        self.pg0.Label_HMO = ttk.Label(
            self.pg0, text='HMO:', **labelConfigure
        )
        self.pg0.Label_HMO.grid(
            column=2, row=3, **gridConfigure
        )
        self.pg0.textVariable_HMO = tk.StringVar(
            value=Indices['HMO']
        )
        self.pg0.Entry_HMO = ttk.Combobox(
            self.pg0, textvariable=self.pg0.textVariable_HMO, style='Custom.TCombobox', **entryConfigure
        )
        self.pg0.Entry_HMO['values'] = (
            'Clalit', 'Maccabi', 'Meuhedet', 'Leumit'
        )
        self.pg0.Entry_HMO.grid(
            column=2, row=4, **gridTEntryConfigure
        )
        # ------------------------- COB ------------------------------------------
        self.pg0.Label_COB = ttk.Label(
            self.pg0, text='Country Of Birth:', **labelConfigure
        )
        self.pg0.Label_COB.grid(
            column=2, row=5, **gridConfigure
        )
        self.pg0.Entry_COB = ttk.Entry(
            self.pg0, **entryConfigure
        )
        self.pg0.Entry_COB.insert(
            0, Indices['COB']
        )
        self.pg0.Entry_COB.grid(
            column=2, row=6, **gridTEntryConfigure
        )
        self.pg0.Entry_COB.config(
            state="disabled"
        )
        # ------------------------- Height ------------------------------------------
        self.pg0.Label_Height = ttk.Label(
            self.pg0, text='Height:', **labelConfigure
        )
        self.pg0.Label_Height.grid(
            column=2, row=7, **gridConfigure
        )
        self.pg0.Entry_Height = tk.Entry(
            self.pg0, **entryConfigure
        )
        self.pg0.Entry_Height.grid(
            column=2, row=8, **gridTEntryConfigure
        )
        self.pg0.Entry_Height.insert(
            0, Indices['height']
        )
        # ------------------------- Weight ------------------------------------------
        self.pg0.Label_Weight = ttk.Label(
            self.pg0, text='Weight:', **labelConfigure
        )
        self.pg0.Label_Weight.grid(
            column=2, row=9, **gridConfigure
        )
        self.pg0.Entry_Weight = ttk.Entry(
            self.pg0, **entryConfigure
        )
        self.pg0.Entry_Weight.grid(
            column=2, row=10, **gridTEntryConfigure
        )
        self.pg0.Entry_Weight.insert(
            0, Indices['weight']
        )
        # ------------------------- Support ------------------------------------------
        self.pg0.Label_Support = ttk.Label(
            self.pg0, text='Support:', **labelConfigure
        )
        self.pg0.Label_Support.grid(
            column=2, row=11, **gridConfigure
        )
        sup = Indices['support']
        if sup == '1':
            sup = 'Yes'
        else:
            sup = 'No'
        self.pg0.textVariable_Support = tk.StringVar(value=sup)
        self.pg0.Entry_Support = ttk.Combobox(
            self.pg0, textvariable=self.pg0.textVariable_Support, style='Custom.TCombobox', **entryConfigure
        )
        self.pg0.Entry_Support['values'] = (
            'Yes', 'No'
        )
        self.pg0.Entry_Support.grid(
            column=2, row=12, **gridTEntryConfigure
        )

        # ------------------------- Separator ------------------------------------------
        ttk.Separator(
            self.pg0, orient=VERTICAL
        ).grid(
            row=1, column=3, rowspan=13, ipady=150, sticky=tk.N + tk.S
        )
        # ------------------------- Researchers ------------------------------------------

        self.pg0.Label_Researchers = ttk.Label(
            self.pg0, text='Researchers in which you participate:', **labelConfigure
        )
        self.pg0.Label_Researchers.grid(
            column=5, row=1, columnspan=3, sticky=tk.N + tk.W + tk.E, pady=5, padx=5
        )
        self.pg0.Table_Researchers = ttk.Treeview(
            self.pg0, style='Custom.Treeview'
        )
        self.pg0.Table_Researchers['columns'] = list(
            researchers.columns
        )
        self.pg0.Table_Researchers.column(
            "#0", width=0, stretch=tk.NO
        )
        for col in list(researchers.columns):
            w = 100
            if col == 'Mail':
                w = 200
            self.pg0.Table_Researchers.column(
                col, anchor=tk.CENTER, width=w, stretch=True
            )
            self.pg0.Table_Researchers.heading(
                col, text=col, anchor=tk.CENTER
            )
        for row in researchers.index:
            vals = list(researchers.loc[row, :])
            if row % 2:
                self.pg0.Table_Researchers.insert(
                    parent='', index='end', iid=int(row), text='', values=vals, tags=('even',)
                )
            else:
                self.pg0.Table_Researchers.insert(
                    parent='', index='end', iid=int(row), text='', values=vals, tags=('odd',)
                )
        self.pg0.Table_Researchers.tag_configure(
            'odd', background='snow2'
        )
        self.pg0.Table_Researchers.tag_configure(
            'even', background='white'
        )
        self.pg0.Table_Researchers.grid(
            column=5, row=3, columnspan=5, rowspan=9, sticky=tk.N + tk.W + tk.E, pady=5
        )
        self.pg0.Button_UpDate = RoundedButton(
            master=self.pg0, text="UPDATE", radius=10, btnbackground="LightSkyBlue4", btnforeground="white",
            width=150, height=60, highlightthickness=0, font=("Helvetica", 18, "bold"), masterBackground='white'
        )
        self.pg0.Button_UpDate.grid(
            column=9, row=14, padx=5, pady=5, sticky=tk.W
        )
        self.pg0.Button_UpDate.bind(
            '<Button-1>', lambda e: self.buttonUpDate()
        )
        return

    def _initPatientMainPg1(self, MasterPanel, *args, **kwargs):
        UserSymptoms = self.app_queries.dequeueUserIndices('PatientMainPg1')
        self.pg1 = ttk.Frame(
            master=MasterPanel, *args, **kwargs
        )
        self.pg1.columnconfigure(
            list(range(1, 9)), weight=1
        )
        self.pg1.rowconfigure(
            list(range(1, 14)), weight=1
        )
        entryConfigure = {
            'font': ("Helvetica", 18), 'background': 'white'
        }
        labelConfigure = {
            'font': ("Helvetica", 18, "bold"), 'background': 'white', 'borderwidth': 0, 'foreground': 'LightSkyBlue4'
        }
        s = ttk.Style()
        s.configure(
            'Custom.Treeview', rowheight=30, highlightthickness=2, bd=0, font=('Helvetica', 18)
        )
        s.map(
            "Custom.Treeview", background=[("selected", "ivory4")]
        )
        # ------------------------- Symptoms ------------------------------------------
        self.pg1.Label_UserSymptoms = ttk.Label(
            self.pg1, text='Your Symptoms:', **labelConfigure
        )
        self.pg1.Label_UserSymptoms.grid(
            column=1, row=1, columnspan=3, sticky=tk.W + tk.N, padx=10, pady=10
        )
        self.pg1.Table_UserSymptoms = ttk.Treeview(
            self.pg1, style='Custom.Treeview'
        )
        self.pg1.Table_UserSymptoms['columns'] = ['Symptoms']
        self.pg1.Table_UserSymptoms.column(
            "#0", width=0, stretch=tk.NO
        )
        self.pg1.Table_UserSymptoms.column(
            'Symptoms', anchor=tk.W, width=400
        )
        self.pg1.Table_UserSymptoms.tag_configure(
            'odd', background='snow2'
        )
        self.pg1.Table_UserSymptoms.tag_configure(
            'even', background='white'
        )
        self.pg1.Table_UserSymptoms.grid(
            column=1, row=2, columnspan=3, rowspan=4, sticky=tk.W + tk.E, padx=10
        )
        self.pg1.Button_deleteSelect = RoundedButton(
            master=self.pg1, text="Delete Selected", radius=10, btnbackground="LightSkyBlue4", btnforeground="white",
            width=80, height=60, highlightthickness=0, font=("Helvetica", 18, "bold"), masterBackground='white'
        )
        self.pg1.Button_deleteSelect.grid(
            column=1, row=6, sticky=tk.W + tk.E
        )
        # ------------------------- Separator ------------------------------------------
        ttk.Separator(
            self.pg1, orient=VERTICAL
        ).grid(
            row=1, column=4, rowspan=13, ipady=150, sticky=tk.N + tk.S
        )
        # ------------------------- New Symptoms ------------------------------------------
        self.pg1.Label_NewUserSymptoms = ttk.Label(
            self.pg1, text='Search for Symptoms:', **labelConfigure
        )
        self.pg1.Label_NewUserSymptoms.grid(
            column=5, row=1, columnspan=2, sticky=tk.W + tk.N, pady=10, padx=10
        )
        self.pg1.Entry_UserSymptomsNew = ttk.Entry(
            self.pg1, textvariable=tk.StringVar(), width=40, **entryConfigure
        )
        self.pg1.Entry_UserSymptomsNew.grid(
            column=5, row=2, columnspan=2, rowspan=2, sticky=tk.W + tk.N + tk.E
        )
        self.pg1.Listbox_NewUserSymptoms = tk.Listbox(
            self.pg1, selectmode=tk.EXTENDED, font=("Helvetica", 18), bg='white', highlightcolor='LightSkyBlue4',
            highlightthickness=1, relief='flat', width=40
        )
        self.pg1.Listbox_NewUserSymptoms.grid(
            column=5, row=3, columnspan=2, rowspan=3, sticky=tk.W + tk.E, padx=10
        )
        self.pg1.Button_select = RoundedButton(
            master=self.pg1, text="Select", radius=10, btnbackground="LightSkyBlue4", btnforeground="white",
            width=80, height=60, highlightthickness=0, font=("Helvetica", 18, "bold"), masterBackground='white'
        )
        self.pg1.Button_select.grid(
            column=5, row=6, sticky=tk.W + tk.E
        )
        temp = self.master.__dict__.get('symptomsTrie')
        if temp:
            self.AutoComplete = AUTO_complete(
                temp, self.pg1.Entry_UserSymptomsNew, self.pg1.Listbox_NewUserSymptoms,
                treeview=self.pg1.Table_UserSymptoms, select=self.pg1.Button_select,
                deleteSelect=self.pg1.Button_deleteSelect, initSymptoms=UserSymptoms
            )
        self.pg1.Button_UpDate = RoundedButton(
            master=self.pg1, text="UPDATE", radius=10, btnbackground="LightSkyBlue4",
            btnforeground="white", width=150, height=60, highlightthickness=0,
            font=("Helvetica", 18, "bold"), masterBackground='white'
        )
        self.pg1.Button_UpDate.grid(
            column=9, row=14, padx=5, pady=5, sticky=tk.W
        )
        self.pg1.Button_UpDate.bind(
            '<Button-1>', lambda e: self.buttonUpDate()
        )
        return

    def _initPatientMainPg2(self, MasterPanel, *args, **kwargs):
        availableResearch = self.app_queries.dequeueUserIndices('PatientMainPg2')
        self.pg2 = ttk.Frame(
            master=MasterPanel, *args, **kwargs
        )
        self.pg2.columnconfigure(
            list(range(1, 5)), weight=1
        )
        self.pg2.rowconfigure(
            list(range(1, 7)), weight=1
        )
        self.pg2.availableResearch = availableResearch
        labelConfigure = {
            'font': ("Helvetica", 18, "bold"), 'background': 'white', 'borderwidth': 0, 'foreground': 'LightSkyBlue4'
        }
        s = ttk.Style()
        s.configure(
            'Custom.Treeview', rowheight=30, highlightthickness=2, bd=0, font=('Helvetica', 18)
        )
        s.configure(
            'Custom.Treeview.Heading', background='seashell3', foreground='black', font=('Helvetica', 18, 'bold')
        )
        s.map(
            "Custom.Treeview", background=[("selected", "ivory4")]
        )
        # ------------------------- Researchers ------------------------------------------
        self.pg2.Label_Researchers = ttk.Label(
            self.pg2, text='Available Researchers for you:', **labelConfigure
        )
        self.pg2.Label_Researchers.grid(
            column=1, row=1, columnspan=3, sticky=tk.W, pady=5, padx=5
        )
        self.pg2.Table_AvailableResearch = ttk.Treeview(
            self.pg2, style='Custom.Treeview'
        )
        self.pg2.Table_AvailableResearch['columns'] = list(
            availableResearch.columns
        )
        self.pg2.Table_AvailableResearch.column(
            "#0", width=0, stretch=tk.NO
        )
        for col in list(availableResearch.columns):
            w = 100
            if col == 'Mail':
                w = 200
            self.pg2.Table_AvailableResearch.column(
                col, anchor=tk.CENTER, width=w
            )
            self.pg2.Table_AvailableResearch.heading(
                col, text=col, anchor=tk.CENTER
            )
        for row in availableResearch.index:
            vals = list(availableResearch.loc[row, :])
            if row % 2:
                self.pg2.Table_AvailableResearch.insert(
                    parent='', index='end', iid=int(row), text='', values=vals, tags=('even',)
                )
            else:
                self.pg2.Table_AvailableResearch.insert(
                    parent='', index='end', iid=int(row), text='', values=vals, tags=('odd',)
                )

        self.pg2.Table_AvailableResearch.tag_configure(
            'odd', background='snow2'
        )
        self.pg2.Table_AvailableResearch.tag_configure(
            'even', background='white'
        )
        self.pg2.Table_AvailableResearch.grid(
            column=1, row=2, columnspan=4, rowspan=3, sticky=tk.W + tk.E, padx=5
        )
        return


class ResearcherSignInPanel(SignInPanel):
    def __init__(self, MasterPanel):
        super().__init__(MasterPanel)
        self._create_sub_frames(MasterPanel)

    def _create_sub_frames(self, MasterPanel):
        self.Page_Frames = ttk.Notebook(
            self, width=700, height=600
        )
        self.Page_Frames.grid(
            column=2, row=3, padx=10, pady=10, sticky="nsew", columnspan=3, rowspan=2
        )

        self._initResearcherSignInPg0(
            self.Page_Frames, style='TFrame'
        )
        self.pg0.grid(
            column=2, row=3, padx=10, pady=10, sticky="nsew", columnspan=3, rowspan=2
        )

        self.Page_Frames.add(
            self.pg0, text='                        Personal Details                        ',
        )
        self.Page_Frames.select(0)
        return

    def _initResearcherSignInPg0(self, MasterPanel, *args, **kwargs):
        self.pg0 = ttk.Frame(
            master=MasterPanel, *args, **kwargs
        )
        self.pg0.columnconfigure(
            list(range(1, 5)), weight=1
        )
        self.pg0.rowconfigure(
            list(range(1, 14)), weight=1
        )

        gridConfigure = {
            'padx': 20, 'pady': 0, 'sticky': tk.W
        }
        gridTEntryConfigure = {
            'padx': 20, 'pady': 0, 'sticky': tk.W, 'ipady': 5, 'ipadx': 0
        }
        entryConfigure = {
            'font': ("Helvetica", 18), 'background': 'white'
        }
        labelConfigure = {
            'font': ("Helvetica", 18, "bold"), 'background': 'white', 'borderwidth': 0
        }

        # ------------------------- ID ------------------------------------------
        self.Label_ID = ttk.Label(
            self.pg0, text='ID: *', **labelConfigure
        )
        self.Label_ID.grid(
            column=1, row=1, **gridConfigure
        )
        self.Entry_ID = ttk.Entry(
            self.pg0, **entryConfigure
        )
        self.Entry_ID.grid(
            column=1, row=2, **gridTEntryConfigure
        )
        # ------------------------- FName ------------------------------------------
        self.Label_Fname = ttk.Label(
            self.pg0, text='First Name: *', **labelConfigure
        )
        self.Label_Fname.grid(
            column=1, row=3, **gridConfigure
        )
        self.Entry_Fname = ttk.Entry(
            self.pg0, **entryConfigure
        )
        self.Entry_Fname.grid(
            column=1, row=4, columnspan=2, **gridTEntryConfigure
        )
        # ------------------------- LName ------------------------------------------
        self.Label_Lname = ttk.Label(
            self.pg0, text='Last Name: *', **labelConfigure
        )
        self.Label_Lname.grid(
            column=1, row=5, **gridConfigure
        )
        self.Entry_Lname = ttk.Entry(
            self.pg0, **entryConfigure
        )
        self.Entry_Lname.grid(
            column=1, row=6, columnspan=2, **gridTEntryConfigure
        )
        # ------------------------- Gender ------------------------------------------
        self.Label_Gender = ttk.Label(
            self.pg0, text='Gender: *', **labelConfigure
        )
        self.Label_Gender.grid(
            column=1, row=7, **gridConfigure
        )
        self.textVariable_Gender = tk.StringVar()
        self.Entry_Gender = ttk.Combobox(
            self.pg0, textvariable=self.textVariable_Gender, **entryConfigure
        )
        self.Entry_Gender['values'] = (
            'Female', 'Male'
        )
        self.Entry_Gender.grid(
            column=1, row=8, **gridTEntryConfigure
        )
        # ------------------------- Phone ------------------------------------------
        self.Label_Phone = ttk.Label(
            self.pg0, text='Phone: *', **labelConfigure
        )
        self.Label_Phone.grid(
            column=3, row=1, **gridConfigure
        )
        self.Entry_Phone = ttk.Entry(
            self.pg0, **entryConfigure
        )
        self.Entry_Phone.grid(
            column=3, row=2, columnspan=2, **gridTEntryConfigure
        )
        # ------------------------- Mail ------------------------------------------
        self.Label_Mail = ttk.Label(
            self.pg0, text='Mail: *', **labelConfigure
        )
        self.Label_Mail.grid(
            column=3, row=3, **gridConfigure
        )
        self.Entry_Mail = ttk.Entry(
            self.pg0, **entryConfigure
        )
        self.Entry_Mail.grid(
            column=3, row=4, columnspan=2, **gridTEntryConfigure
        )
        # ------------------------- SignIN ------------------------------------------
        self.Button_SignIN = RoundedButton(
            master=self.pg0, text="Sign In", radius=10, btnbackground="LightSkyBlue4",
            btnforeground="white", width=150, height=60, highlightthickness=0,
            font=("Helvetica", 18, "bold"), masterBackground='white'
        )
        self.Button_SignIN.grid(
            column=3, row=6, sticky=tk.E + tk.S + tk.W
        )
        self.Button_SignIN.bind(
            "<Button-1>", lambda e: self.app_inputs.validUserSignIn()
        )
        self.Entry_Conifer = tk.IntVar()
        self.Check_conifer = tk.Checkbutton(
            self.pg0, text="I agree to the terms", variable=self.Entry_Conifer,
            onvalue=1, offvalue=0, width=20, background="white", font=("Helvetica", 12), foreground='black'
        )
        self.Check_conifer.grid(
            column=3, row=7, sticky=tk.E + tk.S + tk.W
        )
        return

    def getEntry(self, key):
        entry = self.__dict__.get(f'Entry_{key[0].upper()}{key[1:]}')
        if type(entry) == tkcalendar.DateEntry:
            return entry.get_date()
        if isinstance(entry, tk.ttk.Entry) or type(entry) == tk.IntVar:
            return entry.get()
        return


class ResearcherMainPanel(MainPanel):

    def __init__(self, MasterPanel):
        super().__init__(MasterPanel)
        self._initNoteBook()

    def _initNoteBook(self):
        index = 0
        if self.__dict__.get('Page_Frames'):
            Page_Frames = self.__dict__.get('Page_Frames')
            index = Page_Frames.index(Page_Frames.select())
            Page_Frames.destroy()
        self.Page_Frames = ttk.Notebook(
            self, width=800, height=600
        )
        self.Page_Frames.grid(
            column=1, row=2, padx=1, pady=1, sticky="nsew", columnspan=3, rowspan=3
        )
        self._initResearcherMainPg0(
            self.Page_Frames, style='TFrame'
        )
        self.pg0.grid(
            column=2, row=3, padx=10, pady=10, sticky="nsew", columnspan=3, rowspan=2
        )
        self._initResearcherMainPg1(
            self.Page_Frames, style='TFrame'
        )
        self.pg1.grid(
            column=2, row=3, padx=10, pady=10, sticky="nsew", columnspan=3, rowspan=2
        )
        self._initResearcherMainPg2(
            self.Page_Frames, style='TFrame'
        )
        self.pg2.grid(
            column=2, row=3, padx=10, pady=10, sticky="nsew", columnspan=3, rowspan=2
        )
        self._initResearcherMainPg3(
            self.Page_Frames, style='TFrame'
        )
        self.pg3.grid(
            column=2, row=3, padx=10, pady=10, sticky="nsew", columnspan=3, rowspan=2
        )
        self._initResearcherMainPg4(
            self.Page_Frames, style='TFrame'
        )
        self.pg4.grid(
            column=2, row=3, padx=10, pady=10, sticky="nsew", columnspan=3, rowspan=2
        )
        self.Page_Frames.add(
            self.pg0, text='Profile'
        )
        self.Page_Frames.add(
            self.pg1, text='New Research'
        )
        self.Page_Frames.add(
            self.pg2, text='Available patients'
        )
        self.Page_Frames.add(
            self.pg3, text='Add New Disease'
        )
        self.Page_Frames.add(
            self.pg4, text='Add New Symptom'
        )
        self.Page_Frames.select(index)
        return

    def _initResearcherMainPg0(self, MasterPanel, *args, **kwargs):
        UserIndices = self.app_queries.dequeueUserIndices('ResearcherMainPg0')
        self.pg0 = ttk.Frame(
            master=MasterPanel, *args, **kwargs
        )
        self.pg0.columnconfigure(
            list(range(1, 10)), weight=1
        )
        self.pg0.rowconfigure(
            list(range(1, 14)), weight=1
        )
        self.pg0.UserIndices = UserIndices
        gridConfigure = {
            'padx': 5, 'pady': 5, 'sticky': tk.W
        }
        gridTEntryConfigure = {
            'padx': 5, 'pady': 0, 'sticky': tk.W, 'ipady': 0, 'ipadx': 0
        }
        entryConfigure = {
            'font': ("Helvetica", 18), 'background': 'white'
        }
        labelConfigure = {
            'font': ("Helvetica", 18, "bold"), 'background': 'white', 'borderwidth': 0, 'foreground': 'LightSkyBlue4'
        }
        s = ttk.Style()
        s.configure(
            'Custom.Treeview', rowheight=30, highlightthickness=2, bd=0, font=('Helvetica', 18)
        )
        s.configure(
            'Custom.Treeview.Heading', background='seashell3', foreground='black', font=('Helvetica', 18, 'bold')
        )
        s.map(
            "Custom.Treeview", background=[("selected", "ivory4")]
        )
        Indices = self.pg0.UserIndices['Indices']
        researchers = self.pg0.UserIndices['researchers']
        # ------------------------- ID ------------------------------------------
        self.pg0.Label_ID = ttk.Label(
            self.pg0, text='ID:', **labelConfigure
        )
        self.pg0.Label_ID.grid(
            column=2, row=1, **gridConfigure
        )
        self.pg0.Entry_ID = ttk.Entry(
            self.pg0, **entryConfigure
        )
        self.pg0.Entry_ID.grid(
            column=2, row=2, **gridTEntryConfigure
        )
        self.pg0.Entry_ID.insert(
            0, Indices['ID']
        )
        self.pg0.Entry_ID.config(
            state="disabled"
        )
        # ------------------------- FName ------------------------------------------
        self.pg0.Label_Fname = ttk.Label(
            self.pg0, text='First Name:', **labelConfigure
        )
        self.pg0.Label_Fname.grid(
            column=2, row=3, **gridConfigure
        )
        self.pg0.Entry_Fname = ttk.Entry(
            self.pg0, **entryConfigure
        )
        self.pg0.Entry_Fname.grid(
            column=2, row=4, columnspan=2, **gridTEntryConfigure
        )
        self.pg0.Entry_Fname.insert(
            0, Indices['Fname']
        )
        self.pg0.Entry_Fname.config(
            state="disabled"
        )
        # ------------------------- LName ------------------------------------------
        self.pg0.Label_Lname = ttk.Label(
            self.pg0, text='Last Name:', **labelConfigure
        )
        self.pg0.Label_Lname.grid(
            column=2, row=5, **gridConfigure
        )
        self.pg0.Entry_Lname = ttk.Entry(
            self.pg0, **entryConfigure
        )
        self.pg0.Entry_Lname.grid(
            column=2, row=6, columnspan=2, **gridTEntryConfigure
        )
        self.pg0.Entry_Lname.insert(
            0, Indices['Lname']
        )
        self.pg0.Entry_Lname.config(
            state="disabled"
        )
        # ------------------------- Gender ------------------------------------------
        self.pg0.Label_Gender = ttk.Label(
            self.pg0, text='Gender:', **labelConfigure
        )
        self.pg0.Label_Gender.grid(
            column=2, row=7, **gridConfigure
        )
        self.pg0.Entry_Gender = ttk.Entry(
            self.pg0, **entryConfigure
        )
        self.pg0.Entry_Gender.grid(
            column=2, row=8, **gridTEntryConfigure
        )
        self.pg0.Entry_Gender.insert(
            0, Indices['gender']
        )
        self.pg0.Entry_Gender.config(
            state="disabled"
        )
        # ------------------------- Phone ------------------------------------------
        self.pg0.Label_Phone = ttk.Label(
            self.pg0, text='Phone:', **labelConfigure
        )
        self.pg0.Label_Phone.grid(
            column=2, row=9, **gridConfigure
        )
        self.pg0.Entry_Phone = ttk.Entry(
            self.pg0, **entryConfigure
        )
        self.pg0.Entry_Phone.grid(
            column=2, row=10, columnspan=2, **gridTEntryConfigure
        )
        self.pg0.Entry_Phone.insert(
            0, Indices['phone']
        )
        # ------------------------- Mail ------------------------------------------
        self.pg0.Label_Mail = ttk.Label(
            self.pg0, text='Mail:', **labelConfigure
        )
        self.pg0.Label_Mail.grid(
            column=2, row=11, **gridConfigure
        )
        self.pg0.Entry_Mail = ttk.Entry(
            self.pg0, **entryConfigure
        )
        self.pg0.Entry_Mail.grid(
            column=2, row=12, columnspan=2, **gridTEntryConfigure
        )
        self.pg0.Entry_Mail.insert(
            0, Indices['Mail']
        )
        self.pg0.Button_UpDate = RoundedButton(
            master=self.pg0, text="UPDATE", radius=10, btnbackground="LightSkyBlue4",
            btnforeground="white", width=150, height=60, highlightthickness=0,
            font=("Helvetica", 18, "bold"), masterBackground='white'
        )
        self.pg0.Button_UpDate.grid(
            column=2, row=14, padx=5, pady=5, sticky=tk.W
        )
        self.pg0.Button_UpDate.bind(
            '<Button-1>', lambda e: self.buttonUpDate()
        )
        # ------------------------- Separator ------------------------------------------
        ttk.Separator(
            self.pg0, orient=VERTICAL
        ).grid(
            row=1, column=3, rowspan=13, ipady=150, sticky=tk.N + tk.S + tk.W
        )
        # ------------------------- Researchers ------------------------------------------
        self.pg0.Label_Researchers = ttk.Label(
            self.pg0, text='Researchers in which you participate:', **labelConfigure
        )
        self.pg0.Label_Researchers.grid(
            column=5, row=2, columnspan=3, sticky=tk.N + tk.W + tk.E, pady=5, padx=5
        )
        self.pg0.Table_Researchers = ttk.Treeview(
            self.pg0, style='Custom.Treeview'
        )
        self.pg0.Table_Researchers['columns'] = list(
            researchers.columns
        )
        self.pg0.Table_Researchers.column(
            "#0", width=50, stretch=tk.NO
        )
        for col in list(researchers.columns):
            w = 100
            if col == 'Mail':
                w = 200
            self.pg0.Table_Researchers.column(
                col, anchor=tk.CENTER, width=w, stretch=True
            )
            self.pg0.Table_Researchers.heading(
                col, text=col, anchor=tk.CENTER
            )
        tempGroup = researchers.groupby(
            ['ResearchID'], as_index=False
        )
        row = 0
        for rID, group in tempGroup:
            parentVals = list(
                group.loc[group.index[0], list(self.pg0.Table_Researchers['columns'])[1:-1]]
            )
            if row % 2:
                self.pg0.Table_Researchers.insert(
                    parent='', index='end', iid=str(rID), text='',
                    values=[str(rID), f'{parentVals[0]}', f'{parentVals[1]}', ''],
                    tags=('even',), open=False
                )
            else:
                self.pg0.Table_Researchers.insert(
                    parent='', index='end', iid=str(rID), text='',
                    values=[str(rID), f'{parentVals[0]}', f'{parentVals[1]}', ''],
                    tags=('odd',), open=False
                )
            row += 1
            for idx in group.index:
                vals = list(group.loc[idx, list(self.pg0.Table_Researchers['columns'])])
                if row % 2:
                    self.pg0.Table_Researchers.insert(
                        parent=str(rID), index='end', iid=int(row), text='', values=vals, tags=('even',)
                    )
                else:
                    self.pg0.Table_Researchers.insert(
                        parent=str(rID), index='end', iid=int(row), text='', values=vals, tags=('odd',)
                    )
                row += 1
        self.pg0.Table_Researchers.tag_configure(
            'odd', background='snow2'
        )
        self.pg0.Table_Researchers.tag_configure(
            'even', background='white'
        )
        self.pg0.Table_Researchers.grid(
            column=5, row=3, columnspan=5, rowspan=9, sticky=tk.N + tk.W + tk.E, pady=5
        )
        return

    def _initResearcherMainPg1(self, MasterPanel, *args, **kwargs):
        self.pg1 = ttk.Frame(
            master=MasterPanel, *args, **kwargs
        )
        self.pg1.columnconfigure(
            list(range(1, 10)), weight=1
        )
        self.pg1.rowconfigure(
            list(range(1, 14)), weight=1
        )
        diseasesTable = self.app_queries.dequeueUserIndices('ResearcherMainPg1')
        gridConfigure = {
            'padx': 20, 'pady': 0, 'sticky': tk.W
        }
        gridTEntryConfigure = {
            'padx': 5, 'pady': 0, 'sticky': tk.W, 'ipady': 0, 'ipadx': 0
        }
        entryConfigure = {
            'font': ("Helvetica", 18), 'background': 'white'
        }
        labelConfigure = {
            'font': ("Helvetica", 18, "bold"), 'background': 'white', 'borderwidth': 0, 'foreground': 'LightSkyBlue4'
        }
        s = ttk.Style()
        s.configure(
            'Custom.Treeview', rowheight=30, highlightthickness=2, bd=0, font=('Helvetica', 18)
        )
        s.configure(
            'Custom.TMenubutton', background='white', font=('Helvetica', 18, "bold"),
            bordercolor='LightSkyBlue4', borderwidth=1, foreground='LightSkyBlue4'
        )
        s.configure(
            'Custom.TSpinbox', background='white', foreground='black', font=('Helvetica', 18)
        )
        s.configure(
            'Custom.TCombobox', background='white', foreground='black', font=('Helvetica', 18)
        )
        s.map(
            "Custom.Treeview", background=[("selected", "ivory4")]
        )
        self.option_add(
            "*TCombobox*Entry*font", ('Helvetica', 18)
        )
        self.option_add(
            "*TSpinbox*Listbox*font", ('Helvetica', 18)
        )
        # ------------------------- Gender ------------------------------------------
        self.pg1.Entry_Research_gender = ttk.Menubutton(
            self.pg1, text="Gender", style='Custom.TMenubutton'
        )
        drop = tk.Menu(
            self.pg1.Entry_Research_gender, tearoff=False, activebackground='LightSkyBlue4',
            activeforeground='white', borderwidth=0
        )
        self.pg1.Entry_Research_gender.optionList = []
        for i, val in enumerate(['Female', 'Male']):
            currVar = tk.IntVar()
            self.pg1.Entry_Research_gender.optionList.append(
                (currVar, val)
            )
            drop.add_checkbutton(
                label=val, variable=currVar, onvalue=1, offvalue=0, font=('Helvetica', 18, "bold")
            )
            currVar.set(1)
        self.pg1.Entry_Research_gender["menu"] = drop
        self.pg1.Entry_Research_gender.grid(
            column=1, row=1, **gridTEntryConfigure
        )
        # ------------------------- Support ------------------------------------------
        self.pg1.Entry_Research_support = ttk.Menubutton(
            self.pg1, text="Support", style='Custom.TMenubutton'
        )
        drop = tk.Menu(
            self.pg1.Entry_Research_support, tearoff=False, activebackground='LightSkyBlue4',
            activeforeground='white', borderwidth=0
        )
        self.pg1.Entry_Research_support.optionList = []
        for i, val in enumerate(['Yes', 'No']):
            currVar = tk.IntVar()
            self.pg1.Entry_Research_support.optionList.append(
                (currVar, val)
            )
            drop.add_checkbutton(
                label=val, variable=currVar, onvalue=1, offvalue=0, font=('Helvetica', 18, "bold")
            )
            currVar.set(1)
        self.pg1.Entry_Research_support["menu"] = drop
        self.pg1.Entry_Research_support.grid(
            column=1, row=3, **gridTEntryConfigure
        )
        # ------------------------- HMO ------------------------------------------

        self.pg1.Entry_Research_HMO = ttk.Menubutton(
            self.pg1, text="HMO", style='Custom.TMenubutton'
        )
        drop = tk.Menu(
            self.pg1.Entry_Research_HMO, tearoff=False, activebackground='LightSkyBlue4',
            activeforeground='white', borderwidth=0
        )
        self.pg1.Entry_Research_HMO.optionList = []
        for i, val in enumerate(['Clalit', 'Maccabi', 'Meuhedet', 'Leumit']):
            currVar = tk.IntVar()
            self.pg1.Entry_Research_HMO.optionList.append(
                (currVar, val)
            )
            drop.add_checkbutton(
                label=val, variable=currVar, onvalue=1, offvalue=0, font=('Helvetica', 18, "bold")
            )
            currVar.set(1)
        self.pg1.Entry_Research_HMO["menu"] = drop
        self.pg1.Entry_Research_HMO.grid(
            column=2, row=1, **gridTEntryConfigure
        )
        # ------------------------- Area ------------------------------------------
        self.pg1.Entry_Research_area = ttk.Menubutton(
            self.pg1, text="Area", style='Custom.TMenubutton'
        )
        drop = tk.Menu(
            self.pg1.Entry_Research_area, tearoff=False, activebackground='LightSkyBlue4',
            activeforeground='white', borderwidth=0
        )
        self.pg1.Entry_Research_area.optionList = []
        for i, val in enumerate(['North', 'Center', 'South']):
            currVar = tk.IntVar()
            self.pg1.Entry_Research_area.optionList.append(
                (currVar, val)
            )
            drop.add_checkbutton(
                label=val, variable=currVar, onvalue=1, offvalue=0, font=('Helvetica', 18, "bold")
            )
            currVar.set(1)
        self.pg1.Entry_Research_area["menu"] = drop
        self.pg1.Entry_Research_area.grid(
            column=2, row=3, **gridTEntryConfigure
        )
        # ------------------------- Age ------------------------------------------
        self.pg1.Label_Research_age = ttk.Label(
            self.pg1, text='Age between:', **labelConfigure
        )
        self.pg1.Label_Research_age.grid(
            column=5, row=1, columnspan=2, **gridConfigure
        )
        self.pg1.Entry_Research_age = []
        start = ttk.Spinbox(
            self.pg1, from_=18, to=100, style='Custom.TSpinbox'
        )
        start.grid(
            column=5, row=3, **gridConfigure
        )
        stop = ttk.Spinbox(
            self.pg1, from_=18, to=100, style='Custom.TSpinbox'
        )
        stop.grid(
            column=6, row=3, **gridConfigure
        )
        self.pg1.Entry_Research_age = [
            start, stop
        ]
        # ------------------------- Height ------------------------------------------
        self.pg1.Label_Research_height = ttk.Label(
            self.pg1, text='Height between:', **labelConfigure
        )
        self.pg1.Label_Research_height.grid(
            column=7, row=1, columnspan=2, **gridConfigure
        )
        self.pg1.Entry_Research_height = []
        start = ttk.Spinbox(
            self.pg1, from_=80, to=250, style='Custom.TSpinbox'
        )
        start.grid(
            column=7, row=3, **gridConfigure
        )
        stop = ttk.Spinbox(
            self.pg1, from_=80, to=250, style='Custom.TSpinbox'
        )
        stop.grid(
            column=8, row=3, **gridConfigure
        )
        self.pg1.Entry_Research_height = [
            start, stop
        ]
        # ------------------------- Weight ------------------------------------------
        self.pg1.Label_Research_weight = ttk.Label(
            self.pg1, text='Weight between:', **labelConfigure
        )
        self.pg1.Label_Research_weight.grid(
            column=9, row=1, columnspan=2, **gridConfigure
        )
        self.pg1.Entry_Research_weight = []
        start = ttk.Spinbox(
            self.pg1, from_=30, to=200, style='Custom.TSpinbox'
        )
        start.grid(
            column=9, row=3, **gridConfigure
        )
        stop = ttk.Spinbox(
            self.pg1, from_=30, to=200, style='Custom.TSpinbox'
        )
        stop.grid(
            column=10, row=3, **gridConfigure
        )
        self.pg1.Entry_Research_weight = [
            start, stop
        ]
        # ------------------------- Separator ------------------------------------------
        ttk.Separator(
            self.pg1, orient=HORIZONTAL
        ).grid(
            row=5, column=0, columnspan=11, ipadx=150, sticky=tk.W + tk.E + tk.S
        )
        # ------------------------- Disease Department ------------------------------------------
        self.pg1.Label_Research_depName = ttk.Label(
            self.pg1, text='Department:', **labelConfigure
        )
        self.pg1.Label_Research_depName.grid(
            column=1, row=6, columnspan=3, **gridConfigure
        )
        self.pg1.textVariable_Research_depName = tk.StringVar()
        self.pg1.Entry_Research_depName = ttk.Combobox(
            self.pg1, textvariable=self.pg1.textVariable_Research_depName, style='Custom.TCombobox', **entryConfigure
        )
        if diseasesTable is not None:
            self.pg1.Entry_Research_depName['values'] = tuple(
                diseasesTable['depName'].unique()
            )
        self.pg1.Entry_Research_depName.grid(
            column=1, row=7, columnspan=3, **gridTEntryConfigure
        )
        # ------------------------- Disease Name ------------------------------------------
        self.pg1.Label_Research_disName = ttk.Label(
            self.pg1, text='Name:', **labelConfigure
        )
        self.pg1.Label_Research_disName.grid(
            column=4, row=6, columnspan=3, **gridConfigure
        )
        self.pg1.textVariable_Research_disName = tk.StringVar()
        self.pg1.Entry_Research_disName = ttk.Combobox(
            self.pg1, textvariable=self.pg1.textVariable_Research_disName, style='Custom.TCombobox', **entryConfigure
        )
        if diseasesTable is not None:
            self.pg1.Entry_Research_disName['values'] = tuple(
                diseasesTable['disName'].unique()
            )
        self.pg1.Entry_Research_disName.grid(
            column=4, row=7, columnspan=3, **gridTEntryConfigure
        )

        def buttonDisUpdate():
            if diseasesTable is None:
                return
            txt = self.pg1.Entry_Research_depName.get()
            if not txt:
                self.pg1.Entry_Research_disName['values'] = tuple(diseasesTable['disName'].unique())
                return
            self.pg1.Entry_Research_disName['values'] = tuple(
                diseasesTable.loc[diseasesTable['depName'] == txt, 'disName'].unique()
            )

        def buttonDepUpdate():
            if diseasesTable is None:
                return
            txt = self.pg1.Entry_Research_disName.get()
            if not txt:
                self.pg1.Entry_Research_depName['values'] = tuple(diseasesTable['depName'].unique())
                return
            self.pg1.Entry_Research_depName['values'] = tuple(
                diseasesTable.loc[diseasesTable['disName'] == txt, 'depName'].unique()
            )

        self.pg1.Entry_Research_depName.bind(
            "<FocusOut>", lambda e: buttonDisUpdate()
        )
        self.pg1.Entry_Research_disName.bind(
            "<FocusOut>", lambda e: buttonDepUpdate()
        )
        # ------------------------- Symptoms ------------------------------------------
        self.pg1.Label_ResearchSymptoms = ttk.Label(
            self.pg1, text='Symptoms:', **labelConfigure
        )
        self.pg1.Label_ResearchSymptoms.grid(
            column=1, row=9, columnspan=5, sticky=tk.W + tk.N, pady=10, padx=10
        )
        self.pg1.Entry_ResearchSymptoms = ttk.Entry(
            self.pg1, textvariable=tk.StringVar(), width=40, **entryConfigure
        )
        self.pg1.Entry_ResearchSymptoms.grid(
            column=1, row=10, columnspan=6, rowspan=2, sticky=tk.W + tk.N + tk.E
        )
        self.pg1.Listbox_ResearchSymptoms = tk.Listbox(
            self.pg1, selectmode=tk.EXTENDED, font=("Helvetica", 18), bg='white',
            highlightcolor='LightSkyBlue4', highlightthickness=1, relief='flat', width=40
        )
        self.pg1.Listbox_ResearchSymptoms.grid(
            column=1, row=11, columnspan=6, rowspan=3, sticky=tk.W + tk.E, padx=10
        )
        self.pg1.Button_select = RoundedButton(
            master=self.pg1, text="Select", radius=10, btnbackground="LightSkyBlue4",
            btnforeground="white", width=80, height=60, highlightthickness=0, font=("Helvetica", 18, "bold"),
            masterBackground='white'
        )
        self.pg1.Button_select.grid(
            column=2, row=14, columnspan=2, sticky=tk.W + tk.E
        )
        # ------------------------- Selected Symptoms ------------------------------------------
        self.pg1.Label_ResearchSelectSymptoms = ttk.Label(
            self.pg1, text='Selected Symptoms:', **labelConfigure
        )
        self.pg1.Label_ResearchSelectSymptoms.grid(
            column=8, row=9, columnspan=3, sticky=tk.W + tk.N, padx=10, pady=10
        )
        self.pg1.Entry_Research_symptoms = ttk.Treeview(
            self.pg1, style='Custom.Treeview'
        )
        self.pg1.Entry_Research_symptoms['columns'] = ['Symptoms']
        self.pg1.Entry_Research_symptoms.column(
            "#0", width=0, stretch=tk.NO
        )
        self.pg1.Entry_Research_symptoms.column(
            'Symptoms', anchor=tk.W, width=400
        )

        self.pg1.Entry_Research_symptoms.tag_configure(
            'odd', background='snow2'
        )
        self.pg1.Entry_Research_symptoms.tag_configure(
            'even', background='white'
        )

        self.pg1.Entry_Research_symptoms.grid(
            column=8, row=10, columnspan=3, rowspan=4, sticky=tk.W + tk.E, padx=10
        )
        self.pg1.Button_deleteSelect = RoundedButton(
            master=self.pg1, text="Delete Selected", radius=10, btnbackground="LightSkyBlue4",
            btnforeground="white", width=80, height=60, highlightthickness=0,
            font=("Helvetica", 18, "bold"), masterBackground='white'
        )
        self.pg1.Button_deleteSelect.grid(
            column=8, row=14, sticky=tk.W + tk.E
        )
        temp = self.master.__dict__.get('symptomsTrie')
        if temp:
            self.AutoComplete = AUTO_complete(
                temp, self.pg1.Entry_ResearchSymptoms, self.pg1.Listbox_ResearchSymptoms,
                treeview=self.pg1.Entry_Research_symptoms, select=self.pg1.Button_select,
                deleteSelect=self.pg1.Button_deleteSelect
            )

        # ------------------------- Create New Research ------------------------------------------
        self.pg1.Button_createResearch = RoundedButton(
            master=self.pg1, text="Create Research", radius=10, btnbackground="LightSkyBlue4",
            btnforeground="white", width=80, height=60, highlightthickness=0, font=("Helvetica", 18, "bold"),
            masterBackground='white'
        )
        self.pg1.Button_createResearch.grid(
            column=10, row=14, sticky=tk.W + tk.E
        )
        self.pg1.Button_createResearch.bind(
            "<Button-1>", lambda e: self.app_inputs.pushNewResearch()
        )
        return

    def _initResearcherMainPg2(self, MasterPanel, *args, **kwargs):
        availablePatients = self.app_queries.dequeueUserIndices('ResearcherMainPg2')
        self.pg2 = ttk.Frame(
            master=MasterPanel, *args, **kwargs
        )
        self.pg2.columnconfigure(
            list(range(1, 5)), weight=1
        )
        self.pg2.rowconfigure(
            list(range(1, 7)), weight=1
        )
        self.pg2.availablePatients = availablePatients
        labelConfigure = {
            'font': ("Helvetica", 18, "bold"), 'background': 'white', 'borderwidth': 0, 'foreground': 'LightSkyBlue4'
        }
        s = ttk.Style()
        s.configure(
            'Custom.Treeview', rowheight=30, highlightthickness=2, bd=0, font=('Helvetica', 18)
        )
        s.configure(
            'Custom.Treeview.Heading', background='seashell3', foreground='black', font=('Helvetica', 18, 'bold')
        )
        s.map(
            "Custom.Treeview", background=[("selected", "ivory4")]
        )
        # ------------------------- Researchers ------------------------------------------
        self.pg2.Label_Researchers = ttk.Label(
            self.pg2, text='Available Patients:', **labelConfigure
        )
        self.pg2.Label_Researchers.grid(
            column=1, row=1, columnspan=3, sticky=tk.W, pady=5, padx=5
        )
        self.pg2.Table_AvailablePatients = ttk.Treeview(
            self.pg2, style='Custom.Treeview'
        )
        self.pg2.Table_AvailablePatients['columns'] = [availablePatients.columns[-1]] + list(
            availablePatients.columns[:-1]
        )
        self.pg2.Table_AvailablePatients.column(
            "#0", width=50, stretch=tk.NO
        )
        for col in list(self.pg2.Table_AvailablePatients['columns']):
            w = 100
            if col == 'Mail':
                w = 200
            self.pg2.Table_AvailablePatients.column(
                col, anchor=tk.CENTER, width=w
            )
            self.pg2.Table_AvailablePatients.heading(
                col, text=col, anchor=tk.CENTER
            )
        tempGroup = availablePatients.groupby(
            ['researchID'], as_index=False
        )
        row = 0
        for rID, group in tempGroup:
            if row % 2:
                self.pg2.Table_AvailablePatients.insert(
                    parent='', index='end', iid=str(rID), text='',
                    values=[str(rID), '', '', ''], tags=('even',), open=False
                )
            else:
                self.pg2.Table_AvailablePatients.insert(
                    parent='', index='end', iid=str(rID), text='',
                    values=[str(rID), '', '', ''], tags=('odd',), open=False
                )
            row += 1
            for idx in group.index:
                vals = list(
                    group.loc[idx, list(self.pg2.Table_AvailablePatients['columns'])]
                )
                if row % 2:
                    self.pg2.Table_AvailablePatients.insert(
                        parent=str(rID), index='end', iid=int(row), text='', values=vals, tags=('even',)
                    )
                else:
                    self.pg2.Table_AvailablePatients.insert(
                        parent=str(rID), index='end', iid=int(row), text='', values=vals, tags=('odd',)
                    )
                row += 1
        self.pg2.Table_AvailablePatients.tag_configure(
            'odd', background='snow2'
        )
        self.pg2.Table_AvailablePatients.tag_configure(
            'even', background='white'
        )
        self.pg2.Table_AvailablePatients.grid(
            column=1, row=2, columnspan=4, rowspan=3, sticky=tk.W + tk.E, padx=5
        )
        self.pg2.Button_addPatient = RoundedButton(
            master=self.pg2, text="Add patient to research", radius=10,
            btnbackground="LightSkyBlue4", btnforeground="white", width=80, height=60, highlightthickness=0,
            font=("Helvetica", 18, "bold"), masterBackground='white'
        )
        self.pg2.Button_addPatient.grid(
            column=4, row=5, sticky=tk.W + tk.E
        )
        self.pg2.Button_addPatient.bind(
            '<Button-1>', lambda e: self.app_inputs.addPatientToResearch()
        )
        return

    def _initResearcherMainPg3(self, MasterPanel, *args, **kwargs):
        UserIndices = self.app_queries.dequeueUserIndices('ResearcherMainPg3')
        self.pg3 = ttk.Frame(
            master=MasterPanel, *args, **kwargs
        )
        self.pg3.columnconfigure(
            list(range(1, 10)), weight=1
        )
        self.pg3.rowconfigure(
            list(range(1, 14)), weight=1
        )
        self.pg3.UserIndices = UserIndices
        gridConfigure = {
            'padx': 5, 'pady': 5, 'sticky': tk.W
        }
        gridTEntryConfigure = {
            'padx': 5, 'pady': 0, 'sticky': tk.W, 'ipady': 0, 'ipadx': 0
        }
        entryConfigure = {
            'font': ("Helvetica", 18), 'background': 'white'
        }
        labelConfigure = {
            'font': ("Helvetica", 18, "bold"), 'background': 'white', 'borderwidth': 0, 'foreground': 'LightSkyBlue4'
        }
        s = ttk.Style()
        s.configure(
            'Custom.Treeview', rowheight=30, highlightthickness=2, bd=0, font=('Helvetica', 18)
        )
        s.configure(
            'Custom.Treeview.Heading', background='seashell3', foreground='black', font=('Helvetica', 18, 'bold')
        )
        s.map(
            "Custom.Treeview", background=[("selected", "ivory4")]
        )
        # ------------------------- Department ------------------------------------------
        self.pg3.Label_DiseaseDepName = ttk.Label(
            self.pg3, text='Department: *', **labelConfigure
        )
        self.pg3.Label_DiseaseDepName.grid(
            column=2, row=2, **gridConfigure
        )
        self.pg3.textVariable_DiseaseDepName = tk.StringVar()
        self.pg3.Entry_DiseaseDepName = ttk.Combobox(
            self.pg3, textvariable=self.pg3.textVariable_DiseaseDepName, **entryConfigure
        )
        self.pg3.Entry_DiseaseDepName['values'] = (
            'Oncology', 'Neurological', 'Vascular'
        )
        self.pg3.Entry_DiseaseDepName.grid(
            column=2, row=3, **gridTEntryConfigure
        )
        # ------------------------- Disease Name ------------------------------------------
        self.pg3.Label_DiseaseDisName = ttk.Label(
            self.pg3, text='Disease Name: *', **labelConfigure
        )
        self.pg3.Label_DiseaseDisName.grid(
            column=3, row=2, **gridConfigure
        )
        self.pg3.Entry_DiseaseDisName = ttk.Entry(
            self.pg3, **entryConfigure
        )
        self.pg3.Entry_DiseaseDisName.grid(
            column=3, row=3, **gridTEntryConfigure
        )
        # ------------------------- Enter Symptoms ------------------------------------------
        self.pg3.Label_DiseaseSymptoms = ttk.Label(
            self.pg3, text='Symptoms:', **labelConfigure
        )
        self.pg3.Label_DiseaseSymptoms.grid(
            column=2, row=6, columnspan=2, sticky=tk.W + tk.N, pady=10, padx=10
        )
        self.pg3.Entry_DiseaseSymptoms = ttk.Entry(
            self.pg3, textvariable=tk.StringVar(), width=40, **entryConfigure
        )
        self.pg3.Entry_DiseaseSymptoms.grid(
            column=2, row=7, columnspan=2, rowspan=2, sticky=tk.W + tk.N + tk.E
        )
        self.pg3.Listbox_DiseaseSymptoms = tk.Listbox(
            self.pg3, selectmode=tk.EXTENDED, font=("Helvetica", 18), bg='white',
            highlightcolor='LightSkyBlue4', highlightthickness=1, relief='flat', width=40
        )
        self.pg3.Listbox_DiseaseSymptoms.grid(
            column=2, row=8, columnspan=2, rowspan=3, sticky=tk.W + tk.E, padx=10
        )
        self.pg3.Button_select = RoundedButton(
            master=self.pg3, text="Select", radius=10, btnbackground="LightSkyBlue4",
            btnforeground="white", width=80, height=60, highlightthickness=0,
            font=("Helvetica", 18, "bold"), masterBackground='white'
        )
        self.pg3.Button_select.grid(
            column=2, row=11, sticky=tk.E + tk.S + tk.W
        )
        # ------------------------- Selected Symptoms ------------------------------------------
        self.pg3.Label_DiseaseSelectSymptoms = ttk.Label(
            self.pg3, text='Selected Symptoms:', **labelConfigure
        )
        self.pg3.Label_DiseaseSelectSymptoms.grid(
            column=5, row=6, columnspan=3, sticky=tk.W + tk.N, padx=10, pady=10
        )
        self.pg3.Table_DiseaseSelectSymptoms = ttk.Treeview(
            self.pg3, style='Custom.Treeview'
        )
        self.pg3.Table_DiseaseSelectSymptoms['columns'] = ['Symptoms']
        self.pg3.Table_DiseaseSelectSymptoms.column(
            "#0", width=0, stretch=tk.NO
        )
        self.pg3.Table_DiseaseSelectSymptoms.column(
            'Symptoms', anchor=tk.W, width=400
        )
        self.pg3.Table_DiseaseSelectSymptoms.tag_configure(
            'odd', background='snow2'
        )
        self.pg3.Table_DiseaseSelectSymptoms.tag_configure(
            'even', background='white'
        )
        self.pg3.Table_DiseaseSelectSymptoms.grid(
            column=5, row=7, columnspan=3, rowspan=4, sticky=tk.W + tk.E, padx=10
        )
        self.pg3.Button_deleteSelect = RoundedButton(
            master=self.pg3, text="Delete Selected", radius=10,
            btnbackground="LightSkyBlue4", btnforeground="white", width=80, height=60, highlightthickness=0,
            font=("Helvetica", 18, "bold"), masterBackground='white'
        )
        temp = self.master.__dict__.get('symptomsTrie')
        if temp:
            self.AutoComplete = AUTO_complete(
                temp, self.pg3.Entry_DiseaseSymptoms, self.pg3.Listbox_DiseaseSymptoms,
                treeview=self.pg3.Table_DiseaseSelectSymptoms,
                select=self.pg3.Button_select, deleteSelect=self.pg3.Button_deleteSelect
            )
        self.pg3.Button_deleteSelect.grid(
            column=5, row=11, sticky=tk.E + tk.S + tk.W
        )
        self.pg3.Label_DiseaseNewSymptom = ttk.Label(
            self.pg3, text='New symptom:', **labelConfigure
        )
        self.pg3.Label_DiseaseNewSymptom.grid(
            column=5, row=2, **gridConfigure
        )
        self.pg3.Entry_DiseaseNewSymptom = ttk.Entry(
            self.pg3, **entryConfigure
        )
        self.pg3.Entry_DiseaseNewSymptom.grid(
            column=5, row=3, columnspan=3, sticky=tk.W + tk.E
        )
        self.pg3.Button_addSymptom = RoundedButton(
            master=self.pg3, text="Add", radius=10,
            btnbackground="LightSkyBlue4",
            btnforeground="white", width=40, height=50, highlightthickness=0,
            font=("Helvetica", 18, "bold"), masterBackground='white'
        )
        self.pg3.Button_addSymptom.grid(
            column=6, row=2, sticky=tk.W + tk.E
        )

        def addSymptom():
            txt = self.pg3.Entry_DiseaseNewSymptom.get()
            self.AutoComplete.updateSelectSymptoms(txt)

        self.pg3.Button_addSymptom.bind(
            "<Button-1>", lambda e: addSymptom()
        )
        self.pg3.Button_AddDisease = RoundedButton(
            master=self.pg3, text="Add New Disease", radius=10,
            btnbackground="LightSkyBlue4",
            btnforeground="white", width=80, height=60, highlightthickness=0,
            font=("Helvetica", 18, "bold"), masterBackground='white'
        )
        self.pg3.Button_AddDisease.grid(
            column=7, row=11, sticky=tk.E + tk.S + tk.W
        )
        self.pg3.Button_AddDisease.bind(
            "<Button-1>", lambda e: self.app_inputs.pushNewDiseases()
        )
        return

    def _initResearcherMainPg4(self, MasterPanel, *args, **kwargs):
        self.pg4 = ttk.Frame(
            master=MasterPanel, *args, **kwargs
        )
        self.pg4.columnconfigure(
            list(range(1, 10)), weight=1
        )
        self.pg4.rowconfigure(
            list(range(1, 14)), weight=1
        )
        gridConfigure = {
            'padx': 5, 'pady': 5, 'sticky': tk.W
        }
        gridTEntryConfigure = {
            'padx': 5, 'pady': 0, 'sticky': tk.W, 'ipady': 0, 'ipadx': 0
        }
        entryConfigure = {
            'font': ("Helvetica", 18), 'background': 'white'
        }
        labelConfigure = {
            'font': ("Helvetica", 18, "bold"), 'background': 'white', 'borderwidth': 0, 'foreground': 'LightSkyBlue4'
        }
        s = ttk.Style()
        s.configure(
            'Custom.Treeview', rowheight=30, highlightthickness=2, bd=0, font=('Helvetica', 18)
        )
        s.configure(
            'Custom.Treeview.Heading', background='seashell3', foreground='black', font=('Helvetica', 18, 'bold')
        )
        s.map(
            "Custom.Treeview", background=[("selected", "ivory4")]
        )
        # ------------------------- Disease Name ------------------------------------------
        self.pg4.Label_DiseaseDisName = ttk.Label(
            self.pg4, text='Disease Name: *', **labelConfigure
        )
        self.pg4.Label_DiseaseDisName.grid(
            column=2, row=2, **gridConfigure
        )
        self.pg4.Entry_DiseaseDisName = ttk.Entry(
            self.pg4, **entryConfigure
        )
        self.pg4.Entry_DiseaseDisName.grid(
            column=2, row=3, **gridTEntryConfigure
        )
        self.pg4.Button_ShowSymptoms = RoundedButton(
            master=self.pg4, text="Show Existing Symptoms", radius=10,
            btnbackground="LightSkyBlue4", btnforeground="white", width=80, height=60, highlightthickness=0,
            font=("Helvetica", 18, "bold"), masterBackground='white'
        )
        self.pg4.Button_ShowSymptoms.grid(
            column=3, row=3, sticky=tk.W
        )
        # -------------------------Existing Symptoms ------------------------------------------
        self.pg4.Label_DiseaseExistingSymptoms = ttk.Label(
            self.pg4, text='Existing Symptoms:', **labelConfigure
        )
        self.pg4.Label_DiseaseExistingSymptoms.grid(
            column=2, row=6, columnspan=3, sticky=tk.W, padx=10, pady=10
        )
        self.pg4.Table_DiseaseExistingSymptoms = ttk.Treeview(
            self.pg4, style='Custom.Treeview'
        )
        self.pg4.Table_DiseaseExistingSymptoms['columns'] = ['Symptoms']
        self.pg4.Table_DiseaseExistingSymptoms.column(
            "#0", width=0, stretch=tk.NO
        )
        self.pg4.Table_DiseaseExistingSymptoms.tag_configure(
            'odd', background='snow2'
        )
        self.pg4.Table_DiseaseExistingSymptoms.tag_configure(
            'even', background='white'
        )
        self.pg4.Table_DiseaseExistingSymptoms.grid(
            column=2, row=7, columnspan=2, rowspan=9, sticky=tk.W + tk.E, pady=5
        )
        self.pg4.Button_ShowSymptoms.bind(
            "<Button-1>",
            lambda e: self.buttonShowSymptoms(
                self.pg4.Entry_DiseaseDisName, self.pg4.Table_DiseaseExistingSymptoms
            )
        )
        # -------------------------New Symptom Name ------------------------------------------
        self.pg4.Label_DiseaseSymptom = ttk.Label(
            self.pg4, text='New Symptom Name: *', **labelConfigure
        )
        self.pg4.Label_DiseaseSymptom.grid(
            column=5, row=2, **gridConfigure
        )
        self.pg4.Entry_DiseaseSymptom = ttk.Entry(
            self.pg4, **entryConfigure
        )
        self.pg4.Entry_DiseaseSymptom.grid(
            column=5, row=3, **gridTEntryConfigure
        )
        self.pg4.Button_AddSymptom = RoundedButton(
            master=self.pg4, text="Add New Symptom", radius=10,
            btnbackground="LightSkyBlue4", btnforeground="white", width=80, height=60, highlightthickness=0,
            font=("Helvetica", 18, "bold"), masterBackground='white'
        )
        self.pg4.Button_AddSymptom.grid(
            column=6, row=3, sticky=tk.W
        )
        self.pg4.Button_AddSymptom.bind(
            "<Button-1>", lambda e: self.app_inputs.pushNewSymptoms()
        )
        return

    def buttonShowSymptoms(self, entry, treeView):
        disName = entry.get()
        symptoms = self.app_queries.querySymptomsDiseases(disName)
        for i, row in enumerate(symptoms):
            if i % 2:
                treeView.insert(
                    parent='', index='end', iid=int(i), text='', values=[row[0]], tags=('even',)
                )
            else:
                treeView.insert(
                    parent='', index='end', iid=int(i), text='', values=[row[0]], tags=('odd',)
                )
        return
