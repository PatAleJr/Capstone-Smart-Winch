import sys
import os

# Add parent Application directory to path so Icons_rc can be imported
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6 import QtCore as qtc
from PySide6 import QtWidgets as qtw
from PySide6 import QtGui as qtg

from Login.UI.login_window_ui import Ui_w_LoginForm

class LoginForm(qtw.QWidget, Ui_w_LoginForm):

    login_success = qtc.Signal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.pb_Cancel.clicked.connect(self.close)
        self.pb_OK.clicked.connect(self.process_login)

    @qtc.Slot()
    def process_login(self):
        if self.le_UserID.text() == "Jason" and self.le_Password.text() == "Password":
            self.login_success.emit()
            self.close()
        else:
            self.lb_Message.setText("Login incorrect!")



if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    window = LoginForm()
    window.show()

    sys.exit(app.exec())