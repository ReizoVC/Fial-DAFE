class Progreso:
    def __init__(self, id_progreso, id_habito, fecha, completado):
        self.id_progreso = id_progreso
        self.id_habito = id_habito
        self.fecha = fecha
        self.completado = completado

    def __str__(self):
        return f"Progreso: Hábito ID {self.id_habito}, Fecha: {self.fecha}, Completado: {self.completado}"
