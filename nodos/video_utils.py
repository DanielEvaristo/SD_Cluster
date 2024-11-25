import cv2
import os

def procesar_video(filepath, output_path):
    """
    Editar la parte del video (aplicar un filtro de contraste en blanco y negro).
    """
    cap = cv2.VideoCapture(filepath)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height), isColor=False)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Convertir a escala de grises
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        out.write(gray_frame)
    
    cap.release()
    out.release()
    print(f"Video procesado y guardado en: {output_path}")


def guardar_archivo(conn, filepath):
    """
    Recibe un archivo del cluster y lo guarda en el nodo.
    """
    with open(filepath, 'wb') as f:
        while (data := conn.recv(1024)):
            f.write(data)
    print(f"Archivo guardado en: {filepath}")


def enviar_archivo(conn, filepath):
    """
    Envía un archivo procesado de vuelta al cluster.
    """
    filename = os.path.basename(filepath)
    filename_bytes = filename.encode("utf-8")
    filename_length = len(filename_bytes)
    conn.sendall(filename_length.to_bytes(4, "big"))
    conn.sendall(filename_bytes)

    with open(filepath, "rb") as f:
        while (data := f.read(1024)):
            conn.sendall(data)
    print(f"Archivo enviado: {filepath}")
