# Interfaz gráfica
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import time

# Algoritmos de busqueda
import BusquedaNoInformada.amplitud as amplitud
import BusquedaNoInformada.costoUniforme as costoUniforme 
import BusquedaNoInformada.profundidad as profundidad

# Ventana general
ventana = tk.Tk()
ventana.title("Smart Astronaut")
ventana.geometry("800x700")
ventana.resizable(False, False)

# -------------------------------
# Ventana de tablero
# -------------------------------

def cuadricula():
    ventana_tablero.tkraise()

ventana_tablero = tk.Frame(ventana)
ventana_tablero.place(relwidth=1, relheight=1)

# Fondo
img_fondo2 = Image.open("assets/fondo2.png")
img_fondo2 = img_fondo2.resize((800, 700))  
fondo_tk2 = ImageTk.PhotoImage(img_fondo2)

lbl_fondo2 = tk.Label(ventana_tablero, image=fondo_tk2)
lbl_fondo2.place(relwidth=1, relheight=1)

fila = 10
columna = 10
celda = 50

canvas = tk.Canvas(ventana_tablero, width=columna*celda, height=fila*celda, bg="white", highlightthickness=1)
canvas.pack(pady=60)

# Cuadricula
for c in range(1, columna):
    for f in range(1, fila):
        x = c * celda
        y = f * celda
        canvas.create_line(x, 0, x, fila * celda, fill="black")
        canvas.create_line(0, y, columna * celda, y, fill="black")


# -------------------------------
# Ventana de bienvenida
# -------------------------------

def bienvenida():
    ventana_bienvenida.tkraise()

ventana_bienvenida = tk.Frame(ventana, bg="white")
ventana_bienvenida.place(relwidth=1, relheight=1)

# Fondo
img_fondo = Image.open("assets/fondo.png")
img_fondo = img_fondo.resize((800, 700))  
fondo_tk = ImageTk.PhotoImage(img_fondo)

lbl_fondo = tk.Label(ventana_bienvenida, image=fondo_tk)
lbl_fondo.place(relwidth=1, relheight=1)

#----------------------------------
# Texto
#---------------------------------

textInfo = tk.Canvas(ventana_bienvenida, highlightthickness=0)
textInfo.place(relwidth=1, relheight=1)
textInfo.create_image(0, 0, image=fondo_tk, anchor="nw")

textInfo.create_text(385, 280, text="Ingrese un archivo.txt del mundo", fill="#FFFFFF",font=("Arial", 12, "bold"))

textInfo.create_text(380, 370, text="Seleccione el algoritmo de búsqueda a aplicar", fill="#FFFFFF", font=("Arial", 12, "bold")  )

#--------------------
# Cargar archivo
#--------------------

def archivo_txt():
    filepath = filedialog.askopenfilename()

    with open(filepath, 'r') as archivo:
        matriz = [line.strip().split() for line in archivo.readlines()]
    return matriz

def cargar_mundo():
    matriz = archivo_txt()
    if matriz:
        ventana.matriz = matriz
        print("Mundo cargado")
        print("Matriz:", matriz)
    
        
#--------------------
# Imagenes
#--------------------

imagenes = {
    "1":ImageTk.PhotoImage(Image.open("assets/muro.png").resize((50, 50))),
    "2":ImageTk.PhotoImage(Image.open("assets/astronauta.png").resize((50, 50))),
    "3":ImageTk.PhotoImage(Image.open("assets/piedras.png").resize((50, 50))),
    "4":ImageTk.PhotoImage(Image.open("assets/volcan.png").resize((50, 50))),
    "5":ImageTk.PhotoImage(Image.open("assets/cohete.png").resize((50, 50))),
    "6":ImageTk.PhotoImage(Image.open("assets/muestra.png").resize((50, 50)))
    
}

botonArchivo = tk.Button(ventana_bienvenida, text="Mundo", command=cargar_mundo)
botonArchivo.place(x=365, y=315)

#----------------------------------------------
# Opciones de busqueda No informada e informada
#----------------------------------------------

opcionesBusqueda = {
    "Búsqueda No informada": ["Amplitud", "Costo uniforme", "Profundidad evitando ciclo"],
    "Búsqueda Informada": ["Avara", "A*"]
}

def actualizarOpciones():
    seleccion = despegable.get()
    if seleccion in opcionesBusqueda:
        subOpciones['values'] = opcionesBusqueda[seleccion]
        subOpciones.set("")  
    else:
        subOpciones['values'] = []
        subOpciones.set("")
        
        
# Primer lista despegable
algoritmoBusqueda = ['Búsqueda No informada', 'Búsqueda Informada']
despegable = ttk.Combobox(ventana_bienvenida,value=algoritmoBusqueda, state="readonly", width=25)
despegable.place(x=300, y=400)

