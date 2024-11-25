import os
import socket

# Configuración del servidor
HOST = '127.0.0.1'  # Dirección local
PORT = 5000         # Puerto para la conexión
RECEIVED_FOLDER = "./cluster_received"

if not os.path.exists(RECEIVED_FOLDER):
    os.makedirs(RECEIVED_FOLDER)

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"Servidor escuchando en {HOST}:{PORT}...")

        while True:
            conn, addr = server_socket.accept()
            print(f"Conexión aceptada desde {addr}")
            with conn:
                # Recibir el nombre del archivo
                filename_length = conn.recv(4)  # Leer los primeros 4 bytes para obtener la longitud
                filename_length = int.from_bytes(filename_length, "big")
                filename = conn.recv(filename_length).decode("utf-8")  # Recibir el nombre con longitud específica

                if not filename:
                    continue
                filepath = os.path.join(RECEIVED_FOLDER, filename)

                # Recibir el archivo
                with open(filepath, 'wb') as f:
                    while True:
                        data = conn.recv(1024)
                        if not data:
                            break
                        f.write(data)
                print(f"Archivo recibido y guardado en: {filepath}")

if __name__ == "__main__":
    start_server()
