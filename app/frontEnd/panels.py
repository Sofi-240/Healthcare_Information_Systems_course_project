import tkinter as tk
from tkinter import ttk, HORIZONTAL
import tkcalendar
from app.frontEnd.widgets import RoundedButton


class SignInPanel(ttk.Frame):

    def __init__(self, MasterPanel):
        ttk.Frame.__init__(
            self, master=MasterPanel,
            relief=tk.RAISED, borderwidth=2
        )
        self.width = 0.5 * MasterPanel.width
        self.height = 0.5 * MasterPanel.height
        self.columnconfigure(
            list(range(1, 6)), weight=1
        )
        self.rowconfigure(
            list(range(1, 11)), weight=1
        )
        self._init(MasterPanel)

    def _init(self, MasterPanel):
        app_inputs = MasterPanel.__dict__.get('app_inputs')
        if not app_inputs:
            return
        self.app_inputs = app_inputs

        app_queries = MasterPanel.__dict__.get('app_queries')
        if not app_queries:
            return
        self.app_queries = app_queries

        self.style = ttk.Style(self)
        self.style.configure(
            'TFrame', background='white', borderwidth=10, relief='RAISED'
        )
        self.style.configure(
            'TNotebook', background="LightSkyBlue4", weight=50, tabmargins=[5, 5, 0, 0]
        )
        self.style.configure(
            'TNotebook.Tab', background="tomato3", compound=tk.LEFT, font=("Helvetica", 18, "bold"),
            weight=50, padding=[50, 20]
        )

        Label_title = ttk.Label(
            self, text='                                            Sign In',
            font=("Helvetica", 50, "bold"),
            background="DarkGoldenrod2", foreground='black'
        )
        Label_title.grid(
            row=1, column=0, columnspan=6, ipadx=150, sticky=tk.W + tk.E
        )
        ttk.Separator(self, orient=HORIZONTAL).grid(
            row=2, column=0, columnspan=6, ipadx=150, sticky=tk.W + tk.E
        )

        # Return button
        self.Button_Return = RoundedButton(
            master=self, text="Return", radius=10, btnbackground="LightSkyBlue4", btnforeground="white", width=150,
            height=60, highlightthickness=0, font=("Helvetica", 18, "bold"), masterBackground='white'
        )
        self.Button_Return.grid(
            column=2, row=10, padx=5, pady=5, sticky=tk.W
        )
        self.Button_Return.bind(
            "<Button-1>", lambda e: app_inputs.exSignOut()
        )
        return

    def raiseError(self, labelName):
        if labelName == 'Conifer':
            entry = self.__dict__.get('Check_conifer')
            if not entry:
                return
            entry.configure(
                foreground='red', font=("Helvetica", 12, "bold", 'underline')
            )
            return
        label = self.__dict__.get(f'Label_{labelName}')
        if not label:
            return
        label.config(foreground="red")
        return

    def deleteError(self, labelName):
        if labelName == 'Conifer':
            entry = self.__dict__.get('Check_conifer')
            if not entry:
                return
            entry.configure(
                foreground='black', font=("Helvetica", 12)
            )
            return
        label = self.__dict__.get(f'Label_{labelName}')
        if not label:
            return
        label.config(foreground="black")
        return

    def getEntry(self, key):
        entry = self.__dict__.get(f'Entry_{key[0].upper()}{key[1:]}')
        if type(entry) == tkcalendar.DateEntry:
            return entry.get_date()
        if isinstance(entry, tk.ttk.Entry) or type(entry) == tk.IntVar:
            return entry.get()
        if isinstance(entry, tk.ttk.Treeview):
            return entry
        return


