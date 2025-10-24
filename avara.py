from collections import deque
from objeto import Objeto
from seachTree import searchTree
import time
import copy
from utils import Mapa

def SOLUCION(head: searchTree, solucion: list) -> None:
    """
    Añade recursivamente los operadores realizados
    desde el ultimo de una rama, hasta el nodo 
    raiz o nodo padre del arbol
    
    Args
    - head (searchTree): ultimo nodo generado en la solucion
    - solucion (list): lista donde se guardaran los operadores
    """    
    if head.nodoPadre != None:
        solucion.append(head.operadorRealizado)
        SOLUCION(head.nodoPadre, solucion)
    else:
        pass

def yaPasePorAqui(nodoPadre, nuevaPosicionAstronauta) -> tuple[bool, object]:
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
        return yaPasePorAqui(nodoPadre.nodoPadre, nuevaPosicionAstronauta)

def esMismoEstado(nodo, nodoCola) -> bool:
    """
    Si se pasa por una casilla en la cual ya se estubo y el estado es igual para ambos
    nodos se retorna True y la rama muere, en caso contraria sigue expandiendo.

    Args
    - nodo (searchTree): nodo padre
    - nodoCola (searchTree): nodo encontrado con el que se compara el estado

    Return
    - Representa si es igual o no el estado de los nodos (bool)
    """
    if nodo.tieneNave == nodoCola.tieneNave and nodo.muestras==nodoCola.muestras:
        return True
    else: 
        return False # Si se retorna False, se crea el hijo
    

def nuevaPosicion(posicionActual: tuple, direccion: str) -> tuple:
    """
    Retorna una tupla con la posicion actual del astronauta
    más la direccion de movimiento

    Args 
    - posicionActual (tupla): posicion actual del astronauta, ej:. (a, b)
    - direccion (str): up | left | down | right
    """
    x, y = posicionActual
    if direccion == "up": return (x - 1, y)
    if direccion == "left": return (x, y - 1)
    if direccion == "down": return (x + 1, y)
    if direccion == "right": return (x, y + 1)


def calcularHeuristica(listaObjetos: list[Objeto], nodo: searchTree, posicion: tuple) -> int:
    """
    Distancia Manhattan hasta la muestra más cercana en el mapa a la posicion actual del astronauta, divido 2,
    ya que el astronauta puede tomar una nave, por lo que la heuristica debe ser menor a ese caso.
    
    Si ya juntó 3 muestras, la heurística vale 0.
    """
    if nodo.muestras >= 3:
        return 0

    x0, y0 = posicion
    mejor = None
    for i in range(len(listaObjetos)):
            objeto: Objeto = listaObjetos[i]
            if objeto.id == 6 and objeto.recogido == False:
                d = (abs(x0 - objeto.posicion[0]) + abs(y0 - objeto.posicion[1]))/2
                if mejor is None or d < mejor:
                    mejor = d

    if mejor is None:
        # no hay muestras visibles, heurística neutra
        return 0
    return mejor


