import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import time
import funciones_algoritmos as fa

# Ventana principal
ventana = tk.Tk()
ventana.title("Smart Astronaut")
ventana.geometry("1200x650")
ventana.resizable(False, False)

ventana_tablero = tk.Frame(ventana)
ventana_tablero.place(relwidth=1, relheight=1)

# Fondo
fondo_ventana = ImageTk.PhotoImage(Image.open("assets/martefondo.png").resize((1200, 650)))
tk.Label(ventana_tablero, image=fondo_ventana).place(relwidth=1, relheight=1)

# Cuadrícula
fila, columna, celda = 10, 10, 46
canvas = tk.Canvas(ventana_tablero, width=columna * celda, height=fila * celda, bg="white", highlightthickness=1)
canvas.place(x=160, y=130)

# Líneas de la cuadrícula
for c in range(1, columna):
    for f in range(1, fila):
        x, y = c * celda, f * celda
        canvas.create_line(x, 0, x, fila * celda, fill="black")
        canvas.create_line(0, y, columna * celda, y, fill="black")

# Texto en la gui
tk.Label(ventana_tablero, text="Ingrese un archivo.txt del mundo", font=("Arial", 13, "bold"), fg="white", bg="#1b1d20").place(x=790, y=140)
tk.Label(ventana_tablero, text="Seleccione el algoritmo de búsqueda a aplicar", font=("Arial", 11, "bold"), fg="white", bg="#1b1d20").place(x=755, y=220)

# Resultados
lbl_resultado = tk.Label( ventana_tablero, text="", font=("Arial", 13, "bold"), fg="#FFFFFF", bg="#1b1d20", justify="left")
lbl_resultado.place(x=760, y=410)

#Cargar archivo
def archivo_txt():
    filepath = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
    if not filepath:
        return None
    with open(filepath, 'r') as archivo:
        matriz = [line.strip().split() for line in archivo.readlines()]
    return matriz

def cargar_mundo():
    matriz = archivo_txt()
    if matriz:
        ventana.matriz = matriz
        iniciar_tablero()

# Imagenes
imagenes = {
    "1": ImageTk.PhotoImage(Image.open("assets/muro.png").resize((50, 50))),
    "2": ImageTk.PhotoImage(Image.open("assets/astronauta.png").resize((50, 50))),
    "3": ImageTk.PhotoImage(Image.open("assets/piedras.png").resize((50, 50))),
    "4": ImageTk.PhotoImage(Image.open("assets/volcan.png").resize((50, 50))),
    "5": ImageTk.PhotoImage(Image.open("assets/cohete.png").resize((50, 50))),
    "6": ImageTk.PhotoImage(Image.open("assets/muestra.png").resize((50, 50)))
}

botonArchivo = tk.Button(ventana_tablero, text="Mundo", command=cargar_mundo)
botonArchivo.place(x=900, y=180)

# Imagenes en la matriz
def iniciar_tablero():
    for i, fila_ in enumerate(ventana.matriz):
        for j, valor in enumerate(fila_):
            if valor in imagenes:
                x = j * celda + celda // 2
                y = i * celda + celda // 2
                mov = canvas.create_image(x, y, image=imagenes[valor])
                if valor == "2":
                    ventana.astronauta = mov
                    ventana.astronauta_fila, ventana.astronauta_col = i, j
                if valor == "5":
                    ventana.nave_id = mov

# Opciones de busqueda No informada e informada
opcionesBusqueda = {
    "Búsqueda No informada": ["Amplitud", "Costo uniforme", "Profundidad evitando ciclo"],
    "Búsqueda Informada": ["Avara", "A*"]
}

def actualizarOpciones():
    seleccion = despegable.get()
    subOpciones['values'] = opcionesBusqueda.get(seleccion, [])
    subOpciones.set("")

# Primer lista despegable
despegable = ttk.Combobox(ventana_tablero, value=list(opcionesBusqueda.keys()), state="readonly", width=25)
despegable.place(x=840, y=255)

# Botón de busqueda
boton_buscar = tk.Button(ventana_tablero, text="Buscar", command=actualizarOpciones)
boton_buscar.place(x=900, y=290)

# Segunda lista despegable
subOpciones = ttk.Combobox(ventana_tablero, value=[], state="readonly", width=25)
subOpciones.place(x=840, y=330)

