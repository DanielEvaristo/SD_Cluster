import os
import socket
import threading
from video_utils import dividir_video

# Configuración del servidor
HOST = '127.0.0.1'  # Dirección local
PORT = 5000         # Puerto para la conexión
RECEIVED_FOLDER = "./cluster_received"
PROCESSED_PARTS_FOLDER = "./processed_parts"

# Nodos
NODES = [
    {"host": "127.0.0.1", "port": 6000},
    {"host": "127.0.0.1", "port": 6001},
]

if not os.path.exists(RECEIVED_FOLDER):
    os.makedirs(RECEIVED_FOLDER)

if not os.path.exists(PROCESSED_PARTS_FOLDER):
    os.makedirs(PROCESSED_PARTS_FOLDER)


def enviar_archivo(host, port, filepath):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((host, port))
            
            # Enviar el nombre del archivo
            filename = os.path.basename(filepath)
            filename_bytes = filename.encode("utf-8")
            filename_length = len(filename_bytes)
            client_socket.sendall(filename_length.to_bytes(4, "big"))
            client_socket.sendall(filename_bytes)
            
            # Enviar el contenido del archivo
            with open(filepath, "rb") as f:
                while (data := f.read(1024)):
                    client_socket.sendall(data)

            print(f"Archivo enviado a nodo {host}:{port}")
    except Exception as e:
        print(f"Error al enviar archivo al nodo {host}:{port}: {e}")


def procesar_video(filepath):
    print(f"Procesando video: {filepath}")
    try:
        # Dividir el video en partes según la cantidad de nodos
        partes = dividir_video(filepath, PROCESSED_PARTS_FOLDER, len(NODES))
        
        # Enviar cada parte a su nodo correspondiente
        for i, nodo in enumerate(NODES):
            parte_path = partes[i]
            enviar_archivo(nodo["host"], nodo["port"], parte_path)
    except Exception as e:
        print(f"Error al procesar el video: {e}")


def manejar_conexion(conn, addr):
    with conn:
        # Recibir el nombre del archivo
        filename_length = conn.recv(4)  # Leer los primeros 4 bytes para obtener la longitud
        filename_length = int.from_bytes(filename_length, "big")
        filename = conn.recv(filename_length).decode("utf-8")  # Recibir el nombre con longitud específica

        if not filename:
            return
        
        filepath = os.path.join(RECEIVED_FOLDER, filename)

        # Recibir el archivo
        with open(filepath, 'wb') as f:
            while (data := conn.recv(1024)):
                f.write(data)
        
        print(f"Archivo recibido y guardado en: {filepath}")

        # Procesar el video recibido
        procesar_video(filepath)


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"Servidor escuchando en {HOST}:{PORT}...")

        while True:
            conn, addr = server_socket.accept()
            print(f"Conexión aceptada desde {addr}")
            threading.Thread(target=manejar_conexion, args=(conn, addr)).start()


if __name__ == "__main__":
    start_server()
