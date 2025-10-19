import copy
import heapq
import time
from typing import List, Tuple, Dict, Any

from seachTree import searchTree


def SOLUCION(head: searchTree, solucion: list) -> None:
    """
    Arma la ruta de movimientos desde el nodo actual hasta la raíz.
    Se va subiendo por los padres y agregando el operador de cada paso.
    """
    if head.nodoPadre is not None:
        solucion.append(head.operadorRealizado)
        SOLUCION(head.nodoPadre, solucion)


def yaPasePorAqui(nodoPadre, nuevaPosicionAstronauta) -> tuple[bool, object]:
    """
    Revisa si ya pasamos por esa casilla en la rama actual.
    Devuelve (true, nodo) si la encuentra; en otro caso (false, None).

    Args
    - nodoPadre (searchTree): nodo padre
    - nuevaPosicionAstronauta (tupla): nueva posicion del astronauta

    Return
    - el primer argumento representa si ya se paso o no por la casilla, el segundo argumento el nodo con la misma posicion (tuple[bool, object])
    """
    if nodoPadre is None:
        return (False, nodoPadre)
    elif nodoPadre.posicionActual == nuevaPosicionAstronauta:
        return (True, nodoPadre)
    else:
        return yaPasePorAqui(nodoPadre.nodoPadre, nuevaPosicionAstronauta)


def esMismoEstado(nodo, nodoCola) -> bool:
    """
    Considera igual el estado si coinciden 'tieneNave' y 'muestras'.
    Si es igual, no tiene sentido expandir esa rama.

    Args
    - nodo (searchTree): nodo padre
    - nodoCola (searchTree): nodo encontrado con el que se compara el estado

    Return
    - representa si es igual o no el estado de los nodos (bool)
    """
    return nodo.tieneNave == nodoCola.tieneNave and nodo.muestras == nodoCola.muestras


def nuevaPosicion(posicionActual: tuple, direccion: str) -> tuple:
    """
    A partir de una posición y una dirección, calcula la nueva celda.

    Args
    - posicionActual (tupla): (fila, columna)
    - direccion (str): up | left | down | right

    Return
    - tupla con la nueva posición
    """
    x, y = posicionActual
    if direccion == "up":
        return (x - 1, y)
    if direccion == "left":
        return (x, y - 1)
    if direccion == "down":
        return (x + 1, y)
    if direccion == "right":
        return (x, y + 1)
    return posicionActual


def cantidadMuestrasCientificas(mapa: List[List[int]], muestras_actuales: int, posicion: tuple) -> int:
    """
    Si la nueva casilla tiene una muestra (6), suma una al contador,
    de lo contrario deja el valor como esta

    Args
    - mapa (List[List[int]]): mapa del nodo
    - muestras_actuales (int): cantidad actual de muestras
    - posicion (tupla): nueva posicion a la que se movera el astronauta

    Return
    - cantidad de muestras cientificas (int)
    """
    x, y = posicion
    if mapa[x][y] == 6:
        return muestras_actuales + 1
    return muestras_actuales


def totalEnergia(head: searchTree) -> float:
    """
    Costo por moverse:
    - con nave: +0.5
    - sin nave: +1
    Se suma al acumulado del nodo padre.

    Args
    - head (searchTree): nodo padre

    Return
    - cantidad total de energia gastada (float)
    """
    if head.tieneNave is False:
        return head.energiaTotalGastada + 1
    else:
        return head.energiaTotalGastada + 0.5


def nosMontamosEnNave(head: searchTree, mapa: List[List[int]], posicion: tuple) -> bool:
    """
    Indica si al llegar a la nueva casilla estamos sobre la nave.
    Si ya la teníamos y aún hay movimientos, se mantiene activa.

    Args
    - head (searchTree): nodo padre
    - mapa (List[List[int]]): mapa del nodo
    - posicion (tupla): nueva posicion del astronauta

    Return
    - (bool)
    """
    x, y = posicion
    if head.tieneNave is True and head.movimientosNave >= 1:
        return True
    elif head.tieneNave is False and mapa[x][y] == 5:
        return True
    else:
        return False


def movimientosRestantesNave(head: searchTree) -> int:
    """
    Actualiza el contador de movimientos de la nave.
    Si está activa, resta uno; de lo contrario, deja igual.

    Args
    - head (searchTree): nodo padre

    Return
    - (int)
    """
    if head.tieneNave is True:
        return head.movimientosNave - 1
    else:
        return head.movimientosNave


def actualizarMapa(head: searchTree, nuevaPosicionAstronauta: tuple) -> List[List[int]]:
    """
    Copia el mapa del padre, limpia la casilla anterior del astronauta
    y coloca al astronauta en la nueva posición (2). Si había 5 o 6,
    quedan reemplazados por el astronauta.

    Args
    - head (searchTree): nodo padre
    - nuevaPosicionAstronauta (tupla): coordenada de la nueva posicion del astronauta ej:. (a, b)

    Return
    - Mapa actualizado (List[List[int]])
    """
    nuevo_mapa = copy.deepcopy(head.mapa)
    a, b = head.posicionActual
    nuevo_mapa[a][b] = 0
    x, y = nuevaPosicionAstronauta
    nuevo_mapa[x][y] = 2
    return nuevo_mapa


