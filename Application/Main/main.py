import sys
import os

# Add parent Application directory to path so Icons_rc can be imported
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg

from Main.UI.main_window_ui import Ui_mw_Main
from Persons.add_person import AddPerson
from Login.login import LoginForm

class MainWindow(qtw.QMainWindow, Ui_mw_Main):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.action_Quit.triggered.connect(self.close)
        self.actionAdd_Person.triggered.connect(self.open_add_person)

        self.form = LoginForm()
        self.form.login_success.connect(self.show)
        self.form.show()

    @qtc.Slot()
    def open_add_person(self):
        self.form = AddPerson()
        self.form.exec()

if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    
    window= MainWindow()
    sys.exit(app.exec())