def actualizarMapa(listaObjetos: list[Objeto], head: searchTree, nuevaPosicionAstronauta: tuple) -> list[list]:
        """
        Copia el mapa del nodo padre, luego modifica la casilla 
        donde estaba el astronauta por una casilla libre, despues  
        inserta los obtaculos y objetos en el mapa, y para terminar
        añade la nueva posicion del astronauta al mapa

        Args
        - listaObjetos (list[Objeto]): lista de objetos en el mapa
        - head (searchTree): nodo padre
        - nuevaPosicionAstronauta (tupla): coordenada de la nueva posicion del astronauta ej:. (a, b)

        Return
        - Mapa actualizado (list[list])
        """

        newMapa = copy.deepcopy(head.mapa)

        a, b = head.posicionActual # La posicion anterior del astronauta se cambia por un camino libre
        x, y = nuevaPosicionAstronauta # La nueva posicion del astronauta

        newMapa[a][b] = 0

        # Si el astronauta paso por un objeto, se vuelven a colocar 
        # los objetos en el mapa al moverse el astronauta

        # posicionNave = (0, 0)

        for i in range(len(listaObjetos)):
            objeto: Objeto = listaObjetos[i]
            if objeto.id != 5 and (objeto.recogido == False or objeto.recogido == None): # id 5 es la nave
                newMapa[objeto.posicion[0]][objeto.posicion[1]] = objeto.id
            elif objeto.id == 5: # Si el objeto es la nave
                if head.tieneNave == False and head.movimientosNave == 20 and newMapa[x][y] != objeto.id:
                    newMapa[x][y] = 2 # el astronauta navega por el mapa sin estar cerca a la nave
                elif head.tieneNave == False and head.movimientosNave == 20 and newMapa[x][y] == objeto.id: # Si el astronauta no tiene nave, hay dos opciones, la nave esta en la posicion inicial o el astronauta ya la utilizo y la dejo en otra posicion del mapa
                    newMapa[x][y] = 5 # ya esta la nave en la casilla en la que me voy a mover
                elif head.tieneNave == True and head.movimientosNave == 20 and newMapa[x][y] != objeto.id:
                    newMapa[x][y] = 5 # el astronauta llega a la nave
                elif head.tieneNave == True and head.movimientosNave >= 1: # Si el astronauta tiene nave, y movimientos se mueve con el astronauta
                    objeto.posicion = x, y
                    newMapa[objeto.posicion[0]][objeto.posicion[1]] = 5
                elif head.tieneNave == True and head.movimientosNave == 0: # Si el astronauta tiene nave, y cero movimientos la nave muere
                    objeto.posicion = a, b # como no puede avanzar mas se queda en el pasado
                    newMapa[objeto.posicion[0]][objeto.posicion[1]] = 5
                    newMapa[x][y] = 2
                elif head.tieneNave == False and head.movimientosNave == 0: # Si el astronauta no tiene nave, ni movimientos, se inserta en la ultima posicion guardada
                    newMapa[objeto.posicion[0]][objeto.posicion[1]]= objeto.id
                    newMapa[x][y] = 2
            

        return newMapa

def cantidadMuestrasCientificas(listaObjetos: list[Objeto], head: searchTree, posicion: tuple) -> int:
    """
    Dada una nueva posicion a la que se va a mover el astronauta
    Si en esa posicion hay una muestra cientifica, se modifica
    la lista de objetos, para cambiar el atributo de la muestra cientifica
    por recogida, y luego se aumenta el contador de muestras cientificas
    en 1

    Args
    - listaObjetos (list[Objeto]): lista de objetos en el mapa
    - head (searchTree): nodo padre
    - posicion (tupla): nueva posicion a la que se movera el astronauta

    Return
    - cantidad de muestras cientificas (int)
    """
    x, y = posicion
    if head.mapa[x][y] == 6:
        for i in range(len(listaObjetos)):
            if listaObjetos[i].posicion == (x, y):
                listaObjetos[i].recogido = True

        return head.muestras + 1
    else: 
        return head.muestras

def totalEnergia(head: searchTree, posicion: tuple, tieneNave: bool) -> float:
    """
    Se le agregaron los costos segun el terreno, 3 para rocoso y 5 para volcanico, 
    tambien se agrego el bool tieneNave de la funcion crearHijo, ya que si se extrae el atributo "tieneNave"
    de head, este nos daria la informacion del nodo padre, la cual podria ser diferente a la del hijo que se esta creando.
    """
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
    """
    Verifica si en la nueva posicion se encuentra la nave, en caso 
    de que este la nave, se cambia el atributo a True, en caso
    contrario a False. 

    Args
    - head (searchTree): nodo padre
    - posicion (tupla): nueva posicion del astronauta

    Return
    - (bool)
    """
    x, y = posicion
    if head.tieneNave==True and head.movimientosNave>=1:
        return True
    elif head.tieneNave==False and head.mapa[x][y] == 5: 
        return True
    else:
        return False

