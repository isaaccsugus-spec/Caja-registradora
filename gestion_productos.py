import customtkinter as ctk
from tkinter import messagebox
from database import (
    obtener_productos,
    obtener_producto_por_codigo,
    crear_producto,
    actualizar_producto,
    eliminar_producto
)


class VentanaGestionProductos(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)

        self.title("Gestion de Productos")
        self.geometry("700x500")

        self.modo_edicion = False
        self.codigo_editando = None

        self.crear_widgets()
        self.actualizar_tabla()
        self.grab_set()

    def crear_widgets(self):
        self.label_titulo = ctk.CTkLabel(
            self,
            text="GESTION DE PRODUCTOS",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.label_titulo.pack(pady=15)

        self.frame_tabla = ctk.CTkFrame(self)
        self.frame_tabla.pack(fill="both", expand=True, padx=20, pady=10)

        cabeceras = ["Codigo", "Nombre", "Precio"]
        for i, cabecera in enumerate(cabeceras):
            label = ctk.CTkLabel(
                self.frame_tabla,
                text=cabecera,
                font=ctk.CTkFont(size=12, weight="bold")
            )
            label.grid(row=0, column=i, padx=15, pady=8, sticky="w")

        self.filas_tabla = []

        self.frame_acciones = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_acciones.pack(pady=10)

        self.btn_anadir = ctk.CTkButton(
            self.frame_acciones,
            text="ANADIR",
            command=self.modo_anadir,
            width=100
        )
        self.btn_anadir.grid(row=0, column=0, padx=5)

        self.btn_eliminar = ctk.CTkButton(
            self.frame_acciones,
            text="ELIMINAR",
            command=self.eliminar,
            width=100,
            fg_color="#e74c3c",
            hover_color="#c0392b"
        )
        self.btn_eliminar.grid(row=0, column=1, padx=5)

        self.frame_formulario = ctk.CTkFrame(self)
        self.frame_formulario.pack(fill="x", padx=20, pady=10)

        self.label_codigo = ctk.CTkLabel(self.frame_formulario, text="Codigo:")
        self.label_codigo.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.entry_codigo = ctk.CTkEntry(self.frame_formulario, width=150)
        self.entry_codigo.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        self.label_nombre = ctk.CTkLabel(self.frame_formulario, text="Nombre:")
        self.label_nombre.grid(row=0, column=2, padx=10, pady=5, sticky="e")
        self.entry_nombre = ctk.CTkEntry(self.frame_formulario, width=150)
        self.entry_nombre.grid(row=0, column=3, padx=10, pady=5, sticky="w")

        self.label_precio = ctk.CTkLabel(self.frame_formulario, text="Precio:")
        self.label_precio.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.entry_precio = ctk.CTkEntry(self.frame_formulario, width=150)
        self.entry_precio.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        self.btn_guardar = ctk.CTkButton(
            self.frame_formulario,
            text="GUARDAR",
            command=self.guardar,
            fg_color="#27ae60",
            hover_color="#1e8449"
        )
        self.btn_guardar.grid(row=1, column=2, columnspan=2, padx=10, pady=5)

    def actualizar_tabla(self):
        for fila in self.filas_tabla:
            for widget in fila:
                widget.destroy()
        self.filas_tabla.clear()

        productos = obtener_productos()

        for i, producto in enumerate(productos):
            codigo, nombre, precio = producto
            fila = []

            btn_codigo = ctk.CTkButton(
                self.frame_tabla,
                text=codigo,
                font=ctk.CTkFont(size=11),
                fg_color="transparent",
                text_color=("gray10", "gray90"),
                hover_color=("gray70", "gray30"),
                anchor="w",
                width=80,
                command=lambda c=codigo: self.seleccionar_producto(c)
            )
            btn_codigo.grid(row=i + 1, column=0, padx=15, pady=3, sticky="w")
            fila.append(btn_codigo)

            label_nombre = ctk.CTkLabel(self.frame_tabla, text=nombre)
            label_nombre.grid(row=i + 1, column=1, padx=15, pady=3, sticky="w")
            fila.append(label_nombre)

            precio_texto = "{:.2f}".format(precio)
            label_precio = ctk.CTkLabel(self.frame_tabla, text=precio_texto + " EUR")
            label_precio.grid(row=i + 1, column=2, padx=15, pady=3, sticky="w")
            fila.append(label_precio)

            self.filas_tabla.append(fila)

    def seleccionar_producto(self, codigo):
        producto = obtener_producto_por_codigo(codigo)
        if producto:
            self.limpiar_formulario()
            self.entry_codigo.insert(0, producto[0])
            self.entry_nombre.insert(0, producto[1])
            self.entry_precio.insert(0, str(producto[2]))
            self.modo_edicion = True
            self.codigo_editando = codigo
            self.entry_codigo.configure(state="disabled")

    def modo_anadir(self):
        self.limpiar_formulario()
        self.modo_edicion = False
        self.entry_codigo.focus()

    def eliminar(self):
        codigo = self.entry_codigo.get()
        if not codigo:
            messagebox.showwarning("Atencion", "Selecciona un producto.")
            return

        if messagebox.askyesno("Confirmar", "Eliminar " + codigo + "? "):
            if eliminar_producto(codigo):
                messagebox.showinfo("Exito", "Producto eliminado.")
                self.limpiar_formulario()
                self.actualizar_tabla()

    def guardar(self):
        codigo = self.entry_codigo.get().strip()
        nombre = self.entry_nombre.get().strip()
        precio_str = self.entry_precio.get().strip()

        if not codigo or not nombre or not precio_str:
            messagebox.showwarning("Atencion", "Completa todos los campos.")
            return

        try:
            precio = float(precio_str)
        except ValueError:
            messagebox.showerror("Error", "Precio invalido.")
            return

        if self.modo_edicion:
            actualizar_producto(codigo, nombre, precio)
            messagebox.showinfo("Exito", "Producto actualizado.")
        else:
            if crear_producto(codigo, nombre, precio):
                messagebox.showinfo("Exito", "Producto creado.")
            else:
                messagebox.showerror("Error", "El codigo ya existe.")

        self.limpiar_formulario()
        self.actualizar_tabla()

    def limpiar_formulario(self):
        self.entry_codigo.configure(state="normal")
        self.entry_codigo.delete(0, "end")
        self.entry_nombre.delete(0, "end")
        self.entry_precio.delete(0, "end")
        self.modo_edicion = False