import socket
import os
import time

# Configuración del servidor
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5000
RECEIVED_FOLDER = "cluster_received"
PROCESSED_FOLDER = "processed_videos"

# Crear carpetas si no existen
os.makedirs(RECEIVED_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

def process_video(file_path):
    """Simula el procesamiento del video y crea un archivo procesado."""
    processed_path = os.path.join(PROCESSED_FOLDER, f"processed_{os.path.basename(file_path)}")
    # Aquí podrías agregar el procesamiento real del video
    time.sleep(5)  # Simula tiempo de procesamiento
    with open(file_path, "rb") as input_file, open(processed_path, "wb") as output_file:
        output_file.write(input_file.read())  # Simula el archivo procesado
    return processed_path

def handle_client(client_socket, client_address):
    """Maneja la conexión con un cliente."""
    try:
        while True:
            # Recibir el tamaño del nombre del archivo
            file_name_size = client_socket.recv(4)
            if not file_name_size:
                print(f"El cliente {client_address} cerró la conexión.")
                break
            file_name_size = int.from_bytes(file_name_size, "big")

            # Recibir el nombre del archivo
            file_name = client_socket.recv(file_name_size).decode()

            # Guardar el archivo recibido
            file_path = os.path.join(RECEIVED_FOLDER, file_name)
            print(f"Recibiendo archivo: {file_name}...")
            with open(file_path, "wb") as video_file:
                while True:
                    data = client_socket.recv(4096)
                    if not data:
                        break
                    video_file.write(data)
            print(f"Video recibido y guardado en: {file_path}")

            # Procesar el archivo recibido
            print(f"Procesando el archivo: {file_name}...")
            processed_path = process_video(file_path)
            print(f"Archivo procesado: {processed_path}")

            # Enviar el archivo procesado de regreso al cliente
            print(f"Enviando archivo procesado al cliente {client_address}...")
            file_name_processed = os.path.basename(processed_path).encode()
            file_name_size = len(file_name_processed).to_bytes(4, "big")
            client_socket.send(file_name_size)
            client_socket.send(file_name_processed)

            with open(processed_path, "rb") as processed_file:
                while chunk := processed_file.read(4096):
                    client_socket.send(chunk)
            print(f"Archivo procesado enviado al cliente {client_address}.")
    except Exception as e:
        print(f"Error al manejar al cliente {client_address}: {e}")
    finally:
        client_socket.close()

def start_server():
    """Inicia el servidor del cluster para recibir videos."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)
    print(f"Servidor iniciado en {SERVER_HOST}:{SERVER_PORT}")

    while True:
        print("Esperando conexión del cliente...")
        client_socket, client_address = server_socket.accept()
        print(f"Conexión aceptada de {client_address}")
        handle_client(client_socket, client_address)

if __name__ == "__main__":
    start_server()
