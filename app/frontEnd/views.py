import tkinter as tk
from tkinter import ttk, HORIZONTAL, VERTICAL
from app.frontEnd.RoundButton import RoundedButton
from app.frontEnd.autoComplete import AUTO_complete
from tkcalendar import DateEntry
import datetime


class UserLogInPanel(ttk.Frame):

    def __init__(self, MasterPanel):
        ttk.Frame.__init__(self, master=MasterPanel, relief=tk.RAISED, borderwidth=2)
        self.width = 0.5 * MasterPanel.width
        self.height = 0.5 * MasterPanel.height
        self.columnconfigure(list(range(1, 8)), weight=1)
        self.rowconfigure(list(range(1, 8)), weight=1)
        self._create_sub_frames(MasterPanel)

    def _create_sub_frames(self, MasterPanel):
        self.style = ttk.Style(self)
        self.style.configure('Frame1.TFrame', background='LightSkyBlue4', borderwidth=10, relief='RAISED')
        self.logIn_frame = LogInFrame(self, style='Frame1.TFrame')
        self.logIn_frame.grid(column=4, row=2, rowspan=4, padx=50, pady=50, sticky="nsew")
        return


class LogInFrame(ttk.Frame):
    def __init__(self, MasterPanel, *args, **kwargs):
        ttk.Frame.__init__(self, master=MasterPanel, *args, **kwargs)
        self.columnconfigure(list(range(1, 6)), weight=1)
        self.rowconfigure(list(range(1, 9)), weight=1)
        self._create_widgets(MasterPanel)

    def _create_widgets(self, MasterPanel):

        self.style = ttk.Style(self)
        self.style.configure('TRadiobutton', font=("Helvetica", 18, "bold"), background="LightSkyBlue4",
                             foreground='black', weight=40)
        self.style.configure('TEntry', weight=100)
        labelConfigure = {'font': ("Helvetica", 18, "bold"), 'background': 'LightSkyBlue4'}
        entryConfigure = {'font': ("Helvetica", 16, "bold"), 'background': 'white'}
        gridTEntryConfigure = {'padx': 10, 'pady': 0, 'sticky': tk.W, 'ipady': 0, 'ipadx': 0}
        gridConfigure = {'padx': 5, 'pady': 0, 'sticky': tk.W}

        Label_title = ttk.Label(self, text='Log In', font=("Helvetica", 60, "bold", 'underline'),
                                background="LightSkyBlue4", foreground='white')
        Label_title.grid(column=2, row=1, sticky="nsew")

        ttk.Separator(self, orient=HORIZONTAL).grid(row=2, column=0, columnspan=6, ipadx=150, sticky=tk.W + tk.E)

        # User Path researcher or patient
        self.Label_UserPath = ttk.Label(self, text='User', **labelConfigure)
        self.Label_UserPath.grid(column=1, row=3, **gridConfigure)
        self.Entry_UserPath = tk.IntVar()
        self.Entry_UserPath.set(1)
        self.RB_UserPath_Patient = ttk.Radiobutton(self, text='Patient', variable=self.Entry_UserPath,
                                                   value=1)
        self.RB_UserPath_Patient.grid(column=2, row=3, **gridConfigure)

        self.RB_UserPath_Researcher = ttk.Radiobutton(self, text='Researcher',
                                                      variable=self.Entry_UserPath, value=0)
        self.RB_UserPath_Researcher.grid(column=2, row=4, **gridConfigure)

        # User, researcher or patient Insert ID
        self.Label_UserID = ttk.Label(self, text='User ID:', **labelConfigure)
        self.Label_UserID.grid(column=1, row=5, **gridConfigure)
        self.Entry_UserID = ttk.Entry(self, **entryConfigure)
        self.Entry_UserID.insert(0, "ID")
        self.Entry_UserID.grid(column=2, row=5, **gridTEntryConfigure)
        self.Entry_UserID.bind("<FocusOut>", lambda e: self.EntryFocusOut('ID'))
        self.Entry_UserID.bind("<Button-1>", lambda e: self.EntryButton1('ID'))

        # User researcher or patient Insert Name
        self.Label_UserName = ttk.Label(self, text='User Name:', **labelConfigure)
        self.Label_UserName.grid(column=1, row=6, **gridConfigure)
        self.Entry_UserName = ttk.Entry(self, **entryConfigure)
        self.Entry_UserName.insert(0, "Name")
        self.Entry_UserName.grid(column=2, row=6, **gridTEntryConfigure)
        self.Entry_UserName.bind("<FocusOut>", lambda e: self.EntryFocusOut('Name'))
        self.Entry_UserName.bind("<Button-1>", lambda e: self.EntryButton1('Name'))

        # LOGIN button
        self.Button_LogIn = RoundedButton(master=self, text="Log In", radius=25, btnbackground="DarkGoldenrod3",
                                          btnforeground="black", width=250, height=60, highlightthickness=0,
                                          font=("Helvetica", 18, "bold"), masterBackground='LightSkyBlue4')
        self.Button_LogIn.grid(column=2, row=7, **gridConfigure)
        self.Button_LogIn.bind("<Button-1>", lambda e: MasterPanel.master.app_insert2DB.ExLogIn())

        # SingIN button
        self.Button_SignIN = RoundedButton(master=self, text="Sign IN", radius=25, btnbackground="DarkGoldenrod3",
                                           btnforeground="black", width=250, height=60, highlightthickness=0,
                                           font=("Helvetica", 18, "bold"), masterBackground='LightSkyBlue4')
        self.Button_SignIN.grid(column=2, row=8, **gridConfigure)
        self.Button_SignIN.bind("<Button-1>", lambda e: MasterPanel.master.app_insert2DB.ExSignIN())
        return

    def EntryFocusOut(self, EntryName):
        txt = self.__dict__[f'Entry_User{EntryName}'].get()
        if not txt:
            self.__dict__[f'Entry_User{EntryName}'].insert(0, EntryName)
            return
        return self.HandelFiled(EntryName, txt)

    def EntryButton1(self, EntryName):
        txt = self.__dict__[f'Entry_User{EntryName}'].get()
        if txt == EntryName:
            self.__dict__[f'Entry_User{EntryName}'].delete(0, "end")
        return

    def HandelFiled(self, EntryName, txt, appCall=False):
        if EntryName == 'ID':
            if appCall or (txt and (len(txt) < 9 or len(txt) > 9)):
                self.Label_UserID.config(foreground="red")
                return
            self.Label_UserID.config(foreground="black")
            return
        if EntryName == 'Name':
            if appCall:
                self.Label_UserName.config(foreground="red")
                return
            self.Label_UserName.config(foreground="black")
            return
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
        self.Entry_UserID.bind("<Button-1>", lambda e: self.EntryButton1('ID'))
        self.Entry_UserID.bind("<FocusOut>", lambda e: self.EntryFocusOut('ID'))

        # ------------------------- Name ------------------------------------------
        self.Label_UserName = ttk.Label(self, text='Name: *', **labelConfigure)
        self.Label_UserName.grid(column=1, row=3, **gridConfigure)

        self.Entry_UserName = ttk.Entry(self, **entryConfigure)
        self.Entry_UserName.grid(column=1, row=4, columnspan=2, **gridTEntryConfigure)
        self.Entry_UserName.bind("<Button-1>", lambda e: self.EntryButton1('Name'))
        self.Entry_UserName.bind("<FocusOut>", lambda e: self.EntryFocusOut('Name'))

        # ------------------------- Gender ------------------------------------------
        self.Label_UserGender = ttk.Label(self, text='Gender: *', **labelConfigure)
        self.Label_UserGender.grid(column=1, row=5, **gridConfigure)

        self.textVariable_UserGender = tk.StringVar()
        self.Entry_UserGender = ttk.Combobox(self, textvariable=self.textVariable_UserGender, **entryConfigure)
        self.Entry_UserGender['values'] = ('Female', 'Male')
        self.Entry_UserGender.grid(column=1, row=6, **gridTEntryConfigure)
        self.Entry_UserGender.bind("<FocusOut>", lambda e: self.EntryFocusOut('Gender'))

        # ------------------------- Area ------------------------------------------
        self.Label_UserArea = ttk.Label(self, text='Area: *', **labelConfigure)
        self.Label_UserArea.grid(column=1, row=7, **gridConfigure)

        self.textVariable_UserArea = tk.StringVar()
        self.Entry_UserArea = ttk.Combobox(self, textvariable=self.textVariable_UserArea, **entryConfigure)
        self.Entry_UserArea['values'] = ('North', 'Center', 'South')
        self.Entry_UserArea.grid(column=1, row=8, **gridTEntryConfigure)
        self.Entry_UserArea.bind("<FocusOut>", lambda e: self.EntryFocusOut('Area'))

        # ------------------------- City ------------------------------------------
        self.Label_UserCity = ttk.Label(self, text='City: *', **labelConfigure)
        self.Label_UserCity.grid(column=1, row=9, **gridConfigure)

        self.Entry_UserCity = ttk.Entry(self, **entryConfigure)
        self.Entry_UserCity.grid(column=1, row=10, columnspan=2, **gridTEntryConfigure)
        self.Entry_UserCity.bind("<FocusOut>", lambda e: self.EntryFocusOut('City'))

        # ------------------------- Phone ------------------------------------------
        self.Label_UserPhone = ttk.Label(self, text='Phone: *', **labelConfigure)
        self.Label_UserPhone.grid(column=1, row=11, **gridConfigure)

        self.Entry_UserPhone = ttk.Entry(self, **entryConfigure)
        self.Entry_UserPhone.grid(column=1, row=12, columnspan=2, **gridTEntryConfigure)
        self.Entry_UserPhone.bind("<Button-1>", lambda e: self.EntryButton1('Phone'))
        self.Entry_UserPhone.bind("<FocusOut>", lambda e: self.EntryFocusOut('Phone'))

        # ------------------------- Separator ------------------------------------------
        ttk.Separator(self, orient=VERTICAL).grid(row=1, column=2, rowspan=13, ipady=150, sticky=tk.N + tk.S + tk.E)

        # ------------------------- DOB ------------------------------------------
        self.Label_UserDOB = ttk.Label(self, text='Date of Birth: *', **labelConfigure)
        self.Label_UserDOB.grid(column=3, row=1, **gridConfigure)

        self.Entry_UserDOB = DateEntry(self, selectmode='day', date_pattern='MM-dd-yyyy',
                                       font=("Helvetica", 18, "bold"),
                                       firstweekday='sunday', weekenddays=[6, 7], background='LightSkyBlue4',
                                       foreground='white')
        self.Entry_UserDOB.bind("<<DateEntrySelected>>",
                                lambda e: self.HandelFiled('DOB', self.Entry_UserDOB.get_date()))
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
        self.Entry_UserHeight.bind("<FocusOut>", lambda e: self.EntryFocusOut('Height'))

        # ------------------------- Weight ------------------------------------------
        self.Label_UserWeight = ttk.Label(self, text='Weight: *', **labelConfigure)
        self.Label_UserWeight.grid(column=3, row=9, **gridConfigure)

        self.Entry_UserWeight = ttk.Entry(self, **entryConfigure)
        self.Entry_UserWeight.grid(column=3, row=10, **gridTEntryConfigure)
        self.Entry_UserWeight.bind("<FocusOut>", lambda e: self.EntryFocusOut('Weight'))

        # ------------------------- Support ------------------------------------------
        self.Label_UserSupport = ttk.Label(self, text='Support: *', **labelConfigure)
        self.Label_UserSupport.grid(column=3, row=11, **gridConfigure)

        self.textVariable_UserSupport = tk.StringVar()
        self.Entry_UserSupport = ttk.Combobox(self, textvariable=self.textVariable_UserSupport, **entryConfigure)
        self.Entry_UserSupport['values'] = ('Yes', 'No')
        self.Entry_UserSupport.grid(column=3, row=12, **gridTEntryConfigure)
        self.Entry_UserSupport.bind("<FocusOut>", lambda e: self.EntryFocusOut('Support'))

    def EntryFocusOut(self, EntryName):
        txt = self.__dict__[f'Entry_User{EntryName}'].get()
        if not txt and EntryName == 'COB':
            self.Entry_UserCOB.insert(0, 'Israel')
        self.HandelFiled(EntryName, txt)
        return

    def EntryButton1(self, EntryName):
        txt = self.__dict__[f'Entry_User{EntryName}'].get()
        if EntryName == 'COB' and txt == 'Israel':
            self.__dict__[f'Entry_User{EntryName}'].delete(0, "end")
        return

    def HandelFiled(self, EntryName, txt, appCall=False):
        if EntryName == 'ID':
            if (not txt and appCall) or (txt and (len(txt) < 9 or len(txt) > 9)):
                self.Label_UserID.config(foreground="red")
                return False
            self.Label_UserID.config(foreground="black")
            return True
        if EntryName == 'Name':
            if (not txt and appCall) or (txt and len(txt) < 2):
                self.Label_UserName.config(foreground="red")
                return False
            self.Label_UserName.config(foreground="black")
            return True
        if EntryName == 'Phone':
            if (not txt and appCall) or (txt and (len(txt) < 10 or len(txt) > 10)):
                self.Label_UserPhone.config(foreground="red")
                return False
            self.Label_UserPhone.config(foreground="black")
            return True
        if EntryName == 'DOB':
            today = datetime.date.today()
            if today.year - txt.year - ((today.month, today.day) < (txt.month, txt.day)) < 18:
                self.Label_UserDOB.config(foreground="red")
                return False
            self.Label_UserDOB.config(foreground="black")
            return True
        if EntryName == 'Weight':
            if not txt and not appCall:
                return False
            try:
                digit = int(txt)
            except ValueError:
                digit = 0
            if digit <= 0:
                self.Label_UserWeight.config(foreground="red")
                return False
            self.Label_UserWeight.config(foreground="black")
            return True
        if EntryName == 'Height':
            if not txt and not appCall:
                return False
            try:
                digit = float(txt)
            except ValueError:
                digit = 0
            if digit <= 0:
                self.Label_UserHeight.config(foreground="red")
                return False
            self.Label_UserHeight.config(foreground="black")
            return True
        if EntryName == 'Gender':
            if not txt and appCall:
                self.Label_UserGender.config(foreground="red")
                return False
            self.Label_UserGender.config(foreground="black")
            return True
        if EntryName == 'Area':
            if not txt and appCall:
                self.Label_UserArea.config(foreground="red")
                return False
            self.Label_UserArea.config(foreground="black")
            return True
        if EntryName == 'City':
            if not txt and appCall:
                self.Label_UserCity.config(foreground="red")
                return False
            self.Label_UserCity.config(foreground="black")
            return True
        if EntryName == 'HMO':
            if not txt and appCall:
                self.Label_UserHMO.config(foreground="red")
                return False
            self.Label_UserHMO.config(foreground="black")
            return True
        if EntryName == 'Support':
            if not txt and appCall:
                self.Label_UserSupport.config(foreground="red")
                return False
            self.Label_UserSupport.config(foreground="black")
            return True
        return False


