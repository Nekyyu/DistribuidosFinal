import socket
import threading
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import cv2
import time

ip = "127.0.0.1"
port = 5000
socket_client = ""
chat_display = ""
message_entry = ""


def recibir_msgs():
    while True:
        try:
            # Recibir el mensaje cifrado del servidor
            msg = socket_client.recv(400000000)
            if msg:
                if msg.startswith(b"FRAME:"):
                    archivo_bytes = msg[6:]
                    guardar_archivo(archivo_bytes)
                    fgbg = cv2.createBackgroundSubtractorKNN(history=500, dist2Threshold=400, detectShadows=False)


        except Exception as e:
            print(f"Error al recibir el mensaje: {e}")


def update_chat(message):
    """Actualiza la ventana de chat con nuevos mensajes."""
    chat_display.config(state='normal')
    chat_display.insert(END, message)
    chat_display.config(state='disabled')

"""
COSAS A USAR

    while(ret):
        i=1
        ret, frame = cap.read()

"""
def mandar_archivo():
    """Envía un archivo seleccionado."""
    file_path = filedialog.askopenfilename()
    cap = cv2.VideoCapture(file_path)

    if file_path:
        try:
            with open(file_path, "rb") as file:
                archivo_bytes = file.read()
                socket_client.sendall(b"FILE:" + archivo_bytes)
                update_chat(f"Tú has enviado un archivo: {file_path}\n")
        except Exception as e:
            print(f"Error al enviar el archivo: {e}")


def guardar_archivo(archivo_bytes):
    """Guarda el archivo recibido."""
    file_path = filedialog.asksaveasfilename()
    if file_path:
        try:
            with open(file_path, "wb") as file:
                file.write(archivo_bytes)
                update_chat(f"Archivo recibido y guardado en: {file_path}\n")
        except Exception as e:
            print(f"Error al guardar el archivo: {e}")


# Crear la ventana raíz de tkinter
root = Tk()
root.title("Chat")

frm = ttk.Frame(root, padding=10)
frm.grid(row=0, column=0)

chat_display = Text(frm, height=15, width=50, state='disabled')
chat_display.grid(column=0, row=0, columnspan=3)

message_entry = ttk.Entry(frm, width=30)
message_entry.grid(column=0, row=2)

archivo_button = ttk.Button(frm, text="Enviar Archivo", command=mandar_archivo)
archivo_button.grid(column=2, row=2)

# Conectar al servidor
try:
    socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_client.connect((ip, port))

    threading.Thread(target=recibir_msgs, daemon=True).start()
except Exception as e:
    print(f"Error al conectar al servidor: {e}")
# Iniciar la ventana de tkinter
root.mainloop()


