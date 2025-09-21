from collections import deque
from objeto import Objeto
from seachTree import searchTree
import time
import copy

def SOLUCION(head: searchTree, solucion: list):
    """
    Añade recursivamente los operadores realizados
    desde el ultimo de una rama, hasta el nodo 
    raiz o nodo padre del arbol
    
    Args
    - head: ultimo nodo generado en la solucion
    - solucion: lista donde se guardaran los operadores
    """    
    if head.nodoPadre != None:
        solucion.append(head.operadorRealizado)
        SOLUCION(head.nodoPadre, solucion)
    else:
        pass

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
        newMapa = copy.deepcopy(head.mapa)

        a, b = head.posicionActual # La posicion anterior del astronauta se cambia por un camino libre
        newMapa[a][b] = 0

        for i in range(len(listaObjetos)):
            objeto: Objeto = listaObjetos[i]
            if objeto.recogido == False or objeto.recogido == None:
                newMapa[objeto.posicion[0]][objeto.posicion[1]]= objeto.id

        x, y = nuevaPosicionAstronauta 
        newMapa[x][y] = 2

        return newMapa

def cantidadMuestrasCientificas(head: searchTree, posicion: tuple):
    x, y = posicion
    if head.mapa[x][y] == 6:
        for i in range(len(listaObjetos)):
            if listaObjetos[i].posicion == (x, y):
                listaObjetos[i].recogido = True
                print(f"Muestra recogida en coordenada: {x, y}")

        return head.muestras + 1
    else: 
        return head.muestras

def totalEnergia(head: searchTree):
    if head.tieneNave == False: 
        return head.energiaTotalGastada + 1
    else: 
        return head.energiaTotalGastada + 0.5

def nosMontamosEnNave(head: searchTree, posicion: tuple):
    x, y = posicion
    if head.tieneNave==True and head.movimientosNave>=1:
        return True
    elif head.tieneNave==False and head.mapa[x][y] == 5: 
        return True
    else:
        return False

def movimientosRestantesNave(head: searchTree):
    if head.tieneNave == True:
        return head.movimientosNave - 1
    else:
        return head.movimientosNave

def crearHijo(nodo: searchTree, direccion: str, nuevaPosicionAstronauta: tuple):
    """
    Se crea y añade un nodo hijo al arbol de busqueda
    """

    newMapa = actualizarMapa(nodo, nuevaPosicionAstronauta)
    posicion = nuevaPosicionAstronauta
    muestras = cantidadMuestrasCientificas(nodo, nuevaPosicionAstronauta)
    print(f"cantidad de muestras cientificas recogidas: {nodo.muestras}")
    energiaGastada = totalEnergia(nodo)
    tieneNave = nosMontamosEnNave(nodo, nuevaPosicionAstronauta)
    movimientosNave = movimientosRestantesNave(nodo)

    hijo = searchTree(newMapa, posicion, muestras, energiaGastada, tieneNave, movimientosNave, operadorRealizado=direccion, hijos=list(), nodoPadre=nodo)
    nodo.añadirHijo(hijo)

def traerHijos(nodo: searchTree, direcciones: dict): 
    """
    Busca las casillas a las que el astronauta   
    puede moverser, luego verifica si en el pasado ya paso por la casilla,
    si ya paso y el estado del nodo hijo es igual al padre, se detiene.
    Si sigue, crea un hijo y lo añade al nodo, 
    los hijos ya tienen el movimiento y posicion realizada.
    """
    for i in range(1, len(direcciones) + 1):
        posicionAstronauta: tuple = nodo.posicionActual

        if nodo.puedoMoverme(direcciones[i], posicionAstronauta):
            nuevaPosicionAstronauta = nuevaPosicion(nodo.posicionActual, direcciones[i])

            bool, nodoSimilar = nodo.yaPasePorAqui(nodo, nuevaPosicionAstronauta)
            print("Ya pase por aqui en mi rama?: ", bool, nodoSimilar)
            if bool:
                if nodo.esMismoEstado(nodo, nodoSimilar): 
                    print("Es mismo estado: ", nodo.esMismoEstado(nodo, nodoSimilar))
                    pass # Ya no hace nada se detiene la rama
                else: crearHijo(nodo, direcciones[i], nuevaPosicionAstronauta) # El estado no es el mismo entonces puede seguir
            else:
                crearHijo(nodo, direcciones[i], nuevaPosicionAstronauta)

def posicionObjetos():
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

def meterHijosEnColaEntrada(cola: deque, hijos: list):
  for i in range(len(hijos)):  
    cola.append(hijos[i])

def meterNodoColaSalida(cola: deque, nodo):
   cola.append(nodo)

def expandir(nodo: searchTree, direcciones: dict):
    """
    Busca los hijos de un nodo, 
    luego verifica si un nodo es una meta, 
    si no es meta ingresa los hijos en la cola de entrada, 
    y para terminar saca el nodo actual y lo mete a la cola de salida
    """
    traerHijos(nodo, direcciones) # expandir
    nodo.imprimirPosicionHijos()
    print("\n\n")
    if nodo.esMeta():
        SOLUCION(nodo, solucion)
        print("llegue a la meta"); 
        salirBucle()
    else: 
        meterHijosEnColaEntrada(colaEntrada, nodo.hijos)
        meterNodoColaSalida(colaSalida, nodo)

def salirBucle():
    """Llave de salida del bucle"""
    global key
    key = False

def resolver_amplitud(Mapa: list[list]) -> list:
    while key:
        primerElemento: searchTree = colaEntrada.popleft()
        primerElemento.printMapa()
        primerElemento.imprimirInformacion()

        expandir(primerElemento, direcciones)

    if key==False:
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

solucion = []

key = True

resolver_amplitud(Mapa)
print(solucion)

