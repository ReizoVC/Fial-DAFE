from PyQt5 import QtWidgets, uic

class RegisterUI(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(RegisterUI, self).__init__(parent)
        uic.loadUi('UI/register.ui', self)
