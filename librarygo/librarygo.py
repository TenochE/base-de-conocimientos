import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path

import fitz
from PIL import Image, ImageTk


# ============================================================
# RUTAS DEL PROYECTO
# ============================================================

CARPETA_PROYECTO = Path(__file__).parent
CARPETA_IMAGENES = CARPETA_PROYECTO / "imagenes"
CARPETA_LIBROS = CARPETA_PROYECTO / "libros"


# ============================================================
# CLASE LIBRO
# ============================================================

class Libro:

    def __init__(
        self,
        nombre,
        autor,
        editorial,
        anio,
        clasificaciones,
        imagen,
        pdf
    ):
        self.nombre = nombre
        self.autor = autor
        self.editorial = editorial
        self.anio = anio
        self.clasificaciones = clasificaciones
        self.imagen = imagen
        self.pdf = pdf

    def __str__(self):
        return f"{self.nombre} ({self.anio}) - {self.autor}"


# ============================================================
# BASE DE CONOCIMIENTOS
# ============================================================

base_conocimientos = [

    Libro(
        "Dune",
        "Frank Herbert",
        "Ace Books",
        1965,
        [
            "Ciencia ficción",
            "Aventura",
            "Novela",
            "Literatura adulta"
        ],
        "dune.jpg",
        "Dune.pdf"
    ),

    Libro(
        "1984",
        "George Orwell",
        "Secker & Warburg",
        1949,
        [
            "Ciencia ficción",
            "Novela",
            "Literatura adulta"
        ],
        "1984.jpg",
        "1984.pdf"
    ),

    Libro(
        "Fahrenheit 451",
        "Ray Bradbury",
        "Ballantine Books",
        1953,
        [
            "Ciencia ficción",
            "Novela",
            "Literatura adulta"
        ],
        "fahrenheit451.jpg",
        "Fahrenheit 451.pdf"
    ),

    Libro(
        "Orgullo y prejuicio",
        "Jane Austen",
        "T. Egerton",
        1813,
        [
            "Romance",
            "Novela",
            "Literatura adulta"
        ],
        "orgullo.jpg",
        "Orgullo y prejuicio.pdf"
    ),

    Libro(
        "Cumbres borrascosas",
        "Emily Brontë",
        "Thomas Cautley Newby",
        1847,
        [
            "Romance",
            "Novela",
            "Literatura adulta"
        ],
        "cumbres.jpg",
        "Cumbres borrascosas.pdf"
    ),

    Libro(
        "El nombre de la rosa",
        "Umberto Eco",
        "Bompiani",
        1980,
        [
            "Misterio",
            "Histórico",
            "Novela",
            "Literatura adulta"
        ],
        "nombre_rosa.jpg",
        "El nombre de la rosa.pdf"
    ),

    Libro(
        "El código Da Vinci",
        "Dan Brown",
        "Doubleday",
        2003,
        [
            "Misterio",
            "Aventura",
            "Novela",
            "Literatura adulta"
        ],
        "codigo_davinci.jpg",
        "El código Da Vinci.pdf"
    ),

    Libro(
        "Harry Potter y la piedra filosofal",
        "J. K. Rowling",
        "Bloomsbury",
        1997,
        [
            "Fantasía",
            "Aventura",
            "Literatura juvenil",
            "Novela"
        ],
        "harry_potter.jpg",
        "Harry Potter y la piedra filosofal.pdf"
    ),

    Libro(
        "El hobbit",
        "J. R. R. Tolkien",
        "George Allen & Unwin",
        1937,
        [
            "Fantasía",
            "Aventura",
            "Literatura juvenil",
            "Novela"
        ],
        "hobbit.jpg",
        "El hobbit.pdf"
    ),

    Libro(
        "La isla del tesoro",
        "Robert Louis Stevenson",
        "Cassell and Company",
        1883,
        [
            "Aventura",
            "Literatura juvenil",
            "Novela"
        ],
        "isla_tesoro.jpg",
        "La isla del tesoro.pdf"
    ),

    Libro(
        "Sapiens",
        "Yuval Noah Harari",
        "Harper",
        2011,
        [
            "Histórico",
            "Ensayo",
            "Literatura adulta"
        ],
        "sapiens.jpg",
        "Sapiens.pdf"
    ),

    Libro(
        "El diario de Ana Frank",
        "Ana Frank",
        "Contact Publishing",
        1947,
        [
            "Biografía",
            "Histórico",
            "Literatura juvenil"
        ],
        "ana_frank.jpg",
        "El diario de Ana Frank.pdf"
    ),

    Libro(
        "Steve Jobs",
        "Walter Isaacson",
        "Simon & Schuster",
        2011,
        [
            "Biografía",
            "Literatura adulta"
        ],
        "steve_jobs.jpg",
        "Steve Jobs.pdf"
    ),

    Libro(
        "El principito",
        "Antoine de Saint-Exupéry",
        "Reynal & Hitchcock",
        1943,
        [
            "Literatura infantil",
            "Fantasía",
            "Novela"
        ],
        "principito.jpg",
        "El principito.pdf"
    ),

    Libro(
        "Alicia en el país de las maravillas",
        "Lewis Carroll",
        "Macmillan",
        1865,
        [
            "Literatura infantil",
            "Fantasía",
            "Aventura"
        ],
        "alicia.jpg",
        "Alicia en el país de las maravillas.pdf"
    ),

    Libro(
        "Romeo y Julieta",
        "William Shakespeare",
        "Thomas Creede",
        1597,
        [
            "Romance",
            "Teatro",
            "Literatura adulta"
        ],
        "romeo_julieta.jpg",
        "Romeo y Julieta.pdf"
    ),

    Libro(
        "Hamlet",
        "William Shakespeare",
        "Nicholas Ling",
        1603,
        [
            "Teatro",
            "Literatura adulta"
        ],
        "hamlet.jpg",
        "Hamlet.pdf"
    ),

    Libro(
        "Veinte poemas de amor y una canción desesperada",
        "Pablo Neruda",
        "Editorial Nascimento",
        1924,
        [
            "Poesía",
            "Romance",
            "Literatura adulta"
        ],
        "veinte_poemas.jpg",
        "Veinte poemas de amor.pdf"
    ),

    Libro(
        "Ficciones",
        "Jorge Luis Borges",
        "Sur",
        1944,
        [
            "Cuento",
            "Misterio",
            "Literatura adulta"
        ],
        "ficciones.jpg",
        "Ficciones.pdf"
    ),

    Libro(
        "El llano en llamas",
        "Juan Rulfo",
        "Fondo de Cultura Económica",
        1953,
        [
            "Cuento",
            "Literatura adulta"
        ],
        "llano_llamas.jpg",
        "El llano en llamas.pdf"
    )
]


