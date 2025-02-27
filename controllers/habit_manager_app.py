from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QGraphicsDropShadowEffect
from PyQt5.QtGui import QColor
from view.splash_screen import SplashScreenUI
from view.habit_manager import HabitManagerUI
from controllers.edit_habit_dialog import EditHabitDialog
from models.habit_manager import HabitManager
from .login import LoginApp
import UI.bg_rc  # Importar el archivo de recursos compilado
from PyQt5.QtWidgets import QListWidgetItem, QWidget, QGridLayout, QLabel, QSpacerItem, QSizePolicy

class SplashScreenApp(SplashScreenUI):
    def __init__(self, parent=None):
        super(SplashScreenApp, self).__init__(parent)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.progress)
        self.timer.start(30)
        self.counter = 0
        self.add_shadow_to_progress_bar()
        self.manager = HabitManager()  # Inicializar el atributo manager
        self.show()


    def add_shadow_to_progress_bar(self):
        shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(32.6)
        shadow.setXOffset(4)
        shadow.setYOffset(-4)
        shadow.setColor(QtGui.QColor(0, 0, 0, 64))
        self.progressBar.setGraphicsEffect(shadow)

    def progress(self):
        self.counter += 1
        self.progressBar.setValue(self.counter)
        if self.counter >= 100:
            self.timer.stop()
            user = self.manager.load_session()
            if user:
                self.main = HabitManagerApp(user)
                self.main.show()
            else:
                self.login = LoginApp()
                if self.login.exec_() == QtWidgets.QDialog.Accepted:
                    self.main = HabitManagerApp(self.login.current_user)
                    self.main.show()
            self.close()

    
