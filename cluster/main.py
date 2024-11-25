import os
import socket
import threading
from video_utils import dividir_video, unir_videos

# Configuración del cluster
HOST = '127.0.0.1'
PORT = 5000
CLUSTER_PORT = 5001  # Puerto para recibir videos procesados de los nodos
RECEIVED_FOLDER = "./cluster_received"
PROCESSED_PARTS_FOLDER = "./processed_parts"
PROCESSED_VIDEOS_FOLDER = "./processed_videos"

NODES = [
    {"host": "127.0.0.1", "port": 6000},
    {"host": "127.0.0.1", "port": 6001},
]

if not os.path.exists(RECEIVED_FOLDER):
    os.makedirs(RECEIVED_FOLDER)

if not os.path.exists(PROCESSED_PARTS_FOLDER):
    os.makedirs(PROCESSED_PARTS_FOLDER)

if not os.path.exists(PROCESSED_VIDEOS_FOLDER):
    os.makedirs(PROCESSED_VIDEOS_FOLDER)

def start_cluster():
    threading.Thread(target=receive_processed_parts).start()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"Servidor escuchando en {HOST}:{PORT}...")

        while True:
            conn, addr = server_socket.accept()
            print(f"Conexión aceptada desde {addr}")
            threading.Thread(target=handle_connection, args=(conn, addr)).start()

def handle_connection(conn, addr):
    with conn:
        filename_length = conn.recv(4)
        filename_length = int.from_bytes(filename_length, "big")
        filename = conn.recv(filename_length).decode("utf-8")

        filepath = os.path.join(RECEIVED_FOLDER, filename)
        with open(filepath, 'wb') as f:
            while (data := conn.recv(1024)):
                f.write(data)

        print(f"Archivo recibido y guardado en: {filepath}")

        # Dividir y enviar a nodos
        process_video(filepath)

def process_video(filepath):
    try:
        partes = dividir_video(filepath, PROCESSED_PARTS_FOLDER, len(NODES))
        for i, nodo in enumerate(NODES):
            parte_path = partes[i]
            send_to_node(nodo["host"], nodo["port"], parte_path)
    except Exception as e:
        print(f"Error al procesar el video: {e}")

def send_to_node(host, port, filepath):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((host, port))

            filename = os.path.basename(filepath)
            filename_bytes = filename.encode("utf-8")
            filename_length = len(filename_bytes)
            client_socket.sendall(filename_length.to_bytes(4, "big"))
            client_socket.sendall(filename_bytes)

            with open(filepath, "rb") as f:
                while (data := f.read(1024)):
                    client_socket.sendall(data)

            print(f"Archivo enviado al nodo {host}:{port}")
    except Exception as e:
        print(f"Error al enviar al nodo {host}:{port}: {e}")

def receive_processed_parts():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, CLUSTER_PORT))
        server_socket.listen()
        print(f"Cluster escuchando en {HOST}:{CLUSTER_PORT} para partes procesadas...")

        while True:
            conn, addr = server_socket.accept()
            print(f"Conexión aceptada desde {addr}")
            with conn:
                filename_length = conn.recv(4)
                filename_length = int.from_bytes(filename_length, "big")
                filename = conn.recv(filename_length).decode("utf-8")

                filepath = os.path.join(PROCESSED_VIDEOS_FOLDER, filename)
                with open(filepath, 'wb') as f:
                    while (data := conn.recv(1024)):
                        f.write(data)

                print(f"Parte procesada recibida: {filepath}")

if __name__ == "__main__":
    start_cluster()
