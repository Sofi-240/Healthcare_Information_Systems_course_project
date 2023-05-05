from screeninfo import get_monitors
from tkinter import messagebox
from app.frontEnd.views import *
from app.communication.query import DataQueries
from app.communication.input import insert2DB


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
        self.app_queries = DataQueries("his_project")
        self.app_insert2DB = insert2DB(self)
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


if __name__ == '__main__':
    myPanel = Panel()
    myPanel.mainloop()
