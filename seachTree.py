import time

class searchTree:
    def __init__(self, mapa: list[list], posicionActual: tuple = (0, 0), muestras: int = 0, energiaTotalGastada: float = 0, tieneNave: bool = False, movimientosNave: int = 20, operadorRealizado: str = None, hijos: list = list(), nodoPadre = None):
        self.mapa = mapa
        self.posicionActual = posicionActual
        self.muestras = muestras
        self.energiaTotalGastada = energiaTotalGastada
        self.tieneNave = tieneNave
        self.movimientosNave = movimientosNave
        self.operadorRealizado = operadorRealizado
        self.hijos = hijos
        self.nodoPadre = nodoPadre

    def posicionAstronauta(self):
        for i in range(10):
            for j in range(10):
                if self.mapa[i][j] == 2:
                    self.posicionActual = (i, j)

    def esMeta(self):
        if self.muestras == 3:
            return True
        else: False

    def yaPasePorAqui(self, nodoPadre, nuevaPosicionAstronauta) -> tuple[bool, object]:
        """
        Verifica si el astronauta ya paso por la casilla
        """
        if nodoPadre == None:
            return (False, nodoPadre)
        elif nodoPadre.posicionActual == nuevaPosicionAstronauta:
            return (True, nodoPadre)
        else:
            return self.yaPasePorAqui(nodoPadre.nodoPadre, nuevaPosicionAstronauta)
        
    def esMismoEstado(self, head, nodoCola):
        if head.tieneNave == nodoCola.tieneNave and head.muestras==nodoCola.muestras:
            return True
        else: 
            return False # Si se retorna False, se crea el hijo
        
    def puedoMoverme(self, direccion: str, posicionAstronauta: tuple) -> bool:
        """
        Verifica si un astronauta puede moverse en una direccion
        """
        x, y = posicionAstronauta

        if direccion=="up" and x >= 1:
            if self.mapa[x-1][y] == 1:
                return False
            else: return True
        elif direccion=="left" and y>= 1:
            if self.mapa[x][y - 1] == 1:
                return False
            else: return True
        elif direccion=="down" and x<=8:
            if self.mapa[x + 1][y] == 1:
                return False
            else: return True
        elif direccion=="right" and y <=8:
            if self.mapa[x][y + 1] == 1:
                return False
            else: return True
        else:
            return False

    def añadirHijo(self, hijo):
        self.hijos.append(hijo)


    def printMapa(self):
        """
        Imprime el mapa
        """
        for i in range(10):
            line = ""
            for j in range(10):
                if j==0:
                    line += (f"| {self.mapa[i][j]} |")
                else:
                    line += (f" {self.mapa[i][j]} |")
            #print(line)
        #print("-------------------------------------------------\n")

    def imprimirPosicionHijos(self):
        hijos = ""
        for i in range(len(self.hijos)):
            x, y = self.hijos[i].posicionActual
            hijos += f"hijo {i + 1}: " + "(" + str(x) + ", " + str(y) + ")" + " | "
        #print(hijos)

    def imprimirInformacion(self):
        if self.nodoPadre == None:
            print(f"posicion: {self.posicionActual}, muestras: {self.muestras}, energiaTotal: {self.energiaTotalGastada}, tieneNave: {self.tieneNave}, movimientosNave: {self.movimientosNave}, operadorRealizado: {self.operadorRealizado}, \nhijos:{self.hijos}, nodoPadre: {self.nodoPadre}")
        else:
            print(f"posicion: {self.posicionActual}, muestras: {self.muestras}, energiaTotal: {self.energiaTotalGastada}, tieneNave: {self.tieneNave}, movimientosNave: {self.movimientosNave}, operadorRealizado: {self.operadorRealizado}, \nhijos:{self.hijos}, nodoPadre: {self.nodoPadre.posicionActual}")