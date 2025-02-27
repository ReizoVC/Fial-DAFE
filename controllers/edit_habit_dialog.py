from PyQt5 import QtWidgets, QtCore
from view.edit_habit_dialog import EditHabitDialogUI

class EditHabitDialog(EditHabitDialogUI):
    def __init__(self, habit=None, parent=None):
        super(EditHabitDialog, self).__init__(parent)
        self.habit = habit
        self.frecuenciaComboBox.addItems(["Diario", "Entre semana", "Fin de semana", "Personalizado"])
        self.frecuenciaComboBox.currentIndexChanged.connect(self.toggle_custom_days)
        if habit:
            self.habitNameInput.setText(habit.nombre)
            self.habitDescriptionInput.setText(habit.descripcion)
            self.habitStartTimeInput.setTime(QtCore.QTime.fromString(habit.hora_inicio, "HH:mm"))
            self.habitEndTimeInput.setTime(QtCore.QTime.fromString(habit.hora_fin, "HH:mm"))
            self.set_frecuencia(habit.frecuencia)
        else:
            self.frecuenciaComboBox.setCurrentText("Personalizado")
            self.daysOfWeekGroupBox.setVisible(True)
        self.saveButton.clicked.connect(self.accept)
        self.show()

    def toggle_custom_days(self, index):
        is_custom = self.frecuenciaComboBox.currentText() == "Personalizado"
        self.daysOfWeekGroupBox.setVisible(is_custom)

    def set_frecuencia(self, frecuencia):
        if frecuencia == ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']:
            self.frecuenciaComboBox.setCurrentText("Diario")
        elif frecuencia == ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes']:
            self.frecuenciaComboBox.setCurrentText("Entre semana")
        elif frecuencia == ['Sábado', 'Domingo']:
            self.frecuenciaComboBox.setCurrentText("Fin de semana")
        else:
            self.frecuenciaComboBox.setCurrentText("Personalizado")
            self.mondayCheckbox.setChecked('Lunes' in frecuencia)
            self.tuesdayCheckbox.setChecked('Martes' in frecuencia)
            self.wednesdayCheckbox.setChecked('Miércoles' in frecuencia)
            self.thursdayCheckbox.setChecked('Jueves' in frecuencia)
            self.fridayCheckbox.setChecked('Viernes' in frecuencia)
            self.saturdayCheckbox.setChecked('Sábado' in frecuencia)
            self.sundayCheckbox.setChecked('Domingo' in frecuencia)

    def get_habit_data(self):
        nombre = self.habitNameInput.text()
        descripcion = self.habitDescriptionInput.text()
        hora_inicio = self.habitStartTimeInput.time().toString("HH:mm")
        hora_fin = self.habitEndTimeInput.time().toString("HH:mm")
        frecuencia = []
        if self.frecuenciaComboBox.currentText() == "Diario":
            frecuencia = [1, 2, 3, 4, 5, 6, 7]
        elif self.frecuenciaComboBox.currentText() == "Entre semana":
            frecuencia = [1, 2, 3, 4, 5]
        elif self.frecuenciaComboBox.currentText() == "Fin de semana":
            frecuencia = [6, 7]
        else:
            if self.mondayCheckbox.isChecked():
                frecuencia.append(1)
            if self.tuesdayCheckbox.isChecked():
                frecuencia.append(2)
            if self.wednesdayCheckbox.isChecked():
                frecuencia.append(3)
            if self.thursdayCheckbox.isChecked():
                frecuencia.append(4)
            if self.fridayCheckbox.isChecked():
                frecuencia.append(5)
            if self.saturdayCheckbox.isChecked():
                frecuencia.append(6)
            if self.sundayCheckbox.isChecked():
                frecuencia.append(7)
        return nombre, descripcion, frecuencia, hora_inicio, hora_fin