# Botón de búsqueda
boton_buscar = tk.Button(ventana_bienvenida, text="Buscar", command=actualizarOpciones)
boton_buscar.place(x=365, y=450)

# Segunda lista despegable
subOpciones = ttk.Combobox(ventana_bienvenida,value=[], state="readonly", width=25)
subOpciones.place(x=300, y=500)

#----------------------------------
# Boton Start
#----------------------------------

def muestras():
    cuadricula()
    posiciones = []
    for i, fila in enumerate(ventana.matriz):
        for j, valor in enumerate(fila):              
            if valor == "6":
                posiciones.append((i,j))
    print("Posiciones de las muestras:", posiciones)
    return posiciones


def iniciar_tablero():
    cuadricula()
    for i, fila in enumerate(ventana.matriz):
        for j, valor in enumerate(fila):
            if valor in imagenes:
                x = j * celda + celda // 2
                y = i * celda + celda // 2
                mov = canvas.create_image(x, y, image=imagenes[valor])
                if valor == "2":
                    ventana.astronauta = mov
                    ventana.astronauta_fila = i
                    ventana.astronauta_col = j
                    print(f"Austronauta en posicion: ({i},{j})")
                if valor == "5":
                    ventana.nave_id = mov

    # Verificar selección de algoritmo
    tipo_busqueda = despegable.get()
    algoritmo = subOpciones.get()

    if not tipo_busqueda or not algoritmo:
        messagebox.showwarning("Selección requerida", "Por favor seleccione el tipo y algoritmo de búsqueda antes de continuar.")
        ventana.camino = []
        ventana.nodos_expand = 0
        ventana.profundidad = 0
        return
        
    camino = []    
    ventana.nodos_expand = 0

    if tipo_busqueda == "Búsqueda No informada":
        if algoritmo == "Amplitud":
            
            amplitud.Mapa = [[int(x) for x in fila] for fila in ventana.matriz]
            amplitud.listaObjetos = amplitud.posicionObjetos()  
            amplitud.Tree = amplitud.searchTree(amplitud.Mapa)
            amplitud.Tree.posicionAstronauta()
            amplitud.colaEntrada = amplitud.deque()
            amplitud.colaSalida = amplitud.deque()
            amplitud.colaEntrada.append(amplitud.Tree)
            amplitud.nodoSolucion = []
            amplitud.solucion = []
            amplitud.key = True

            tiempo_inicio = time.time()
            camino = amplitud.resolver_amplitud(amplitud.Mapa)
            ventana.camino = camino  


            ventana.algoritmo = algoritmo 
            ventana.costo_total = 0
            ventana.nodos_expand = len(amplitud.colaSalida)
            ventana.profundidad = len(camino) if camino else 0
            ventana.tiempo_inicio = tiempo_inicio

        elif algoritmo == "Costo uniforme":
            costoUniforme.Mapa = [[int(x) for x in fila] for fila in ventana.matriz]
            costoUniforme.listaObjetos = costoUniforme.posicionObjetos()
            costoUniforme.Tree = costoUniforme.searchTree(costoUniforme.Mapa)
            costoUniforme.Tree.posicionAstronauta()
            costoUniforme.listaEntrada = [costoUniforme.Tree]
            costoUniforme.listaSalida = []
            costoUniforme.nodoSolucion = []
            costoUniforme.solucion = []
            costoUniforme.key = True
            costoUniforme.direcciones = {1: "up", 2: "left", 3: "down", 4: "right"}
            
            tiempo_inicio = time.time()
            camino = costoUniforme.resolver_uniforme(costoUniforme.Mapa)

            ventana.camino = camino  
            
            ventana.algoritmo = algoritmo 
            ventana.nodos_expand = len(costoUniforme.listaSalida)
            ventana.profundidad = len(camino) if camino else 0
            ventana.tiempo_inicio = tiempo_inicio
            ventana.costo_total = costoUniforme.nodoSolucion[0].energiaTotalGastada
                    
            
        elif algoritmo == "Profundidad evitando ciclo":
            profundidad.Mapa = [[int(x) for x in fila] for fila in ventana.matriz]
            profundidad.listaObjetos = profundidad.posicionObjetos()
            profundidad.Tree = profundidad.searchTree(profundidad.Mapa)
            profundidad.Tree.posicionAstronauta()
            profundidad.pila = profundidad.deque()
            profundidad.pila.append(profundidad.Tree)
            profundidad.nodoSolucion = []
            profundidad.solucion = []
            profundidad.nodosExpandidos = []
            profundidad.key = True
            profundidad.direcciones = {1: "up", 2: "left", 3: "down", 4: "right"}
            
            tiempo_inicio = time.time()
            resultado = profundidad.resolver_profundidad(profundidad.Mapa)
            tiempo_final = time.time()
            
            if resultado and len(resultado) == 2:
                camino, nodos_expand_list = resultado
            else:
                camino, nodos_expand_list = [], []
                
                
            ventana.camino = camino
            
            ventana.nodos_expand = len(nodos_expand_list)
            if profundidad.nodoSolucion:
                ventana.profundidad = profundidad.nodoSolucion[0].profundidad
            else:
                ventana.profundidad = len(camino) if camino else 0

            ventana.algoritmo = algoritmo
            ventana.tiempo_inicio = tiempo_inicio
            ventana.tiempo_final = tiempo_final
            ventana.algoritmo = algoritmo 
            ventana.costo_total = 0
 
