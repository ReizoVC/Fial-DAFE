class Progreso:
    def __init__(self, id_progreso, id_habito, racha):
        self.id_progreso = id_progreso
        self.id_habito = id_habito
        self.racha = racha

    def __str__(self):
        return f"Progreso: Hábito ID {self.id_habito}, Racha: {self.racha}"
