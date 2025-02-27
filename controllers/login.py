from PyQt5 import QtWidgets
from view.login_ui import LoginUI
from models.habit_manager import HabitManager
from .register import RegisterApp

class LoginApp(LoginUI):
    def __init__(self, parent=None):
        super(LoginApp, self).__init__(parent)
        self.manager = HabitManager()
        self.loginButton.clicked.connect(self.login)
        self.registerLabel.linkActivated.connect(self.open_register_dialog)
        self.current_user = None
        self.show()

    def login(self):
        email = self.emailInput.text()
        password = self.passwordInput.text()
        user = self.manager.authenticate_user(email, password)
        if user:
            self.current_user = user
            self.accept()
        else:
            QtWidgets.QMessageBox.warning(self, 'Error', 'Credenciales incorrectas')

    def open_register_dialog(self):
        dialog = RegisterApp(self)
        dialog.exec_()
