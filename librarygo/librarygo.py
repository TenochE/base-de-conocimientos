import csv
import unicodedata
import tkinter as tk
from pathlib import Path
from tkinter import ttk, messagebox

import fitz
from PIL import Image, ImageTk

# ============================================================
# RUTAS
# ============================================================

ROOT = Path(__file__).resolve().parent
IMAGES_DIR = ROOT / "imagenes"
BOOKS_DIR = ROOT / "libros"
CSV_FILE = ROOT / "catalogo_extendido_200.csv"

# ============================================================
# COLORES
# ============================================================

BG = "#F6F3EC"
CARD = "#FFFFFF"
INK = "#252525"
MUTED = "#747474"
LINE = "#E3DED2"
ACCENT = "#7A5C3E"
ACCENT_DARK = "#5C432D"
DARK = "#202020"
WARNING = "#8A632B"
VERY = "#496B52"
RECOMMENDED = "#6C6748"
LOW = "#987046"
NO = "#874C4C"

# ============================================================
# CLASIFICACIONES
# ============================================================

CLASIFICACIONES = [
    "Ciencia ficción",
    "Romance",
    "Misterio",
    "Fantasía",
    "Aventura",
    "Histórico",
    "Biografía",
    "Literatura infantil",
    "Literatura juvenil",
    "Literatura adulta",
    "Novela",
    "Poesía",
    "Teatro",
    "Ensayo",
    "Cuento",
]

# ============================================================
# PREGUNTAS DEL CUESTIONARIO
# ============================================================

PREGUNTAS = [
    ("¿Te gustan las historias de ciencia ficción?", ["Ciencia ficción"]),
    ("¿Te gustan las historias de fantasía?", ["Fantasía"]),
    ("¿Te gustan las historias románticas?", ["Romance"]),
    ("¿Te gustan los misterios y las investigaciones?", ["Misterio"]),
    ("¿Te gustan las historias de aventura y acción?", ["Aventura"]),
    ("¿Te interesan los acontecimientos históricos?", ["Histórico"]),
    ("¿Te gustan las historias cortas?", ["Cuento"]),
    ("¿Te atraen los mundos y personajes imaginarios?", ["Fantasía"]),
    ("¿Te interesa leer sobre la vida de personas reales?", ["Biografía"]),
    ("¿Prefieres obras reflexivas o de análisis?", ["Ensayo"]),
]

# ============================================================
# UTILIDADES
# ============================================================

def normalize(text):
    text = str(text or "")
    text = unicodedata.normalize("NFD", text)
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    return text.lower().strip()


def parse_year(value):
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return None


def clamp(value, minimum=0, maximum=10):
    return max(minimum, min(maximum, int(round(value))))


def rating_label(score):
    if score >= 9:
        return "muy recomendado"
    if score >= 6:
        return "recomendado"
    if score >= 3:
        return "poco recomendado"
    return "no recomendado"


def rating_color(score):
    if score >= 9:
        return VERY
    if score >= 6:
        return RECOMMENDED
    if score >= 3:
        return LOW
    return NO


def resolve_file(folder, specified_name, default_name, extensions):
    if specified_name:
        direct = folder / specified_name
        if direct.exists() and direct.is_file():
            return direct.name

    if default_name:
        direct = folder / default_name
        if direct.exists() and direct.is_file():
            return direct.name

    target = normalize(Path(default_name or "").stem)
    if not target or not folder.exists():
        return ""

    for file in folder.iterdir():
        if file.is_file() and file.suffix.lower() in extensions:
            if normalize(file.stem) == target:
                return file.name
    return ""

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
        imagen="",
        pdf="",
        origen="original",
        popularidad=5,
    ):
        self.nombre = str(nombre).strip()
        self.autor = str(autor).strip()
        self.editorial = str(editorial).strip()
        self.anio = str(anio).strip()
        self.clasificaciones = list(clasificaciones)
        self.imagen = str(imagen or "").strip()
        self.pdf = str(pdf or "").strip()
        self.origen = origen
        self.popularidad = int(popularidad or 5)

    def year(self):
        return parse_year(self.anio)

    def tipo_lector(self):
        for tipo in (
            "Literatura infantil",
            "Literatura juvenil",
            "Literatura adulta",
        ):
            if tipo in self.clasificaciones:
                return tipo
        return "Sin especificar"

# ============================================================
# BASE DE CONOCIMIENTOS ORIGINAL
# ============================================================

