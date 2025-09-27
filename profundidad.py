
from collections import deque
from objeto import Objeto
from seachTree import searchTree
import time
import copy

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

def actualizarMapa(head: searchTree, nuevaPosicionAstronauta: tuple) -> list[list]:
        """
        Copia el mapa del nodo padre, luego modifica la casilla 
        donde estaba el astronauta por una casilla libre, despues  
        inserta los obtaculos y objetos en el mapa, y para terminar
        añade la nueva posicion del astronauta al mapa

        Args
        - head (searchTree): nodo padre
        - nuevaPosicionAstronauta (tupla): coordenada de la nueva posicion del astronauta ej:. (a, b)

        Return
        - Mapa actualizado (list[list])
        """
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

def cantidadMuestrasCientificas(head: searchTree, posicion: tuple) -> int:
    """
    Dada una nueva posicion a la que se va a mover el astronauta
    Si en esa posicion hay una muestra cientifica, se modifica
    la lista de objetos, para cambiar el atributo de la muestra cientifica
    por recogida, y luego se aumenta el contador de muestras cientificas
    en 1

    Args
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

def totalEnergia(head: searchTree) -> float:
    """
    Se verifica si el nodo padre tiene nave, en caso de que
    la tenga se aumenta en .5 la energia en caso contrario en 1 
  
    Args 
    - head (searchTree): nodo padre 

    Return 
    - cantidad total de energia gastada (float)
    """
    if head.tieneNave == False: 
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

def movimientosRestantesNave(head: searchTree) -> int:
    """
    Cuenta cuantos movimientos disponibles tiene la nave

    Args
    - head (searchTree): nodo padre

    Return
    - (int)
    """
    if head.tieneNave == True:
        return head.movimientosNave - 1
    else:
        return head.movimientosNave

def crearHijo(nodo: searchTree, direccion: str, nuevaPosicionAstronauta: tuple) -> None:
    """
    Se crea y añade un nodo hijo al nodo padre

    Args
    - nodo (searchTree): nodo padre
    - direccion (str): up | left | down | right
    - nuevaPosicionAstronauta (tupla): coordenadas de la nueva posicion del astronauta ej:. (a, b)
    """

    newMapa = actualizarMapa(nodo, nuevaPosicionAstronauta)
    posicion = nuevaPosicionAstronauta
    muestras = cantidadMuestrasCientificas(nodo, nuevaPosicionAstronauta)
    energiaGastada = totalEnergia(nodo)
    tieneNave = nosMontamosEnNave(nodo, nuevaPosicionAstronauta)
    movimientosNave = movimientosRestantesNave(nodo)

    hijo = searchTree(newMapa, posicion, muestras, energiaGastada, tieneNave, movimientosNave, operadorRealizado=direccion, hijos=list(), nodoPadre=nodo)
    return hijo

def traerHijos(nodo: searchTree, direcciones: dict) -> None: 
    """
    Busca las casillas a las que el astronauta   
    puede moverse, luego verifica si en el pasado ya paso por la casilla,
    si ya paso y el estado del nodo hijo es igual al padre o nodo encontrado, se detiene.
    Si sigue, crea un hijo y lo añade al nodo padre.
    los hijos ya tienen el movimiento y posicion realizada.

    Args
    - nodo (searchTree): nodo padre
    - direcciones (dict): diccionario con los movimientos permitidos en el juego
    """
    for i in range(1, len(direcciones) + 1):
        posicionAstronauta: tuple = nodo.posicionActual

        if nodo.puedoMoverme(direcciones[i], posicionAstronauta):
            nuevaPosicionAstronauta = nuevaPosicion(nodo.posicionActual, direcciones[i])

            bool, nodoSimilar = yaPasePorAqui(nodo, nuevaPosicionAstronauta)
            hijo = crearHijo(nodo, direcciones[i], nuevaPosicionAstronauta) 
            
            if bool:
                if esMismoEstado(hijo, nodoSimilar): 
                    pass # Ya no hace nada se detiene la rama
                else: 
                    nodo.añadirHijo(hijo) # El estado no es el mismo entonces puede seguir 
            else:
                nodo.añadirHijo(hijo)

def posicionObjetos() -> None:
    """
    Almacena en una lista la posicion de los obstaculos y objetos en el mapa
    """
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

def meterHijosEnPilaEntrada(cola: deque, hijos: list):
  for i in range(len(hijos)):  
    cola.append(hijos[i])



def expandir(nodo: searchTree, direcciones: dict):
    """
    Busca los hijos de un nodo, 
    luego verifica si un nodo es una meta, 
    si no es meta ingresa los hijos en la cola de entrada, 
    y para terminar saca el nodo actual y lo mete a la cola de salida
    """
    traerHijos(nodo, direcciones) # expandir
    nodosExpandidos.append(nodo)  # Registrar nodo expandido
    if nodo.esMeta():
        nodoSolucion.append(nodo)
        SOLUCION(nodo, solucion)
        print("llegue a la meta")
        salirBucle()
    else:
        meterHijosEnPilaEntrada(colaEntrada, nodo.hijos)
    

def salirBucle():
    """Llave de salida del bucle"""
    global key
    key = False

def resolver_profundidad(Mapa: list[list]) -> list:
    """
    Funcion principal que pone en marcha el 
    algoritmo de busqueda por amplitud
    """
    while key:
        primerElemento: searchTree = colaEntrada.pop()

        # primerElemento.printMapa()
        # primerElemento.imprimirInformacion()
        # print("\n\n----------------------------------------")

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

nodoSolucion: list = []
solucion = []

# Lista para registrar los nodos expandidos
nodosExpandidos = []

key: bool = True

if __name__ == "__main__":
    start: float = time.time()
    resolver_profundidad(Mapa)
    end: float = time.time()
    print(f"La cantidad de nodos expandidos es: {len(nodosExpandidos)}")
    print("Posiciones de todos los nodos expandidos:")
    for nodo in nodosExpandidos:
        print(nodo.posicionActual)
    '''
    print(f"La profundidad del arbol es: {nodoSolucion[0].profundidadArbol()}")
    print(f"La función tardó {end - start:.4f} segundos")
    print(solucion)
    '''
