from screeninfo import get_monitors
from tkinter import messagebox
from app.frontEnd.views import *
from app.communication.query import DataQueries
from app.communication.input import Insert2DB


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
        self.app_queries = DataQueries("his_project", self)
        self.app_insert2DB = Insert2DB(self)
        self.symptomsTrie = self.app_queries.SymptomsTrie.root
        self._initPanel()

    def _initPanel(self):
        self.frames = {}
        self.framesHash = {}
        for F, strName in zip(
                [UserLogInPanel, PatientSignInPanel, ResearcherSignInPanel],
                ['UserLogInPanel', 'PatientSignInPanel', 'ResearcherSignInPanel']):
            frame = F(self)
            frame.grid(
                column=1, row=1, padx=20, pady=20, sticky="nsew"
            )
            self.frames[F] = frame
            self.framesHash[strName] = F
        return self.show_frame(UserLogInPanel)

    def show_frame(self, name):
        if type(name) == str and name == 'PatientMainPanel':
            self.frame = PatientMainPanel(self)
            self.frame.grid(
                column=1, row=1, padx=20, pady=20, sticky="nsew"
            )
            self.frame.tkraise()
            self.frames[PatientMainPanel] = self.frame
            self.framesHash['PatientMainPanel'] = self.frame
            return
        if type(name) == str and name == 'ResearcherMainPanel':
            self.frame = ResearcherMainPanel(self)
            self.frame.grid(
                column=1, row=1, padx=20, pady=20, sticky="nsew"
            )
            self.frame.tkraise()
            self.frames[ResearcherMainPanel] = self.frame
            self.framesHash['ResearcherMainPanel'] = self.frame
            return
        if type(name) == str:
            name = self.framesHash[name]
        self.frame = self.frames[name]
        self.frame.tkraise()
        return

    def destroy_frame(self, name):
        if name == 'active':
            self.frame.destroy()
            return self.show_frame(UserLogInPanel)
        if type(name) == str and self.framesHash.get(name):
            F = self.framesHash.get(name)
            F = self.frames.get(F)
            if not F:
                return
            F.destroy()
            return self.show_frame(UserLogInPanel)
        F = self.frames.get(name)
        if not F:
            return
        F.destroy()
        return self.show_frame(UserLogInPanel)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()


if __name__ == '__main__':
    app_panel = Panel()
    app_panel.mainloop()


