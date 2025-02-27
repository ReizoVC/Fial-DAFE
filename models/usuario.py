class Usuario:
    def __init__(self, id_usuario, nombre, email, contraseña):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.email = email
        self.contraseña = contraseña

    def __str__(self):
        return f"Usuario: {self.nombre}, Email: {self.email}"
