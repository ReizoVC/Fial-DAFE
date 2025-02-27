class Recordatorio:
    def __init__(self, id_recordatorio, id_usuario, id_habito, mensaje, tipo):
        self.id_recordatorio = id_recordatorio
        self.id_usuario = id_usuario
        self.id_habito = id_habito
        self.mensaje = mensaje
        self.tipo = tipo  # 'inicio' o 'fin'

    def __str__(self):
        return f"Recordatorio: Usuario ID {self.id_usuario}, Hábito ID {self.id_habito}, Mensaje: {self.mensaje}, Tipo: {self.tipo}"
