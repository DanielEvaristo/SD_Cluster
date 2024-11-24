import os
import cv2
from tkinter import PhotoImage, Tk, messagebox
from PIL import Image, ImageTk
from ui import create_ui

# Rutas de las carpetas
VIDEOS_CLIENTE_FOLDER = "./videos_cliente"
VIDEOS_PROCESADOS_FOLDER = "./videos_procesados_c"

# Reproductor de video dentro de la interfaz
class VideoPlayer:
    def __init__(self, video_area):
        self.video_area = video_area
        self.cap = None
        self.running = False

    def play_video(self, video_path):
        # Detener el video actual antes de reproducir uno nuevo
        self.stop_video()

        if not os.path.exists(video_path):
            messagebox.showerror("Error", "El archivo de video no existe.")
            return

        self.cap = cv2.VideoCapture(video_path)
        self.running = True
        self.update_frame()

    def update_frame(self):
        if not self.running or not self.cap:
            return

        ret, frame = self.cap.read()
        if ret:
            # Convertir frame a formato compatible con tkinter
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (400, 300))  # Tamaño del área de reproducción
            img = ImageTk.PhotoImage(Image.fromarray(frame))

            # Actualizar el área de reproducción
            self.video_area.configure(image=img)
            self.video_area.image = img

            # Llamar a esta función de nuevo después de 25ms
            self.video_area.after(25, self.update_frame)
        else:
            self.stop_video()

    def stop_video(self):
        # Detener la reproducción y limpiar recursos
        self.running = False
        if self.cap:
            self.cap.release()
            self.cap = None
        self.video_area.configure(image=None)
        self.video_area.image = None

# Función para cargar miniaturas de videos
def get_video_thumbnails(folder, master):
    thumbnails = []
    try:
        for file in os.listdir(folder):
            if file.endswith((".mp4", ".avi", ".mkv")):
                video_path = os.path.join(folder, file)
                # Capturar la primera imagen del video como miniatura
                cap = cv2.VideoCapture(video_path)
                ret, frame = cap.read()
                if ret:
                    # Convertir el frame (BGR a RGB) y redimensionar
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frame = cv2.resize(frame, (120, 90))  # Tamaño de miniatura
                    image = ImageTk.PhotoImage(Image.fromarray(frame))
                    thumbnails.append((file, image, video_path))
                cap.release()
        return thumbnails
    except Exception as e:
        messagebox.showerror("Error", f"Error al cargar miniaturas: {e}")
        return []

# Función principal
def main():
    root = Tk()
    root.withdraw()  # Ocultar ventana principal hasta que carguemos las miniaturas

    thumbnails_cliente = get_video_thumbnails(VIDEOS_CLIENTE_FOLDER, root)
    thumbnails_procesados = get_video_thumbnails(VIDEOS_PROCESADOS_FOLDER, root)

    root.deiconify()  # Mostrar ventana principal

    video_player = VideoPlayer(None)  # Se inicializará en la UI
    create_ui(thumbnails_cliente, thumbnails_procesados, video_player, root)

if __name__ == "__main__":
    main()
