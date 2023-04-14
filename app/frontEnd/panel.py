import tkinter as tk
from tkinter import ttk
import sys
from screeninfo import get_monitors


class UserInitFrame(ttk.Frame):
    def __init__(self, MasterPanel):
        ttk.Frame.__init__(self, master=MasterPanel, relief=tk.RAISED, borderwidth=2, width=1000, height=200)
        self._create_widgets(MasterPanel)

    def _create_widgets(self, MasterPanel):
        self.columnconfigure([1, 2, 3, 4, 5, 6], weight=1, minsize=10)
        self.rowconfigure([1, 2], weight=1, minsize=120)
        self.labelPatientID = tk.Label(self, text='ID', fg='black', bg='gray', width=12, height=1)
        self.labelPatientID.grid(column=1, row=1, padx=0, pady=1)
        # self.labelPatientID.pack(side=tk.LEFT)
        self.PatientIdEntry = tk.Entry(self, width=22)
        self.PatientIdEntry.insert(0, "ID")
        self.PatientIdEntry.grid(column=2, row=1, padx=1, pady=1)
        self.PatientIdEntry.bind("<Button-1>", lambda e: self.PatientIdEntry.delete(0, "end"))
        # self.PatientIdEntry.bind("<Leave>", lambda e: print(f'{self.PatientIdEntry.get()}'))


class DataFrame(ttk.Frame):
    pass


class UserConnectFrame(ttk.Frame):
    pass


class Panel(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('My panel')
        self.width = get_monitors()[0].width
        self.height = get_monitors()[0].height
        self.geometry(f'{int(self.width * 0.9)}x{int(self.height * 0.9)}')
        self.resizable(True, True)
        self.columnconfigure([1, 2, 3], weight=1, minsize=120)
        self.rowconfigure([1, 2, 3, 4], weight=1, minsize=120)
        self._createFrame()

    def _createFrame(self):
        self.frame1 = UserInitFrame(self)
        self.frame1.grid(column=1, row=1, padx=0, pady=0)


if __name__ == '__main__':
    myPanel = Panel()
    myPanel.mainloop()
