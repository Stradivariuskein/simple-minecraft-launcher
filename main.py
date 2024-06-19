import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk
from PIL import Image, ImageTk
from os import system
import subprocess
import threading
import re
import os
import json

IMG_BG_PATH = "fondo.jpg"
PATH_PORTABLEMC = "./tools/portablemc.exe"
global VERSIONS
MODER_MANAGERS = ["forge", "fabric", "vanilla"]

global APP_FOLDER

WINDOWS_HEIGHT = 600
WINDOWS_WIDTH = 500
MIDLE_WIDTH = WINDOWS_WIDTH / 2


def exec_portablemc():
    nombre_usuario = entry_nombre.get()
    version_juego = combo_version.get()
    moder_manager = combo_moder_manager.get()
    if moder_manager == "vanilla":
        moder_manager = ""
    else:
        moder_manager += ':'

    if nombre_usuario:
        comando = [PATH_PORTABLEMC, 'start',
                   moder_manager+version_juego, "-u", nombre_usuario]
    else:
        comando = [PATH_PORTABLEMC, 'start', moder_manager+version_juego]

    proceso = subprocess.Popen(comando, stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT, text=True, encoding='utf-8', creationflags=subprocess.CREATE_NO_WINDOW)

    while True:
        linea = proceso.stdout.readline()
        if not linea:
            break
        consola.insert(tk.END, linea)
        consola.see(tk.END)


def play():
    global APP_FOLDER
    nombre_usuario = entry_nombre.get()
    version_juego = combo_version.get()
    moder_manager = combo_moder_manager.get()

    # Datos que quieres guardar
    config_data = {
        'user_name': nombre_usuario,
        'version': version_juego,
        'mod_manager': moder_manager
    }

    config_file_path = os.path.join(APP_FOLDER, 'config.json')

    # Guardar datos en un archivo JSON
    with open(config_file_path, 'w') as config_file:
        json.dump(config_data, config_file)

    threading.Thread(target=exec_portablemc, daemon=True).start()
    # if nombre_usuario:
    #     console_out = subprocess.run(
    #         [PATH_PORTABLEMC, 'start', version_juego, "-u", nombre_usuario], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', errors='ignore')
    # else:
    #     console_out = subprocess.run(
    #         [PATH_PORTABLEMC, 'start', version_juego], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', errors='ignore')
    print(f"Nombre de usuario: {nombre_usuario}")
    print(f"Versión del juego: {version_juego}")
    # print(console_out.stdout)


def filter_versions(texto):
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
        [PATH_PORTABLEMC, 'search'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', errors='ignore', creationflags=subprocess.CREATE_NO_WINDOW)
    list_vercions = result.stdout
    list_of_versions = []
    # la version 1.0 y 1.1 dan problemas. las ignoramos
    for line_version in list_vercions.split("\n")[:-2]:
        if line_version.find("release") > -1:
            version = filter_versions(line_version)[0]
            list_of_versions.append(version)

    VERSIONS = list_of_versions


def get_configs(app_folder):
    print(f"Ruta de la carpeta: {app_folder}")
    config_file_path = os.path.join(app_folder, 'config.json')
    if os.path.exists(config_file_path):
        with open(config_file_path, 'r') as config_file:
            config_data = json.load(config_file)
            entry_nombre.insert(0, config_data['user_name'])
            combo_version.set(config_data['version'])
            combo_moder_manager.set(config_data['mod_manager'])


if __name__ == "__main__":
    # Obtén la ruta a la carpeta AppData\Local del usuario

    appdata_local = os.getenv('LOCALAPPDATA')
    APP_FOLDER = os.path.join(appdata_local, 'simple-mc-launcher')

    # Crea la carpeta si no existe
    if not os.path.exists(APP_FOLDER):
        os.makedirs(APP_FOLDER)
    get_versiones()

    # Crear la ventana principal
    root = tk.Tk()
    root.title("Simple mc launcher")
    root.geometry(f"{WINDOWS_WIDTH}x{WINDOWS_HEIGHT}")
    root.resizable(False, False)

    # Configurar el fondo usando Canvas
    canvas = tk.Canvas(root, width=WINDOWS_WIDTH, height=WINDOWS_HEIGHT)
    canvas.pack(fill="both", expand=True)

    # Cargar y redimensionar la imagen de fondo
    # Reemplaza con la ruta a tu imagen
    background_image = Image.open(IMG_BG_PATH)
    background_photo = ImageTk.PhotoImage(
        background_image.resize((WINDOWS_WIDTH, WINDOWS_HEIGHT)))
    canvas.create_image(0, 0, image=background_photo, anchor='nw')

    # Crear los widgets directamente sobre el canvas
    # Campo de texto para el nombre de usuario
    label_nombre = tk.Label(root, text="Nombre de usuario:", bg='white')

    canvas.create_window(MIDLE_WIDTH, 40, window=label_nombre)
    entry_nombre = tk.Entry(root, bd=0, highlightthickness=0, bg='white')

    canvas.create_window(MIDLE_WIDTH, 70, window=entry_nombre)

    # Lista desplegable para seleccionar la versión del juego
    label_version = tk.Label(root, text="Versión del juego:", bg='white')

    canvas.create_window(170, 130, window=label_version)
    combo_version = ttk.Combobox(
        root, values=VERSIONS)
    combo_version.set(VERSIONS[0])  # Establece la opción predeterminada
    # Hace que la combobox sea de solo lectura
    combo_version.state(['readonly'])

    canvas.create_window(170, 160, window=combo_version)

    # Lista desplegable para seleccionar la versión del mode manager
    label_moder_manager = tk.Label(root, text="Mod manager:", bg='white')

    canvas.create_window(325, 130, window=label_moder_manager)
    combo_moder_manager = ttk.Combobox(
        root, values=MODER_MANAGERS)
    # Establece la opción predeterminada
    combo_moder_manager.set(MODER_MANAGERS[2])
    # Hace que la combobox sea de solo lectura
    combo_moder_manager.state(['readonly'])

    canvas.create_window(325, 160, window=combo_moder_manager)
    get_configs(APP_FOLDER)
    # Botón "Jugar"
    button_jugar = tk.Button(root, text="Jugar", command=play, bg='white')

    canvas.create_window(MIDLE_WIDTH, 225, window=button_jugar)

    consola = ScrolledText(root, wrap=tk.WORD, width=55, height=20)
    canvas.create_window(MIDLE_WIDTH, 425, window=consola)

    # Iniciar el bucle principal de la aplicación
    root.mainloop()