# ============================================================
# REGLAS DEL SISTEMA
# ============================================================

reglas = [

    {
        "condicion": lambda libro:
            "Ciencia ficción" in libro.clasificaciones,
        "recomendaciones": [
            "Ciencia ficción",
            "Aventura"
        ]
    },

    {
        "condicion": lambda libro:
            "Romance" in libro.clasificaciones,
        "recomendaciones": [
            "Romance",
            "Poesía"
        ]
    },

    {
        "condicion": lambda libro:
            "Misterio" in libro.clasificaciones,
        "recomendaciones": [
            "Misterio",
            "Aventura"
        ]
    },

    {
        "condicion": lambda libro:
            "Fantasía" in libro.clasificaciones,
        "recomendaciones": [
            "Fantasía",
            "Aventura"
        ]
    },

    {
        "condicion": lambda libro:
            "Aventura" in libro.clasificaciones,
        "recomendaciones": [
            "Aventura",
            "Fantasía",
            "Misterio"
        ]
    },

    {
        "condicion": lambda libro:
            "Histórico" in libro.clasificaciones,
        "recomendaciones": [
            "Histórico",
            "Biografía",
            "Ensayo"
        ]
    },

    {
        "condicion": lambda libro:
            "Biografía" in libro.clasificaciones,
        "recomendaciones": [
            "Biografía",
            "Histórico"
        ]
    },

    {
        "condicion": lambda libro:
            "Literatura infantil" in libro.clasificaciones,
        "recomendaciones": [
            "Literatura infantil",
            "Fantasía",
            "Aventura"
        ]
    },

    {
        "condicion": lambda libro:
            "Literatura juvenil" in libro.clasificaciones,
        "recomendaciones": [
            "Literatura juvenil",
            "Aventura",
            "Fantasía"
        ]
    },

    {
        "condicion": lambda libro:
            "Literatura adulta" in libro.clasificaciones,
        "recomendaciones": [
            "Literatura adulta"
        ]
    },

    {
        "condicion": lambda libro:
            "Novela" in libro.clasificaciones,
        "recomendaciones": [
            "Novela"
        ]
    },

    {
        "condicion": lambda libro:
            "Poesía" in libro.clasificaciones,
        "recomendaciones": [
            "Poesía",
            "Romance"
        ]
    },

    {
        "condicion": lambda libro:
            "Teatro" in libro.clasificaciones,
        "recomendaciones": [
            "Teatro"
        ]
    },

    {
        "condicion": lambda libro:
            "Ensayo" in libro.clasificaciones,
        "recomendaciones": [
            "Ensayo",
            "Histórico"
        ]
    },

    {
        "condicion": lambda libro:
            "Cuento" in libro.clasificaciones,
        "recomendaciones": [
            "Cuento",
            "Misterio"
        ]
    }
]


