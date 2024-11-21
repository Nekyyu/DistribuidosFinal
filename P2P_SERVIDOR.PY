import socket
import threading
import numpy as np
import cv2
import time

clients = {}  
usernames = {}  


def conectar_cliente(client_socket, addr):
    #PRIMER MENSAJE ENVIADO  
    #client_socket.send(variable)


    username = client_socket.recv(1024)  # nombre de usuario
    clients[addr] = client_socket  # Almacenar el cliente 
    usernames[addr] = username  # Almacenar el nombre del cliente

    conectado = f"{username} se ha unido al chat."
    msg = conectado.encode()
    reenviar(msg, addr)

    print(f"Conexión establecida con {username} en {addr}")

    while True:
        try:
            msg = client_socket.recv(400000000)
            print(f"Mensaje recibido de {username}: {msg}")
            reenviar(msg, addr)  # Reenviar el mensaje cifrado a otros clientes
        except Exception as e:
            print(f"Error en la conexión con {addr}: {e}")
            break

    client_socket.close()
    del clients[addr]
    del usernames[addr]

    disconectado = f"{username} se ha desconectado."
    msg = disconectado.encode()
    reenviar(msg, addr)

    print(f"{username} se ha desconectado.")

def reenviar(message, from_addr):
    """Enviar el mensaje a todos los clientes conectados, excepto al que lo envió."""
    for addr, client_socket in clients.items():
        if addr != from_addr:
            try:
                client_socket.sendall(message)  # Enviar el mensaje cifrado
            except Exception as e:
                print(f"Error al enviar mensaje a {addr}: {e}")


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("127.0.0.0", 5000))
server_socket.listen(5)  
print("Servidor escuchando")

while True:
    try:
        client_socket, addr = server_socket.accept()
        thread = threading.Thread(target=conectar_cliente, args=(client_socket, addr))
        thread.start()
    except Exception as e:
        print(f"Error al aceptar la conexión: {e}")
