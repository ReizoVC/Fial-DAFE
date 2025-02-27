import json
from models.habit import Habit
from models.usuario import Usuario
from models.recordatorio import Recordatorio
from supabase import create_client, Client
from config import SUPABASE_URL, SUPABASE_KEY
from datetime import datetime, timedelta
from plyer import notification

class HabitManager:
    def __init__(self):
        self.habits = []
        self.users = []
        self.supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        self.current_user = None

    def add_habit(self, id_usuario, nombre, descripcion, frecuencia, hora_inicio, hora_fin):
        frecuencia_numerica = ''.join(str(day) for day in frecuencia)
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
        self.add_reminder(habit.id_usuario, habit.id_habito, f"Recuerda realizar el hábito: {habit.nombre}", 'inicio')
        self.add_reminder(habit.id_usuario, habit.id_habito, f"¿Has completado el hábito: {habit.nombre}?", 'fin')

    def add_reminder(self, id_usuario, id_habito, mensaje, tipo):
        data = {
            "id_usuario": id_usuario,
            "id_habito": id_habito,
            "mensaje": mensaje,
            "tipo": tipo
        }
        response = self.supabase.table('recordatorios').insert(data).execute()
        reminder_data = response.data[0]
        reminder = Recordatorio(
            id_recordatorio=reminder_data['id_recordatorio'],
            id_usuario=reminder_data['id_usuario'],
            id_habito=reminder_data['id_habito'],
            mensaje=reminder_data['mensaje'],
            tipo=reminder_data['tipo']
        )
        # Aquí podrías agregar el recordatorio a una lista si es necesario

    def update_habit(self, id_habito, id_usuario, nombre, descripcion, frecuencia, hora_inicio, hora_fin):
        frecuencia_numerica = ''.join(str(day) for day in frecuencia)
        data = {
            "id_usuario": id_usuario,
            "nombre": nombre,
            "descripcion": descripcion,
            "frecuencia": frecuencia_numerica,
            "hora_inicio": hora_inicio,
            "hora_fin": hora_fin
        }
        self.supabase.table('habitos').update(data).eq('id_habito', id_habito).execute()
        for habit in self.habits:
            if habit.id_habito == id_habito:
                habit.nombre = nombre
                habit.descripcion = descripcion
                habit.frecuencia = frecuencia_numerica
                habit.hora_inicio = hora_inicio
                habit.hora_fin = hora_fin
                break
        self.delete_reminders(id_habito)
        self.create_reminders(habit)

    def delete_reminders(self, id_habito):
        self.supabase.table('recordatorios').delete().eq('id_habito', id_habito).execute()

    def delete_habit(self, id_habito):
        self.supabase.table('habitos').delete().eq('id_habito', id_habito).execute()
        self.habits = [habit for habit in self.habits if habit.id_habito != id_habito]
        self.delete_reminders(id_habito)

    def show_habits(self, id_usuario):
        response = self.supabase.table('habitos').select('*').eq('id_usuario', id_usuario).execute()
        self.habits = [Habit(**habit) for habit in response.data]
        for habit in self.habits:
            habit.frecuencia = self.convert_frecuencia_to_days(habit.frecuencia)

    def convert_frecuencia_to_days(self, frecuencia):
        days_map = {
            '1': 'Lunes',
            '2': 'Martes',
            '3': 'Miércoles',
            '4': 'Jueves',
            '5': 'Viernes',
            '6': 'Sábado',
            '7': 'Domingo'
        }
        
        # Si la frecuencia ya es una lista de días, devolverla directamente
        if isinstance(frecuencia, list):
            return frecuencia
        
        # Si la frecuencia es una cadena numérica, convertirla
        return [days_map[day] for day in frecuencia if day in days_map]
    
    def add_user(self, nombre, email, contraseña):
        data = {
            "nombre": nombre,
            "email": email,
            "contraseña": contraseña
        }
        response = self.supabase.table('usuarios').insert(data).execute()
        user = Usuario(**response.data[0])
        self.users.append(user)

    def show_users(self):
        response = self.supabase.table('usuarios').select('*').execute()
        self.users = [Usuario(**user) for user in response.data]

    def authenticate_user(self, email, password):
        response = self.supabase.table('usuarios').select('*').eq('email', email).eq('contraseña', password).execute()
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
        # Aquí deberías implementar la lógica para verificar y enviar notificaciones
        # según el tipo de recordatorio y la hora actual.
        pass

    def send_notification(self, message):
        notification.notify(
            title='Recordatorio de Hábito',
            message=message,
            app_name='Proyecto Habitos',
            timeout=10
        )
