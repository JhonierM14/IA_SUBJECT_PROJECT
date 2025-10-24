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
    if head.nodoPadre is not None:
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
    '''
    Si se pasa por una casilla en la cual ya se estubo y el estado es igual para ambos
    nodos se retorna True y la rama muere, en caso contraria sigue expandiendo.
    '''
    if nodo.posicionActual != nodoCola.posicionActual:
        return False

    if nodo.muestras > nodoCola.muestras:
        return False

    if not nodoCola.tieneNave and nodo.tieneNave:
        return False

    return True

def nuevaPosicion(posicionActual: tuple, direccion: str) -> tuple:
    """
        Retorna una tupla con la posicion actual del astronauta
        más la direccion de movimiento

        Args 
        - posicionActual (tupla): posicion actual del astronauta, ej:. (a, b)
        - direccion (str): up | left | down | right
        - listaObjetos (list): lista con los objetos y obstaculos del mapa
    """
    x, y = posicionActual
    if direccion == "up": return (x - 1, y)
    if direccion == "left": return (x, y - 1)
    if direccion == "down": return (x + 1, y)
    if direccion == "right": return (x, y + 1)

def actualizarMapa(listaObjetos: list[Objeto], head: searchTree, nuevaPosicionAstronauta: tuple) -> list[list]:
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
    a, b = head.posicionActual
    x, y = nuevaPosicionAstronauta
    newMapa[a][b] = 0 

    for objeto in listaObjetos:
        if objeto.id != 5 and (objeto.recogido is False or objeto.recogido is None):
            newMapa[objeto.posicion[0]][objeto.posicion[1]] = objeto.id
        elif objeto.id == 5:  # si es la nave
            if head.tieneNave is False and head.movimientosNave == 20 and newMapa[x][y] != objeto.id:
                newMapa[x][y] = 2
            elif head.tieneNave is False and head.movimientosNave == 20 and newMapa[x][y] == objeto.id:
                newMapa[x][y] = 5
            elif head.tieneNave is True and head.movimientosNave == 20 and newMapa[x][y] != objeto.id:
                newMapa[x][y] = 5
            elif head.tieneNave is True and head.movimientosNave >= 1:
                objeto.posicion = (x, y)
                newMapa[objeto.posicion[0]][objeto.posicion[1]] = 5
            elif head.tieneNave is True and head.movimientosNave == 0:
                objeto.posicion = (a, b)
                newMapa[objeto.posicion[0]][objeto.posicion[1]] = 5
                newMapa[x][y] = 2
            elif head.tieneNave is False and head.movimientosNave == 0:
                newMapa[objeto.posicion[0]][objeto.posicion[1]] = objeto.id
                newMapa[x][y] = 2
            break

    return newMapa

def cantidadMuestrasCientificas(head: searchTree, listaObjetos: list[Objeto], posicion: tuple) -> int:
    """
    Verifica si en la nueva posición hay una muestra científica.
    Si la hay, la marca como recogida y aumenta el contador.

    Args:
        head (searchTree): nodo actual.
        listaObjetos (list[Objeto]): lista de objetos del mapa.
        posicion (tuple): nueva posición (x, y).

    Return:
        int: número total de muestras recogidas.
    """
    x, y = posicion
    if head.mapa[x][y] == 6:
        for obj in listaObjetos:
            if obj.posicion == (x, y):
                obj.recogido = True
        return head.muestras + 1
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
    elif head.tieneNave==False and head.mapa[x][y] == 5 and head.movimientosNave == 20:
        return True
    else:
        return False

def movimientosRestantesNave(head: searchTree) -> int:
    """
    Cuenta cuantos movimientos disponibles tiene la nave

    Args
    - head (searchTree): nodo padre

    Return
    - cantidad de movimientos restantes (int)
    """
    if head.tieneNave == True and head.movimientosNave >= 1:
        return head.movimientosNave - 1
    else:
        return head.movimientosNave

def crearHijo(nodo: searchTree, direccion: str, nuevaPosicionAstronauta: tuple, listaObjetos: list[Objeto]) -> searchTree:
    
    newMapa = actualizarMapa(listaObjetos, nodo, nuevaPosicionAstronauta)
    muestras = cantidadMuestrasCientificas(nodo, listaObjetos, nuevaPosicionAstronauta)
    energiaGastada = totalEnergia(nodo)
    tieneNave = nosMontamosEnNave(nodo, nuevaPosicionAstronauta)
    movimientosNave = movimientosRestantesNave(nodo)

    hijo = searchTree(
        mapa=newMapa,
        posicionActual=nuevaPosicionAstronauta,
        muestras=muestras,
        energiaTotalGastada=energiaGastada,
        tieneNave=tieneNave,
        movimientosNave=movimientosNave,
        operadorRealizado=direccion,
        hijos=[],
        nodoPadre=nodo,
        listaObjetos=copy.deepcopy(listaObjetos)
    )
    return hijo

def traerHijos(nodo: searchTree, direcciones: dict, listaObjetos: list[Objeto]) -> None:
    '''
    Genera los hijos validos del nodo actual según las direcciones posibles.
    Se verifica si ya pasó por una posición y si si el estael estado es el mismo
    para evitar ciclos, pero permite devolverse do cambio
    '''
    for i in range(1, len(direcciones) + 1):
        if nodo.puedoMoverme(direcciones[i], nodo.posicionActual):
            nuevaPos = nuevaPosicion(nodo.posicionActual, direcciones[i])
            yaPaso, nodoSimilar = yaPasePorAqui(nodo, nuevaPos)
            hijo = crearHijo(nodo, direcciones[i], nuevaPos, listaObjetos)
            if yaPaso:
                if not esMismoEstado(hijo, nodoSimilar):
                    nodo.añadirHijo(hijo)
            else:
                nodo.añadirHijo(hijo)

def expandir(nodo: searchTree, direcciones: dict) -> bool:
    
    listaObjetos = nodo.listaObjetos  
    traerHijos(nodo, direcciones, listaObjetos)  
    pilaSalida.append(nodo) 

    for hijo in nodo.hijos:
        pilaEntrada.append(hijo)

    for hijo in nodo.hijos:
        if hijo.esMeta():
            nodoSolucion.append(hijo)
            SOLUCION(hijo, solucion)
            return False

    return True

def resolver_profundidad(Mapa: list[list[int]]) -> list:
    
    nodoRaiz = searchTree(Mapa)
    nodoRaiz.posicionAstronauta()
    nodoRaiz.posicionObjetos()
    pilaEntrada.append(nodoRaiz)

    key = True

    while key:
        if not pilaEntrada:
            print("No se encontró solución.")
            break

        actual: searchTree = pilaEntrada.pop() 
        key = expandir(actual, direcciones)

        actual.printMapa()
        actual.imprimirInformacion()
        
    if not key:
        solucion.reverse()
        return solucion
    print("Solución encontrada por profundidad")

pilaEntrada = deque() 
pilaSalida = deque() 

direcciones = {1: "up", 2: "left", 3: "down", 4: "right"}

nodoSolucion: list = []
solucion = []

if __name__ == "__main__":

    start: float = time.time(); 
    resolver_profundidad(Mapa)
    end: float = time.time()

    print(f"La cantidad de nodos expandidos es: {len(pilaSalida) + 1}")
    print(f"La profundidad del arbol es: {nodoSolucion[0].profundidadArbol()}")
    print(f"La función tardó {end - start:.4f} segundos")
    print(solucion)