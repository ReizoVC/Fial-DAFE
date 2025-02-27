class Habit:
    def __init__(self, id_habito, id_usuario, nombre, descripcion, frecuencia, hora_inicio, hora_fin):
        self.id_habito = id_habito
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.descripcion = descripcion
        self.frecuencia = frecuencia
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin

    def __str__(self):
        return f"Hábito: {self.nombre}, Descripción: {self.descripcion}, Frecuencia: {self.frecuencia}, Hora de inicio: {self.hora_inicio}, Hora de fin: {self.hora_fin}"