import threading
from recorder import grabar_video
from utils import cargar_video, actualizar_miniaturas
import os
from PIL import Image, ImageTk
from ffpyplayer.player import MediaPlayer
from tkinter import messagebox
import cv2
import tkinter as tk
from ui import create_ui
import socket

# Rutas de las carpetas
VIDEOS_CLIENTE_FOLDER = "./videos_cliente"
VIDEOS_PROCESADOS_FOLDER = "./videos_procesados_c"

if not os.path.exists(VIDEOS_CLIENTE_FOLDER):
    os.makedirs(VIDEOS_CLIENTE_FOLDER)
    
if not os.path.exists(VIDEOS_PROCESADOS_FOLDER):
    os.makedirs(VIDEOS_PROCESADOS_FOLDER)

class VideoPlayer:
    def __init__(self, video_area):
        self.video_area = video_area
        self.cap = None
        self.player = None
        self.running = False

    def play_video(self, video_path):
        # Detener cualquier video en reproducción antes de iniciar uno nuevo
        self.stop_video()

        if not os.path.exists(video_path):
            messagebox.showerror("Error", "El archivo de video no existe.")
            return

        self.cap = cv2.VideoCapture(video_path)
        self.player = MediaPlayer(video_path)  # Iniciar reproductor de audio y video
        self.running = True
        self.update_frame()

    def update_frame(self):
        if not self.running or not self.cap:
            return

        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Ajustar al tamaño del marco del video manteniendo la proporción
            frame_width, frame_height = frame.shape[1], frame.shape[0]
            max_width, max_height = 800, 450
            aspect_ratio = frame_width / frame_height

            if max_width / max_height > aspect_ratio:
                new_height = max_height
                new_width = int(max_height * aspect_ratio)
            else:
                new_width = max_width
                new_height = int(max_width / aspect_ratio)

            frame = cv2.resize(frame, (new_width, new_height))

            img = ImageTk.PhotoImage(Image.fromarray(frame))
            self.video_area.configure(image=img)
            self.video_area.image = img

            # Sincronizar audio con video
            audio_frame, val = self.player.get_frame()
            if val != 'eof' and audio_frame is not None:
                pass

            # Continuar actualizando el frame
            self.video_area.after(25, self.update_frame)
        else:
            self.stop_video()

    def stop_video(self):
        # Detener reproducción de video y audio
        self.running = False
        if self.cap:
            self.cap.release()
            self.cap = None
        if self.player:
            self.player.close_player()
            self.player = None
        # Limpiar el área de video
        self.video_area.configure(image=None)
        self.video_area.image = None


def get_video_thumbnails(folder):
    thumbnails = []
    try:
        for file in os.listdir(folder):
            if file.endswith((".mp4", ".avi", ".mkv")):
                video_path = os.path.join(folder, file)
                cap = cv2.VideoCapture(video_path)
                ret, frame = cap.read()
                if ret:
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frame = cv2.resize(frame, (120, 90))
                    image = ImageTk.PhotoImage(Image.fromarray(frame))
                    thumbnails.append((file, image, video_path))
                cap.release()
        return thumbnails
    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar miniaturas: {e}")
        return []
    
def enviar_video(video_path):
    HOST = '127.0.0.1'  # Dirección del servidor
    PORT = 5000         # Puerto del servidor

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect((HOST, PORT))

            # Enviar el tamaño del nombre del archivo
            filename = os.path.basename(video_path)
            filename_bytes = filename.encode("utf-8")
            filename_length = len(filename_bytes)
            client_socket.sendall(filename_length.to_bytes(4, "big"))  # Enviar longitud en 4 bytes
            client_socket.sendall(filename_bytes)  # Enviar el nombre del archivo

            # Enviar el contenido del archivo
            with open(video_path, 'rb') as f:
                while True:
                    data = f.read(1024)
                    if not data:
                        break
                    client_socket.sendall(data)
            print(f"Archivo enviado: {video_path}")
            messagebox.showinfo("Éxito", f"Archivo enviado: {filename}")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo enviar el archivo: {e}")

def recibir_video_procesado():
    HOST = '127.0.0.1'  # Dirección local para recibir el video procesado
    PORT = 5002         # Puerto para recibir el video procesado

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"Esperando video procesado en {HOST}:{PORT}...")

        while True:
            conn, addr = server_socket.accept()
            print(f"Conexión aceptada desde {addr}")
            with conn:
                filename_length = conn.recv(4)
                filename_length = int.from_bytes(filename_length, "big")
                filename = conn.recv(filename_length).decode("utf-8")

                filepath = os.path.join(VIDEOS_PROCESADOS_FOLDER, filename)
                with open(filepath, 'wb') as f:
                    while (data := conn.recv(1024)):
                        f.write(data)

                print(f"Video procesado recibido y guardado en: {filepath}")
                

def main():
    root = tk.Tk()
    root.withdraw()  # Ocultar ventana principal hasta que carguemos las miniaturas

    # Generar miniaturas iniciales
    thumbnails_cliente = actualizar_miniaturas(VIDEOS_CLIENTE_FOLDER)
    thumbnails_procesados = actualizar_miniaturas(VIDEOS_PROCESADOS_FOLDER)

    root.deiconify()  # Mostrar ventana principal

    # Crear el reproductor de video
    video_player = VideoPlayer(None)

    # Iniciar servidor para recibir video procesado
    threading.Thread(target=recibir_video_procesado, daemon=True).start()

    # Función para manejar el evento del botón "Cargar"
    def on_cargar(left_thumbnails_frame):
        video_path = cargar_video(VIDEOS_CLIENTE_FOLDER)
        if video_path:
            actualizar_thumbnails()

    # Función para actualizar la interfaz
    def actualizar_thumbnails():
        nonlocal thumbnails_cliente, thumbnails_procesados
        thumbnails_cliente = actualizar_miniaturas(VIDEOS_CLIENTE_FOLDER)
        thumbnails_procesados = actualizar_miniaturas(VIDEOS_PROCESADOS_FOLDER)
        create_ui(thumbnails_cliente, thumbnails_procesados, video_player, root, on_cargar, on_grabar, on_enviar, actualizar_thumbnails)

    # Función para manejar el evento del botón "Grabar" (con threading)
    def on_grabar(left_thumbnails_frame):
        def grabar_y_actualizar():
            grabar_video(VIDEOS_CLIENTE_FOLDER)
            actualizar_thumbnails()

        threading.Thread(target=grabar_y_actualizar).start()

    # Función para manejar el evento del botón "Enviar"
    def on_enviar(video_path):
        if not video_path or not os.path.exists(video_path):
            messagebox.showerror("Error", "No hay ningún video seleccionado o el archivo no existe.")
            return
        enviar_video(video_path)

    create_ui(thumbnails_cliente, thumbnails_procesados, video_player, root, on_cargar, on_grabar, on_enviar, actualizar_thumbnails)

if __name__ == "__main__":
    main()
