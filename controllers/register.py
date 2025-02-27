from PyQt5 import QtWidgets
from view.register_ui import RegisterUI
from models.habit_manager import HabitManager

class RegisterApp(RegisterUI):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.manager = HabitManager()
        self.registerButton.clicked.connect(self.register)
        self.new_user = None

    def register(self):
        nombre = self.nameInput.text()
        email = self.emailInput.text()
        password = self.passwordInput.text()
        self.manager.add_user(nombre, email, password)
        self.new_user = self.manager.authenticate_user(email, password)
        self.accept()
