import json
import time
import threading
from datetime import datetime
from supabase import create_client, Client
from plyer import notification
from models.habit import Habit
from models.usuario import Usuario
from models.recordatorio import Recordatorio
from config import SUPABASE_URL, SUPABASE_KEY
import pytz

class HabitManager:
    def __init__(self):
        self.habits = []
        self.users = []
        self.supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        self.current_user = None

    def add_habit(self, id_usuario, nombre, descripcion, frecuencia, hora_inicio, hora_fin):
        frecuencia_numerica = ''.join(map(str, frecuencia))
        data = {
            "id_usuario": id_usuario,
            "nombre": nombre,
            "descripcion": descripcion,
            "frecuencia": frecuencia_numerica,
            "hora_inicio": hora_inicio,
            "hora_fin": hora_fin
        }
        response = self.supabase.table('habitos').insert(data).execute()
        habit = Habit(**response.data[0])
        self.habits.append(habit)
        self.create_reminders(habit)

    def create_reminders(self, habit):
        reminders = [
            (habit.id_usuario, habit.id_habito, f"Recuerda realizar el hábito: {habit.nombre}", 'inicio'),
            (habit.id_usuario, habit.id_habito, f"¿Has completado el hábito: {habit.nombre}?", 'fin')
        ]
        for reminder in reminders:
            self.add_reminder(*reminder)

    def add_reminder(self, id_usuario, id_habito, mensaje, tipo):
        data = {"id_usuario": id_usuario, "id_habito": id_habito, "mensaje": mensaje, "tipo": tipo}
        response = self.supabase.table('recordatorios').insert(data).execute()
        return Recordatorio(**response.data[0])

    def update_habit(self, id_habito, id_usuario, nombre, descripcion, frecuencia, hora_inicio, hora_fin):
        frecuencia_numerica = ''.join(map(str, frecuencia))
        data = {
            "id_usuario": id_usuario,
            "nombre": nombre,
            "descripcion": descripcion,
            "frecuencia": frecuencia_numerica,
            "hora_inicio": hora_inicio,
            "hora_fin": hora_fin
        }

        # Intentar actualizar en la base de datos
        response = self.supabase.table('habitos').update(data).eq('id_habito', id_habito).execute()
        
        if not response.data:
            print(f"⚠️ Error al actualizar el hábito con ID {id_habito}")
            return False  # Indica que la actualización falló

        # Buscar y actualizar el hábito en la lista local
        for habit in self.habits:
            if habit.id_habito == id_habito:
                habit.nombre = nombre
                habit.descripcion = descripcion
                habit.frecuencia = frecuencia_numerica
                habit.hora_inicio = hora_inicio
                habit.hora_fin = hora_fin
                break  # No necesitamos seguir buscando

        # Actualizar recordatorios
        self.delete_reminders(id_habito)
        self.create_reminders(Habit(id_habito, id_usuario, nombre, descripcion, frecuencia_numerica, hora_inicio, hora_fin))

        return True  # Indica que la actualización fue exitosa


    def delete_reminders(self, id_habito):
        self.supabase.table('recordatorios').delete().eq('id_habito', id_habito).execute()

    def delete_habit(self, id_habito):
        self.supabase.table('habitos').delete().eq('id_habito', id_habito).execute()
        self.habits = [habit for habit in self.habits if habit.id_habito != id_habito]
        self.delete_reminders(id_habito)

    def show_habits(self, id_usuario):
        response = self.supabase.table('habitos').select('*').eq('id_usuario', id_usuario).execute()
        self.habits = [Habit(**habit) for habit in response.data]

    def get_reminders(self, id_usuario):
        response = self.supabase.table('recordatorios').select('*').eq('id_usuario', id_usuario).execute()

        for reminder in response.data:
            reminder["hora_inicio"] = reminder["hora_inicio"][:5]  # Obtener solo HH:MM
            reminder["hora_fin"] = reminder["hora_fin"][:5]  # Obtener solo HH:MM

        return response.data if response.data else []


    def convert_frecuencia_to_days(self, frecuencia):
        days_map = {
            '1': 'Lunes', '2': 'Martes', '3': 'Miércoles',
            '4': 'Jueves', '5': 'Viernes', '6': 'Sábado', '7': 'Domingo'
        }
        return [days_map[day] for day in str(frecuencia) if day in days_map]

    def add_user(self, nombre, email, contraseña):
        data = {"nombre": nombre, "email": email, "contraseña": contraseña}
        response = self.supabase.table('usuarios').insert(data).execute()
        user = Usuario(**response.data[0])
        self.users.append(user)

    def show_users(self):
        response = self.supabase.table('usuarios').select('*').execute()
        self.users = [Usuario(**user) for user in response.data]

    def authenticate_user(self, email, password):
        response = self.supabase.table('usuarios').select('id_usuario, nombre, email, contraseña').eq('email', email).eq('contraseña', password).execute()
        if response.data:
            self.current_user = Usuario(**response.data[0])
            self.save_session()
            return self.current_user
        return None

    def save_session(self):
        if self.current_user:
            with open('session.json', 'w') as f:
                json.dump(self.current_user.__dict__, f)

    def load_session(self):
        try:
            with open('session.json', 'r') as f:
                user_data = json.load(f)
                if user_data:
                    self.current_user = Usuario(**user_data)
                    return self.current_user
        except FileNotFoundError:
            return None
        return None

    def clear_session(self):
        with open('session.json', 'w') as f:
            json.dump({}, f)

    def check_and_send_notifications(self):
        """Verifica y envía notificaciones si es la hora correcta."""
        if not self.current_user:
            return

        zona_local = pytz.timezone("America/Lima")  
        while True:
            now_utc = datetime.now(pytz.utc)  # Hora actual en UTC
            now_local = now_utc.astimezone(zona_local)  # Convertir a hora local
            hora_actual = now_local.strftime("%H:%M")  # Obtener solo HH:MM

            reminders = self.get_reminders(self.current_user.id_usuario)

            for reminder in reminders:
                habit = next((h for h in self.habits if h.id_habito == reminder['id_habito']), None)
                if habit:
                    hora_inicio = datetime.strptime(habit.hora_inicio, "%H:%M").time()
                    hora_fin = datetime.strptime(habit.hora_fin, "%H:%M").time()

                    # Comparar con la hora actual
                    if (reminder['tipo'] == "inicio" and hora_actual == habit.hora_inicio) or \
                    (reminder['tipo'] == "fin" and hora_actual == habit.hora_fin):
                        self.send_notification(reminder['mensaje'])

            time.sleep(60)

    def send_notification(self, message):
        notification.notify(
            title='Recordatorio de Hábito',
            message=message,
            app_name='Proyecto Habitos',
            timeout=10
        )
