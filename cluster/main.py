import os
import socket
import threading
from video_utils import dividir_video, unir_videos

# Configuración del clúster
HOST = '127.0.0.1'
PORT = 5000
CLUSTER_PORT = 5001  # Puerto para recibir videos procesados de los nodos
RECEIVED_FOLDER = "./cluster_received"
PROCESSED_PARTS_FOLDER = "./processed_parts"
PROCESSED_VIDEOS_FOLDER = "./processed_videos"
VIDEO_FINAL_FOLDER = "./video_final"

NODES = [
    {"host": "127.0.0.1", "port": 6000},
    {"host": "127.0.0.1", "port": 6001},
]

# Crear carpetas si no existen
for folder in [RECEIVED_FOLDER, PROCESSED_PARTS_FOLDER, PROCESSED_VIDEOS_FOLDER, VIDEO_FINAL_FOLDER]:
    os.makedirs(folder, exist_ok=True)

# Para almacenar las partes recibidas
processed_parts = []
original_filename = ""


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
    global original_filename
    with conn:
        filename_length = conn.recv(4)
        filename_length = int.from_bytes(filename_length, "big")
        original_filename = conn.recv(filename_length).decode("utf-8")  # Guardar nombre original

        filepath = os.path.join(RECEIVED_FOLDER, original_filename)
        clear_folders()

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
    global processed_parts, original_filename
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
                processed_parts.append(filepath)

                # Verificar si se han recibido todas las partes
                if len(processed_parts) == len(NODES):
                    processed_parts.sort(key=lambda x: int(os.path.basename(x).split('_')[2].split('.')[0]))
                    
                    # Generar el nombre final con el original
                    final_filename = f"{os.path.splitext(original_filename)[0]}_FINAL.mp4"
                    video_final_path = unir_videos(processed_parts, VIDEO_FINAL_FOLDER, final_filename)
                    
                    processed_parts = []  # Reiniciar lista después de unir las partes

                    # Enviar el video final al cliente
                    send_video_to_client(client_host='127.0.0.1', client_port=5002, video_path=video_final_path)


def send_video_to_client(client_host, client_port, video_path):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((client_host, client_port))

            # Enviar el nombre del archivo
            filename = os.path.basename(video_path)
            filename_bytes = filename.encode("utf-8")
            filename_length = len(filename_bytes)
            client_socket.sendall(filename_length.to_bytes(4, "big"))
            client_socket.sendall(filename_bytes)

            # Enviar el contenido del archivo
            with open(video_path, "rb") as f:
                while (data := f.read(1024)):
                    client_socket.sendall(data)

            print(f"Video final enviado al cliente en {client_host}:{client_port}")
    except Exception as e:
        print(f"Error al enviar el video final al cliente: {e}")


def clear_folders():
    """
    Elimina todos los archivos en las carpetas del clúster antes de procesar un nuevo video.
    """
    folders_to_clear = [
        RECEIVED_FOLDER,
        PROCESSED_PARTS_FOLDER,
        PROCESSED_VIDEOS_FOLDER,
        VIDEO_FINAL_FOLDER,
    ]

    for folder in folders_to_clear:
        for file in os.listdir(folder):
            file_path = os.path.join(folder, file)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                    print(f"Archivo eliminado: {file_path}")
                elif os.path.isdir(file_path):
                    os.rmdir(file_path)
                    print(f"Directorio eliminado: {file_path}")
            except Exception as e:
                print(f"Error al eliminar {file_path}: {e}")


if __name__ == "__main__":
    start_cluster()
