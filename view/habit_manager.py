from PyQt5 import QtWidgets, uic

class HabitManagerUI(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(HabitManagerUI, self).__init__(parent)
        uic.loadUi('UI/habit_manager.ui', self)