# ============================================================
# MOTOR DE INFERENCIA
# ============================================================

class MotorInferencia:

    def __init__(self, base_conocimientos, reglas):

        self.base_conocimientos = base_conocimientos
        self.reglas = reglas

    def obtener_recomendaciones(self, libro_seleccionado):

        clasificaciones_recomendadas = set()

        for regla in self.reglas:

            if regla["condicion"](libro_seleccionado):

                for clasificacion in regla["recomendaciones"]:

                    clasificaciones_recomendadas.add(
                        clasificacion
                    )

        resultados = []

        for libro in self.base_conocimientos:

            if libro.nombre == libro_seleccionado.nombre:
                continue

            coincidencias = 0

            for clasificacion in libro.clasificaciones:

                if clasificacion in clasificaciones_recomendadas:

                    coincidencias += 1

            if coincidencias > 0:

                resultados.append(
                    (
                        libro,
                        coincidencias
                    )
                )

        resultados.sort(
            key=lambda resultado: resultado[1],
            reverse=True
        )

        return resultados


# ============================================================
# INTERFAZ PRINCIPAL
# ============================================================

class LibraryGo:

    def __init__(self, ventana):

        self.ventana = ventana

        self.ventana.title(
            "LibraryGo - Sistema de recomendación de libros"
        )

        self.ventana.geometry(
            "1200x800"
        )

        self.ventana.minsize(
            1000,
            700
        )

        self.motor = MotorInferencia(
            base_conocimientos,
            reglas
        )

        self.libro_actual = None

        self.documento_pdf = None

        self.pagina_actual = 0

        self.imagen_logo = None
        self.imagen_portada = None
        self.imagen_pdf = None

        self.crear_estilos()

        self.mostrar_inicio()

    # ========================================================
    # ESTILOS
    # ========================================================

    def crear_estilos(self):

        self.fuente_titulo = (
            "Arial",
            30,
            "bold"
        )

        self.fuente_subtitulo = (
            "Arial",
            15
        )

        self.fuente_seccion = (
            "Arial",
            20,
            "bold"
        )

        self.fuente_normal = (
            "Arial",
            11
        )

    # ========================================================
    # LIMPIAR VENTANA
    # ========================================================

    def limpiar_ventana(self):

        for widget in self.ventana.winfo_children():

            widget.destroy()

    # ========================================================
    # PANTALLA DE INICIO
    # ========================================================

    def mostrar_inicio(self):

        self.limpiar_ventana()

        self.ventana.configure(
            bg="#F5F1E8"
        )

        contenedor = tk.Frame(
            self.ventana,
            bg="#F5F1E8"
        )

        contenedor.pack(
            expand=True
        )

        ruta_logo = (
            CARPETA_IMAGENES / "logo.png"
        )

        if ruta_logo.exists():

            try:

                imagen = Image.open(
                    ruta_logo
                )

                imagen.thumbnail(
                    (350, 350)
                )

                self.imagen_logo = ImageTk.PhotoImage(
                    imagen
                )

                tk.Label(
                    contenedor,
                    image=self.imagen_logo,
                    bg="#F5F1E8"
                ).pack(
                    pady=(20, 10)
                )

            except Exception:

                self.mostrar_logo_texto(
                    contenedor
                )

        else:

            self.mostrar_logo_texto(
                contenedor
            )

        tk.Label(
            contenedor,
            text="LibraryGo",
            font=self.fuente_titulo,
            bg="#F5F1E8",
            fg="#2E2E2E"
        ).pack(
            pady=(10, 5)
        )

        tk.Label(
            contenedor,
            text="Descubre tu próxima lectura",
            font=self.fuente_subtitulo,
            bg="#F5F1E8",
            fg="#666666"
        ).pack(
            pady=(0, 30)
        )

        tk.Button(
            contenedor,
            text="INGRESAR",
            command=self.mostrar_catalogo,
            font=("Arial", 13, "bold"),
            bg="#2E2E2E",
            fg="white",
            activebackground="#444444",
            activeforeground="white",
            relief=tk.FLAT,
            padx=50,
            pady=14,
            cursor="hand2"
        ).pack()

        tk.Label(
            contenedor,
            text="Sistema basado en reglas de recomendación",
            font=("Arial", 9),
            bg="#F5F1E8",
            fg="#888888"
        ).pack(
            pady=30
        )

    # ========================================================
    # LOGO ALTERNATIVO
    # ========================================================

    def mostrar_logo_texto(self, contenedor):

        tk.Label(
            contenedor,
            text="LIBRARYGO",
            font=("Arial", 38, "bold"),
            bg="#F5F1E8",
            fg="#2E2E2E"
        ).pack(
            pady=80
        )

    # ========================================================
    # CATÁLOGO
    # ========================================================

    def mostrar_catalogo(self):

        self.limpiar_ventana()

        self.ventana.configure(
            bg="#FFFFFF"
        )

        # ----------------------------------------------------
        # BARRA SUPERIOR
        # ----------------------------------------------------

        barra = tk.Frame(
            self.ventana,
            bg="#252525",
            height=70
        )

        barra.pack(
            fill=tk.X
        )

        barra.pack_propagate(
            False
        )

        tk.Label(
            barra,
            text="LibraryGo",
            font=("Arial", 22, "bold"),
            bg="#252525",
            fg="white"
        ).pack(
            side=tk.LEFT,
            padx=30
        )

        tk.Button(
            barra,
            text="Inicio",
            command=self.mostrar_inicio,
            font=("Arial", 10),
            bg="#252525",
            fg="white",
            activebackground="#252525",
            activeforeground="white",
            relief=tk.FLAT,
            cursor="hand2"
        ).pack(
            side=tk.RIGHT,
            padx=30
        )

        # ----------------------------------------------------
        # TÍTULO
        # ----------------------------------------------------

        titulo = tk.Label(
            self.ventana,
            text="Catálogo de libros",
            font=("Arial", 25, "bold"),
            bg="#FFFFFF",
            fg="#252525"
        )

        titulo.pack(
            pady=(25, 10)
        )

        # ----------------------------------------------------
        # SELECTOR
        # ----------------------------------------------------

        frame_selector = tk.Frame(
            self.ventana,
            bg="#FFFFFF"
        )

        frame_selector.pack(
            pady=10
        )

        tk.Label(
            frame_selector,
            text="Selecciona un libro:",
            font=("Arial", 12),
            bg="#FFFFFF"
        ).pack(
            side=tk.LEFT,
            padx=10
        )

        nombres = [
            libro.nombre
            for libro in base_conocimientos
        ]

        self.combo_libros = ttk.Combobox(
            frame_selector,
            values=nombres,
            state="readonly",
            width=45,
            font=("Arial", 11)
        )

        self.combo_libros.pack(
            side=tk.LEFT,
            padx=10
        )

        self.combo_libros.bind(
            "<<ComboboxSelected>>",
            self.seleccionar_libro
        )

        # ----------------------------------------------------
        # CONTENIDO PRINCIPAL
        # ----------------------------------------------------

        contenido = tk.Frame(
            self.ventana,
            bg="#FFFFFF"
        )

        contenido.pack(
            fill=tk.BOTH,
            expand=True,
            padx=30,
            pady=10
        )

        # ----------------------------------------------------
        # INFORMACIÓN DEL LIBRO
        # ----------------------------------------------------

        frame_info = tk.Frame(
            contenido,
            bg="#F5F1E8",
            width=300
        )

        frame_info.pack(
            side=tk.LEFT,
            fill=tk.Y,
            padx=(0, 15)
        )

        frame_info.pack_propagate(
            False
        )

        self.label_portada = tk.Label(
            frame_info,
            text="Selecciona un libro",
            bg="#F5F1E8",
            fg="#777777",
            font=("Arial", 11)
        )

        self.label_portada.pack(
            pady=20
        )

        self.label_nombre = tk.Label(
            frame_info,
            text="",
            font=("Arial", 18, "bold"),
            bg="#F5F1E8",
            fg="#252525",
            wraplength=260
        )

        self.label_nombre.pack(
            padx=20,
            pady=10
        )

        self.label_autor = tk.Label(
            frame_info,
            text="",
            font=self.fuente_normal,
            bg="#F5F1E8",
            fg="#555555",
            wraplength=260
        )

        self.label_autor.pack(
            padx=20,
            pady=3
        )

        self.label_editorial = tk.Label(
            frame_info,
            text="",
            font=self.fuente_normal,
            bg="#F5F1E8",
            fg="#555555",
            wraplength=260
        )

        self.label_editorial.pack(
            padx=20,
            pady=3
        )

        self.label_anio = tk.Label(
            frame_info,
            text="",
            font=self.fuente_normal,
            bg="#F5F1E8",
            fg="#555555"
        )

        self.label_anio.pack(
            padx=20,
            pady=3
        )

        self.label_clasificaciones = tk.Label(
            frame_info,
            text="",
            font=("Arial", 10),
            bg="#F5F1E8",
            fg="#555555",
            wraplength=260,
            justify=tk.LEFT
        )

        self.label_clasificaciones.pack(
            padx=20,
            pady=15
        )

        # ----------------------------------------------------
        # PARTE DERECHA
        # ----------------------------------------------------

        frame_derecho = tk.Frame(
            contenido,
            bg="#FFFFFF"
        )

        frame_derecho.pack(
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=True
        )

        # ----------------------------------------------------
        # PDF
        # ----------------------------------------------------

        tk.Label(
            frame_derecho,
            text="Contenido del libro",
            font=self.fuente_seccion,
            bg="#FFFFFF",
            fg="#252525"
        ).pack(
            anchor="w",
            pady=(0, 10)
        )

        frame_pdf = tk.Frame(
            frame_derecho,
            bg="#E8E8E8",
            relief=tk.SOLID,
            borderwidth=1
        )

        frame_pdf.pack(
            fill=tk.BOTH,
            expand=True
        )

        self.label_pdf = tk.Label(
            frame_pdf,
            text="Selecciona un libro para visualizar su PDF",
            font=("Arial", 11),
            bg="#E8E8E8",
            fg="#777777"
        )

        self.label_pdf.pack(
            expand=True
        )

        # ----------------------------------------------------
        # CONTROLES PDF
        # ----------------------------------------------------

        controles_pdf = tk.Frame(
            frame_derecho,
            bg="#FFFFFF"
        )

        controles_pdf.pack(
            fill=tk.X,
            pady=8
        )

        self.boton_anterior = tk.Button(
            controles_pdf,
            text="◀ Anterior",
            command=self.pagina_anterior,
            state=tk.DISABLED,
            relief=tk.FLAT,
            bg="#252525",
            fg="white",
            padx=15,
            pady=5
        )

        self.boton_anterior.pack(
            side=tk.LEFT
        )

        self.label_pagina = tk.Label(
            controles_pdf,
            text="Página -",
            font=("Arial", 10),
            bg="#FFFFFF"
        )

        self.label_pagina.pack(
            side=tk.LEFT,
            expand=True
        )

        self.boton_siguiente = tk.Button(
            controles_pdf,
            text="Siguiente ▶",
            command=self.pagina_siguiente,
            state=tk.DISABLED,
            relief=tk.FLAT,
            bg="#252525",
            fg="white",
            padx=15,
            pady=5
        )

        self.boton_siguiente.pack(
            side=tk.RIGHT
        )

        # ----------------------------------------------------
        # RECOMENDACIONES
        # ----------------------------------------------------

        tk.Label(
            frame_derecho,
            text="Posibles recomendaciones",
            font=self.fuente_seccion,
            bg="#FFFFFF",
            fg="#252525"
        ).pack(
            anchor="w",
            pady=(10, 8)
        )

        frame_recomendaciones = tk.Frame(
            frame_derecho,
            bg="#FFFFFF"
        )

        frame_recomendaciones.pack(
            fill=tk.X
        )

        self.lista_recomendaciones = tk.Listbox(
            frame_recomendaciones,
            height=5,
            font=("Arial", 10),
            relief=tk.SOLID,
            borderwidth=1
        )

        self.lista_recomendaciones.pack(
            fill=tk.X
        )

    # ========================================================
    # SELECCIONAR LIBRO
    # ========================================================

    def seleccionar_libro(self, evento=None):

        nombre = self.combo_libros.get()

        for libro in base_conocimientos:

            if libro.nombre == nombre:

                self.libro_actual = libro

                self.mostrar_informacion(
                    libro
                )

                self.cargar_pdf(
                    libro
                )

                self.generar_recomendaciones()

                break

    # ========================================================
    # INFORMACIÓN DEL LIBRO
    # ========================================================

    def mostrar_informacion(self, libro):

        self.label_nombre.config(
            text=libro.nombre
        )

        self.label_autor.config(
            text=f"Autor: {libro.autor}"
        )

        self.label_editorial.config(
            text=f"Editorial: {libro.editorial}"
        )

        self.label_anio.config(
            text=f"Año: {libro.anio}"
        )

        self.label_clasificaciones.config(
            text=(
                "Clasificaciones:\n\n"
                + "\n".join(
                    f"• {clasificacion}"
                    for clasificacion in libro.clasificaciones
                )
            )
        )

        # ----------------------------------------------------
        # PORTADA
        # ----------------------------------------------------

        ruta = CARPETA_IMAGENES / libro.imagen

        if not ruta.exists():

            self.label_portada.config(
                image="",
                text="Portada no disponible"
            )

            return

        try:

            imagen = Image.open(
                ruta
            )

            imagen.thumbnail(
                (240, 280)
            )

            self.imagen_portada = ImageTk.PhotoImage(
                imagen
            )

            self.label_portada.config(
                image=self.imagen_portada,
                text=""
            )

        except Exception:

            self.label_portada.config(
                image="",
                text="No se pudo cargar la portada"
            )

    # ========================================================
    # CARGAR PDF
    # ========================================================

    def cargar_pdf(self, libro):

        if self.documento_pdf is not None:

            self.documento_pdf.close()

            self.documento_pdf = None

        ruta_pdf = (
            CARPETA_LIBROS / libro.pdf
        )

        if not ruta_pdf.exists():

            self.label_pdf.config(
                image="",
                text=(
                    "Contenido del libro:\n\n"
                    + str(ruta_pdf)
                )
            )

            self.boton_anterior.config(
                state=tk.DISABLED
            )

            self.boton_siguiente.config(
                state=tk.DISABLED
            )

            self.label_pagina.config(
                text="Realiza el pago de $100 para poder leer el libro completo"
            )

            return

        try:

            self.documento_pdf = fitz.open(
                ruta_pdf
            )

            self.pagina_actual = 0

            self.mostrar_pagina()

        except Exception as error:

            self.label_pdf.config(
                image="",
                text=(
                    "No se pudo abrir el PDF.\n\n"
                    + str(error)
                )
            )

    # ========================================================
    # MOSTRAR PÁGINA PDF
    # ========================================================

    def mostrar_pagina(self):

        if self.documento_pdf is None:
            return

        if len(self.documento_pdf) == 0:
            return

        pagina = self.documento_pdf[
            self.pagina_actual
        ]

        matriz = fitz.Matrix(
            1.25,
            1.25
        )

        pixmap = pagina.get_pixmap(
            matrix=matriz,
            alpha=False
        )

        imagen = Image.frombytes(
            "RGB",
            [
                pixmap.width,
                pixmap.height
            ],
            pixmap.samples
        )

        ancho_maximo = 650
        alto_maximo = 500

        imagen.thumbnail(
            (
                ancho_maximo,
                alto_maximo
            )
        )

        self.imagen_pdf = ImageTk.PhotoImage(
            imagen
        )

        self.label_pdf.config(
            image=self.imagen_pdf,
            text=""
        )

        total_paginas = len(
            self.documento_pdf
        )

        self.label_pagina.config(
            text=(
                f"Página "
                f"{self.pagina_actual + 1}"
                f" de "
                f"{total_paginas}"
            )
        )

        if self.pagina_actual == 0:

            self.boton_anterior.config(
                state=tk.DISABLED
            )

        else:

            self.boton_anterior.config(
                state=tk.NORMAL
            )

        if self.pagina_actual >= total_paginas - 1:

            self.boton_siguiente.config(
                state=tk.DISABLED
            )

        else:

            self.boton_siguiente.config(
                state=tk.NORMAL
            )

    # ========================================================
    # PÁGINA ANTERIOR
    # ========================================================

    def pagina_anterior(self):

        if self.documento_pdf is None:
            return

        if self.pagina_actual > 0:

            self.pagina_actual -= 1

            self.mostrar_pagina()

    # ========================================================
    # PÁGINA SIGUIENTE
    # ========================================================

    def pagina_siguiente(self):

        if self.documento_pdf is None:
            return

        if (
            self.pagina_actual
            < len(self.documento_pdf) - 1
        ):

            self.pagina_actual += 1

            self.mostrar_pagina()

    # ========================================================
    # RECOMENDACIONES
    # ========================================================

    def generar_recomendaciones(self):

        self.lista_recomendaciones.delete(
            0,
            tk.END
        )

        if self.libro_actual is None:
            return

        recomendaciones = (
            self.motor.obtener_recomendaciones(
                self.libro_actual
            )
        )

        if not recomendaciones:

            self.lista_recomendaciones.insert(
                tk.END,
                "No se encontraron recomendaciones."
            )

            return

        for libro, coincidencias in recomendaciones:

            texto = (
                f"  {libro.nombre}  |  "
                f"{libro.autor}  |  "
                f"{coincidencias} coincidencias"
            )

            self.lista_recomendaciones.insert(
                tk.END,
                texto
            )

    # ========================================================
    # CERRAR APLICACIÓN
    # ========================================================

    def cerrar(self):

        if self.documento_pdf is not None:

            self.documento_pdf.close()

        self.ventana.destroy()


# ============================================================
# EJECUCIÓN
# ============================================================

if __name__ == "__main__":

    ventana = tk.Tk()

    aplicacion = LibraryGo(
        ventana
    )

    ventana.protocol(
        "WM_DELETE_WINDOW",
        aplicacion.cerrar
    )

    ventana.mainloop()