BASE_ORIGINAL = [
    Libro("Dune", "Frank Herbert", "Ace Books", 1965,
          ["Ciencia ficción", "Aventura", "Novela", "Literatura adulta"],
          "dune.jpg", "Dune.pdf", popularidad=7),
    Libro("1984", "George Orwell", "Secker & Warburg", 1949,
          ["Ciencia ficción", "Novela", "Literatura adulta"],
          "1984.jpg", "1984.pdf", popularidad=5),
    Libro("Fahrenheit 451", "Ray Bradbury", "Ballantine Books", 1953,
          ["Ciencia ficción", "Novela", "Literatura adulta"],
          "fahrenheit451.jpg", "Fahrenheit 451.pdf", popularidad=2),
    Libro("Orgullo y prepucio", "Jane Austen", "T. Egerton", 1813,
          ["Romance", "Novela", "Literatura adulta"],
          "orgullo.jpg", "Orgullo y prejuicio.pdf", popularidad=10),
    Libro("Cumbres cochambrosas", "Emily Brontë", "Thomas Cautley Newby", 1847,
          ["Romance", "Novela", "Literatura adulta"],
          "cumbres.jpg", "Cumbres borrascosas.pdf", popularidad=9),
    Libro("El nombre de la rosa", "Umberto Eco", "Bompiani", 1980,
          ["Misterio", "Histórico", "Novela", "Literatura adulta"],
          "nombre_rosa.jpg", "El nombre de la rosa.pdf", popularidad=3),
    Libro("El código Da Vinci", "Dan Brown", "Doubleday", 2003,
          ["Misterio", "Aventura", "Novela", "Literatura adulta"],
          "codigo_davinci.jpg", "El código Da Vinci.pdf", popularidad=8),
    Libro("Harry Potter y la piedra filosofal", "J. K. Rowling", "Bloomsbury", 1997,
          ["Fantasía", "Aventura", "Literatura juvenil", "Novela"],
          "harry_potter.jpg", "Harry Potter y la piedra filosofal.pdf", popularidad=10),
    Libro("El hobbit", "J. R. R. Tolkien", "George Allen & Unwin", 1937,
          ["Fantasía", "Aventura", "Literatura juvenil", "Novela"],
          "hobbit.jpg", "El hobbit.pdf", popularidad=9),
    Libro("La isla del tesoro", "Robert Louis Stevenson", "Cassell and Company", 1883,
          ["Aventura", "Literatura juvenil", "Novela"],
          "isla_tesoro.jpg", "La isla del tesoro.pdf", popularidad=10),
    Libro("Sapiens", "Yuval Noah Harari", "Harper", 2011,
          ["Histórico", "Ensayo", "Literatura adulta"],
          "sapiens.jpg", "Sapiens.pdf", popularidad=3),
    Libro("El diario de Ana Frank", "Ana Frank", "Contact Publishing", 1947,
          ["Biografía", "Histórico", "Literatura juvenil"],
          "ana_frank.jpg", "El diario de Ana Frank.pdf", popularidad=0),
    Libro("Steve Jobs", "Walter Isaacson", "Simon & Schuster", 2011,
          ["Biografía", "Literatura adulta"],
          "steve_jobs.jpg", "Steve Jobs.pdf", popularidad=1),
    Libro("Los hornos de Hitler", "Max Gallo", "Éditions du Seuil", 1981,
          ["Histórico", "Ensayo", "Literatura adulta"],
          "hornos_hitler.jpg", "Los hornos de Hitler.pdf", popularidad=10),
    Libro("El principito", "Antoine de Saint-Exupéry", "Reynal & Hitchcock", 1943,
          ["Literatura infantil", "Fantasía", "Novela"],
          "principito.jpg", "El principito.pdf", popularidad=10),
    Libro("Alicia en el país de las maravillas", "Lewis Carroll", "Macmillan", 1865,
          ["Literatura infantil", "Fantasía", "Aventura"],
          "alicia.jpg", "Alicia en el país de las maravillas.pdf", popularidad=8),
    Libro("Romeo y Julieta", "William Shakespeare", "Thomas Creede", 1597,
          ["Romance", "Teatro", "Literatura adulta"],
          "romeo_julieta.jpg", "Romeo y Julieta.pdf", popularidad=8),
    Libro("Hamlet", "William Shakespeare", "Nicholas Ling", 1603,
          ["Teatro", "Literatura adulta"],
          "hamlet.jpg", "Hamlet.pdf", popularidad=9),
    Libro("Veinte poemas de amor y una canción desesperada", "Pablo Neruda", "Editorial Nascimento", 1924,
          ["Poesía", "Romance", "Literatura adulta"],
          "veinte_poemas.jpg", "Veinte poemas de amor.pdf", popularidad=5),
    Libro("Ficciones", "Jorge Luis Borges", "Sur", 1944,
          ["Cuento", "Misterio", "Literatura adulta"],
          "ficciones.jpg", "Ficciones.pdf", popularidad=9),
    Libro("El llano en llamas", "Juan Rulfo", "Fondo de Cultura Económica", 1953,
          ["Cuento", "Literatura adulta"],
          "llano_llamas.jpg", "El llano en llamas.pdf", popularidad=3),
    Libro("La rata con thiner", "Juan Rulfo", "Fondo de Cultura Económica", 1953,
          ["Antología", "Literatura adulta","Ensayo", "Histórico"],
          "rata_thiner.jpg", "rata_thiner.pdf", popularidad=10),
]

# ============================================================
# CARGAR CATALOGO EXTENDIDO DESDE CSV
# ============================================================

def cargar_catalogo_csv():
    catalogo = []
    if not CSV_FILE.exists():
        print(f"No se encontró: {CSV_FILE}")
        return catalogo

    try:
        with CSV_FILE.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            required = {
                "nombre", "autor", "editorial", "anio",
                "clasificaciones", "imagen", "pdf"
            }
            if not required.issubset(set(reader.fieldnames or [])):
                print("El CSV no tiene la estructura esperada.")
                return catalogo

            existing = {normalize(book.nombre) for book in BASE_ORIGINAL}

            for index, row in enumerate(reader, start=1):
                nombre = str(row.get("nombre", "")).strip()
                if not nombre or normalize(nombre) in existing:
                    continue

                clases = []
                for clase in str(row.get("clasificaciones", "")).split(";"):
                    clase = clase.strip()
                    if clase in CLASIFICACIONES and clase not in clases:
                        clases.append(clase)

                if not clases:
                    continue

                imagen = resolve_file(
                    IMAGES_DIR,
                    str(row.get("imagen", "")).strip(),
                    nombre,
                    {".jpg", ".jpeg", ".png", ".webp"},
                )
                pdf = resolve_file(
                    BOOKS_DIR,
                    str(row.get("pdf", "")).strip(),
                    nombre,
                    {".pdf"},
                )

                popularity_value = str(row.get("popularidad", "")).strip()
                popularity = parse_year(popularity_value) or 5

                catalogo.append(
                    Libro(
                        nombre,
                        str(row.get("autor", "")).strip(),
                        str(row.get("editorial", "")).strip(),
                        str(row.get("anio", "")).strip(),
                        clases,
                        imagen,
                        pdf,
                        "extendido",
                        popularity,
                    )
                )
                existing.add(normalize(nombre))

    except Exception as error:
        print("Error leyendo CSV:", error)

    return catalogo


CATALOGO_EXTENDIDO = cargar_catalogo_csv()
BASE_CONOCIMIENTOS = BASE_ORIGINAL + CATALOGO_EXTENDIDO

# ============================================================
# MOTOR DE INFERENCIA
# ============================================================