class HabitManagerApp(HabitManagerUI):
    def __init__(self, user):
        super().__init__()
        self.manager = HabitManager()
        self.user = user

        self.addHabitButton.clicked.connect(self.open_add_habit_dialog)
        self.updateHabitButton.clicked.connect(self.open_edit_habit_dialog)
        self.deleteHabitButton.clicked.connect(self.confirm_delete_habit)
        self.logoutButton.clicked.connect(self.logout)
        self.habitListWidget.itemClicked.connect(self.display_habit_details)

        self.update_habit_list()
        self.habitListWidget.viewport().installEventFilter(self)

        self.userLabel.setText(self.user.nombre)

        self.rightLayoutWidget = self.findChild(QtWidgets.QWidget, "rightSidebarContainer")
        if self.rightLayoutWidget:
            self.rightLayoutWidget.setVisible(False)
            self.apply_shadow_effect(self.rightLayoutWidget)

        
    
    def apply_shadow_effect(self, widget):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(30)
        shadow.setXOffset(-3)
        shadow.setYOffset(0)
        shadow.setColor(QColor(0, 0, 0, 100))  # Color negro con opacidad
        widget.setGraphicsEffect(shadow)

    

    def open_add_habit_dialog(self):
        dialog = EditHabitDialog(parent=self)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            id_usuario = self.user.id_usuario  # Asegurarse de usar el ID del usuario en sesión actual
            nombre, descripcion, frecuencia, hora_inicio, hora_fin = dialog.get_habit_data()
            self.manager.add_habit(id_usuario, nombre, descripcion, frecuencia, hora_inicio, hora_fin)
            self.update_habit_list()

    def open_edit_habit_dialog(self):
        habit_name = self.habitTitleLabel.text()
        habit = next((habit for habit in self.manager.habits if habit.nombre == habit_name), None)

        if habit:
            dialog = EditHabitDialog(habit, self)
            if dialog.exec_() == QtWidgets.QDialog.Accepted:
                nombre, descripcion, frecuencia, hora_inicio, hora_fin = dialog.get_habit_data()

                # Actualizar en la base de datos
                self.manager.update_habit(habit.id_habito, habit.id_usuario, nombre, descripcion, frecuencia, hora_inicio, hora_fin)
                
                # Refrescar la lista de hábitos en la UI
                self.update_habit_list()

                # Esperar brevemente para que la UI se actualice completamente
                QtWidgets.QApplication.processEvents()

                # Buscar el hábito en la lista actualizada
                items = self.habitListWidget.findItems(nombre, QtCore.Qt.MatchExactly)

                if items:  # Si el hábito fue encontrado en la UI, mostrarlo
                    self.display_habit_details(items[0])
                else:
                    print(f"⚠️ No se encontró el hábito '{nombre}' en la lista después de actualizar.")


    def confirm_delete_habit(self):
        habit_name = self.habitTitleLabel.text()  # Usar habitTitleLabel en lugar de habitDetailsLabel
        habit = next((habit for habit in self.manager.habits if habit.nombre == habit_name), None)
        if habit:
            reply = QtWidgets.QMessageBox.question(self, 'Confirmar Eliminación', f"¿Estás seguro de que deseas eliminar el hábito '{habit.nombre}'?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
            if reply == QtWidgets.QMessageBox.Yes:
                self.manager.delete_habit(habit.id_habito)
                self.update_habit_list()
                if self.rightLayoutWidget:
                    self.rightLayoutWidget.setVisible(False)  # Ocultar el widget que contiene la barra lateral derecha después de eliminar un hábito

    def update_habit_list(self):
        self.habitListWidget.clear()
        self.manager.show_habits(self.user.id_usuario)
        colors = ["#573353", "#FC9D45", "#F65B4E", "#29319F"]
        for index, habit in enumerate(self.manager.habits):
            item_widget = QWidget()
            layout = QGridLayout(item_widget)
            
            icon_label = QLabel()
            icon_label.setFixedSize(56, 56)
            color = colors[index % len(colors)]
            icon_label.setStyleSheet(f"background-color: {color}; border-radius: 9px;")
            
            text_label = QLabel(habit.nombre)
            text_label.setStyleSheet("font-size: 14px; font-family: 'Microsoft YaHei';")
            
            spacer = QSpacerItem(40, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
            
            layout.addWidget(icon_label, 1, 0)
            layout.addItem(spacer, 1, 1)
            layout.addWidget(text_label, 1, 2)
            
            item = QListWidgetItem(self.habitListWidget)
            item.setSizeHint(item_widget.sizeHint())
            self.habitListWidget.addItem(item)
            self.habitListWidget.setItemWidget(item, item_widget)

    def display_habit_details(self, item):
        if item is None:
            print("Error: Se hizo clic en un elemento vacío de la lista.")
            return

        widget = self.habitListWidget.itemWidget(item)
        if widget is None:
            print("Error: No se encontró el widget del item seleccionado.")
            return

        labels = widget.findChildren(QLabel)  # Buscar todos los QLabel dentro del widget
        print("Labels encontrados:", [label.text() for label in labels])

        habit_label = next((label for label in labels if label.text().strip()), None)
        if habit_label is None:
            print("Error: No se encontró QLabel con texto dentro del item seleccionado.")
            return

        habit_name = habit_label.text().strip()
        print(f"Clicked on habit: {habit_name}")
        print("Lista de hábitos disponibles:", [habit.nombre for habit in self.manager.habits])

        habit = next((habit for habit in self.manager.habits if habit.nombre == habit_name), None)
        if habit is None:
            print("Error: No se encontró el hábito en la lista.")
            return

        print(f"Frecuencia en base de datos: {habit.frecuencia}")

        frecuencia = ', '.join(self.manager.convert_frecuencia_to_days(habit.frecuencia))
        print(f"Frecuencia convertida: {frecuencia}")

        self.habitTitleLabel.setText(habit.nombre)
        self.habitDescriptionLabel.setText(habit.descripcion)
        self.habitFrequencyLabel.setText(frecuencia)  # Verifica que aquí se asigna correctamente
        self.habitTimeLabel.setText(f"{habit.hora_inicio} - {habit.hora_fin}")
        self.streakDaysLabel.setText("15 días")

        if self.rightLayoutWidget:
            self.rightLayoutWidget.setVisible(True)
            print("Sidebar mostrado")





    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.MouseButtonPress and source is self.habitListWidget.viewport():
            item = self.habitListWidget.itemAt(event.pos())
            if item is None and self.rightLayoutWidget:
                self.rightLayoutWidget.setVisible(False)  # Ocultar el widget que contiene la barra lateral derecha si se hace clic fuera de un hábito
        return super().eventFilter(source, event)

    def logout(self):
        self.manager.current_user = None
        self.manager.clear_session()
        self.close()
        self.login = LoginApp()
        if self.login.exec_() == QtWidgets.QDialog.Accepted:
            self.__init__(self.login.current_user)
            self.show()
        else:
            QtWidgets.QApplication.quit()