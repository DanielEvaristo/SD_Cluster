import os
import cv2

def dividir_video(filepath, output_folder, num_partes):
    """
    Divide un video en partes iguales.

    Args:
        filepath (str): Ruta del archivo de video.
        output_folder (str): Carpeta donde se guardarán las partes divididas.
        num_partes (int): Número de partes en las que dividir el video.

    Returns:
        list: Lista de rutas de las partes del video.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    cap = cv2.VideoCapture(filepath)
    if not cap.isOpened():
        raise Exception(f"Error al abrir el archivo de video: {filepath}")

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frames_por_parte = total_frames // num_partes
    ancho = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    alto = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    print(f"Total de frames: {total_frames}, Frames por parte: {frames_por_parte}, FPS: {fps}")

    partes = []
    for i in range(num_partes):
        output_path = os.path.join(output_folder, f"parte_{i + 1}.mp4")
        partes.append(output_path)

        # Crear el VideoWriter para cada parte
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (ancho, alto))

        # Escribir los frames de la parte actual
        for _ in range(frames_por_parte):
            ret, frame = cap.read()
            if not ret:
                break
            out.write(frame)

        out.release()

    # Si quedan frames extra, añadirlos a la última parte
    if total_frames % num_partes > 0:
        print("Distribuyendo frames extra a la última parte.")
        extra_writer = cv2.VideoWriter(partes[-1], cv2.VideoWriter_fourcc(*'mp4v'), fps, (ancho, alto))
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            extra_writer.write(frame)
        extra_writer.release()

    cap.release()
    return partes
