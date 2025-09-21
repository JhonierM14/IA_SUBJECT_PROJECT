class Objeto:
    def __init__(self, id: int, nombre: str, posicion: tuple, recogido: bool = None):
        self.id = id
        self.nombre = nombre
        self.posicion = posicion
        self.recogido = recogido