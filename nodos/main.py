import os
import socket

# Configuración del nodo
HOST = '127.0.0.1'  # Dirección local del nodo
PORT = 6000         # Puerto del nodo
PROCESSED_FOLDER = "./node_processed"

if not os.path.exists(PROCESSED_FOLDER):
    os.makedirs(PROCESSED_FOLDER)


def start_node():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as node_socket:
        node_socket.bind((HOST, PORT))
        node_socket.listen()
        print(f"Nodo escuchando en {HOST}:{PORT}...")

        while True:
            conn, addr = node_socket.accept()
            print(f"Conexión aceptada desde {addr}")
            with conn:
                # Recibir el nombre del archivo
                filename_length = conn.recv(4)
                filename_length = int.from_bytes(filename_length, "big")
                filename = conn.recv(filename_length).decode("utf-8")

                if not filename:
                    continue
                
                filepath = os.path.join(PROCESSED_FOLDER, filename)

                # Recibir el archivo
                with open(filepath, 'wb') as f:
                    while (data := conn.recv(1024)):
                        f.write(data)
                
                print(f"Parte recibida y guardada en: {filepath}")


if __name__ == "__main__":
    start_node()