def crearHijo(nodo: searchTree, direccion: str) -> searchTree | None:
    """
    Crea un hijo aplicando la 'direccion' al nodo dado.
    Calcula el nuevo estado (muestras, energía, nave, etc.) y lo devuelve.
    Si el movimiento no es válido, retorna None.

    Args
    - nodo (searchTree): nodo padre
    - direccion (str): up | left | down | right

    Return
    - nodo hijo (searchTree | None)
    """
    if not nodo.puedoMoverme(direccion, nodo.posicionActual):
        return None

    nueva_posicion = nuevaPosicion(nodo.posicionActual, direccion)

    # calcular nuevos atributos del hijo
    nuevas_muestras = cantidadMuestrasCientificas(nodo.mapa, nodo.muestras, nueva_posicion)
    nueva_energia = totalEnergia(nodo)
    nueva_tiene_nave = nosMontamosEnNave(nodo, nodo.mapa, nueva_posicion)
    nuevos_mov_nave = movimientosRestantesNave(nodo)

    nuevo_mapa = actualizarMapa(nodo, nueva_posicion)

    hijo = searchTree(
        nuevo_mapa,
        nueva_posicion,
        nuevas_muestras,
        nueva_energia,
        nueva_tiene_nave,
        nuevos_mov_nave,
        operadorRealizado=direccion,
        hijos=list(),
        nodoPadre=nodo,
    )
    return hijo


def traerHijos(nodo: searchTree, direcciones: dict) -> List[searchTree]:
    """
    Genera los hijos validos del nodo en las cuatro direcciones.

    Args
    - nodo (searchTree): nodo padre
    - direcciones (dict): diccionario con los movimientos permitidos en el juego

    Return
    - lista de hijos creados (List[searchTree])
    """
    hijos_creados: List[searchTree] = []
    for i in range(1, len(direcciones) + 1):
        direccion = direcciones[i]
        if nodo.puedoMoverme(direccion, nodo.posicionActual):
            nueva_pos = nuevaPosicion(nodo.posicionActual, direccion)
            ya_pase, nodo_similar = yaPasePorAqui(nodo, nueva_pos)
            hijo = crearHijo(nodo, direccion)
            if hijo is None:
                continue
            if ya_pase:
                if esMismoEstado(hijo, nodo_similar):
                    continue
                else:
                    hijos_creados.append(hijo)
            else:
                hijos_creados.append(hijo)
    nodo.hijos = hijos_creados
    return hijos_creados


def heuristica(nodo: searchTree) -> int:
    """
    Distancia Manhattan hasta la muestra (6) más cercana en el mapa del nodo.
    Si ya juntó 3 muestras, la heurística vale 0.
    """
    if nodo.muestras >= 3:
        return 0

    x0, y0 = nodo.posicionActual
    mejor = None
    for i in range(10):
        for j in range(10):
            if nodo.mapa[i][j] == 6:  # muestra no recogida
                d = abs(x0 - i) + abs(y0 - j)
                if mejor is None or d < mejor:
                    mejor = d

    if mejor is None:
        # no hay muestras visibles, heurística neutra
        return 0
    return mejor


def resolver_avara_info(matriz: List[List[str | int]]) -> Tuple[List[str], Dict[str, Any]]:
    """
    Funcion principal que ejecuta la busqueda avara sobre la matriz del mundo.
    """
    # convertir la matriz a enteros si viene como strings
    mapa: List[List[int]] = [
        [int(celda) if not isinstance(celda, int) else celda for celda in fila]
        for fila in matriz
    ]

    # nodo raíz
    raiz = searchTree(mapa)
    raiz.posicionAstronauta()

    heap: List[Tuple[int, int, searchTree]] = []
    contador = 0  # desempate

    start = time.time()
    expandidos = 0
    heapq.heappush(heap, (heuristica(raiz), contador, raiz))

    direcciones = {1: "up", 2: "left", 3: "down", 4: "right"}
    solucion: List[str] = []

    while heap:
        _, _, actual = heapq.heappop(heap)
        expandidos += 1

        if actual.esMeta():
            SOLUCION(actual, solucion)
            solucion.reverse()
            end = time.time()
            info: Dict[str, Any] = {
                "nodos_expandidos": expandidos,
                "profundidad": actual.profundidadArbol(),
                "tiempo_segundos": end - start,
            }
            
            print(f"La cantidad de nodos expandidos es: {info['nodos_expandidos']}")
            print(f"La profundidad del arbol es: {info['profundidad']}")
            print(f"La función tardó {info['tiempo_segundos']:.4f} segundos")
            print(solucion)
            return solucion, info

        hijos = traerHijos(actual, direcciones)
        for hijo in hijos:
            contador += 1
            heapq.heappush(heap, (heuristica(hijo), contador, hijo))

    end = time.time()
    info: Dict[str, Any] = {
        "nodos_expandidos": expandidos,
        "profundidad": 0,
        "tiempo_segundos": end - start,
    }
    print(f"La cantidad de nodos expandidos es: {info['nodos_expandidos']}")
    print(f"La profundidad del arbol es: {info['profundidad']}")
    print(f"La función tardó {info['tiempo_segundos']:.4f} segundos")
    print([])
    return [], info


def resolver_avara(matriz: List[List[str | int]]) -> List[str]:
    """
    Atajo que solo retorna la lista de movimientos.
    """
    movimientos, _ = resolver_avara_info(matriz)
    return movimientos
