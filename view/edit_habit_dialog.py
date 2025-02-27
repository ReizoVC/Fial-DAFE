from PyQt5 import QtWidgets, uic

class EditHabitDialogUI(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(EditHabitDialogUI, self).__init__(parent)
        uic.loadUi('UI/edit_habit_dialog.ui', self)
