import sys
import os

# Add parent Application directory to path so Icons_rc can be imported
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg

from Persons.UI.add_person_window_ui import Ui_d_Person

class AddPerson(qtw.QDialog, Ui_d_Person):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.gb_Person.setTitle("Add Person")
        self.lb_Message.clear()
        self.pb_Close.clicked.connect(self.reject)
        self.pb_Submit.clicked.connect(self.process_entry)

    @qtc.Slot()
    def process_entry(self):
        self.lb_Message.setText("New person added.")
        self.le_FirstName.clear()
        self.le_LastName.clear()

        self.le_FirstName.setFocus()


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    
    form = AddPerson()
    form.open()

    sys.exit(app.exec())