class MotorInferencia:
    def __init__(self, libros):
        self.libros = libros

    # --------------------------------------------------------
    # RECOMENDACION POR LIBRO
    # --------------------------------------------------------

    def recomendaciones_por_libro(self, seleccionado, limite=4):
        resultados = []
        for libro in self.libros:
            if libro is seleccionado:
                continue

            coincidencias = len(
                set(libro.clasificaciones)
                & set(seleccionado.clasificaciones)
            )

            if coincidencias:
                resultados.append((libro, coincidencias))

        resultados.sort(
            key=lambda item: (-item[1], normalize(item[0].nombre))
        )
        return resultados[:limite]

    # --------------------------------------------------------
    # REGLAS DEL CUESTIONARIO
    # --------------------------------------------------------

    def aplicar_reglas(self, respuestas):
        hechos = {
            f"q{i + 1}": bool(respuestas[i])
            for i in range(len(PREGUNTAS))
        }

        preferencias = {genero: 0 for genero in CLASIFICACIONES}
        excluidos = set()
        inferidas = set()

        # Hechos directos.
        for i, (_, generos) in enumerate(PREGUNTAS):
            for genero in generos:
                if hechos[f"q{i + 1}"]:
                    preferencias[genero] += 2
                else:
                    preferencias[genero] -= 2
                    excluidos.add(genero)

        # Regla 1: AND - ciencia ficción + aventura.
        if hechos["q1"] and hechos["q5"]:
            preferencias["Ciencia ficción"] += 1
            preferencias["Aventura"] += 1
            preferencias["Novela"] += 1
            inferidas.update({"Ciencia ficción", "Aventura", "Novela"})

        # Regla 2: OR - fantasía directa o mundos imaginarios.
        if hechos["q2"] or hechos["q8"]:
            preferencias["Fantasía"] += 2
            inferidas.add("Fantasía")

        # Regla 3: NOT - rechazo de romance.
        if not hechos["q3"]:
            preferencias["Romance"] -= 3
            excluidos.add("Romance")

        # Regla 4: AND con negaciones - evita misterio y ciencia ficción,
        # por lo que se favorecen lecturas de aventura y novela.
        if (not hechos["q4"]) and (not hechos["q1"]):
            preferencias["Aventura"] += 2
            preferencias["Novela"] += 1
            inferidas.update({"Aventura", "Novela"})

        # Regla 5: ciencia ficción y rechazo de historias cortas.
        # Inferencia de novelas de ciencia ficción más extensas.
        if hechos["q1"] and (not hechos["q7"]):
            preferencias["Ciencia ficción"] += 2
            preferencias["Novela"] += 2
            inferidas.update({"Ciencia ficción", "Novela"})

        # Regla 6: biografía + histórico.
        if hechos["q9"] and hechos["q6"]:
            preferencias["Biografía"] += 2
            preferencias["Histórico"] += 1
            inferidas.update({"Biografía", "Histórico"})

        # Regla 7: NOT ensayo.
        if not hechos["q10"]:
            preferencias["Ensayo"] -= 1
            excluidos.add("Ensayo")

        todas_falsas = not any(respuestas)

        # Regla de consistencia: si todo es falso, se desactivan exclusiones
        # y se usan popularidad y clasificación introductoria.
        if todas_falsas:
            excluidos.clear()
            preferencias["Aventura"] += 1
            preferencias["Novela"] += 1
            inferidas.update({"Aventura", "Novela"})

        return hechos, preferencias, excluidos, inferidas, todas_falsas

    # --------------------------------------------------------
    # RECOMENDACION POR CUESTIONARIO
    # --------------------------------------------------------

    def recomendaciones_por_cuestionario(self, respuestas, limite=10):
        (
            hechos,
            preferencias,
            excluidos,
            inferidas,
            todas_falsas,
        ) = self.aplicar_reglas(respuestas)

        resultados = []

        for libro in self.libros:
            if not todas_falsas and any(
                genero in libro.clasificaciones
                for genero in excluidos
            ):
                continue

            if todas_falsas:
                # Recomendaciones de consistencia por popularidad.
                score = clamp(libro.popularidad)
            else:
                # Cada una de las 10 preguntas aporta una evidencia concreta.
                # Una respuesta verdadera suma si el libro coincide con la
                # característica de la pregunta; una falsa resta.
                raw = 0

                for index, (_, generos) in enumerate(PREGUNTAS):
                    coincide = any(
                        genero in libro.clasificaciones
                        for genero in generos
                    )
                    if coincide:
                        raw += 1 if hechos[f"q{index + 1}"] else -1

                # Las reglas inferidas agregan evidencia adicional.
                raw += sum(
                    1
                    for genero in libro.clasificaciones
                    if genero in inferidas
                )

                # Conversión de la evidencia a una escala de 0 a 10.
                score = clamp((raw + 10) / 2)

            resultados.append((libro, score))

        resultados.sort(
            key=lambda item: (-item[1], -item[0].popularidad, normalize(item[0].nombre))
        )

        return resultados[:limite]


MOTOR = MotorInferencia(BASE_CONOCIMIENTOS)

# ============================================================
# APLICACION
# ============================================================

