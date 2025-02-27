from PyQt5 import QtWidgets, uic

class SplashScreenUI(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(SplashScreenUI, self).__init__(parent)
        uic.loadUi('UI/splash_screen.ui', self)
