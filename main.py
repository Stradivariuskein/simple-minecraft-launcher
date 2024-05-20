import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk
from PIL import Image, ImageTk
from os import system
import subprocess
import threading
import re

PATH_PORTABLEMC = "./tools/portablemc.exe"
global VERSIONS

WINDOWS_HEIGHT = 600
WINDOWS_WIDTH = 500
MIDLE_WIDTH = WINDOWS_WIDTH / 2


def ejecutar_comando():
    nombre_usuario = entry_nombre.get()
    version_juego = combo_version.get()
    if nombre_usuario:
        comando = [PATH_PORTABLEMC, 'start',
                   version_juego, "-u", nombre_usuario]
    else:
        comando = [PATH_PORTABLEMC, 'start', version_juego]

    proceso = subprocess.Popen(comando, stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT, text=True, encoding='utf-8')

    while True:
        linea = proceso.stdout.readline()
        if not linea:
            break
        consola.insert(tk.END, linea)
        consola.see(tk.END)


def jugar():
    nombre_usuario = entry_nombre.get()
    version_juego = combo_version.get()

    threading.Thread(target=ejecutar_comando, daemon=True).start()
    # if nombre_usuario:
    #     console_out = subprocess.run(
    #         [PATH_PORTABLEMC, 'start', version_juego, "-u", nombre_usuario], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', errors='ignore')
    # else:
    #     console_out = subprocess.run(
    #         [PATH_PORTABLEMC, 'start', version_juego], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', errors='ignore')
    print(f"Nombre de usuario: {nombre_usuario}")
    print(f"Versión del juego: {version_juego}")
    # print(console_out.stdout)


def filtrar_versiones(texto):
    # Expresión regular para coincidir con las versiones de software
    patron = r"\b\d+\.\d+\.\d+\b"

    # Encontrar todas las coincidencias en el texto
    versiones = re.findall(patron, texto)
    if not versiones:
        patron = r"\s+(\d+\.\d+(\.\d+)?)"
        versiones = re.findall(patron, texto)[0]

    return versiones


def get_versiones():
    global VERSIONS
    result = subprocess.run(
        [PATH_PORTABLEMC, 'search'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', errors='ignore')
    list_vercions = result.stdout
    list_of_versions = []
    # la version 1.0 y 1.1 dan problemas. las ignoramos
    for line_version in list_vercions.split("\n")[:-2]:
        if line_version.find("release") > -1:
            version = filtrar_versiones(line_version)[0]
            list_of_versions.append(version)

    VERSIONS = list_of_versions


get_versiones()

# Crear la ventana principal
root = tk.Tk()
root.title("Juego")
root.geometry(f"{WINDOWS_WIDTH}x{WINDOWS_HEIGHT}")
root.resizable(False, False)

# Configurar el fondo usando Canvas
canvas = tk.Canvas(root, width=WINDOWS_WIDTH, height=WINDOWS_HEIGHT)
canvas.pack(fill="both", expand=True)

# Cargar y redimensionar la imagen de fondo
# Reemplaza con la ruta a tu imagen
background_image = Image.open("fondo.jpg")
background_photo = ImageTk.PhotoImage(
    background_image.resize((WINDOWS_WIDTH, WINDOWS_HEIGHT)))
canvas.create_image(0, 0, image=background_photo, anchor='nw')

# Crear los widgets directamente sobre el canvas
# Campo de texto para el nombre de usuario
label_nombre = tk.Label(root, text="Nombre de usuario:", bg='white')
# Ajusta las coordenadas según sea necesario
canvas.create_window(MIDLE_WIDTH, 100, window=label_nombre)
entry_nombre = tk.Entry(root, bd=0, highlightthickness=0, bg='white')
# Ajusta las coordenadas según sea necesario
canvas.create_window(MIDLE_WIDTH, 130, window=entry_nombre)

# Lista desplegable para seleccionar la versión del juego
label_version = tk.Label(root, text="Versión del juego:", bg='white')
# Ajusta las coordenadas según sea necesario
canvas.create_window(MIDLE_WIDTH, 160, window=label_version)
combo_version = ttk.Combobox(
    root, values=VERSIONS)
# Ajusta las coordenadas según sea necesario
canvas.create_window(MIDLE_WIDTH, 190, window=combo_version)

# Botón "Jugar"
button_jugar = tk.Button(root, text="Jugar", command=jugar, bg='white')
# Ajusta las coordenadas según sea necesario
canvas.create_window(MIDLE_WIDTH, 230, window=button_jugar)

consola = ScrolledText(root, wrap=tk.WORD, width=55, height=20)
canvas.create_window(MIDLE_WIDTH, 425, window=consola)

# Iniciar el bucle principal de la aplicación
root.mainloop()
