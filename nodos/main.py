import os
import socket
from video_utils import editar_video_invertir

# Configuración del nodo
HOST = '127.0.0.1'  # Dirección local del nodo
PORT = 6000         # Puerto del nodo
CLUSTER_HOST = '127.0.0.1'  # Dirección del servidor del cluster
CLUSTER_PORT = 5001         # Puerto para devolver los archivos al cluster
RECEIVED_FOLDER = "./node_received"
PROCESSED_FOLDER = "./node_processed"

if not os.path.exists(RECEIVED_FOLDER):
    os.makedirs(RECEIVED_FOLDER)

if not os.path.exists(PROCESSED_FOLDER):
    os.makedirs(PROCESSED_FOLDER)

def start_node():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"Nodo escuchando en {HOST}:{PORT}...")

        while True:
            conn, addr = server_socket.accept()
            print(f"Conexión aceptada desde {addr}")
            with conn:
                filename_length = conn.recv(4)
                filename_length = int.from_bytes(filename_length, "big")
                filename = conn.recv(filename_length).decode("utf-8")

                filepath = os.path.join(RECEIVED_FOLDER, filename)
                with open(filepath, 'wb') as f:
                    while (data := conn.recv(1024)):
                        f.write(data)

                print(f"Archivo recibido: {filepath}")

                # Editar el video
                processed_path = editar_video_invertir(filepath, PROCESSED_FOLDER)

                # Enviar el archivo procesado de vuelta al cluster
                send_back_to_cluster(processed_path)

def send_back_to_cluster(filepath):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((CLUSTER_HOST, CLUSTER_PORT))
            
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

            print(f"Archivo procesado enviado al cluster: {filepath}")
    except Exception as e:
        print(f"Error al enviar el archivo procesado al cluster: {e}")

if __name__ == "__main__":
    start_node()
