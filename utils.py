def convertir_matriz_numerica(mapa: list[list]) -> list[list[int]]:
    """
    Convierte una matriz que contiene números en formato string a formato int.
    Si ya son numeros, devuelve la matriz sin cambios.
    """
    # Si el primer elemento no es string, toda la matriz es numérica
    if(type(mapa[0][0]) == int): 
        return mapa
    
    try:
        # Convierte cada elemento a int
        return [[int(valor) for valor in fila] for fila in mapa]
    except ValueError:
        # Si algún valor no es numérico, lanza un error claro
        print("No se puede continuar: la matriz contiene valores no numéricos.")
        raise