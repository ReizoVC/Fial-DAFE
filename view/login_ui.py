from PyQt5 import QtWidgets, uic

class LoginUI(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(LoginUI, self).__init__(parent)
        uic.loadUi('UI/login.ui', self)
