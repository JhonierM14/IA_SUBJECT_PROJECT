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
        """Busca la posicion del astronauta en el mapa y la añade al objeto creado invocador"""
        for i in range(10):
            for j in range(10):
                if self.mapa[i][j] == 2:
                    self.posicionActual = (i, j)

    def esMeta(self):
        """verifica si ya se llego a la meta"""
        if self.muestras == 3:
            return True
        else: False

    def yaPasePorAqui(self, nodoPadre, nuevaPosicionAstronauta) -> tuple[bool, object]:
        """
        Verifica si el astronauta ya paso por la casilla, si el nodo padre actual es none
        retorna (False, none), si el nodo padre actual tiene la misma posicion que la nueva
        posicion del astronauta se retorna (True, nodoPadre), para el resto de casos sigue
        buscando recursivamente

        Args
        - nodoPadre (searchTree): nodo padre
        - nuevaPosicionAstronauta (tupla): nueva posicion del astronauta

        Return 
        - el primer argumento representa si ya se paso o no por la casilla, el segundo argumento el nodo con la misma posicion (tuple[bool, object])
        """
        if nodoPadre == None:
            return (False, nodoPadre)
        elif nodoPadre.posicionActual == nuevaPosicionAstronauta:
            return (True, nodoPadre)
        else:
            return self.yaPasePorAqui(nodoPadre.nodoPadre, nuevaPosicionAstronauta)
        
    def esMismoEstado(self, head, nodoCola) -> bool:
        """
        Si se pasa por una casilla en la cual ya se estubo y el estado es igual para ambos
        nodos se retorna True y la rama muere, en caso contraria sigue expandiendo.

        Args
        - head (searchTree): nodo padre
        - nodoCola (searchTree): nodo encontrado con el que se compara el estado

        Return
        - Representa si es igual o no el estado de los nodos (bool)
        """
        if head.tieneNave == nodoCola.tieneNave and head.muestras==nodoCola.muestras:
            return True
        else: 
            return False # Si se retorna False, se crea el hijo
        
    def puedoMoverme(self, direccion: str, posicionAstronauta: tuple) -> bool:
        """
        Verifica si un astronauta puede moverse en una direccion

        Args
        - direccion (str): direccion a la que estoy verificando si puedo moverme
        - posicionAstronauta (tupla): la posicion actual del astronauta

        Return
        - Represeta si se puede desplazar el astronauta en la direccion (bool)
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

    def printMapa(self) -> None:
        """
        Imprime el mapa actual del nodo
        """
        for i in range(10):
            line = ""
            for j in range(10):
                if j==0:
                    line += (f"| {self.mapa[i][j]} |")
                else:
                    line += (f" {self.mapa[i][j]} |")
            print(line)
        print("-------------------------------------------------\n")

    def imprimirPosicionHijos(self) -> None:
        """Imprime la posicion de los hijos"""
        hijos = ""
        for i in range(len(self.hijos)):
            x, y = self.hijos[i].posicionActual
            hijos += f"hijo {i + 1}: " + "(" + str(x) + ", " + str(y) + ")" + " | "
        print(hijos)

    def imprimirInformacion(self) -> None:
        """Imprime la informacion del nodo"""
        if self.nodoPadre == None:
            print(f"posicion: {self.posicionActual}, muestras: {self.muestras}, energiaTotal: {self.energiaTotalGastada}, tieneNave: {self.tieneNave}, movimientosNave: {self.movimientosNave}, operadorRealizado: {self.operadorRealizado}, \nhijos:{self.hijos}, nodoPadre: {self.nodoPadre}")
        else:
            print(f"posicion: {self.posicionActual}, muestras: {self.muestras}, energiaTotal: {self.energiaTotalGastada}, tieneNave: {self.tieneNave}, movimientosNave: {self.movimientosNave}, operadorRealizado: {self.operadorRealizado}, \nhijos:{self.hijos}, nodoPadre: {self.nodoPadre.posicionActual}")