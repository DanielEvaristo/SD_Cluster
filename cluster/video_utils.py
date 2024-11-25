import os
import cv2


def dividir_video(filepath, output_folder, num_partes):
    """
    Divide un video en partes iguales.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    cap = cv2.VideoCapture(filepath)
    if not cap.isOpened():
        raise Exception(f"Error al abrir el archivo de video: {filepath}")

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    ancho = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    alto = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    frames_por_parte = total_frames // num_partes
    frames_sobrantes = total_frames % num_partes

    print(f"Total de frames: {total_frames}, Frames por parte: {frames_por_parte}, FPS: {fps}, Frames sobrantes: {frames_sobrantes}")

    partes = []
    for i in range(num_partes):
        output_path = os.path.join(output_folder, f"parte_{i + 1}.mp4")
        partes.append(output_path)

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (ancho, alto))

        num_frames_actual = frames_por_parte + (1 if i < frames_sobrantes else 0)

        for _ in range(num_frames_actual):
            ret, frame = cap.read()
            if not ret:
                break
            out.write(frame)

        out.release()

    cap.release()
    return partes


def unir_videos(partes, output_folder, output_filename="video_final.mp4"):
    """
    Une múltiples videos en un solo archivo y los guarda en una carpeta.
    """
    if not partes:
        raise ValueError("No se proporcionaron partes para unir.")

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    output_path = os.path.join(output_folder, output_filename)

    cap = cv2.VideoCapture(partes[0])
    if not cap.isOpened():
        raise Exception(f"Error al abrir el archivo de video: {partes[0]}")

    ancho = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    alto = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    cap.release()

    out = cv2.VideoWriter(output_path, fourcc, fps, (ancho, alto))

    for parte in partes:
        cap = cv2.VideoCapture(parte)
        if not cap.isOpened():
            raise Exception(f"Error al abrir el archivo de video: {parte}")

        while True:
            ret, frame = cap.read()
            if not ret:
                break
            out.write(frame)

        cap.release()

    out.release()
    print(f"Video final guardado en: {output_path}")
    return output_path
