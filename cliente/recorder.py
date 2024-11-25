import cv2
import os
import time
from tkinter import messagebox


def grabar_video(output_folder):
    """
    Captura un video desde la cámara y lo guarda en la carpeta especificada.
    """
    cap = cv2.VideoCapture(0)  # Abrir la cámara
    if not cap.isOpened():
        messagebox.showerror("Error", "No se pudo acceder a la cámara.")
        return None

    # Configurar el nombre y la ruta del archivo de salida
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(output_folder, f"video_{timestamp}.mp4")

    # Configurar el formato de video y los codecs
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec para .mp4
    fps = 20.0
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    messagebox.showinfo("Información", "Presione 'Q' en la ventana para detener la grabación.")

    # Iniciar grabación
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        out.write(frame)  # Escribir el frame en el archivo de salida

        # Mostrar la captura en tiempo real
        cv2.imshow('Grabando...', frame)

        # Detener la grabación si se presiona 'Q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Liberar recursos
    cap.release()
    out.release()
    cv2.destroyAllWindows()

    messagebox.showinfo("Información", f"Grabación completada y guardada en: {output_path}")
    return output_path
