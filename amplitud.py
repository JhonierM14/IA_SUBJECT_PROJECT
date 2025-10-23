from collections import deque
from objeto import Objeto
from seachTree import searchTree
import time
import copy

def SOLUCION(head: searchTree, solucion: list) -> None:
    if head.nodoPadre != None:
        solucion.append(head.operadorRealizado)
        SOLUCION(head.nodoPadre, solucion)

def yaPasePorAqui(nodoPadre, nuevaPosicionAstronauta) -> tuple[bool, object]:
    if nodoPadre == None:
        return (False, nodoPadre)
    elif nodoPadre.posicionActual == nuevaPosicionAstronauta:
        return (True, nodoPadre)
    else:
        return yaPasePorAqui(nodoPadre.nodoPadre, nuevaPosicionAstronauta)

def esMismoEstado(nodo, nodoCola) -> bool:
    if nodo.tieneNave == nodoCola.tieneNave and nodo.muestras == nodoCola.muestras:
        return True
    else: 
        return False

def nuevaPosicion(posicionActual: tuple, direccion: str) -> tuple:
    x, y = posicionActual
    if direccion == "up": return (x - 1, y)
    if direccion == "left": return (x, y - 1)
    if direccion == "down": return (x + 1, y)
    if direccion == "right": return (x, y + 1)

def actualizarMapa(head: searchTree, nuevaPosicionAstronauta: tuple) -> list[list]:
    newMapa = copy.deepcopy(head.mapa)
    a, b = head.posicionActual
    newMapa[a][b] = 0
    for i in range(len(listaObjetos)):
        objeto: Objeto = listaObjetos[i]
        if objeto.recogido == False or objeto.recogido == None:
            newMapa[objeto.posicion[0]][objeto.posicion[1]] = objeto.id
    x, y = nuevaPosicionAstronauta
    newMapa[x][y] = 2
    return newMapa

def cantidadMuestrasCientificas(head: searchTree, posicion: tuple) -> int:
    x, y = posicion
    if head.mapa[x][y] == 6:
        for i in range(len(listaObjetos)):
            if listaObjetos[i].posicion == (x, y):
                listaObjetos[i].recogido = True
        return head.muestras + 1
    else: 
        return head.muestras

def totalEnergia(head: searchTree) -> float:
    if head.tieneNave == False: 
        return head.energiaTotalGastada + 1
    else: 
        return head.energiaTotalGastada + 0.5

def nosMontamosEnNave(head: searchTree, posicion: tuple) -> bool:
    x, y = posicion
    if head.tieneNave == True and head.movimientosNave >= 1:
        return True
    elif head.tieneNave == False and head.mapa[x][y] == 5:
        return True
    else:
        return False

def movimientosRestantesNave(head: searchTree) -> int:
    if head.tieneNave == True:
        return head.movimientosNave - 1
    else:
        return head.movimientosNave

def crearHijo(nodo: searchTree, direccion: str, nuevaPosicionAstronauta: tuple) -> None:
    newMapa = actualizarMapa(nodo, nuevaPosicionAstronauta)
    posicion = nuevaPosicionAstronauta
    muestras = cantidadMuestrasCientificas(nodo, nuevaPosicionAstronauta)
    energiaGastada = totalEnergia(nodo)
    tieneNave = nosMontamosEnNave(nodo, nuevaPosicionAstronauta)
    movimientosNave = movimientosRestantesNave(nodo)
    hijo = searchTree(newMapa, posicion, muestras, energiaGastada, tieneNave, movimientosNave, operadorRealizado=direccion, hijos=list(), nodoPadre=nodo)
    return hijo

def traerHijos(nodo: searchTree, direcciones: dict) -> None: 
    for i in range(1, len(direcciones) + 1):
        posicionAstronauta: tuple = nodo.posicionActual
        if nodo.puedoMoverme(direcciones[i], posicionAstronauta):
            nuevaPosicionAstronauta = nuevaPosicion(nodo.posicionActual, direcciones[i])
            bool, nodoSimilar = yaPasePorAqui(nodo, nuevaPosicionAstronauta)
            hijo = crearHijo(nodo, direcciones[i], nuevaPosicionAstronauta) 
            if bool:
                if esMismoEstado(hijo, nodoSimilar): 
                    pass
                else: 
                    nodo.añadirHijo(hijo)
            else:
                nodo.añadirHijo(hijo)

def posicionObjetos() -> None:
    lista = list()
    for i in range(10):
        for j in range(10):
            if Mapa[i][j] == 3:
                lista.append(Objeto(3, "terreno rocoso", (i, j)))
            elif Mapa[i][j] == 4:
                lista.append(Objeto(4, "terreno volcanico", (i, j)))
            elif Mapa[i][j] == 5:
                lista.append(Objeto(5, "nave", (i, j), False))
            elif Mapa[i][j] == 6:
                lista.append(Objeto(6, "muestra cientifica", (i, j), False))
    return lista

def meterHijosEnColaEntrada(cola: deque, hijos: list):
    for i in range(len(hijos)):  
        cola.append(hijos[i])

def meterNodoColaSalida(cola: deque, nodo):
    cola.append(nodo)

def expandir(nodo: searchTree, direcciones: dict):
    traerHijos(nodo, direcciones)
    if nodo.esMeta():
        nodoSolucion.append(nodo)
        SOLUCION(nodo, solucion)
        print("llegue a la meta")
        salirBucle()
    else: 
        meterHijosEnColaEntrada(colaEntrada, nodo.hijos)
        meterNodoColaSalida(colaSalida, nodo)

def salirBucle():
    global key
    key = False

def resolver_amplitud(Mapa: list[list]) -> list:
    while key:
        primerElemento: searchTree = colaEntrada.popleft()
        expandir(primerElemento, direcciones)
    if key == False:
        solucion.reverse()
        return solucion

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

listaObjetos = posicionObjetos()
Tree = searchTree(Mapa)
Tree.posicionAstronauta()

colaEntrada = deque()
colaSalida = deque()
colaEntrada.append(Tree)

direcciones = {1: "up", 2: "left", 3: "down", 4: "right"}

nodoSolucion: list = []
solucion = []
key: bool = True

if __name__ == "__main__":
    start: float = time.time()
    resolver_amplitud(Mapa)
    end: float = time.time()