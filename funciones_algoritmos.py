import time
import amplitud
import costoUniforme
import profundidad

def ejecutar_algoritmo(matriz, tipo, algoritmo):
    camino = []
    nombre_algoritmo = ""
    nodos_expandidos = 0
    profundidad_algoritmo = 0
    costo_total = 0
    tiempo_inicio = time.time()

    if tipo == "Búsqueda No informada":
        if algoritmo == "Amplitud":
            amplitud.Mapa = [[int(x) for x in f] for f in matriz]
            amplitud.listaObjetos = amplitud.posicionObjetos()
            amplitud.Tree = amplitud.searchTree(amplitud.Mapa)
            amplitud.Tree.posicionAstronauta()
            amplitud.colaEntrada, amplitud.colaSalida = amplitud.deque(), amplitud.deque()
            amplitud.colaEntrada.append(amplitud.Tree)
            amplitud.nodoSolucion, amplitud.solucion = [], []
            amplitud.key = True
            camino = amplitud.resolver_amplitud(amplitud.Mapa)
            nombre_algoritmo, nodos_expandidos, profundidad_algoritmo, costo_total = "Amplitud", len(amplitud.colaSalida), len(camino), 0

        elif algoritmo == "Costo uniforme":
            costoUniforme.Mapa = [[int(x) for x in f] for f in matriz]
            costoUniforme.listaObjetos = costoUniforme.posicionObjetos()
            costoUniforme.Tree = costoUniforme.searchTree(costoUniforme.Mapa)
            costoUniforme.Tree.posicionAstronauta()
            costoUniforme.listaEntrada = [costoUniforme.Tree]
            costoUniforme.listaSalida = []
            costoUniforme.nodoSolucion = []
            costoUniforme.solucion = []
            costoUniforme.key = True
            costoUniforme.direcciones = {1:"up",2:"left",3:"down",4:"right"}
            camino = costoUniforme.resolver_uniforme(costoUniforme.Mapa)
            nombre_algoritmo, nodos_expandidos, profundidad_algoritmo, costo_total = "Costo uniforme", len(costoUniforme.listaSalida), len(camino), costoUniforme.nodoSolucion[0].energiaTotalGastada

        elif algoritmo == "Profundidad evitando ciclo":
            profundidad.Mapa = [[int(x) for x in f] for f in matriz]
            profundidad.listaObjetos = profundidad.posicionObjetos()
            profundidad.Tree = profundidad.searchTree(profundidad.Mapa)
            profundidad.Tree.posicionAstronauta()
            profundidad.pila = profundidad.deque()
            profundidad.pila.append(profundidad.Tree)
            profundidad.nodoSolucion, profundidad.solucion, profundidad.nodosExpandidos = [], [], []
            profundidad.key = True
            profundidad.direcciones = {1:"up",2:"left",3:"down",4:"right"}
            resultado = profundidad.resolver_profundidad(profundidad.Mapa)
            if resultado and len(resultado) == 2:
                camino, nodos_expand_list = resultado
            else:
                camino, nodos_expand_list = [], []
            nombre_algoritmo = "Profundidad evitando ciclo"
            nodos_expandidos = len(nodos_expand_list)
            profundidad_algoritmo = profundidad.nodoSolucion[0].profundidad if profundidad.nodoSolucion else len(camino)
            costo_total = 0

    return camino, nombre_algoritmo, nodos_expandidos, profundidad_algoritmo, costo_total, tiempo_inicio
