import os
import cv2

def editar_video(filepath, output_folder):
    """
    Aplica un efecto cromático (COLORMAP_JET) al video y lo guarda con el nombre estándar.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Cambiar el nombre del archivo procesado
    base_name = os.path.basename(filepath).replace("parte_", "processed_parte_")
    output_path = os.path.join(output_folder, base_name)
    
    cap = cv2.VideoCapture(filepath)
    if not cap.isOpened():
        raise Exception(f"Error al abrir el archivo de video: {filepath}")

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    ancho = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    alto = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(output_path, fourcc, fps, (ancho, alto))

    print(f"Editando video (cromático): {filepath}")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # Apply chromatic effect
        chromatic_frame = cv2.applyColorMap(frame, cv2.COLORMAP_JET)
        out.write(chromatic_frame)

    cap.release()
    out.release()
    print(f"Video procesado y guardado en: {output_path}")
    return output_path


def editar_video_bn(filepath, output_folder):
    """
    Convierte el video a blanco y negro y lo guarda con el nombre estándar.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Cambiar el nombre del archivo procesado
    base_name = os.path.basename(filepath).replace("parte_", "processed_parte_")
    output_path = os.path.join(output_folder, base_name)

    cap = cv2.VideoCapture(filepath)
    if not cap.isOpened():
        raise Exception(f"Error al abrir el archivo de video: {filepath}")

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    ancho = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    alto = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(output_path, fourcc, fps, (ancho, alto))

    print(f"Editando video (blanco y negro): {filepath}")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # Convert frame to grayscale
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Convert back to BGR for saving in the output video
        bw_frame = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2BGR)
        out.write(bw_frame)

    cap.release()
    out.release()
    print(f"Video procesado y guardado en: {output_path}")
    return output_path


def editar_video_desenfoque(filepath, output_folder):
    """
    Aplica un efecto de desenfoque gaussiano al video y lo guarda con el nombre estándar.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Cambiar el nombre del archivo procesado
    base_name = os.path.basename(filepath).replace("parte_", "processed_parte_")
    output_path = os.path.join(output_folder, base_name)

    cap = cv2.VideoCapture(filepath)
    if not cap.isOpened():
        raise Exception(f"Error al abrir el archivo de video: {filepath}")

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    ancho = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    alto = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(output_path, fourcc, fps, (ancho, alto))

    print(f"Editando video (desenfoque): {filepath}")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # Apply Gaussian blur
        blurred_frame = cv2.GaussianBlur(frame, (15, 15), 0)
        out.write(blurred_frame)

    cap.release()
    out.release()
    print(f"Video procesado y guardado en: {output_path}")
    return output_path

def editar_video_bordeado(filepath, output_folder):
    """
    Resalta los bordes del video usando el operador Canny.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    base_name = os.path.basename(filepath).replace("parte_", "processed_parte_")
    output_path = os.path.join(output_folder, base_name)

    cap = cv2.VideoCapture(filepath)
    if not cap.isOpened():
        raise Exception(f"Error al abrir el archivo de video: {filepath}")

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    ancho = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    alto = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(output_path, fourcc, fps, (ancho, alto))

    print(f"Editando video (bordeado): {filepath}")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray_frame, 100, 200)
        edge_frame = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
        out.write(edge_frame)

    cap.release()
    out.release()
    print(f"Video procesado y guardado en: {output_path}")
    return output_path

def editar_video_invertir(filepath, output_folder):
    """
    Invierte los colores del video (efecto negativo).
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    base_name = os.path.basename(filepath).replace("parte_", "processed_parte_")
    output_path = os.path.join(output_folder, base_name)

    cap = cv2.VideoCapture(filepath)
    if not cap.isOpened():
        raise Exception(f"Error al abrir el archivo de video: {filepath}")

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    ancho = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    alto = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(output_path, fourcc, fps, (ancho, alto))

    print(f"Editando video (inversión de colores): {filepath}")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        inverted_frame = cv2.bitwise_not(frame)
        out.write(inverted_frame)

    cap.release()
    out.release()
    print(f"Video procesado y guardado en: {output_path}")
    return output_path
