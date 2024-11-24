import os
import shutil
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2


def cargar_video(folder):
    """
    Abre un cuadro de diálogo para seleccionar un archivo de video y lo guarda en la carpeta especificada.
    """
    file_path = filedialog.askopenfilename(
        title="Seleccionar un archivo de video",
        filetypes=[("Archivos de video", "*.mp4 *.avi *.mkv")]
    )
    if not file_path:
        return None  # Si no se selecciona un archivo, no se hace nada

    # Copiar el archivo al directorio especificado
    try:
        filename = os.path.basename(file_path)
        destination = os.path.join(folder, filename)
        shutil.copy(file_path, destination)
        return destination  # Retornar la ruta del archivo copiado
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar el video: {e}")
        return None


def actualizar_miniaturas(folder):
    """
    Genera una lista de miniaturas para todos los videos en la carpeta especificada.
    """
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
        messagebox.showerror("Error", f"Error al actualizar miniaturas: {e}")
        return []