# Informe de los resultados
def mostrar_resultados():
    tiempo_final = time.time()
    tiempo_computo = tiempo_final - ventana.tiempo_inicio

    lbl_resultado.config(
        text=(f"Informe:\n"
              f"Algoritmo: {ventana.algoritmo}\n"
              f"Nodos expandidos: {ventana.nodos_expand}\n"
              f"Profundidad: {ventana.profundidad}\n"
              f"Costo total: {ventana.costo_total:.2f}\n"
              f"Tiempo: {tiempo_computo:.3f} seg")
    )

    # Botón para cerrar
    btn_salir = tk.Button(
        ventana,
        text="Reiniciar para probar otro algoritmo",
        font=("Arial", 10, "bold"),
        cursor="hand2",
        command=cerrar_programa
    )
    btn_salir.place(x=800, y=550, width=260, height=20)

# Cerrar programa
def cerrar_programa():
    messagebox.showinfo("Smart Astronaut", "Hasta la próxima misión en Marte.")
    ventana.destroy()

# Ejecucion del algoritmo
def ejecutar_algoritmo_gui():
    tipo_busqueda, algoritmo = despegable.get(), subOpciones.get()

    # Desactivar controles
    for w in (botonArchivo, boton_buscar, despegable, subOpciones, botonStart):
        w.config(state="disabled")

    lbl_resultado.config(text="Ejecutando algoritmo, por favor espere...")
    ventana.update()

    # Ejecutar algoritmo
    camino, nombre_algoritmo, nodos_expandidos, profundidad_algoritmo, costo_total, tiempo_inicio = fa.ejecutar_algoritmo(
        ventana.matriz, tipo_busqueda, algoritmo
    )

    # Guardar resultados en variables globales
    ventana.camino = camino
    ventana.algoritmo = nombre_algoritmo
    ventana.nodos_expand = nodos_expandidos
    ventana.profundidad = profundidad_algoritmo
    ventana.costo_total = costo_total
    ventana.tiempo_inicio = tiempo_inicio

    recorrer_camino()

# Animacion del astronauta
def recorrer_camino():
    if not ventana.camino:
        return

    fila, columna = ventana.astronauta_fila, ventana.astronauta_col
    usando_nave = False
    pasos_nave = 0
    nave_mov = None

    coordenadas = [(fila, columna)]
    movimientos = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}

    def mover_astronauta(i=0):
        nonlocal fila, columna, usando_nave, pasos_nave, nave_mov
        if i >= len(ventana.camino):
            print("Camino recorrido:", coordenadas)
            print("Movimientos realizados:", ventana.camino)
            mostrar_resultados()
            return

        direccion = ventana.camino[i]
        df, dc = movimientos.get(direccion.lower(), (0, 0))
        fila += df
        columna += dc
        coordenadas.append((fila, columna))
        x = columna * celda + celda // 2
        y = fila * celda + celda // 2

        # Mover astronauta
        canvas.coords(ventana.astronauta, x, y)
        canvas.tag_raise(ventana.astronauta)

        # Si monta nave
        if ventana.matriz[fila][columna] == "5" and not usando_nave:
            usando_nave = True
            pasos_nave = 20
            if hasattr(ventana, "nave_id"):
                canvas.delete(ventana.nave_id)
                ventana.nave_id = None
            nave_mov = canvas.create_image(x, y, image=imagenes["5"])

        # Uso nave
        if usando_nave and pasos_nave > 0:
            canvas.coords(nave_mov, x, y)
            pasos_nave -= 1
            if pasos_nave == 0:
                usando_nave = False

        # Si llega a una muestra
        if ventana.matriz[fila][columna] == "6":
            x1, y1 = columna * celda, fila * celda
            x2, y2 = x1 + celda, y1 + celda
            rect = canvas.create_rectangle(x1, y1, x2, y2, fill="yellow", outline="black")
            canvas.tag_lower(rect, "all")

        ventana.after(500, mover_astronauta, i + 1)

    mover_astronauta()

# Boton Start
botonStart = tk.Button(ventana_tablero, text="START", state="disabled", command=ejecutar_algoritmo_gui)
botonStart.place(x=900, y=368)

def actualizar_estado_start(*args):
    botonStart.config(state="normal" if despegable.get() and subOpciones.get() else "disabled")

# Eventos de selección
despegable.bind("<<ComboboxSelected>>", actualizar_estado_start)
subOpciones.bind("<<ComboboxSelected>>", actualizar_estado_start)

ventana.mainloop()
