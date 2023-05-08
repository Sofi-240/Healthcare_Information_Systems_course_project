import tkinter as tk
from tkinter import ttk, HORIZONTAL, VERTICAL
from app.frontEnd.RoundButton import RoundedButton
from tkcalendar import DateEntry


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