class MainPanel(ttk.Frame):

    def __init__(self, MasterPanel):
        ttk.Frame.__init__(self, master=MasterPanel, relief=tk.RAISED, borderwidth=2)
        self.width = 0.5 * MasterPanel.width
        self.height = 0.5 * MasterPanel.height
        self.columnconfigure(
            list(range(1, 5)), weight=1
        )
        self.rowconfigure(
            list(range(1, 6)), weight=1
        )
        self._create_sub_frames(MasterPanel)

    def _create_sub_frames(self, MasterPanel):
        self.style = ttk.Style(self)
        self.style.configure(
            'TFrame', background='white', borderwidth=10, relief='RAISED'
        )
        self.style.configure(
            'TNotebook', background="LightSkyBlue4", weight=50, tabmargins=[5, 5, 0, 0]
        )
        self.style.configure(
            'TNotebook.Tab', background="tomato3", compound=tk.LEFT, font=("Helvetica", 18, "bold"),
            weight=50, padding=[50, 20]
        )
        app_inputs = MasterPanel.__dict__.get('app_inputs')
        if not app_inputs:
            return
        self.app_inputs = app_inputs

        app_queries = MasterPanel.__dict__.get('app_queries')
        if not app_queries:
            return
        self.app_queries = app_queries

        Label_title = ttk.Label(
            self, text=' ', font=("Helvetica", 50, "bold"), background="DarkGoldenrod2", foreground='black'
        )
        Label_title.grid(
            row=0, column=0, columnspan=11, ipadx=150, sticky=tk.W + tk.E
        )
        ttk.Separator(self, orient=HORIZONTAL).grid(
            row=1, column=0, columnspan=11, ipadx=150, sticky=tk.W + tk.E + tk.N
        )
        self.Button_SignOut = RoundedButton(
            master=self, text="Sign Out", radius=10, btnbackground="LightSkyBlue4", btnforeground="white",
            width=150, height=60, highlightthickness=0, font=("Helvetica", 18, "bold"),
            masterBackground='DarkGoldenrod2'
        )
        self.Button_SignOut.grid(
            column=0, row=0, padx=5, pady=5, sticky=tk.W
        )
        self.Button_SignOut.bind(
            "<Button-1>", lambda e: app_inputs.exSignOut()
        )
        self.Button_Refresh = RoundedButton(
            master=self, text="Refresh", radius=10, btnbackground="LightSkyBlue4", btnforeground="white",
            width=150, height=60, highlightthickness=0, font=("Helvetica", 18, "bold"),
            masterBackground='DarkGoldenrod2'
        )
        self.Button_Refresh.grid(
            column=1, row=0, padx=5, pady=5, sticky=tk.W
        )
        self.Button_Refresh.bind(
            '<Button-1>', lambda e: self.buttonRefresh()
        )
        self.Button_DisConnect = RoundedButton(
            master=self, text="DisConnect", radius=10, btnbackground="LightSkyBlue4", btnforeground="white",
            width=150, height=60, highlightthickness=0, font=("Helvetica", 18, "bold"),
            masterBackground='DarkGoldenrod2'
        )
        self.Button_DisConnect.grid(
            column=5, row=0, padx=5, pady=5, sticky=tk.E
        )
        self.Button_DisConnect.bind(
            "<Button-1>", lambda e: app_inputs.exDisConnect()
        )
        return

    def _initNoteBook(self):
        return

    def buttonUpDate(self):
        if self.app_inputs.userUpDate():
            return self.buttonRefresh()
        return

    def buttonRefresh(self):
        self.app_queries.activateLogIn(
            'active', None, None
        )
        return self._initNoteBook()

    def raiseError(self, pgIndex, labelName=None):
        pg = self.__dict__.get(f'pg{pgIndex}')
        if not pg:
            return
        label = pg.__dict__.get(f'Label_{labelName}')
        if not label:
            return
        label.config(foreground="red")
        return

    def deleteError(self, pgIndex, labelName=None):
        pg = self.__dict__.get(f'pg{pgIndex}')
        if not pg:
            return
        label = pg.__dict__.get(f'Label_{labelName}')
        if not label:
            return
        label.config(foreground="black")
        return
