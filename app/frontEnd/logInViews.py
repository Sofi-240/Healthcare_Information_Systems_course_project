import tkinter as tk
from tkinter import ttk, HORIZONTAL
from app.frontEnd.RoundButton import RoundedButton


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
        if not self.__dict__[f'Entry_User{EntryName}'].get():
            self.__dict__[f'Entry_User{EntryName}'].insert(0, EntryName)
        return

    def EntryButton1(self, EntryName):
        if self.__dict__[f'Entry_User{EntryName}'].get() == EntryName:
            self.__dict__[f'Entry_User{EntryName}'].delete(0, "end")
        return

    def raiseError(self, EntryName):
        self.__dict__[f'Label_User{EntryName}'].config(foreground="red")
        return

    def deleteError(self, EntryName):
        self.__dict__[f'Label_User{EntryName}'].config(foreground="black")
        return