# Funcion de movimiento 
def recorrer_camino():
    if not hasattr(ventana, "camino") or not ventana.camino:
        print("No hay camino calculado todavía.")
        return
    
    # Obtener la posición inicial del astronauta
    fila = ventana.astronauta_fila
    columna = ventana.astronauta_col
    
    usando_nave = False
    pasos_nave = 0
    nave_mov = None

    # Iniciar la lista de coordenadas con la posición inicial
    coordenadas = [(fila, columna)]
    movimientos = {
        "up": (-1, 0),
        "down": (1, 0),
        "left": (0, -1),
        "right": (0, 1)
    }

    # Solo muestra el camino en la consola
    for direccion in ventana.camino:
            df, dc = movimientos.get(direccion.lower(), (0, 0))
            # Actualizar la posición
            fila += df
            columna += dc
            coordenadas.append((fila, columna))
            
    print("Camino recorrido:", coordenadas)
    print("Movimientos:", ventana.camino)

    fila = ventana.astronauta_fila
    columna = ventana.astronauta_col
    
    # Movimiento visual del astronauta
    def mover_astronauta(i=0):
        nonlocal fila, columna, usando_nave, pasos_nave, nave_mov
        
        if i >= len(ventana.camino):
            tiempo_final = time.time()
            messagebox.showinfo(
                    "Resultados del Algoritmo",
                    f"Algoritmo: {ventana.algoritmo}\n"
                    f"Nodos expandidos: {ventana.nodos_expand}\n"
                    f"Profundidad del árbol: {ventana.profundidad}\n"
                    f"Costo total: {ventana.costo_total: .2f}\n"
                    f"Tiempo de cómputo: {tiempo_final - ventana.tiempo_inicio:.4f} segundos"
            )
            return
    
        # Obtener la direccion actual del movimiento
        direccion = ventana.camino[i]
        df, dc = movimientos.get(direccion.lower(), (0, 0))
            
        # Actualizar la posición del astronauta
        fila += df
        columna += dc


        x = columna * celda + celda // 2
        y = fila * celda + celda // 2
            
        canvas.coords(ventana.astronauta, x, y)
        canvas.tag_raise(ventana.astronauta)
                
        if ventana.matriz[fila][columna] == "5" and not usando_nave:
            usando_nave = True
            pasos_nave = 20
            # Eliminar la nave original
            if hasattr(ventana, "nave_id"):
                canvas.delete(ventana.nave_id)
            nave_mov = canvas.create_image(x, y, image=imagenes["5"])
        if usando_nave and pasos_nave > 0:
            canvas.coords(nave_mov, x, y)
            pasos_nave -= 1
            if pasos_nave == 0:
                usando_nave = False
            
        if ventana.matriz[fila][columna] == "6":
            x1, y1 = columna * celda, fila * celda
            x2, y2 = x1 + celda, y1 + celda
                
                # Crear rectángulo amarillo
            rect = canvas.create_rectangle(x1, y1, x2, y2, fill="yellow", outline="black")
                
                # Enviar el rectángulo al fondo 
            canvas.tag_lower(rect, "all")  
                
        ventana.after(500, mover_astronauta, i + 1)

    mover_astronauta()

# Crear el botón START desactivado
botonStart = tk.Button(ventana_bienvenida, text="START", command=iniciar_tablero, state="disabled")
botonStart.place(x=365, y=550)

# Función para habilitar/deshabilitar el botón START
def actualizar_estado_start(*args):
    tipo_busqueda = despegable.get()
    algoritmo = subOpciones.get()
    if tipo_busqueda and algoritmo:
        botonStart.config(state="normal")
    else:
        botonStart.config(state="disabled")

despegable.bind("<<ComboboxSelected>>", actualizar_estado_start)
subOpciones.bind("<<ComboboxSelected>>", actualizar_estado_start)

botonTablero = tk.Button(ventana_tablero, text="RECORRER", command=recorrer_camino)
botonTablero.place(x=400, y=580)


bienvenida()
ventana.mainloop()