class PatientSignInPg2(ttk.Frame):
    def __init__(self, MasterPanel, *args, **kwargs):
        ttk.Frame.__init__(self, master=MasterPanel, *args, **kwargs)
        self.List_UserSelectSymptoms = {}
        self.columnconfigure(list(range(1, 6)), weight=1)
        self.rowconfigure(list(range(1, 16)), weight=1)
        self.symptomsTrie = AUTO_complete()
        self._create_widgets(MasterPanel)
        self.keyRelBool = True

    def _create_widgets(self, MasterPanel):
        gridConfigure = {'padx': 20, 'pady': 0}
        gridTEntryConfigure = {'padx': 20, 'pady': 0, 'ipady': 0, 'ipadx': 0}
        entryConfigure = {'font': ("Helvetica", 18), 'background': 'white'}
        labelConfigure = {'font': ("Helvetica", 18, "bold"), 'background': 'white', 'borderwidth': 0}

        def make_scrollbar_styles():
            style = ttk.Style()

            for is_hori in (True, False):
                v = "Horizontal" if is_hori else "Vertical"
                style.element_create(f'CustomScrollbarStyle.{v}.Scrollbar.trough', 'from', 'default')
                style.element_create(f'CustomScrollbarStyle.{v}.Scrollbar.thumb', 'from', 'default')
                style.element_create(f'CustomScrollbarStyle.{v}.Scrollbar.leftarrow', 'from', 'default')
                style.element_create(f'CustomScrollbarStyle.{v}.Scrollbar.rightarrow', 'from', 'default')
                style.element_create(f'CustomScrollbarStyle.{v}.Scrollbar.grip', 'from', 'default')
                style.layout(
                    f'CustomScrollbarStyle.{v}.TScrollbar',
                    [(f'CustomScrollbarStyle.{v}.Scrollbar.trough', {
                        'children': [
                            # Commenting in these 2 lines adds arrows (at least horizontally)
                            (f'CustomScrollbarStyle.{v}.Scrollbar.leftarrow',
                             {'side': 'left', 'sticky': 'we'}) if is_hori else (
                                f'CustomScrollbarStyle.{v}.Scrollbar.uparrow', {}),
                            (f'CustomScrollbarStyle.{v}.Scrollbar.rightarrow',
                             {'side': 'right', 'sticky': 'we'}) if is_hori else (
                                f'CustomScrollbarStyle.{v}.Scrollbar.downarrow', {}),
                            (f'CustomScrollbarStyle.{v}.Scrollbar.thumb', {
                                'unit': '20',
                                'children': [(f'CustomScrollbarStyle.{v}.Scrollbar.grip', {'sticky': ''})],
                                'sticky': 'nswe'}
                             )
                        ],
                        'sticky': 'we' if is_hori else 'ns'}),
                     ])
                style.configure(f'CustomScrollbarStyle.{v}.TScrollbar', troughcolor='white',
                                background='LightSkyBlue4',
                                arrowcolor='white', borderwidth=0)
                style.map(f'CustomScrollbarStyle.{v}.TScrollbar',
                          background=[('pressed', '!disabled', 'white'), ('active', 'white')])
            return "CustomScrollbarStyle.Horizontal.TScrollbar", "CustomScrollbarStyle.Vertical.TScrollbar"

        hstyle, vstyle = make_scrollbar_styles()

        # ------------------------- Enter Symptoms ------------------------------------------
        self.Label_UserSymptoms = ttk.Label(self, text='Symptoms:', **labelConfigure)
        self.Label_UserSymptoms.grid(column=1, row=3, columnspan=2, sticky=tk.W + tk.N, **gridConfigure)

        self.symptomText = tk.StringVar()
        self.Entry_UserSymptoms = ttk.Entry(self, textvariable=self.symptomText, width=40, **entryConfigure)
        self.Entry_UserSymptoms.insert(0, 'Enter your common symptoms...')
        self.Entry_UserSymptoms.grid(column=1, row=4, columnspan=2, rowspan=2, sticky=tk.W + tk.N,
                                     **gridTEntryConfigure)
        self.Entry_UserSymptoms.bind("<Button-1>", lambda e: self.EntryButton1('Symptoms'))
        self.Entry_UserSymptoms.bind("<FocusOut>", lambda e: self.EntryFocusOut('Symptoms'))
        self.Entry_UserSymptoms.bind("<space>", lambda e: self._space())
        self.Entry_UserSymptoms.bind("<BackSpace>", lambda e: self._backSpace())
        self.Entry_UserSymptoms.bind("<KeyRelease>", lambda e: self._KeyRelease())

        self.Listbox_UserSymptoms = tk.Listbox(self, selectmode=tk.EXTENDED, font=("Helvetica", 18),
                                               bg='white', highlightcolor='white', highlightthickness=0,
                                               relief='flat', width=40)
        self.Listbox_UserSymptoms.grid(column=1, row=6, columnspan=2, rowspan=3, sticky=tk.W + tk.N, **gridConfigure)

        self.Listbox_UserSymptoms = tk.Listbox(self, selectmode=tk.EXTENDED, font=("Helvetica", 18),
                                               bg='white', highlightcolor='white', highlightthickness=0,
                                               relief='flat', width=40)
        self.Listbox_UserSymptoms.grid(column=1, row=6, columnspan=2, rowspan=3, sticky=tk.W + tk.N, **gridConfigure)
        self.Listbox_UserSymptoms.bind('<<ListboxSelect>>', lambda e: self.updateSelectSymptoms())
        self.Scrollbar_UserSymptoms_y = ttk.Scrollbar(self, orient=VERTICAL, command=self.Listbox_UserSymptoms.yview,
                                                      cursor="arrow", style=vstyle)
        self.Scrollbar_UserSymptoms_x = ttk.Scrollbar(self, orient=HORIZONTAL, command=self.Listbox_UserSymptoms.xview,
                                                      cursor="arrow", style=hstyle)
        self.Scrollbar_UserSymptoms_y.grid(column=1, row=6, rowspan=3, sticky=tk.W + tk.N)
        self.Scrollbar_UserSymptoms_x.grid(column=1, row=9, columnspan=2, sticky=tk.W + tk.N)
        self.Listbox_UserSymptoms['yscrollcommand'] = self.Scrollbar_UserSymptoms_y.set
        self.Listbox_UserSymptoms['xscrollcommand'] = self.Scrollbar_UserSymptoms_x.set
        var = tk.Variable(value=self.symptomsTrie.initValues())
        self.Listbox_UserSymptoms.config(listvariable=var)

        # ------------------------- Separator ------------------------------------------
        ttk.Separator(self, orient=VERTICAL).grid(row=1, column=3, rowspan=13, ipady=150, sticky=tk.N + tk.S)
        gridConfigure['padx'] = 2
        gridTEntryConfigure['padx'] = 2

        # ------------------------- Selected Symptoms ------------------------------------------

        self.Label_UserSelectSymptoms = ttk.Label(self, text='Selected Symptoms:', **labelConfigure)
        self.Label_UserSelectSymptoms.grid(column=4, row=3, columnspan=2, sticky=tk.W + tk.N, **gridConfigure)

        self.Listbox_UserSelectSymptoms = tk.Listbox(self, selectmode=tk.EXTENDED, font=("Helvetica", 18),
                                                     bg='white', highlightcolor='white', highlightthickness=0,
                                                     relief='flat', width=40)
        self.Listbox_UserSelectSymptoms.grid(column=4, row=6, columnspan=2, rowspan=3, sticky=tk.W + tk.N,
                                             **gridConfigure)

        self.Listbox_UserSelectSymptoms.bind('<<ListboxSelect>>', lambda e: self.deleteSelectSymptoms())
        self.Scrollbar_UserSelectSymptoms_y = ttk.Scrollbar(self, orient=VERTICAL,
                                                            command=self.Listbox_UserSelectSymptoms.yview,
                                                            cursor="arrow")
        self.Scrollbar_UserSelectSymptoms_x = ttk.Scrollbar(self, orient=HORIZONTAL,
                                                            command=self.Listbox_UserSelectSymptoms.xview,
                                                            cursor="arrow", style=hstyle)
        self.Scrollbar_UserSelectSymptoms_x.grid(column=4, row=9, columnspan=2, sticky=tk.W + tk.N)
        self.Listbox_UserSelectSymptoms['yscrollcommand'] = self.Scrollbar_UserSelectSymptoms_y.set
        self.Listbox_UserSelectSymptoms['xscrollcommand'] = self.Scrollbar_UserSelectSymptoms_x.set

        # ------------------------- SignIN ------------------------------------------
        self.Button_SignIN = RoundedButton(master=self, text="Sign In", radius=10, btnbackground="LightSkyBlue4",
                                           btnforeground="white", width=150, height=60, highlightthickness=0,
                                           font=("Helvetica", 18, "bold"), masterBackground='white')
        self.Button_SignIN.grid(column=3, row=14, sticky=tk.N + tk.S)
        self.Button_SignIN.bind("<Button-1>", lambda e: self.SignINButton(MasterPanel))
        self.Entry_coniferVar = tk.IntVar()
        self.Entry_conifer = tk.Checkbutton(self, text="I agree to the terms", variable=self.Entry_coniferVar,
                                            onvalue=1, offvalue=0, width=20, background="white",
                                            font=("Helvetica", 12), foreground='black')
        self.Entry_conifer.grid(column=3, row=15, sticky=tk.N + tk.S)

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
        if self.List_UserSelectSymptoms.get(txt):
            return
        self.List_UserSelectSymptoms[txt] = True
        var = tk.Variable(value=list(self.List_UserSelectSymptoms.keys()))
        self.Listbox_UserSelectSymptoms.config(listvariable=var)
        return print(txt)

    def deleteSelectSymptoms(self):
        selected = self.Listbox_UserSelectSymptoms.curselection()
        if not selected:
            return
        txt = self.Listbox_UserSelectSymptoms.get(selected[0])
        self.List_UserSelectSymptoms.pop(txt)
        var = tk.Variable(value=list(self.List_UserSelectSymptoms.keys()))
        self.Listbox_UserSelectSymptoms.config(listvariable=var)
        return

    def EntryButton1(self, EntryName):
        txt = self.__dict__[f'Entry_User{EntryName}'].get()
        if EntryName == 'Symptoms' and txt == 'Enter your common symptoms...':
            self.__dict__[f'Entry_User{EntryName}'].delete(0, "end")
        return

    def EntryFocusOut(self, EntryName):
        txt = self.__dict__[f'Entry_User{EntryName}'].get()
        if not txt and EntryName == 'Symptoms':
            self.Entry_UserSymptoms.insert(0, 'Enter your common symptoms...')
        return

    def _space(self):
        self.symptomsTrie.space()
        return

    def _backSpace(self):
        self.symptomsTrie.backSpace()
        return

    def _KeyRelease(self):
        sentence = self.Entry_UserSymptoms.get()
        sentence_list = self.symptomsTrie.keyRelease(sentence)
        var = tk.Variable(value=sentence_list)
        self.Listbox_UserSymptoms.config(listvariable=var)
        return