class LibraryGo:
    def __init__(self, root):
        self.root = root
        self.root.title("LibraryGo")
        self.root.geometry("1240x820")
        self.root.minsize(1050, 700)
        self.root.configure(bg=BG)

        self.current_book = None
        self.current_page = 0
        self.pdf_doc = None
        self.images = []
        self.logo_image = None
        self.cover_image = None
        self.pdf_image = None
        self.question_vars = []

        self.style = ttk.Style()
        try:
            self.style.theme_use("clam")
        except tk.TclError:
            pass
        self.style.configure("TCombobox", padding=7, fieldbackground="white")
        self.style.configure("Treeview", rowheight=34, font=("Segoe UI", 10))
        self.style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

        self.show_introduction()

    # --------------------------------------------------------
    # GENERAL
    # --------------------------------------------------------

    def clear(self):
        self.close_pdf()
        for widget in self.root.winfo_children():
            widget.destroy()

    def rounded_button(self, parent, text, command, primary=False, width=None):
        return tk.Button(
            parent,
            text=text,
            command=command,
            font=("Segoe UI", 10, "bold" if primary else "normal"),
            bg=ACCENT if primary else CARD,
            fg="white" if primary else INK,
            activebackground=ACCENT_DARK if primary else LINE,
            activeforeground="white" if primary else INK,
            relief="flat",
            bd=0,
            padx=18,
            pady=10,
            cursor="hand2",
            width=width,
        )

    def header(self, title, subtitle="", show_menu=True):
        bar = tk.Frame(self.root, bg=DARK, height=72)
        bar.pack(fill="x")
        bar.pack_propagate(False)

        tk.Label(
            bar,
            text="LibraryGo",
            bg=DARK,
            fg="white",
            font=("Segoe UI", 20, "bold"),
        ).pack(side="left", padx=28)

        if show_menu:
            tk.Button(
                bar,
                text="Menú",
                command=self.show_menu,
                bg=DARK,
                fg="white",
                activebackground=DARK,
                activeforeground="white",
                relief="flat",
                bd=0,
                font=("Segoe UI", 10, "bold"),
                cursor="hand2",
            ).pack(side="right", padx=28)

        tk.Frame(self.root, bg=BG, height=2).pack(fill="x")

        area = tk.Frame(self.root, bg=BG)
        area.pack(fill="x", padx=34, pady=(22, 8))

        tk.Label(
            area,
            text=title,
            bg=BG,
            fg=INK,
            font=("Segoe UI", 26, "bold"),
        ).pack(anchor="w")

        if subtitle:
            tk.Label(
                area,
                text=subtitle,
                bg=BG,
                fg=MUTED,
                font=("Segoe UI", 11),
            ).pack(anchor="w", pady=(3, 0))

    def create_scrollable_body(self, bg=BG):
        outer = tk.Frame(self.root, bg=bg)
        outer.pack(fill="both", expand=True)

        canvas = tk.Canvas(
            outer,
            bg=bg,
            highlightthickness=0,
            bd=0,
        )
        scrollbar = ttk.Scrollbar(
            outer,
            orient="vertical",
            command=canvas.yview,
        )
        body = tk.Frame(canvas, bg=bg)

        window_id = canvas.create_window(
            (0, 0),
            window=body,
            anchor="nw",
        )

        def update_scroll_region(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))

        def resize_body(event):
            canvas.itemconfigure(window_id, width=event.width)

        body.bind("<Configure>", update_scroll_region)
        canvas.bind("<Configure>", resize_body)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def on_mousewheel(event):
            try:
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            except tk.TclError:
                pass

        canvas.bind_all("<MouseWheel>", on_mousewheel)

        return body

    def add_book_image(self, parent, book, max_size=(210, 290)):
        if book.imagen:
            path = IMAGES_DIR / book.imagen
            if path.exists():
                try:
                    img = Image.open(path).convert("RGB")
                    img.thumbnail(max_size)
                    photo = ImageTk.PhotoImage(img)
                    self.images.append(photo)
                    label = tk.Label(parent, image=photo, bg=parent.cget("bg"))
                    label.pack()
                    return label
                except Exception:
                    pass

        label = tk.Label(
            parent,
            text="Portada\nno disponible",
            bg="#EDE7DB",
            fg=MUTED,
            font=("Segoe UI", 10, "bold"),
            width=19,
            height=12,
        )
        label.pack()
        return label

    # --------------------------------------------------------
    # INTRODUCCION - PRIMERA INTERFAZ
    # --------------------------------------------------------

    def show_introduction(self):
        self.clear()
        self.root.configure(bg=BG)

        body = tk.Frame(self.root, bg=BG)
        body.pack(fill="both", expand=True)

        top = tk.Frame(body, bg=DARK, height=90)
        top.pack(fill="x")
        top.pack_propagate(False)

        tk.Label(
            top,
            text="LibraryGo",
            bg=DARK,
            fg="white",
            font=("Segoe UI", 25, "bold"),
        ).pack(side="left", padx=45)

        tk.Label(
            top,
            text="Sistema de recomendación de libros",
            bg=DARK,
            fg="#D9D3C8",
            font=("Segoe UI", 11),
        ).pack(side="right", padx=45)

        content = tk.Frame(body, bg=BG)
        content.pack(fill="both", expand=True, padx=65, pady=45)

        left = tk.Frame(content, bg=BG)
        left.pack(fill="both", expand=True)

        tk.Label(
            left,
            text="INTRODUCCIÓN",
            bg=BG,
            fg=ACCENT,
            font=("Segoe UI", 13, "bold"),
        ).pack(anchor="w")

        tk.Label(
            left,
            text="Encuentra una lectura acorde con tus preferencias",
            bg=BG,
            fg=INK,
            font=("Segoe UI", 29, "bold"),
            wraplength=850,
            justify="left",
        ).pack(anchor="w", pady=(8, 15))

        intro = (
            "LibraryGo es un Sistema Basado en Conocimiento orientado a facilitar "
            "la elección de libros. El sistema obtiene las preferencias del usuario "
            "mediante un cuestionario de diez preguntas de Verdadero/Falso y convierte "
            "las respuestas en hechos que son procesados por un Motor de Inferencia.\n\n"
            "El motor aplica reglas lógicas con operadores AND, OR y NOT, considera "
            "respuestas positivas y negativas, genera preferencias inferidas y calcula "
            "una puntuación para cada libro. Finalmente presenta hasta diez recomendaciones "
            "ordenadas de acuerdo con la evidencia obtenida."
        )

        card = tk.Frame(
            left,
            bg=CARD,
            highlightbackground=LINE,
            highlightthickness=1,
        )
        card.pack(fill="x", pady=18)

        tk.Label(
            card,
            text=intro,
            bg=CARD,
            fg=MUTED,
            font=("Segoe UI", 11),
            wraplength=940,
            justify="left",
        ).pack(padx=28, pady=25)

        meth = tk.Frame(left, bg="#ECE5D9")
        meth.pack(fill="x", pady=8)

        tk.Label(
            meth,
            text="Sistema de Recomendación basado en Cuestionarios de Verdadero/Falso",
            bg="#ECE5D9",
            fg=INK,
            font=("Segoe UI", 11, "bold"),
            wraplength=900,
        ).pack(padx=25, pady=18)

        tk.Label(
            left,
            text=(
                "Problema que resuelve: la gran cantidad de opciones disponibles puede "
                "dificultar la selección de una lectura adecuada. LibraryGo utiliza reglas "
                "explícitas para deducir recomendaciones a partir de las respuestas del usuario."
            ),
            bg=BG,
            fg=MUTED,
            font=("Segoe UI", 10),
            wraplength=940,
            justify="left",
        ).pack(anchor="w", pady=(12, 24))

        self.rounded_button(
            left,
            "Ir al menú",
            self.show_menu,
            primary=True,
            width=18,
        ).pack(anchor="w", pady=(4, 20))

    # --------------------------------------------------------
    # MENU
    # --------------------------------------------------------

    def show_menu(self):
        self.clear()
        self.root.configure(bg=BG)
        self.header("Menú", "Selecciona una sección de LibraryGo", show_menu=False)

        body = tk.Frame(self.root, bg=BG)
        body.pack(fill="both", expand=True, padx=70, pady=30)
        body.columnconfigure((0, 1), weight=1)
        body.rowconfigure(0, weight=1)

        sections = [
            (
                "Cuestionario V/F",
                "Responde 10 preguntas de Verdadero/Falso para que el Motor de Inferencia genere hasta 10 recomendaciones.",
                self.show_questionnaire,
            ),
            (
                "Catálogo",
                f"Consulta la Base de Conocimientos original ({len(BASE_ORIGINAL)} libros) y el Catálogo Extendido ({len(CATALOGO_EXTENDIDO)} libros).",
                self.show_catalog,
            ),
        ]

        for col, (title, description, command) in enumerate(sections):
            card = tk.Frame(
                body,
                bg=CARD,
                highlightbackground=LINE,
                highlightthickness=1,
            )
            card.grid(
                row=0,
                column=col,
                padx=18,
                pady=18,
                sticky="nsew",
            )

            tk.Label(
                card,
                text=f"0{col + 1}",
                bg=ACCENT,
                fg="white",
                font=("Segoe UI", 13, "bold"),
                width=4,
            ).pack(pady=(55, 25))

            tk.Label(
                card,
                text=title,
                bg=CARD,
                fg=INK,
                font=("Segoe UI", 21, "bold"),
            ).pack(pady=5)

            tk.Label(
                card,
                text=description,
                bg=CARD,
                fg=MUTED,
                font=("Segoe UI", 11),
                wraplength=400,
                justify="center",
            ).pack(padx=45, pady=25)

            self.rounded_button(
                card,
                "Abrir sección",
                command,
                primary=True,
                width=18,
            ).pack(pady=(10, 55))

    # --------------------------------------------------------
    # CUESTIONARIO V/F
    # --------------------------------------------------------

    def show_questionnaire(self):
        self.clear()
        self.root.configure(bg=BG)
        self.header(
            "Cuestionario de Verdadero/Falso",
            "Tus respuestas se convierten en hechos para el Motor de Inferencia.",
        )

        body = self.create_scrollable_body(BG)
        form = tk.Frame(body, bg=CARD, highlightbackground=LINE, highlightthickness=1)
        form.pack(fill="x", padx=55, pady=15)

        tk.Label(
            form,
            text="Responde las 10 preguntas",
            bg=CARD,
            fg=INK,
            font=("Segoe UI", 17, "bold"),
        ).pack(anchor="w", padx=28, pady=(25, 5))

        tk.Label(
            form,
            text="Verdadero suma evidencia positiva; Falso puede generar exclusión y reglas negativas.",
            bg=CARD,
            fg=MUTED,
            font=("Segoe UI", 10),
        ).pack(anchor="w", padx=28, pady=(0, 20))

        self.question_vars = []

        for index, (question, _) in enumerate(PREGUNTAS, start=1):
            var = tk.StringVar(value="")
            self.question_vars.append(var)

            qcard = tk.Frame(form, bg="#FAF8F3", highlightbackground=LINE, highlightthickness=1)
            qcard.pack(fill="x", padx=25, pady=7)

            tk.Label(
                qcard,
                text=f"{index}. {question}",
                bg="#FAF8F3",
                fg=INK,
                font=("Segoe UI", 11, "bold"),
                wraplength=760,
                justify="left",
            ).pack(side="left", padx=18, pady=17, anchor="w")

            options = tk.Frame(qcard, bg="#FAF8F3")
            options.pack(side="right", padx=18)

            tk.Radiobutton(
                options,
                text="Verdadero",
                variable=var,
                value="true",
                bg="#FAF8F3",
                activebackground="#FAF8F3",
                font=("Segoe UI", 10),
            ).pack(anchor="w")

            tk.Radiobutton(
                options,
                text="Falso",
                variable=var,
                value="false",
                bg="#FAF8F3",
                activebackground="#FAF8F3",
                font=("Segoe UI", 10),
            ).pack(anchor="w")

        button_area = tk.Frame(form, bg=CARD)
        button_area.pack(fill="x", pady=25)

        self.rounded_button(
            button_area,
            "Obtener recomendaciones",
            self.run_questionnaire,
            primary=True,
            width=22,
        ).pack(side="left", padx=28)

        self.rounded_button(
            button_area,
            "Restablecer",
            self.reset_questionnaire,
            width=16,
        ).pack(side="left", padx=5)

        self.question_results = tk.Frame(body, bg=BG)
        self.question_results.pack(fill="x", padx=55, pady=(5, 35))

    def reset_questionnaire(self):
        for variable in self.question_vars:
            variable.set("")

        for widget in self.question_results.winfo_children():
            widget.destroy()

    def run_questionnaire(self):
        if not self.question_vars:
            return

        if any(var.get() == "" for var in self.question_vars):
            messagebox.showwarning(
                "Cuestionario incompleto",
                "Responde las 10 preguntas antes de obtener recomendaciones.",
            )
            return

        respuestas = [var.get() == "true" for var in self.question_vars]
        results = MOTOR.recomendaciones_por_cuestionario(respuestas, 10)

        for widget in self.question_results.winfo_children():
            widget.destroy()

        tk.Label(
            self.question_results,
            text="Tus recomendaciones",
            bg=BG,
            fg=INK,
            font=("Segoe UI", 20, "bold"),
        ).pack(anchor="w", pady=(5, 4))

        tk.Label(
            self.question_results,
            text="Las categorías se asignan según la puntuación final del motor.",
            bg=BG,
            fg=MUTED,
            font=("Segoe UI", 10),
        ).pack(anchor="w", pady=(0, 12))

        for position, (book, score) in enumerate(results, start=1):
            self.create_recommendation_card(
                self.question_results,
                book,
                score,
                position,
            )

    def create_recommendation_card(self, parent, book, score, position):
        card = tk.Frame(
            parent,
            bg=CARD,
            highlightbackground=LINE,
            highlightthickness=1,
        )
        card.pack(fill="x", pady=6)

        cover = tk.Frame(card, bg=CARD, width=95)
        cover.pack(side="left", padx=15, pady=12)
        cover.pack_propagate(False)
        self.add_book_image(cover, book, (78, 110))

        information = tk.Frame(card, bg=CARD)
        information.pack(side="left", fill="both", expand=True, padx=10, pady=16)

        tk.Label(
            information,
            text=f"{position}. {book.nombre}",
            bg=CARD,
            fg=INK,
            font=("Segoe UI", 13, "bold"),
            wraplength=580,
            justify="left",
        ).pack(anchor="w")

        tk.Label(
            information,
            text=f"{book.autor}  •  {book.anio}  •  {book.editorial}",
            bg=CARD,
            fg=MUTED,
            font=("Segoe UI", 9),
            wraplength=650,
            justify="left",
        ).pack(anchor="w", pady=(5, 3))

        tk.Label(
            information,
            text=" • ".join(book.clasificaciones),
            bg=CARD,
            fg=ACCENT,
            font=("Segoe UI", 9),
            wraplength=650,
            justify="left",
        ).pack(anchor="w")

        badge = tk.Label(
            card,
            text=rating_label(score),
            bg=rating_color(score),
            fg="white",
            font=("Segoe UI", 10, "bold"),
            padx=12,
            pady=7,
        )
        badge.pack(side="left", padx=15)

        tk.Button(
            card,
            text="Ver libro",
            command=lambda b=book: self.show_book_detail(b),
            bg=CARD,
            fg=ACCENT,
            activebackground=LINE,
            relief="flat",
            bd=0,
            font=("Segoe UI", 9, "bold"),
            cursor="hand2",
        ).pack(side="right", padx=18)

    # --------------------------------------------------------
    # CATALOGO
    # --------------------------------------------------------

    def show_catalog(self):
        self.clear()
        self.root.configure(bg=BG)
        self.header(
            "Catálogo",
            "Consulta por separado la Base de Conocimientos y el Catálogo Extendido.",
        )

        body = tk.Frame(self.root, bg=BG)
        body.pack(fill="both", expand=True, padx=30, pady=12)
        body.columnconfigure((0, 1), weight=1)
        body.rowconfigure(0, weight=1)

        self.original_panel = self.create_catalog_panel(
            body,
            "Base de Conocimientos",
            BASE_ORIGINAL,
            0,
            "Acceso gratuito",
        )
        self.extended_panel = self.create_catalog_panel(
            body,
            f"Catálogo Extendido ({len(CATALOGO_EXTENDIDO)} libros)",
            CATALOGO_EXTENDIDO,
            1,
            "Sección de paga",
        )

    def create_catalog_panel(self, parent, title, books, column, access_text):
        panel = tk.Frame(
            parent,
            bg=CARD,
            highlightbackground=LINE,
            highlightthickness=1,
        )
        panel.grid(row=0, column=column, sticky="nsew", padx=8)

        tk.Label(
            panel,
            text=title,
            bg=CARD,
            fg=INK,
            font=("Segoe UI", 15, "bold"),
        ).pack(anchor="w", padx=18, pady=(16, 3))

        tk.Label(
            panel,
            text=access_text,
            bg=CARD,
            fg=ACCENT,
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w", padx=18, pady=(0, 10))

        search = tk.Entry(
            panel,
            font=("Segoe UI", 10),
            relief="solid",
            bd=1,
        )
        search.pack(fill="x", padx=18, pady=(0, 8), ipady=6)

        frame = tk.Frame(panel, bg=CARD)
        frame.pack(fill="both", expand=True, padx=12, pady=(0, 12))

        tree = ttk.Treeview(
            frame,
            columns=("libro", "autor", "anio"),
            show="headings",
            height=17,
        )
        tree.heading("libro", text="Libro")
        tree.heading("autor", text="Autor")
        tree.heading("anio", text="Año")
        tree.column("libro", width=260, anchor="w")
        tree.column("autor", width=170, anchor="w")
        tree.column("anio", width=65, anchor="center")

        scroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scroll.set)
        tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        tree.book_results = {}

        def populate(book_list):
            for item in tree.get_children():
                tree.delete(item)
            tree.book_results.clear()

            for book in book_list:
                iid = str(id(book))
                tree.insert(
                    "",
                    "end",
                    iid=iid,
                    values=(book.nombre, book.autor, book.anio),
                )
                tree.book_results[iid] = book

        def filter_books(event=None):
            query = normalize(search.get())
            if not query:
                populate(books)
                return
            filtered = [
                book for book in books
                if query in normalize(book.nombre)
                or query in normalize(book.autor)
                or query in normalize(book.editorial)
            ]
            populate(filtered)

        search.bind("<KeyRelease>", filter_books)
        tree.bind(
            "<Double-1>",
            lambda event: self.open_catalog_row(event, tree),
        )
        populate(books)

        return tree

    def open_catalog_row(self, event, tree):
        item = tree.identify_row(event.y)
        if not item:
            return
        book = tree.book_results.get(item)
        if book:
            self.show_book_detail(book)

    # --------------------------------------------------------
    # DETALLE DEL LIBRO
    # --------------------------------------------------------

    def show_book_detail(self, book):
        self.close_pdf()
        self.current_book = book
        self.images = []
        self.clear()
        self.root.configure(bg=BG)
        self.header(
            "Interfaz del libro",
            "Información, acceso al contenido y recomendaciones por similitud.",
        )

        body = self.create_scrollable_body(BG)

        center = tk.Frame(body, bg=BG)
        center.pack(fill="x", padx=55, pady=10)

        info = tk.Frame(
            center,
            bg=CARD,
            highlightbackground=LINE,
            highlightthickness=1,
        )
        info.pack(anchor="center")

        cover_area = tk.Frame(info, bg=CARD)
        cover_area.pack(side="left", padx=28, pady=25)
        self.add_book_image(cover_area, book, (205, 280))

        data = tk.Frame(info, bg=CARD, width=600)
        data.pack(side="left", fill="y", padx=(5, 35), pady=28)
        data.pack_propagate(False)

        tk.Label(
            data,
            text=book.nombre,
            bg=CARD,
            fg=INK,
            font=("Segoe UI", 24, "bold"),
            wraplength=600,
            justify="left",
        ).pack(anchor="w")

        tk.Label(
            data,
            text=f"Autor: {book.autor}",
            bg=CARD,
            fg=MUTED,
            font=("Segoe UI", 11),
        ).pack(anchor="w", pady=(13, 3))
        tk.Label(
            data,
            text=f"Editorial: {book.editorial}",
            bg=CARD,
            fg=MUTED,
            font=("Segoe UI", 11),
        ).pack(anchor="w", pady=3)
        tk.Label(
            data,
            text=f"Año de publicación: {book.anio}",
            bg=CARD,
            fg=MUTED,
            font=("Segoe UI", 11),
        ).pack(anchor="w", pady=3)
        tk.Label(
            data,
            text=f"Tipo de lector: {book.tipo_lector()}",
            bg=CARD,
            fg=MUTED,
            font=("Segoe UI", 11),
        ).pack(anchor="w", pady=3)

        tk.Label(
            data,
            text="Clasificaciones",
            bg=CARD,
            fg=INK,
            font=("Segoe UI", 10, "bold"),
        ).pack(anchor="w", pady=(15, 4))

        tk.Label(
            data,
            text=" • ".join(book.clasificaciones),
            bg=CARD,
            fg=ACCENT,
            font=("Segoe UI", 10),
            wraplength=600,
            justify="left",
        ).pack(anchor="w")

        origin_text = (
            "Base de Conocimientos - acceso gratuito"
            if book.origen == "original"
            else "Catálogo Extendido - acceso de paga"
        )

        tk.Label(
            data,
            text=origin_text,
            bg=CARD,
            fg=ACCENT,
            font=("Segoe UI", 10, "bold"),
        ).pack(anchor="w", pady=(16, 0))

        # ----------------------------------------------------
        # CONTENIDO
        # ----------------------------------------------------

        content_card = tk.Frame(
            body,
            bg=CARD,
            highlightbackground=LINE,
            highlightthickness=1,
        )
        content_card.pack(fill="x", padx=55, pady=10)

        tk.Label(
            content_card,
            text="Contenido del libro",
            bg=CARD,
            fg=INK,
            font=("Segoe UI", 18, "bold"),
        ).pack(anchor="w", padx=22, pady=(18, 7))

        self.detail_content = tk.Frame(
            content_card,
            bg="#F0EDE6",
            height=125,
        )
        self.detail_content.pack(fill="x", padx=22, pady=(0, 12))
        self.detail_content.pack_propagate(False)

        if book.origen == "extendido":
            message = (
                "Esta sección únicamente es de paga.\n"
                "Realiza el pago para poder acceder al contenido."
            )
        else:
            message = (
                "Contenido disponible en la Base de Conocimientos.\n"
                "Presiona 'Leer libro' para cargar el lector."
            )

        tk.Label(
            self.detail_content,
            text=message,
            bg="#F0EDE6",
            fg=WARNING if book.origen == "extendido" else MUTED,
            font=("Segoe UI", 11, "bold"),
            justify="center",
        ).pack(expand=True)

        self.rounded_button(
            content_card,
            "Acceder al contenido" if book.origen == "extendido" else "Leer libro",
            lambda: self.read_book(book),
            primary=True,
        ).pack(pady=(0, 18))

        # ----------------------------------------------------
        # RECOMENDACIONES POR SIMILITUD
        # ----------------------------------------------------

        tk.Label(
            body,
            text="Posibles recomendaciones",
            bg=BG,
            fg=INK,
            font=("Segoe UI", 18, "bold"),
        ).pack(anchor="w", padx=55, pady=(8, 7))

        rec_frame = tk.Frame(body, bg=BG)
        rec_frame.pack(fill="x", padx=55, pady=(0, 25))

        recommendations = MOTOR.recomendaciones_por_libro(book, 4)

        for recommended, score in recommendations:
            card = tk.Frame(
                rec_frame,
                bg=CARD,
                highlightbackground=LINE,
                highlightthickness=1,
            )
            card.pack(side="left", fill="both", expand=True, padx=4)

            tk.Label(
                card,
                text=recommended.nombre,
                bg=CARD,
                fg=INK,
                font=("Segoe UI", 11, "bold"),
                wraplength=235,
            ).pack(padx=10, pady=(12, 4))

            tk.Label(
                card,
                text=f"{recommended.autor}\n{score} coincidencias",
                bg=CARD,
                fg=MUTED,
                font=("Segoe UI", 9),
                justify="center",
            ).pack(padx=8, pady=(0, 9))

            tk.Button(
                card,
                text="Ver",
                command=lambda b=recommended: self.show_book_detail(b),
                bg=CARD,
                fg=ACCENT,
                activebackground=CARD,
                relief="flat",
                bd=0,
                font=("Segoe UI", 9, "bold"),
                cursor="hand2",
            ).pack(pady=(0, 11))

    # --------------------------------------------------------
    # LECTURA
    # --------------------------------------------------------

    def read_book(self, book):
        if book.origen == "extendido":
            for widget in self.detail_content.winfo_children():
                widget.destroy()

            tk.Label(
                self.detail_content,
                text=(
                    "Esta sección únicamente es de paga.\n"
                    "Realiza el pago para poder acceder al contenido."
                ),
                bg="#F0EDE6",
                fg=WARNING,
                font=("Segoe UI", 12, "bold"),
                justify="center",
            ).pack(expand=True)
            return

        self.show_reader_loading(book)

    def show_reader_loading(self, book):
        self.clear()
        self.root.configure(bg=BG)
        self.header("Lector", book.nombre)

        box = tk.Frame(
            self.root,
            bg=CARD,
            highlightbackground=LINE,
            highlightthickness=1,
        )
        box.pack(expand=True, fill="both", padx=80, pady=40)

        tk.Label(
            box,
            text="cargando....",
            bg=CARD,
            fg=MUTED,
            font=("Segoe UI", 18, "bold"),
        ).pack(expand=True)

        self.root.after(650, lambda: self.show_reader(book))

    def show_reader(self, book):
        self.clear()
        self.root.configure(bg="#E7E3DA")
        self.header("Lector", f"{book.nombre}  •  {book.autor}")

        main = tk.Frame(self.root, bg="#E7E3DA")
        main.pack(fill="both", expand=True, padx=45, pady=12)
        main.rowconfigure(0, weight=1)
        main.columnconfigure(0, weight=1)

        page_card = tk.Frame(
            main,
            bg="#D9D5CC",
            highlightbackground=LINE,
            highlightthickness=1,
        )
        page_card.grid(row=0, column=0, sticky="nsew")

        self.reader_label = tk.Label(
            page_card,
            text="Preparando el libro...",
            bg="#D9D5CC",
            fg=MUTED,
            font=("Segoe UI", 11),
        )
        self.reader_label.pack(expand=True)

        controls = tk.Frame(self.root, bg=DARK, height=68)
        controls.pack(fill="x")
        controls.pack_propagate(False)

        self.previous_btn = tk.Button(
            controls,
            text="◀ Página anterior",
            command=self.previous_page,
            bg=DARK,
            fg="white",
            activebackground=DARK,
            activeforeground="white",
            relief="flat",
            bd=0,
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
        )
        self.previous_btn.pack(side="left", padx=25)

        self.page_label = tk.Label(
            controls,
            text="Página -",
            bg=DARK,
            fg="white",
            font=("Segoe UI", 10, "bold"),
        )
        self.page_label.pack(side="left", expand=True)

        tk.Button(
            controls,
            text="Volver al libro",
            command=lambda: self.show_book_detail(book),
            bg=DARK,
            fg="white",
            activebackground=DARK,
            activeforeground="white",
            relief="flat",
            bd=0,
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
        ).pack(side="left", padx=20)

        self.next_btn = tk.Button(
            controls,
            text="Página siguiente ▶",
            command=self.next_page,
            bg=DARK,
            fg="white",
            activebackground=DARK,
            activeforeground="white",
            relief="flat",
            bd=0,
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
        )
        self.next_btn.pack(side="right", padx=25)

        self.current_book = book
        self.current_page = 0
        self.images = []

        if not book.pdf:
            self.reader_label.config(text="No hay un PDF disponible para este libro.")
            self.previous_btn.config(state="disabled")
            self.next_btn.config(state="disabled")
            self.page_label.config(text="PDF no disponible")
            return

        pdf_path = BOOKS_DIR / book.pdf
        if not pdf_path.exists():
            self.reader_label.config(text=f"No se encontró el archivo:\n{book.pdf}")
            self.previous_btn.config(state="disabled")
            self.next_btn.config(state="disabled")
            self.page_label.config(text="PDF no disponible")
            return

        try:
            self.pdf_doc = fitz.open(pdf_path)
            self.show_page()
        except Exception as exc:
            self.reader_label.config(text=f"No se pudo abrir el PDF.\n{exc}")
            self.previous_btn.config(state="disabled")
            self.next_btn.config(state="disabled")

    def show_page(self):
        if not self.pdf_doc or len(self.pdf_doc) == 0:
            return

        page = self.pdf_doc[self.current_page]
        pix = page.get_pixmap(matrix=fitz.Matrix(1.15, 1.15), alpha=False)
        image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        available_width = max(self.root.winfo_width() - 150, 700)
        available_height = max(self.root.winfo_height() - 210, 430)
        image.thumbnail((available_width, available_height))

        self.pdf_image = ImageTk.PhotoImage(image)
        self.reader_label.config(image=self.pdf_image, text="")

        total = len(self.pdf_doc)
        self.page_label.config(
            text=f"Página {self.current_page + 1} de {total}"
        )

        self.previous_btn.config(
            state="normal" if self.current_page > 0 else "disabled"
        )
        self.next_btn.config(
            state="normal" if self.current_page < total - 1 else "disabled"
        )

    def previous_page(self):
        if self.pdf_doc and self.current_page > 0:
            self.current_page -= 1
            self.show_page()

    def next_page(self):
        if self.pdf_doc and self.current_page < len(self.pdf_doc) - 1:
            self.current_page += 1
            self.show_page()

    def close_pdf(self):
        if self.pdf_doc is not None:
            try:
                self.pdf_doc.close()
            except Exception:
                pass
            self.pdf_doc = None

    def close(self):
        self.close_pdf()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryGo(root)
    root.protocol("WM_DELETE_WINDOW", app.close)
    root.mainloop()
