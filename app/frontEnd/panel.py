import tkinter as tk
from tkinter import ttk, HORIZONTAL, VERTICAL
from screeninfo import get_monitors
from tkinter import messagebox
from app.frontEnd.RoundButton import RoundedButton
from app.frontEnd.autoComplete import AUTO_complete
from tkcalendar import DateEntry
import datetime


class Panel(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('App Panel')
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
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
        for F in [UserLogInPanel, PatientSignInPanel, ResearcherSignInPanel, ResearcherMainPanel, PatientMainPanel]:
            frame = F(self)
            frame.grid(column=1, row=1, padx=20, pady=20, sticky="nsew")
            self.frames[F] = frame
        return self.show_frame(UserLogInPanel)

    def show_frame(self, name):
        self.frame = self.frames[name]
        self.frame.tkraise()
        return

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()


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
        self.LabelError_UserID = ttk.Label(self, **labelConfigure)
        self.LabelError_UserID.grid(column=3, row=5, padx=0, pady=0)
        self.LabelError_UserID.configure(foreground="red")

        # User researcher or patient Insert Name
        self.Label_UserName = ttk.Label(self, text='User Name:', **labelConfigure)
        self.Label_UserName.grid(column=1, row=6, **gridConfigure)
        self.Entry_UserName = ttk.Entry(self, **entryConfigure)
        self.Entry_UserName.insert(0, "Name")
        self.Entry_UserName.grid(column=2, row=6, **gridTEntryConfigure)
        self.Entry_UserName.bind("<FocusOut>", lambda e: self.EntryFocusOut('Name'))
        self.Entry_UserName.bind("<Button-1>", lambda e: self.EntryButton1('Name'))
        self.LabelError_UserName = ttk.Label(self, **labelConfigure)

        # LOGIN button
        self.Button_LogIn = RoundedButton(master=self, text="Log In", radius=25, btnbackground="LightGoldenrod1",
                                          btnforeground="black", width=250, height=60, highlightthickness=0,
                                          font=("Helvetica", 18, "bold"), masterBackground='LightSkyBlue4')
        self.Button_LogIn.grid(column=2, row=7, **gridConfigure)
        self.Button_LogIn.bind("<Button-1>", lambda e: self.ExLogIn(MasterPanel))

        # SingIN button
        self.Button_SignIN = RoundedButton(master=self, text="Sign IN", radius=25, btnbackground="LightGoldenrod1",
                                           btnforeground="black", width=250, height=60, highlightthickness=0,
                                           font=("Helvetica", 18, "bold"), masterBackground='LightSkyBlue4')
        self.Button_SignIN.grid(column=2, row=8, **gridConfigure)
        self.Button_SignIN.bind("<Button-1>", lambda e: self.ExSignIN(MasterPanel))
        return

    def EntryFocusOut(self, EntryName):
        txt = self.__dict__[f'Entry_User{EntryName}'].get()
        if not txt:
            self.__dict__[f'Entry_User{EntryName}'].insert(0, EntryName)
            return
        if self.__dict__.get(f'LabelError_User{EntryName}'):
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
                self.LabelError_UserID.configure(text='*The ID is not valid')
                return
            self.Entry_UserID.config(foreground="black")
            self.LabelError_UserID.configure(text='')
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
            return MasterPanel.master.show_frame(ResearcherMainPanel)
        return MasterPanel.master.show_frame(PatientMainPanel)

    def ExSignIN(self, MasterPanel):
        selected = self.Entry_UserPath.get()
        if selected == 0:
            return MasterPanel.master.show_frame(ResearcherSignInPanel)
        return MasterPanel.master.show_frame(PatientSignInPanel)


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
        self.style.configure('TNotebook', background="LightSkyBlue4", weight=50, tabmargins=[0, 5, 0, 0])
        self.style.configure('TNotebook.Tab', background="LightGoldenrod1", compound=tk.LEFT,
                             font=("Helvetica", 18, "bold"), weight=50, padding=[50, 20])

        Label_title = ttk.Label(self, text='                      Sign In', font=("Helvetica", 50, "bold"),
                                background="white", foreground='black')
        Label_title.grid(column=2, row=1, padx=5, pady=5, sticky=tk.E)

        ttk.Separator(self, orient=HORIZONTAL).grid(row=2, column=0, columnspan=6, ipadx=150, sticky=tk.W + tk.E)

        # Back button
        self.Button_Back = RoundedButton(master=self, text="Back", radius=10, btnbackground="LightSkyBlue4",
                                         btnforeground="white", width=150, height=60, highlightthickness=0,
                                         font=("Helvetica", 18, "bold"), masterBackground='white')
        self.Button_Back.grid(column=2, row=1, padx=5, pady=5, sticky=tk.W)
        self.Button_Back.bind("<Button-1>", lambda e: self.back())

        # Next button
        self.Button_Next = RoundedButton(master=self, text="Next", radius=10, btnbackground="LightSkyBlue4",
                                         btnforeground="white", width=150, height=60, highlightthickness=0,
                                         font=("Helvetica", 18, "bold"), masterBackground='white')
        self.Button_Next.grid(column=4, row=1, padx=5, pady=5, sticky=tk.E)
        self.Button_Next.bind("<Button-1>", lambda e: self.forward())

        # Return button
        self.Button_Return = RoundedButton(master=self, text="Return", radius=10, btnbackground="LightSkyBlue4",
                                           btnforeground="white", width=150, height=60, highlightthickness=0,
                                           font=("Helvetica", 18, "bold"), masterBackground='white')
        self.Button_Return.grid(column=2, row=10, padx=5, pady=5, sticky=tk.W)
        self.Button_Return.bind("<Button-1>", lambda e: MasterPanel.show_frame(UserLogInPanel))

        self.Page_Frames = ttk.Notebook(self, width=500, height=600)
        self.Page_Frames.grid(column=2, row=3, padx=10, pady=10, sticky="nsew", columnspan=3, rowspan=2)

        self.pg0 = PatientSignInPg1(self.Page_Frames, style='TFrame')
        self.pg0.grid(column=2, row=3, padx=10, pady=10, sticky="nsew", columnspan=3, rowspan=2)
        self.pg1 = PatientSignInPg2(self.Page_Frames, style='TFrame')
        self.pg1.grid(column=2, row=3, padx=10, pady=10, sticky="nsew", columnspan=3, rowspan=2)
        self.frames = {}
        self.Page_Frames.add(self.pg0, text='                Step 1                ')
        self.Page_Frames.add(self.pg1, text='                Step 2                ')
        self.Page_Frames.select(0)

        return

    def back(self):
        index = self.Page_Frames.index(self.Page_Frames.select())
        if index == 1:
            self.Page_Frames.select(0)
        return

    def forward(self):
        index = self.Page_Frames.index(self.Page_Frames.select())
        if index == 0:
            errCache = False
            for val, item in self.pg0.__dict__.items():
                if len(val) > 10 and val[:10] == 'Entry_User' and val[10:] in ['ID', 'Phone', 'DOB']:
                    txt = item.get()
                    if val[10:] == 'ID' and txt and (len(txt) < 9 or len(txt) > 9):
                        errCache = True
                        self.pg0.HandelFiled('ID', txt)
                    if val[10:] == 'Phone' and txt and (len(txt) < 10 or len(txt) > 10):
                        errCache = True
                        self.pg0.HandelFiled('Phone', txt)
                    if not txt:
                        errCache = True
            if errCache:
                self.Page_Frames.select(1)
                return
            self.Page_Frames.select(1)
        return


class PatientSignInPg1(ttk.Frame):
    def __init__(self, MasterPanel, *args, **kwargs):
        ttk.Frame.__init__(self, master=MasterPanel, *args, **kwargs)
        self.columnconfigure(list(range(1, 5)), weight=1)
        self.rowconfigure(list(range(1, 14)), weight=1)
        self._create_widgets(MasterPanel)

    def _create_widgets(self, MasterPanel):
        gridConfigure = {'padx': 10, 'pady': 0, 'sticky': tk.W}
        gridTEntryConfigure = {'padx': 10, 'pady': 0, 'sticky': tk.W, 'ipady': 5, 'ipadx': 0}
        entryConfigure = {'font': ("Helvetica", 18), 'background': 'white'}
        labelConfigure = {'font': ("Helvetica", 18, "bold"), 'background': 'white', 'borderwidth': 0}

        # ------------------------- ID ------------------------------------------
        self.Label_UserID = ttk.Label(self, text='ID: *', **labelConfigure)
        self.Label_UserID.grid(column=1, row=1, **gridConfigure)

        self.Entry_UserID = ttk.Entry(self, **entryConfigure)
        self.Entry_UserID.grid(column=1, row=2, **gridTEntryConfigure)
        self.Entry_UserID.bind("<Button-1>", lambda e: self.EntryButton1('ID'))
        self.Entry_UserID.bind("<FocusOut>", lambda e: self.EntryFocusOut('ID'))

        self.EntryError_UserID = ttk.Label(self, font=("Helvetica", 14), background='white', foreground='red')
        self.EntryError_UserID.grid(column=2, row=1, padx=0, pady=0, sticky=tk.W)
        self.EntryError_UserID.configure(foreground="red", font=("Helvetica", 12))

        # ------------------------- Name ------------------------------------------
        self.Label_UserName = ttk.Label(self, text='Name: *', **labelConfigure)
        self.Label_UserName.grid(column=1, row=3, **gridConfigure)

        self.Entry_UserName = ttk.Entry(self, **entryConfigure)
        self.Entry_UserName.grid(column=1, row=4, columnspan=2, **gridTEntryConfigure)
        self.Entry_UserName.bind("<Button-1>", lambda e: self.EntryButton1('Name'))

        # ------------------------- Gender ------------------------------------------
        self.Label_UserGender = ttk.Label(self, text='Gender:', **labelConfigure)
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
        self.Entry_UserPhone.bind("<Button-1>", lambda e: self.EntryButton1('Phone'))
        self.Entry_UserPhone.bind("<FocusOut>", lambda e: self.EntryFocusOut('Phone'))

        self.EntryError_UserPhone = ttk.Label(self)
        self.EntryError_UserPhone.grid(column=2, row=11, **gridConfigure)
        self.EntryError_UserPhone.configure(foreground="red", font=("Helvetica", 12))

        # ------------------------- Separator ------------------------------------------
        ttk.Separator(self, orient=VERTICAL).grid(row=1, column=2, rowspan=13, ipady=150, sticky=tk.N + tk.S)
        gridConfigure['padx'] = 2
        gridTEntryConfigure['padx'] = 2

        # ------------------------- DOB ------------------------------------------
        self.Label_UserDOB = ttk.Label(self, text='Date of Birth: *', **labelConfigure)
        self.Label_UserDOB.grid(column=3, row=1, **gridConfigure)

        self.Entry_UserDOB = DateEntry(self, selectmode='day', date_pattern='MM-dd-yyyy',
                                       font=("Helvetica", 18, "bold"),
                                       firstweekday='sunday', weekenddays=[6, 7], background='LightGoldenrod1',
                                       foreground='black')
        self.Entry_UserDOB.bind("<<DateEntrySelected>>",
                                lambda e: self.HandelFiled('DOB', self.Entry_UserDOB.get_date()))
        self.Entry_UserDOB.grid(column=3, row=2, **gridConfigure)

        self.EntryError_UserDOB = ttk.Label(self, **labelConfigure)
        self.EntryError_UserDOB.configure(foreground="red", font=("Helvetica", 12))
        self.EntryError_UserDOB.grid(column=4, row=1, **gridConfigure)

        # ------------------------- HMO ------------------------------------------
        self.Label_UserHMO = ttk.Label(self, text='HMO: *', **labelConfigure)
        self.Label_UserHMO.grid(column=3, row=3, **gridConfigure)

        self.textVariable_UserHMO = tk.StringVar()
        self.Entry_UserHMO = ttk.Combobox(self, textvariable=self.textVariable_UserHMO, **entryConfigure)
        self.Entry_UserHMO['values'] = ('Clalit', 'Maccabi', 'Meuhedet', 'Leumit')
        self.Entry_UserHMO.grid(column=3, row=4, **gridTEntryConfigure)

        # ------------------------- COB ------------------------------------------
        self.Label_UserCOB = ttk.Label(self, text='COB:', **labelConfigure)
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

        self.EntryError_UserHeight = ttk.Label(self, **labelConfigure)
        self.EntryError_UserHeight.configure(foreground="red", font=("Helvetica", 12))
        self.EntryError_UserHeight.grid(column=4, row=7, **gridConfigure)

        # ------------------------- Weight ------------------------------------------
        self.Label_UserWeight = ttk.Label(self, text='Weight: *', **labelConfigure)
        self.Label_UserWeight.grid(column=3, row=9, **gridConfigure)

        self.Entry_UserWeight = ttk.Entry(self, **entryConfigure)
        self.Entry_UserWeight.grid(column=3, row=10, **gridTEntryConfigure)
        self.Entry_UserWeight.bind("<FocusOut>", lambda e: self.EntryFocusOut('Weight'))

        self.EntryError_UserWeight = ttk.Label(self, **labelConfigure)
        self.EntryError_UserWeight.configure(foreground="red", font=("Helvetica", 12))
        self.EntryError_UserWeight.grid(column=4, row=9, **gridConfigure)

        # ------------------------- Support ------------------------------------------
        self.Label_UserSupport = ttk.Label(self, text='Support: *', **labelConfigure)
        self.Label_UserSupport.grid(column=3, row=11, **gridConfigure)

        self.textVariable_UserSupport = tk.StringVar()
        self.Entry_UserSupport = ttk.Combobox(self, textvariable=self.textVariable_UserSupport, **entryConfigure)
        self.Entry_UserSupport['values'] = ('Yes', 'No')
        self.Entry_UserSupport.grid(column=3, row=12, **gridTEntryConfigure)

    def EntryFocusOut(self, EntryName):
        txt = self.__dict__[f'Entry_User{EntryName}'].get()
        if not txt and EntryName == 'COB':
            self.Entry_UserCOB.insert(0, 'Israel')
        if self.__dict__.get(f'EntryError_User{EntryName}'):
            return self.HandelFiled(EntryName, txt)
        return

    def EntryButton1(self, EntryName):
        txt = self.__dict__[f'Entry_User{EntryName}'].get()
        if txt == EntryName or (EntryName == 'COB' and txt == 'Israel'):
            self.__dict__[f'Entry_User{EntryName}'].delete(0, "end")
        return

    def HandelFiled(self, EntryName, txt):
        if EntryName == 'ID':
            if txt and (len(txt) < 9 or len(txt) > 9):
                self.Entry_UserID.config(foreground="red")
                self.EntryError_UserID.configure(text='The ID is not valid')
                return
            self.Entry_UserID.config(foreground="black")
            self.EntryError_UserID.configure(text='')
            return
        if EntryName == 'Phone':
            if txt and (len(txt) < 10 or len(txt) > 10):
                self.Entry_UserPhone.config(foreground="red")
                self.EntryError_UserPhone.configure(text='The Phone number is not valid')
                return
            self.Entry_UserPhone.config(foreground="black")
            self.EntryError_UserPhone.configure(text='')
            return
        if EntryName == 'DOB':
            today = datetime.date.today()
            if today.year - txt.year - ((today.month, today.day) < (txt.month, txt.day)) < 18:
                self.Entry_UserDOB.config(foreground="red")
                self.EntryError_UserDOB.configure(text='The minimum age is 18')
                return
            self.Entry_UserDOB.config(foreground="black")
            self.EntryError_UserDOB.configure(text='')
            return
        if EntryName == 'Weight':
            txt = list(txt.split())
            if txt and (not str.isdigit(txt[0]) or (str.isdigit(txt[0]) and int(txt[0]) < 0)):
                self.Entry_UserWeight.config(foreground="red")
                self.EntryError_UserWeight.configure(text='The Weight need to be positive number')
                return
            self.Entry_UserWeight.config(foreground="black")
            self.EntryError_UserWeight.configure(text='')
            return
        if EntryName == 'Height':
            txt = list(txt.split())
            if txt and (not str.isdigit(txt[0]) or (str.isdigit(txt[0]) and int(txt[0]) < 0)):
                self.Entry_UserHeight.config(foreground="red")
                self.EntryError_UserHeight.configure(text='The Height need to be positive number')
                return
            self.Entry_UserHeight.config(foreground="black")
            self.EntryError_UserHeight.configure(text='')
            return
        return


class PatientSignInPg2(ttk.Frame):
    def __init__(self, MasterPanel, *args, **kwargs):
        ttk.Frame.__init__(self, master=MasterPanel, *args, **kwargs)
        self.List_UserSelectSymptoms = {}
        self.columnconfigure(list(range(1, 14)), weight=1)
        self.rowconfigure(list(range(1, 16)), weight=1)
        self.symptomsTrie = AUTO_complete()
        self._create_widgets(MasterPanel)
        self.keyRelBool = True

    def _create_widgets(self, MasterPanel):
        gridConfigure = {'padx': 50, 'pady': 0}
        gridTEntryConfigure = {'padx': 50, 'pady': 0, 'ipady': 0, 'ipadx': 0}
        entryConfigure = {'font': ("Helvetica", 18), 'background': 'white'}
        labelConfigure = {'font': ("Helvetica", 18, "bold"), 'background': 'white', 'borderwidth': 0}

        self.Label_UserSymptoms = ttk.Label(self, text='Symptoms:', **labelConfigure)
        self.Label_UserSymptoms.grid(column=1, row=3, columnspan=5, sticky=tk.W + tk.N, **gridConfigure)

        self.symptomText = tk.StringVar()
        self.Entry_UserSymptoms = ttk.Entry(self, textvariable=self.symptomText, width=40, **entryConfigure)
        self.Entry_UserSymptoms.grid(column=1, row=4, columnspan=5, rowspan=2, sticky=tk.W + tk.N, **gridTEntryConfigure)
        self.Entry_UserSymptoms.bind("<space>", lambda e: self._space())
        self.Entry_UserSymptoms.bind("<BackSpace>", lambda e: self._backSpace())
        self.Entry_UserSymptoms.bind("<KeyRelease>", lambda e: self._KeyRelease())

        self.Listbox_UserSymptoms = tk.Listbox(self, selectmode=tk.EXTENDED, font=("Helvetica", 18),
                                               bg='white', highlightcolor='white', highlightthickness=3,
                                               relief='flat', width=40)
        self.Listbox_UserSymptoms.grid(column=1, row=6, columnspan=5, rowspan=3, sticky=tk.W + tk.N, **gridConfigure)

        self.Scrollbar_UserSymptoms = ttk.Scrollbar(self, orient=VERTICAL, command=self.Listbox_UserSymptoms.yview)
        self.Listbox_UserSymptoms['yscrollcommand'] = self.Scrollbar_UserSymptoms.set
        self.Listbox_UserSymptoms.bind('<<ListboxSelect>>', lambda e: self.updateSelectSymptoms())

        # ------------------------- Separator ------------------------------------------
        ttk.Separator(self, orient=VERTICAL).grid(row=1, column=6, rowspan=13, ipady=150, sticky=tk.N + tk.S)
        gridConfigure['padx'] = 0
        gridTEntryConfigure['padx'] = 0
        self.Label_UserSelectSymptoms = ttk.Label(self, text='Selected Symptoms:', **labelConfigure)
        self.Label_UserSelectSymptoms.grid(column=7, row=3, columnspan=5, sticky=tk.W + tk.N, **gridConfigure)

        self.Listbox_UserSelectSymptoms = tk.Listbox(self, selectmode=tk.EXTENDED, font=("Helvetica", 18),
                                               bg='white', highlightcolor='white', highlightthickness=3,
                                               relief='flat', width=40)
        self.Listbox_UserSelectSymptoms.grid(column=7, row=6, columnspan=5, rowspan=3, sticky=tk.W + tk.N, **gridConfigure)

        self.Scrollbar_UserSelectSymptoms = ttk.Scrollbar(self, orient=VERTICAL, command=self.Listbox_UserSelectSymptoms.yview)
        self.Listbox_UserSelectSymptoms['yscrollcommand'] = self.Scrollbar_UserSelectSymptoms.set
        self.Listbox_UserSelectSymptoms.bind('<<ListboxSelect>>', lambda e: self.deleteSelectSymptoms())

        # ------------------------- SignIN ------------------------------------------
        self.Button_SignIN = RoundedButton(master=self, text="Sign In", radius=10, btnbackground="LightSkyBlue4",
                                           btnforeground="white", width=150, height=60, highlightthickness=0,
                                           font=("Helvetica", 18, "bold"), masterBackground='white')
        self.Button_SignIN.grid(column=6, row=14, sticky=tk.N + tk.S)
        self.Button_SignIN.bind("<Button-1>", lambda e: self.SignINButton(MasterPanel))
        self.Entry_coniferVar = tk.IntVar()
        self.Entry_conifer = tk.Checkbutton(self, text="I agree to the terms", variable=self.Entry_coniferVar,
                                            onvalue=1, offvalue=0, width=20, background="white",
                                            font=("Helvetica", 12), foreground='black')
        self.Entry_conifer.grid(column=6, row=15, sticky=tk.N + tk.S)

    def SignINButton(self, MasterPanel):
        var = self.Entry_coniferVar.get()
        if var == 1:
            return MasterPanel.master.master.show_frame(PatientMainPanel)
        self.Entry_conifer.configure(foreground='red', font=("Helvetica", 12, "bold", 'underline'))
        return

    def HandelFiled(self, EntryName, txt):
        return

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

    def _space(self):
        word = self.Entry_UserSymptoms.get()
        self.symptomsTrie.space(word)
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


if __name__ == '__main__':
    myPanel = Panel()
    myPanel.mainloop()
