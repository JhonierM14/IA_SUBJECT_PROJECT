from collections import deque
from objeto import Objeto
from seachTree import searchTree
import time
import copy

def SOLUCION(head: searchTree, solucion: list) -> None:
    if head.nodoPadre != None:
        solucion.append(head.operadorRealizado)
        SOLUCION(head.nodoPadre, solucion)

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

def totalEnergia(head: searchTree, posicion: tuple, tieneNave: bool) -> float:
    x, y = posicion
    if tieneNave == False:
        if head.mapa[x][y] == 3:
            return head.energiaTotalGastada + 3
        elif head.mapa[x][y] == 4:
            return head.energiaTotalGastada + 5
        else:
            return head.energiaTotalGastada + 1
    else: 
        return head.energiaTotalGastada + 0.5

def nosMontamosEnNave(head: searchTree, posicion: tuple) -> bool:
    x, y = posicion
    if head.tieneNave==True and head.movimientosNave>=1:
        return True
    elif head.tieneNave==False and head.mapa[x][y] == 5: 
        return True
    else:
        return False

def movimientosRestantesNave(head: searchTree, tieneNave: bool) -> int:
    if tieneNave == True:
        return head.movimientosNave - 1
    else:
        return head.movimientosNave

def crearHijo(nodo: searchTree, direccion: str, nuevaPosicionAstronauta: tuple) -> None:
    newMapa = actualizarMapa(nodo, nuevaPosicionAstronauta)
    posicion = nuevaPosicionAstronauta
    muestras = cantidadMuestrasCientificas(nodo, posicion)
    tieneNave = nosMontamosEnNave(nodo, posicion)
    movimientosNave = movimientosRestantesNave(nodo, tieneNave)
    energiaGastada = totalEnergia(nodo, posicion, tieneNave)
    hijo = searchTree(newMapa, posicion, muestras, energiaGastada, tieneNave, movimientosNave, operadorRealizado=direccion, hijos=list(), nodoPadre=nodo)
    nodo.añadirHijo(hijo)

def traerHijos(nodo: searchTree, direcciones: dict) -> None: 
    for i in range(1, len(direcciones) + 1):
        posicionAstronauta: tuple = nodo.posicionActual
        if nodo.puedoMoverme(direcciones[i], posicionAstronauta):
            nuevaPosicionAstronauta = nuevaPosicion(nodo.posicionActual, direcciones[i])
            bool, nodoSimilar = nodo.yaPasePorAqui(nodo, nuevaPosicionAstronauta)
            if bool:
                if nodo.esMismoEstado(nodo, nodoSimilar): 
                    pass
                else:
                    crearHijo(nodo, direcciones[i], nuevaPosicionAstronauta)
            else:
                crearHijo(nodo, direcciones[i], nuevaPosicionAstronauta)

def posicionObjetos() -> None:
    lista = list()
    for i in range(10):
        for j in range(10):
            if Mapa[i][j] == 3:
                lista.append(Objeto(3, "terreno rocoso", (i, j)))
            elif Mapa[i][j] == 4:
                lista.append(Objeto(4, "terreno volcanico", (i, j)))
            elif Mapa[i][j] == 5:
                lista.append(Objeto(5, "nave", (i, j)))
            elif Mapa[i][j] == 6:
                lista.append(Objeto(6, "muestra cientifica", (i, j), False))
    return lista

def meterHijosEnlistaEntrada(lista: list, hijos: list):
    for i in range(len(hijos)):  
        lista.append(hijos[i])

def meterNodoListaSalida(lista: list, nodo):
    lista.append(nodo)

def menorEnergia(lista: list) -> searchTree:
    menor = float('inf')
    for i in range(len(lista)):
        if lista[i].getEnergiaTotalGastada() < menor:
            menor = lista[i].getEnergiaTotalGastada()
            indice = i
    return lista.pop(indice)

def expandir(nodo: searchTree, direcciones: dict):
    traerHijos(nodo, direcciones)
    if nodo.esMeta():
        nodoSolucion.append(nodo)
        SOLUCION(nodo, solucion)
        print("llegue a la meta")
        salirBucle()
    else: 
        meterHijosEnlistaEntrada(listaEntrada, nodo.hijos)
        meterNodoListaSalida(listaSalida, nodo)

def salirBucle():
    global key
    key = False

def resolver_uniforme(Mapa: list[list]) -> list:
    while key:
        menorNodo: searchTree = menorEnergia(listaEntrada)
        expandir(menorNodo, direcciones)
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

listaEntrada = list()
listaSalida = list()
listaEntrada.append(Tree)

direcciones = {1: "up", 2: "left", 3: "down", 4: "right"}

nodoSolucion: list = []
solucion = []

key = True

if __name__ == "__main__":
    start: float = time.time()
    resolver_uniforme(Mapa)
    end: float = time.time()
