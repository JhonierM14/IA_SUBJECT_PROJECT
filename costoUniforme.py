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
                print(f"Muestra recogida en coordenada: {x, y}")

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
    """
    Se modifico la funcion para que reciba el bool tieneNave que se crea en la funcion crearHijo,
    ya que si se extrae el atributo "tieneNave" de head, este nos daria la informacion del nodo padre, la cual
    podria ser diferente a la del hijo que se esta creando.
    """
    if tieneNave == True:
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
    muestras = cantidadMuestrasCientificas(nodo, posicion)
    tieneNave = nosMontamosEnNave(nodo, posicion)
    movimientosNave = movimientosRestantesNave(nodo, tieneNave)
    energiaGastada = totalEnergia(nodo, posicion, tieneNave)

    hijo = searchTree(newMapa, posicion, muestras, energiaGastada, tieneNave, movimientosNave, operadorRealizado=direccion, hijos=list(), nodoPadre=nodo)
    nodo.añadirHijo(hijo)

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

            bool, nodoSimilar = nodo.yaPasePorAqui(nodo, nuevaPosicionAstronauta)
            if bool:
                if nodo.esMismoEstado(nodo, nodoSimilar): 
                    pass # Ya no hace nada se detiene la rama
                else: crearHijo(nodo, direcciones[i], nuevaPosicionAstronauta) # El estado no es el mismo entonces puede seguir
            else:
                crearHijo(nodo, direcciones[i], nuevaPosicionAstronauta)

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
    """
    Busca el nodo con menor energia gastada
    en la lista de entrada, lo elimina de la lista
    y lo retorna

    Args
    - cola (list): lista de nodos

    Return
    - nodo con menor energia (searchTree)
    """
    menor = float('inf')
    for i in range(len(lista)):
        if lista[i].getEnergiaTotalGastada() < menor:
            menor = lista[i].getEnergiaTotalGastada()
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
        print("llegue a la meta"); 
        salirBucle()
    else: 
        meterHijosEnlistaEntrada(listaEntrada, nodo.hijos)
        meterNodoListaSalida(listaSalida, nodo)

def salirBucle():
    """Llave de salida del bucle"""
    global key
    key = False

def resolver_uniforme(Mapa: list[list]) -> list:
    """
    Funcion principal que pone en marcha el 
    algoritmo de busqueda por costo uniforme
    """
    while key:
        menorNodo: searchTree = menorEnergia(listaEntrada)

        menorNodo.printMapa()
        menorNodo.imprimirInformacion()
        expandir(menorNodo, direcciones)

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

listaEntrada = list()
listaSalida = list()

listaEntrada.append(Tree)

direcciones = {1: "up", 2: "left", 3: "down", 4: "right"}

nodoSolucion: list = []
solucion = []

key = True


start: float = time.time(); 
resolver_uniforme(Mapa)
end: float = time.time()

print(f"La cantidad de nodos expandidos es: {len(listaSalida)}")
print(f"La profundidad del arbol es: {nodoSolucion[0].profundidadArbol()}")
print(f"La función tardó {end - start:.4f} segundos")
print(solucion)


