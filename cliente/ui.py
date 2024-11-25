import tkinter as tk


def create_ui(thumbnails_cliente, thumbnails_procesados, video_player, root, on_cargar=None, on_grabar=None, on_enviar=None):
    root.title("Interfaz de Video")
    root.geometry("1000x600")
    root.configure(bg="white")
    root.state('zoomed')  # Abrir en pantalla completa

    # Variables para manejar la selección
    selected_video = tk.StringVar()
    selected_widget = None  # Almacena el widget actualmente seleccionado

    # Funciones de selección y deselección
    def clear_selection():
        nonlocal selected_widget
        if selected_widget:
            selected_widget.config(bg="white")  # Restaurar el fondo del widget previamente seleccionado
        selected_widget = None
        selected_video.set("")  # Limpiar el video seleccionado
        send_button.config(state="disabled")  # Deshabilitar el botón "Enviar"

    def select_video(widget, path):
        nonlocal selected_widget
        clear_selection()  # Limpiar selección previa
        widget.config(bg="blue")  # Resaltar el widget actual
        selected_widget = widget
        selected_video.set(path)
        print(f"Video seleccionado: {path}")
        send_button.config(state="normal")  # Habilitar el botón "Enviar"

    # Parte izquierda: Lista de videos cliente
    left_frame = tk.Frame(root, bg="lightgray", padx=10, pady=10)
    left_frame.grid(row=0, column=0, sticky="nswe", padx=5, pady=5)

    left_label = tk.Label(left_frame, text="Videos Disponibles", bg="lightgray", font=("Arial", 14, "bold"))
    left_label.pack(anchor="n", pady=10)

    left_thumbnails_frame = tk.Frame(left_frame, bg="lightgray")
    left_thumbnails_frame.pack(anchor="n", fill="both", expand=True)

    # Función para manejar eventos de clic y doble clic
    def on_left_thumbnail_click(event, widget, path):
        select_video(widget, path)

    def on_left_thumbnail_double_click(event, path):
        video_player.play_video(path)

    # Agregar miniaturas de videos disponibles
    for i, (file, image, path) in enumerate(thumbnails_cliente):
        thumbnail_button = tk.Label(
            left_thumbnails_frame,
            image=image,
            text=file,
            compound="top",
            width=150,
            height=120,
            relief="groove",
            bg="white",
        )
        thumbnail_button.image = image
        row = i // 2
        col = i % 2
        thumbnail_button.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")

        # Asociar eventos a las miniaturas
        thumbnail_button.bind("<Button-1>", lambda event, w=thumbnail_button, p=path: on_left_thumbnail_click(event, w, p))
        thumbnail_button.bind("<Double-Button-1>", lambda event, p=path: on_left_thumbnail_double_click(event, p))

    # Parte central: Reproducción y botones
    center_frame = tk.Frame(root, bg="white")
    center_frame.grid(row=0, column=1, sticky="nswe", padx=5, pady=5)
    center_frame.grid_rowconfigure(0, weight=1)
    center_frame.grid_rowconfigure(1, weight=0)
    center_frame.grid_columnconfigure(0, weight=1)

    # Marco para la reproducción de video
    video_frame = tk.Frame(center_frame, bg="black", width=800, height=450)
    video_frame.grid(row=0, column=0, pady=(0, 20), sticky="n")
    video_frame.grid_propagate(False)
    video_area = tk.Label(video_frame, bg="black")
    video_area.pack(fill="both", expand=True)
    video_player.video_area = video_area

    # Botones de control
    button_frame = tk.Frame(center_frame, bg="white")
    button_frame.grid(row=1, column=0, pady=10, sticky="n")

    button_style = {"width": 12, "font": ("Arial", 10, "bold")}

    load_button = tk.Button(
        button_frame,
        text="Cargar",
        command=lambda: on_cargar(left_thumbnails_frame),
        **button_style
    )
    load_button.pack(side="left", padx=10)

    record_button = tk.Button(
        button_frame,
        text="Grabar",
        command=lambda: on_grabar(left_thumbnails_frame),
        **button_style
    )
    record_button.pack(side="left", padx=10)

    send_button = tk.Button(
        button_frame,
        text="Enviar",
        state="disabled",  # Deshabilitado inicialmente
        command=lambda: on_enviar(selected_video.get()),
        **button_style
    )
    send_button.pack(side="left", padx=10)

    stop_button = tk.Button(
        button_frame,
        text="Detener",
        command=video_player.stop_video,
        **button_style
    )
    stop_button.pack(side="left", padx=10)

    # Parte derecha: Videos procesados
    right_frame = tk.Frame(root, bg="lightgray", padx=10, pady=10)
    right_frame.grid(row=0, column=2, sticky="nswe", padx=5, pady=5)

    right_label = tk.Label(right_frame, text="Videos Procesados", bg="lightgray", font=("Arial", 14, "bold"))
    right_label.pack(anchor="n", pady=10)

    right_thumbnails_frame = tk.Frame(right_frame, bg="lightgray")
    right_thumbnails_frame.pack(anchor="n", fill="both", expand=True)

    # Función para manejar eventos de clic y doble clic en procesados
    def on_right_thumbnail_click(event, widget, path):
        select_video(widget, path)

    def on_right_thumbnail_double_click(event, path):
        video_player.play_video(path)

    # Agregar miniaturas de videos procesados
    for i, (file, image, path) in enumerate(thumbnails_procesados):
        thumbnail_button = tk.Label(
            right_thumbnails_frame,
            image=image,
            text=file,
            compound="top",
            width=150,
            height=120,
            relief="groove",
            bg="white",
        )
        thumbnail_button.image = image
        row = i // 2
        col = i % 2
        thumbnail_button.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")

        # Asociar eventos a las miniaturas
        thumbnail_button.bind("<Button-1>", lambda event, w=thumbnail_button, p=path: on_right_thumbnail_click(event, w, p))
        thumbnail_button.bind("<Double-Button-1>", lambda event, p=path: on_right_thumbnail_double_click(event, p))

    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=3)
    root.grid_columnconfigure(2, weight=1)

    root.mainloop()
