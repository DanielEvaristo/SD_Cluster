import os
from PIL import Image, ImageTk
from ffpyplayer.player import MediaPlayer
from tkinter import messagebox
import cv2
import tkinter as tk
from ui import create_ui

# Rutas de las carpetas
VIDEOS_CLIENTE_FOLDER = "./videos_cliente"
VIDEOS_PROCESADOS_FOLDER = "./videos_procesados_c"


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


def get_video_thumbnails(folder, master):
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


def main():
    root = tk.Tk()
    root.withdraw()  # Ocultar ventana principal hasta que carguemos las miniaturas

    thumbnails_cliente = get_video_thumbnails(VIDEOS_CLIENTE_FOLDER, root)
    thumbnails_procesados = get_video_thumbnails(VIDEOS_PROCESADOS_FOLDER, root)

    root.deiconify()  # Mostrar ventana principal

    video_player = VideoPlayer(None)  # Inicializar sin área de video, se asigna en la UI
    create_ui(thumbnails_cliente, thumbnails_procesados, video_player, root)


if __name__ == "__main__":
    main()
