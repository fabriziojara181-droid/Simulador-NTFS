
import tkinter as tk
from tkinter import ttk, messagebox

from src.SistemaArchivos import SistemaArchivos


class VentanaPrincipal:
    def __init__(self, ventana: tk.Tk):
        self.ventana = ventana
        self.ventana.title("Simulador NTFS - Sistemas Operativos")
        self.ventana.geometry("1050x750")

        self.sistema = SistemaArchivos(32, 4)

        self.capacidad = tk.StringVar(value="32")
        self.cluster = tk.StringVar(value="4")
        self.nombre = tk.StringVar()
        self.tamano = tk.StringVar(value="3")
        self.resumen = tk.StringVar()
        self.mensaje = tk.StringVar(value="Simulador iniciado")

        self.construir_interfaz()
        self.actualizar()

    def construir_interfaz(self):
        contenedor = ttk.Frame(self.ventana, padding=15)
        contenedor.pack(fill="both", expand=True)

        ttk.Label(
            contenedor,
            text="Simulador de Sistema de Archivos NTFS",
            font=("Arial", 17, "bold")
        ).pack(pady=10)

        configuracion = ttk.LabelFrame(
            contenedor, text="Configuracion del disco", padding=10
        )
        configuracion.pack(fill="x", pady=5)

        ttk.Label(configuracion, text="Bloques:").pack(side="left")
        ttk.Entry(
            configuracion, textvariable=self.capacidad, width=10
        ).pack(side="left", padx=8)

        ttk.Label(configuracion, text="Cluster (KB):").pack(side="left")
        ttk.Combobox(
            configuracion,
            textvariable=self.cluster,
            values=["1", "2", "4", "8"],
            width=7,
            state="readonly"
        ).pack(side="left", padx=8)

        ttk.Button(
            configuracion,
            text="Reiniciar disco",
            command=self.reiniciar
        ).pack(side="left", padx=10)

        operaciones = ttk.LabelFrame(
            contenedor, text="Administracion de archivos", padding=10
        )
        operaciones.pack(fill="x", pady=5)

        ttk.Label(operaciones, text="Nombre:").pack(side="left")
        ttk.Entry(
            operaciones, textvariable=self.nombre, width=22
        ).pack(side="left", padx=6)

        ttk.Label(operaciones, text="Bloques:").pack(side="left")
        ttk.Entry(
            operaciones, textvariable=self.tamano, width=8
        ).pack(side="left", padx=6)

        ttk.Button(
            operaciones, text="Crear", command=self.crear
        ).pack(side="left", padx=4)

        ttk.Button(
            operaciones, text="Modificar", command=self.modificar
        ).pack(side="left", padx=4)

        ttk.Button(
            operaciones, text="Eliminar", command=self.eliminar
        ).pack(side="left", padx=4)

        ttk.Label(
            contenedor,
            textvariable=self.resumen,
            font=("Arial", 10, "bold")
        ).pack(pady=10)

        marco_mapa = ttk.LabelFrame(
            contenedor, text="Mapa de bloques del disco", padding=8
        )
        marco_mapa.pack(fill="both", expand=True, pady=5)

        self.canvas = tk.Canvas(marco_mapa, height=210)
        barra = ttk.Scrollbar(
            marco_mapa, orient="vertical", command=self.canvas.yview
        )
        self.marco_bloques = ttk.Frame(self.canvas)

        self.marco_bloques.bind(
            "<Configure>",
            lambda evento: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window(
            (0, 0), window=self.marco_bloques, anchor="nw"
        )
        self.canvas.configure(yscrollcommand=barra.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        barra.pack(side="right", fill="y")

        marco_tabla = ttk.LabelFrame(
            contenedor, text="MFT simulada - Archivos registrados", padding=8
        )
        marco_tabla.pack(fill="both", expand=True, pady=5)

        columnas = ("nombre", "tamano", "extensiones")

        self.tabla = ttk.Treeview(
            marco_tabla, columns=columnas, show="headings", height=6
        )

        self.tabla.heading("nombre", text="Archivo")
        self.tabla.heading("tamano", text="Bloques")
        self.tabla.heading("extensiones", text="Extensiones")
        self.tabla.column("nombre", width=170)
        self.tabla.column("tamano", width=80)
        self.tabla.column("extensiones", width=450)
        self.tabla.pack(fill="both", expand=True)

        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_archivo)

        ttk.Label(
            contenedor, textvariable=self.mensaje
        ).pack(pady=5)

    def ejecutar(self, operacion):
        # Mostramos los errores sin cerrar el programa
        try:
            operacion()
            self.actualizar()
        except (ValueError, IndexError) as error:
            messagebox.showerror("Operacion no realizada", str(error))

    def crear(self):
        def operacion():
            archivo = self.sistema.crear_archivo(
                self.nombre.get(),
                int(self.tamano.get())
            )
            self.mensaje.set(f"Archivo creado: {archivo.nombre}")

        self.ejecutar(operacion)

    def eliminar(self):
        def operacion():
            nombre = self.nombre.get().strip()
            self.sistema.eliminar_archivo(nombre)
            self.mensaje.set(f"Archivo eliminado: {nombre}")

        self.ejecutar(operacion)

    def modificar(self):
        def operacion():
            nombre = self.nombre.get().strip()
            nuevo = int(self.tamano.get())
            self.sistema.modificar_tamano(nombre, nuevo)
            self.mensaje.set(f"Tamaño actualizado: {nombre}")

        self.ejecutar(operacion)

    def reiniciar(self):
        respuesta = messagebox.askyesno(
            "Reiniciar disco",
            "Se eliminaran los archivos simulados. ¿Continuar?"
        )

        if not respuesta:
            return

        def operacion():
            self.sistema = SistemaArchivos(
                int(self.capacidad.get()),
                int(self.cluster.get())
            )
            self.mensaje.set("Disco reiniciado correctamente")

        self.ejecutar(operacion)

    def seleccionar_archivo(self, evento):
        seleccion = self.tabla.selection()

        if seleccion:
            valores = self.tabla.item(seleccion[0], "values")
            self.nombre.set(valores[0])
            self.tamano.set(valores[1])

    def actualizar(self):
        metricas = self.sistema.obtener_metricas()

        self.resumen.set(
            f"Total: {metricas['total']} | "
            f"Ocupados: {metricas['ocupados']} | "
            f"Libres: {metricas['libres']} | "
            f"Ocupacion: {metricas['porcentaje']}% | "
            f"Extensiones: {metricas['extensiones']} | "
            f"Grupos libres: {metricas['grupos_libres']}"
        )

        # Dibujamos nuevamente el estado de cada bloque
        for elemento in self.marco_bloques.winfo_children():
            elemento.destroy()

        mapa = self.sistema.mapa_disco()

        for posicion, archivo in enumerate(mapa):
            color = "#B9E4C9" if archivo is None else "#94BFF1"
            texto = f"{posicion}\nLibre" if archivo is None else f"{posicion}\nOcupado"

            etiqueta = tk.Label(
                self.marco_bloques,
                text=texto,
                bg=color,
                fg="#172B4D",
                width=10,
                height=2,
                relief="ridge"
            )
            etiqueta.grid(
                row=posicion // 10,
                column=posicion % 10,
                padx=2,
                pady=2
            )

        for elemento in self.tabla.get_children():
            self.tabla.delete(elemento)

        for registro in self.sistema.consultar_mft():
            self.tabla.insert(
                "",
                "end",
                values=(
                    registro["nombre"],
                    registro["tamano"],
                    str(registro["extensiones"])
                )
            )
