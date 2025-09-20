from collections import deque
import time

class searchTree:
    def __init__(self, mapa: list[list], posicionActual: tuple, muestras: int = 0, energiaTotalGastada: float = 0, tieneNave: bool = False, movimientosNave: int = 20, operadorRealizado: str = None, hijos: list = list(), nodoPadre = None):
        self.mapa = mapa
        self.posicionActual = posicionActual
        self.muestras = muestras
        self.energiaTotalGastada = energiaTotalGastada
        self.tieneNave = tieneNave
        self.movimientosNave = movimientosNave
        self.operadorRealizado = operadorRealizado
        self.hijos = hijos
        self.nodoPadre = nodoPadre

    def esMeta(self):
        if self.muestras == 3:
            return True
        else: False

    def yaPasePorAqui(self, head, auxHead) -> tuple[bool, object]:
        if auxHead.nodoPadre == None: 
            return (False, None)
        else:
            nP = auxHead.nodoPadre
            if head.posicionActual==nP.posicionActual:
                return (True, nP)
            else:
                return self.yaPasePorAqui(head, nP)
        
    def esMismoEstado(self, head, nodoCola):
        if head.tieneNave == nodoCola.tieneNave and head.muestras==nodoCola.muestras:
            return True
        else: 
            return False
        
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
            print(line)
        print("-------------------------------------------------\n")

def nuevaPosicion(posicionActual: tuple, direccion: str):
    """
    Retorna una tupla con la nueva posicion del astronauta añadida la direccion pasada como parametro
    """
    x, y = posicionActual
    if direccion == "up": return (x - 1, y)
    if direccion == "left": return (x, y - 1)
    if direccion == "down": return (x + 1, y)
    if direccion == "right": return (x, y + 1)

def actualizarMapa(head: searchTree, nuevaPosicionAstronauta: tuple):
        newMapa = head.mapa.copy()

        a, b = head.posicionActual # La posicion anterior del astronauta se cambia por un camino libre
        newMapa[a][b] = 0

        for i in range(len(listaObstaculos)):
            x, y, z = listaObstaculos[i]
            newMapa[x][y]= z

        x, y = nuevaPosicionAstronauta 
        newMapa[x][y] = 2

        return newMapa

def traerHijos(head: searchTree, direcciones: dict): 
    """
    Busca las casillas a las que el astronauta   
    puede moverser y las añade como hijos de un
    nodo, los hijos ya tienen el movimiento y
    posicion realizada.
    """
    for i in range(1, len(direcciones) + 1):
        posicionAstronauta: tuple = head.posicionActual
        if head.puedoMoverme(direcciones[i], posicionAstronauta):
            nuevaPosicionAstronauta: tuple = nuevaPosicion(head.posicionActual, direcciones[i])
            newMapa = actualizarMapa(head, nuevaPosicionAstronauta)
            
            muestras = 0
            energiaGastada = head.energiaTotalGastada + 1
            posicion = nuevaPosicionAstronauta
            tieneNave = False
            movimientosNave = 20
            hijo = searchTree(newMapa, posicion, muestras, energiaGastada, tieneNave, movimientosNave, operadorRealizado=direcciones[i], nodoPadre=head)
            print(head.puedoMoverme(direcciones[i], posicionAstronauta), hijo.posicionActual)
            head.añadirHijo(hijo)

key = True

Mapa = [
            [0, 5, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 0, 1, 1, 1, 0, 1, 0],
            [0, 2, 0, 0, 3, 3, 3, 6, 0, 0],
            [0, 1, 0, 1, 1, 1, 1, 0, 1, 1],
            [0, 1, 0, 1, 0, 0, 0, 0, 1, 1],
            [0, 1, 0, 1, 4, 1, 1, 1, 1, 1],
            [0, 0, 6, 4, 4, 0, 0, 1, 1, 1],
            [1, 0, 1, 1, 0, 1, 0, 1, 0, 6],
            [0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
            [0, 1, 1, 1, 0, 0, 0, 0, 0, 1]
        ]

def posicionObjectos():
    lista = list()
    for i in range(10):
        for j in range(10):
            if Mapa[i][j] == 3 or Mapa[i][j] == 4:
                lista.append((i , j, Mapa[i][j]))
    return lista

listaObstaculos = posicionObjectos()

Tree = searchTree(Mapa, (2,1))

colaEntrada = deque()
colaSalida = deque()

direcciones = {1: "up", 2: "left", 3: "down", 4: "right"}

colaEntrada.append(Tree)

def meterHijosEnColaEntrada(cola: deque, hijos: list):
  for i in range(len(hijos)):  
    cola.append(hijos[i])

def meterNodoColaSalida(cola: deque, nodo):
   cola.append(nodo)

def expandir(nodo: searchTree):
    traerHijos(nodo, direcciones) # expandir
    if nodo.esMeta(): 
        print("llegue a la meta"); 
        salirBucle()
    else: 
        meterHijosEnColaEntrada(colaEntrada, nodo.hijos)
        meterNodoColaSalida(colaSalida, nodo)

def salirBucle():
    global key
    key = False

while key:
  primerElemento: searchTree = colaEntrada.popleft()
  a, b = Tree.yaPasePorAqui(primerElemento, primerElemento)
  if a:
    if Tree.esMismoEstado(primerElemento, b):
       pass
    else:  
       expandir(primerElemento)
  else:
    expandir(primerElemento)

