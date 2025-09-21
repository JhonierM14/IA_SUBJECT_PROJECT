# Interfaz grafica
import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk 
from tkinter import filedialog
from amplitud import resolver_amplitud


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
        subOpciones.current(0)
    else:
        subOpciones['values'] = []
        
        
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


# ----------------------------
# Verificar el tipo de busqueda
# ----------------------------

        tipo_busqueda = despegable.get()
        algoritmo = subOpciones.get()

        camino = []

        if tipo_busqueda == "Búsqueda No informada":
            if algoritmo == "Amplitud":
                camino = resolver_amplitud(ventana.matriz)
            elif algoritmo == "Costo uniforme":
                camino = [] # resolver_costo_uniforme(ventana.matriz)
            elif algoritmo == "Profundidad evitando ciclo":
                camino = [] # resolver_profundidad(ventana.matriz)
                
        ventana.camino = camino
 

def recorrer_camino():
    if not hasattr(ventana, "camino") or not ventana.camino:
        print("No hay camino calculado todavía.")
        return
    
    # Obtener la posición inicial del astronauta
    fila = ventana.astronauta_fila
    columna = ventana.astronauta_col
    
    # Iniciar la lista de coordenadas con la posición inicial
    coordenadas = [(fila, columna)]
    movimientos = {
        "up": (-1, 0),
        "down": (1, 0),
        "left": (0, -1),
        "right": (0, 1)
    }
    
    #  Solo muestra el camino en la consola
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
        nonlocal fila, columna
        
        if i >= len(ventana.camino):
            return

        # Obtener la direccion actual del movimiento
        direccion = ventana.camino[i]
        df, dc = movimientos.get(direccion.lower(), (0, 0))
        
        # Actualizar la posición del astronauta
        fila += df
        columna += dc

        # Coordenadas en pixeles para el canva
        x = columna * celda + celda // 2
        y = fila * celda + celda // 2
        
        canvas.coords(ventana.astronauta, x, y)
        ventana.after(500, mover_astronauta, i + 1)
        
    mover_astronauta()

botonTablero = tk.Button(ventana_bienvenida, text="START", command=iniciar_tablero)
botonTablero.place(x=365, y=550)

botonTablero = tk.Button(ventana_tablero, text="RECORRER", command=recorrer_camino)
botonTablero.place(x=365, y=580)

bienvenida()
ventana.mainloop()