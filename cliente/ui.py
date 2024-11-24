import tkinter as tk
def create_ui(thumbnails_cliente, thumbnails_procesados, video_player, root):
    root.title("Interfaz de Video")
    root.geometry("1000x600")
    root.configure(bg="white")  # Fondo blanco
    root.state('zoomed')  # Inicia en pantalla completa

    # Parte izquierda: Lista de videos cliente
    left_frame = tk.Frame(root, bg="lightgray", padx=10, pady=10)
    left_frame.grid(row=0, column=0, sticky="nswe", padx=5, pady=5)

    left_label = tk.Label(left_frame, text="Videos Disponibles", bg="lightgray", font=("Arial", 14, "bold"))
    left_label.pack(anchor="n", pady=10)

    left_thumbnails_frame = tk.Frame(left_frame, bg="lightgray")
    left_thumbnails_frame.pack(anchor="n", fill="both", expand=True)

    for i, (file, image, path) in enumerate(thumbnails_cliente):
        thumbnail_button = tk.Button(
            left_thumbnails_frame,
            image=image,
            text=file,
            compound="top",
            command=lambda p=path: video_player.play_video(p),
            width=150,
            height=120,
            relief="groove",
        )
        thumbnail_button.image = image
        row = i // 2
        col = i % 2
        thumbnail_button.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")

    # Parte central: Reproducción y botones
    center_frame = tk.Frame(root, bg="white")
    center_frame.grid(row=0, column=1, sticky="nswe", padx=5, pady=5)
    center_frame.grid_rowconfigure(0, weight=1)  # Centrar video verticalmente
    center_frame.grid_rowconfigure(1, weight=0)  # Mantener botones en la parte inferior
    center_frame.grid_columnconfigure(0, weight=1)  # Centrar horizontalmente

    # Marco para la reproducción de video (centrado)
    video_frame = tk.Frame(center_frame, bg="black", width=800, height=450)
    video_frame.grid(row=0, column=0, pady=(0, 20), sticky="n")  # Mantenerlo centrado con separación inferior
    video_frame.grid_propagate(False)  # Evitar que el marco cambie de tamaño
    video_area = tk.Label(video_frame, bg="black")
    video_area.pack(fill="both", expand=True)
    video_player.video_area = video_area

    # Botones de control (centrados debajo del área de reproducción)
    button_frame = tk.Frame(center_frame, bg="white")
    button_frame.grid(row=1, column=0, pady=10, sticky="n")  # Centrar debajo del video

    button_style = {"width": 12, "font": ("Arial", 10, "bold")}

    load_button = tk.Button(button_frame, text="Cargar", **button_style)
    load_button.pack(side="left", padx=10)

    send_button = tk.Button(button_frame, text="Enviar", **button_style)
    send_button.pack(side="left", padx=10)

    record_button = tk.Button(button_frame, text="Grabar", **button_style)
    record_button.pack(side="left", padx=10)

    stop_button = tk.Button(button_frame, text="Detener", command=video_player.stop_video, **button_style)
    stop_button.pack(side="left", padx=10)

    # Parte derecha: Videos procesados
    right_frame = tk.Frame(root, bg="lightgray", padx=10, pady=10)
    right_frame.grid(row=0, column=2, sticky="nswe", padx=5, pady=5)

    right_label = tk.Label(right_frame, text="Videos Procesados", bg="lightgray", font=("Arial", 14, "bold"))
    right_label.pack(anchor="n", pady=10)

    right_thumbnails_frame = tk.Frame(right_frame, bg="lightgray")
    right_thumbnails_frame.pack(anchor="n", fill="both", expand=True)

    for i, (file, image, path) in enumerate(thumbnails_procesados):
        thumbnail_button = tk.Button(
            right_thumbnails_frame,
            image=image,
            text=file,
            compound="top",
            command=lambda p=path: video_player.play_video(p),
            width=150,
            height=120,
            relief="groove",
        )
        thumbnail_button.image = image
        row = i // 2
        col = i % 2
        thumbnail_button.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")

    # Ajustar proporciones de las columnas y filas
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)  # Columna izquierda
    root.grid_columnconfigure(1, weight=3)  # Columna central (área de video)
    root.grid_columnconfigure(2, weight=1)  # Columna derecha

    root.mainloop()