class PatientMainPanel(ttk.Frame):

    def __init__(self, MasterPanel):
        ttk.Frame.__init__(self, master=MasterPanel, relief=tk.RAISED, borderwidth=2)
        self.width = 0.5 * MasterPanel.width
        self.height = 0.5 * MasterPanel.height
        self.columnconfigure(list(range(1, 11)), weight=1)
        self.rowconfigure(list(range(1, 11)), weight=1)
        self._create_sub_frames(MasterPanel)

    def _create_sub_frames(self, MasterPanel):
        gridConfigure = {'padx': 20, 'pady': 0}
        gridTEntryConfigure = {'padx': 20, 'pady': 0, 'ipady': 0, 'ipadx': 0}
        entryConfigure = {'font': ("Helvetica", 18), 'background': 'white'}
        labelConfigure = {'font': ("Helvetica", 18, "bold"), 'background': 'white', 'borderwidth': 0}
        self.style = ttk.Style(self)
        self.style.configure('TFrame', background='white', borderwidth=10, relief='RAISED')

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

        ttk.Separator(self, orient=VERTICAL).grid(row=2, column=2, rowspan=9, ipady=150,
                                                    sticky=tk.W + tk.S + tk.N)
        Indices_title = ttk.Label(self, text='Your Indices', font=("Helvetica", 16, "bold"), background="white", foreground='LightSkyBlue4')
        Indices_title.grid(row=2, column=0)

        Indices = MasterPanel.app_insert2DB.dequeueIndices()
        print(Indices)
        txt = ''
        for lab in ['ID', 'name', 'gender', 'DOB', 'area', 'city', 'phone', 'HMO', 'height', 'weight']:
            labName = lab[0].upper() + lab[1:]
            txt += f'- {labName}:   {str(Indices[lab])}\n'

        self.Label_Indices = ttk.Label(self, text=txt, font=("Helvetica", 16, "bold"), background="white",
                                       foreground='black')
        self.Label_Indices.grid(row=3, column=0, sticky=tk.N)

        symptom_title = ttk.Label(self, text='Your Symptoms', font=("Helvetica", 16, "bold"), background="white",
                                foreground='LightSkyBlue4')
        symptom_title.grid(row=5, column=0)
        symptom = Indices.get('symptoms')
        txt = ''
        if symptom:
            for sym in symptom:
                txt += f'- {sym}\n'
        self.Label_Symptoms = ttk.Label(self, text=txt, font=("Helvetica", 16, "bold"), background="white",
                                       foreground='black')
        self.Label_Symptoms.grid(row=6, column=0, sticky=tk.N)
        return


class ResearcherSignInPanel(ttk.Frame):

    def __init__(self, MasterPanel):
        ttk.Frame.__init__(self, master=MasterPanel, relief=tk.RAISED, borderwidth=2)
        self.width = 0.5 * MasterPanel.width
        self.height = 0.5 * MasterPanel.height
        self.columnconfigure(list(range(1, 11)), weight=1)
        self.rowconfigure(list(range(1, 11)), weight=1)
        self._create_sub_frames(MasterPanel)

    def _create_sub_frames(self, MasterPanel):
        return


class ResearcherMainPanel(ttk.Frame):

    def __init__(self, MasterPanel):
        ttk.Frame.__init__(self, master=MasterPanel, relief=tk.RAISED, borderwidth=2)
        self.width = 0.5 * MasterPanel.width
        self.height = 0.5 * MasterPanel.height
        self.columnconfigure(list(range(1, 11)), weight=1)
        self.rowconfigure(list(range(1, 11)), weight=1)
        self._create_sub_frames(MasterPanel)

    def _create_sub_frames(self, MasterPanel):
        return