def movimientosRestantesNave(head: searchTree, tieneNave: bool) -> int:
    if tieneNave == True and head.movimientosNave > 0:
        return head.movimientosNave - 1
    else:
        return head.movimientosNave

def crearHijo(nodo: searchTree, direccion: str, nuevaPosicionAstronauta: tuple) -> None:

    posicion = nuevaPosicionAstronauta 
    listaObjetos = copy.deepcopy(nodo.listaObjetos)
    muestras = cantidadMuestrasCientificas(listaObjetos, nodo, posicion)
    newMapa = actualizarMapa(listaObjetos, nodo, posicion)
    tieneNave = nosMontamosEnNave(nodo, posicion)
    movimientosNave = movimientosRestantesNave(nodo, tieneNave)
    energiaGastada = totalEnergia(nodo, posicion, tieneNave)
    #A diferencia del costoUniforme, aqui se debe calcular la heuristica para cada nodo
    heuristica= calcularHeuristica(nodo.listaObjetos, nodo, posicion)
    
    hijo = searchTree(newMapa, posicion, muestras, energiaGastada, tieneNave, movimientosNave, 
                      operadorRealizado=direccion, hijos=list(), nodoPadre=nodo, listaObjetos=listaObjetos, heuristica=heuristica)
    nodo.añadirHijo(hijo)


def traerHijos(nodo: searchTree, direcciones: dict) -> None: 
    for i in range(1, len(direcciones) + 1):
        posicionAstronauta: tuple = nodo.posicionActual
        if nodo.puedoMoverme(direcciones[i], posicionAstronauta):
            nuevaPosicionAstronauta = nuevaPosicion(nodo.posicionActual, direcciones[i])
            bool, nodoSimilar = yaPasePorAqui(nodo, nuevaPosicionAstronauta)
            if bool:
                if esMismoEstado(nodo, nodoSimilar): 
                    pass
                else:
                    crearHijo(nodo, direcciones[i], nuevaPosicionAstronauta)
            else:
                crearHijo(nodo, direcciones[i], nuevaPosicionAstronauta)

def meterHijosEnlistaEntrada(lista: list, hijos: list):
  for i in range(len(hijos)):  
    lista.append(hijos[i])

def meterNodoListaSalida(lista: list, nodo):
   lista.append(nodo)

def menorHeuristica(lista: list) -> searchTree:
    """
    Busca el nodo con menor heuristica
    en la lista de entrada, lo elimina de la lista
    y lo retorna

    Args
    - cola (list): lista de nodos

    Return
    - nodo con menor energia (searchTree)
    """
    menor = float('inf')
    for i in range(len(lista)):
        if lista[i].getHeuristica() < menor:
            menor = lista[i].getHeuristica()
            indice = i
    return lista.pop(indice)

def expandir(nodo: searchTree, direcciones: dict):
    """
    Busca los hijos de un nodo, 
    luego verifica si un nodo es una meta, 
    si no es meta ingresa los hijos en la cola de entrada, 
    y para terminar saca el nodo actual y lo mete a la cola de salida
    """
    traerHijos(nodo, direcciones) # expandir
    if nodo.esMeta():
        nodoSolucion.append(nodo)
        SOLUCION(nodo, solucion)
        salirBucle()
    else: 
        meterHijosEnlistaEntrada(listaEntrada, nodo.hijos)
        meterNodoListaSalida(listaSalida, nodo)

def salirBucle():
    """Llave de salida del bucle"""
    global key
    key = False

def resolver_avara(Mapa: list[list]) -> list:
    raiz = searchTree(Mapa)
    raiz.posicionAstronauta()
    raiz.posicionObjetos()
    listaEntrada.append(raiz)

    while key:
        menorNodo: searchTree = menorHeuristica(listaEntrada)
        expandir(menorNodo, direcciones)

    if key==False:
        solucion.reverse()
        return solucion

listaEntrada = list()
listaSalida = list()

direcciones = {1: "up", 2: "left", 3: "down", 4: "right"}

nodoSolucion: list = []
solucion = []

key = True

