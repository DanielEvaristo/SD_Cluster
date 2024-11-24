import tkinter as tk
from tkinter import ttk


def create_ui(thumbnails_cliente, thumbnails_procesados, video_player, root):
    root.title("Interfaz de Video")
    root.geometry("1000x600")
    root.configure(bg="white")  # Fondo blanco

    # Parte izquierda: Lista de videos cliente
    left_frame = tk.Frame(root, bg="lightgray", padx=10, pady=10)
    left_frame.grid(row=0, column=0, sticky="nswe", padx=5, pady=5)

    left_label = tk.Label(left_frame, text="Videos Disponibles", bg="lightgray", font=("Arial", 14, "bold"))
    left_label.pack(anchor="n", pady=10)

    # Contenedor para las miniaturas (centrado)
    left_thumbnails_frame = tk.Frame(left_frame, bg="lightgray")
    left_thumbnails_frame.pack(anchor="center", expand=True)

    for i, (file, image, path) in enumerate(thumbnails_cliente):
        thumbnail_button = tk.Button(
            left_thumbnails_frame,
            image=image,
            text=file,
            compound="top",
            command=lambda p=path: video_player.play_video(p),
            width=150,
            height=120,
            relief="groove",  # Estilo de los bordes
        )
        thumbnail_button.image = image
        row = i // 2
        col = i % 2
        thumbnail_button.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")

    # Parte central: Reproducción y botones
    center_frame = tk.Frame(root, bg="white", padx=5, pady=5)
    center_frame.grid(row=0, column=1, sticky="nswe", padx=5, pady=5)

    # Área de reproducción
    video_area = tk.Label(center_frame, bg="black", width=50, height=20)
    video_area.pack(fill="both", expand=True, pady=10)
    video_player.video_area = video_area

    # Botones de control
    button_frame = tk.Frame(center_frame, bg="white")
    button_frame.pack(pady=10)

    button_style = {"width": 12, "font": ("Arial", 10, "bold")}

    load_button = tk.Button(button_frame, text="Cargar", **button_style)
    load_button.grid(row=0, column=0, padx=10)

    send_button = tk.Button(button_frame, text="Enviar", **button_style)
    send_button.grid(row=0, column=1, padx=10)

    record_button = tk.Button(button_frame, text="Grabar", **button_style)
    record_button.grid(row=0, column=2, padx=10)

    stop_button = tk.Button(button_frame, text="Detener", command=video_player.stop_video, **button_style)
    stop_button.grid(row=0, column=3, padx=10)

    # Parte derecha: Videos procesados
    right_frame = tk.Frame(root, bg="lightgray", padx=10, pady=10)
    right_frame.grid(row=0, column=2, sticky="nswe", padx=5, pady=5)

    right_label = tk.Label(right_frame, text="Videos Procesados", bg="lightgray", font=("Arial", 14, "bold"))
    right_label.pack(anchor="n", pady=10)

    # Contenedor para las miniaturas procesadas (centrado)
    right_thumbnails_frame = tk.Frame(right_frame, bg="lightgray")
    right_thumbnails_frame.pack(anchor="center", expand=True)

    for i, (file, image, path) in enumerate(thumbnails_procesados):
        thumbnail_button = tk.Button(
            right_thumbnails_frame,
            image=image,
            text=file,
            compound="top",
            command=lambda p=path: video_player.play_video(p),
            width=150,
            height=120,
            relief="groove",  # Estilo de los bordes
        )
        thumbnail_button.image = image
        row = i // 2
        col = i % 2
        thumbnail_button.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")

    # Ajustar proporciones
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=2)  # La parte central tiene mayor peso
    root.grid_columnconfigure(2, weight=1)

    # Iniciar la interfaz
    root.mainloop()
