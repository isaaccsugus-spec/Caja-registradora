import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
import os
from database import inicializar_base_datos, obtener_producto_por_codigo
from gestion_productos import VentanaGestionProductos
from fpdf import FPDF


def formato_precio(valor):
    """Formatea un precio a 2 decimales."""
    return "{:.2f}".format(valor)


class VentanaPagoEfectivo(ctk.CTkToplevel):
    def __init__(self, parent, total, cesta, callback_completado):
        super().__init__(parent)

        self.title("Pago en Efectivo")
        self.geometry("400x350")
        self.resizable(False, False)

        self.total = total
        self.cesta = cesta
        self.callback_completado = callback_completado

        self.crear_widgets()
        self.grab_set()

    def crear_widgets(self):
        self.label_titulo = ctk.CTkLabel(
            self,
            text="PAGO EN EFECTIVO",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.label_titulo.pack(pady=20)

        total_texto = "Total a pagar: " + formato_precio(self.total) + " EUR"
        self.label_total = ctk.CTkLabel(
            self,
            text=total_texto,
            font=ctk.CTkFont(size=18)
        )
        self.label_total.pack(pady=10)

        self.frame_entrada = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_entrada.pack(pady=20)

        self.label_recibido = ctk.CTkLabel(
            self.frame_entrada,
            text="Cantidad recibida (EUR):",
            font=ctk.CTkFont(size=16)
        )
        self.label_recibido.pack(side="left", padx=5)

        self.entry_recibido = ctk.CTkEntry(
            self.frame_entrada,
            width=120,
            font=ctk.CTkFont(size=16)
        )
        self.entry_recibido.pack(side="left", padx=5)
        self.entry_recibido.bind("<KeyRelease>", self.calcular_cambio)

        self.label_cambio = ctk.CTkLabel(
            self,
            text="Cambio a devolver:  0.00 EUR",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.label_cambio.pack(pady=10)

        self.frame_botones = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_botones.pack(pady=30)

        self.btn_cancelar = ctk.CTkButton(
            self.frame_botones,
            text="CANCELAR",
            command=self.destroy,
            width=120,
            fg_color="#95a5a6",
            hover_color="#7f8c8d"
        )
        self.btn_cancelar.pack(side="left", padx=10)

        self.btn_cobrar = ctk.CTkButton(
            self.frame_botones,
            text="COBRAR",
            command=self.procesar_pago,
            width=120,
            fg_color="#27ae60",
            hover_color="#1e8449"
        )
        self.btn_cobrar.pack(side="left", padx=10)

    def calcular_cambio(self, event=None):
        try:
            recibido = float(self.entry_recibido.get())
            cambio = recibido - self.total
            if cambio >= 0:
                texto = "Cambio a devolver:  " + formato_precio(cambio) + " EUR"
            else:
                texto = "Falta:  " + formato_precio(abs(cambio)) + " EUR"
            self.label_cambio.configure(text=texto)
        except ValueError:
            self.label_cambio.configure(text="Cambio a devolver: 0.00 EUR")

    def procesar_pago(self):
        try:
            recibido = float(self.entry_recibido.get())
        except ValueError:
            messagebox.showerror("Error", "Introduce una cantidad valida.")
            return

        if recibido < self.total:
            falta = formato_precio(self.total - recibido)
            messagebox.showerror("Error", "Cantidad insuficiente.  Faltan " + falta + " EUR")
            return

        cambio = recibido - self.total

        generar_ticket(self.cesta, self.total, "EFECTIVO", recibido, cambio)

        mensaje = "Pago realizado correctamente\n\n"
        mensaje += "Total: " + formato_precio(self.total) + " EUR\n"
        mensaje += "Recibido: " + formato_precio(recibido) + " EUR\n"
        mensaje += "Cambio: " + formato_precio(cambio) + " EUR"

        messagebox.showinfo("Pago Completado", mensaje)

        self.callback_completado()
        self.destroy()


class VentanaPagoTarjeta(ctk.CTkToplevel):
    def __init__(self, parent, total, cesta, callback_completado):
        super().__init__(parent)

        self.title("Pago con Tarjeta")
        self.geometry("400x300")
        self.resizable(False, False)

        self.total = total
        self.cesta = cesta
        self.callback_completado = callback_completado

        self.crear_widgets()
        self.grab_set()

    def crear_widgets(self):
        self.label_titulo = ctk.CTkLabel(
            self,
            text="PAGO CON TARJETA",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.label_titulo.pack(pady=30)

        total_texto = "Total a cobrar: " + formato_precio(self.total) + " EUR"
        self.label_total = ctk.CTkLabel(
            self,
            text=total_texto,
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.label_total.pack(pady=20)

        self.label_info = ctk.CTkLabel(
            self,
            text="Esperando confirmacion del terminal.. .",
            font=ctk.CTkFont(size=14)
        )
        self.label_info.pack(pady=10)

        self.frame_botones = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_botones.pack(pady=40)

        self.btn_cancelar = ctk.CTkButton(
            self.frame_botones,
            text="CANCELAR",
            command=self.destroy,
            width=120,
            fg_color="#95a5a6",
            hover_color="#7f8c8d"
        )
        self.btn_cancelar.pack(side="left", padx=10)

        self.btn_confirmar = ctk.CTkButton(
            self.frame_botones,
            text="CONFIRMAR",
            command=self.procesar_pago,
            width=120,
            fg_color="#3498db",
            hover_color="#2980b9"
        )
        self.btn_confirmar.pack(side="left", padx=10)

    def procesar_pago(self):
        generar_ticket(self.cesta, self.total, "TARJETA", self.total, 0)

        mensaje = "Pago con tarjeta realizado correctamente\n\n"
        mensaje += "Total cobrado: " + formato_precio(self.total) + " EUR"

        messagebox.showinfo("Pago Completado", mensaje)

        self.callback_completado()
        self.destroy()


def generar_ticket(cesta, total, metodo_pago, recibido, cambio):
    if not os.path.exists("tickets"):
        os.makedirs("tickets")

    fecha_hora = datetime.now().strftime("%Y%m%d_%H%M%S")
    numero_ticket = datetime.now().strftime("%Y%m%d%H%M%S")
    nombre_archivo = "tickets/ticket_" + fecha_hora + ". pdf"

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "MI TIENDA S.L.", ln=True, align="C")
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 5, "C/ Ejemplo, 123", ln=True, align="C")
    pdf.cell(0, 5, "Tel: 912 345 678", ln=True, align="C")
    pdf.ln(5)

    pdf.cell(0, 0, "", ln=True, border="T")
    pdf.ln(3)

    pdf.set_font("Helvetica", "", 10)
    fecha_formateada = datetime.now().strftime("%d/%m/%Y %H:%M")
    pdf.cell(0, 5, "Fecha: " + fecha_formateada, ln=True)
    pdf.cell(0, 5, "Ticket: #" + numero_ticket, ln=True)
    pdf.ln(3)

    pdf.cell(0, 0, "", ln=True, border="T")
    pdf.ln(3)

    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(70, 6, "Producto", border=0)
    pdf.cell(20, 6, "Cant.", border=0, align="C")
    pdf.cell(30, 6, "Precio", border=0, align="R")
    pdf.cell(30, 6, "Subtotal", border=0, align="R")
    pdf.ln()

    pdf.set_font("Helvetica", "", 10)
    for item in cesta:
        nombre = item["nombre"][: 25]
        pdf.cell(70, 5, nombre, border=0)
        pdf.cell(20, 5, str(item["cantidad"]), border=0, align="C")
        pdf.cell(30, 5, formato_precio(item["precio_unitario"]), border=0, align="R")
        pdf.cell(30, 5, formato_precio(item["subtotal"]), border=0, align="R")
        pdf.ln()

    pdf.ln(3)
    pdf.cell(0, 0, "", ln=True, border="T")
    pdf.ln(3)

    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(120, 8, "TOTAL:", border=0)
    pdf.cell(30, 8, formato_precio(total) + " EUR", border=0, align="R")
    pdf.ln(10)

    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 5, "Metodo de pago:  " + metodo_pago, ln=True)

    if metodo_pago == "EFECTIVO":
        pdf.cell(0, 5, "Recibido: " + formato_precio(recibido) + " EUR", ln=True)
        pdf.cell(0, 5, "Cambio:  " + formato_precio(cambio) + " EUR", ln=True)

    pdf.ln(10)

    pdf.set_font("Helvetica", "I", 10)
    pdf.cell(0, 5, "Gracias por su compra!", ln=True, align="C")

    pdf.output(nombre_archivo)
    print("Ticket generado:  " + nombre_archivo)

    try:
        ruta_completa = os.path.abspath(nombre_archivo)
        os.startfile(ruta_completa)
    except Exception as e:
        print("No se pudo abrir el PDF: " + str(e))


class CajaRegistradora(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("CAJA REGISTRADORA")
        self.geometry("900x650")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.cesta = []
        self.total = 0.0

        self.crear_widgets()

    def crear_widgets(self):
        # Cabecera
        self.frame_cabecera = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_cabecera.pack(fill="x", padx=20, pady=10)

        self.label_titulo = ctk.CTkLabel(
            self.frame_cabecera,
            text="CAJA REGISTRADORA",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        self.label_titulo.pack(side="left")

        self.btn_gestion = ctk.CTkButton(
            self.frame_cabecera,
            text="Productos",
            command=self.abrir_gestion_productos,
            width=120
        )
        self.btn_gestion.pack(side="right")

        # Escaner
        self.frame_escaner = ctk.CTkFrame(self)
        self.frame_escaner.pack(fill="x", padx=20, pady=10)

        self.label_escaner = ctk.CTkLabel(
            self.frame_escaner,
            text="Codigo:",
            font=ctk.CTkFont(size=16)
        )
        self.label_escaner.pack(side="left", padx=10)

        self.entry_codigo = ctk.CTkEntry(
            self.frame_escaner,
            width=200,
            font=ctk.CTkFont(size=16),
            placeholder_text="Escanear o escribir codigo..."
        )
        self.entry_codigo.pack(side="left", padx=10)
        self.entry_codigo.bind("<Return>", self.escanear_producto)

        self.btn_buscar = ctk.CTkButton(
            self.frame_escaner,
            text="Buscar",
            command=self.escanear_producto,
            width=100
        )
        self.btn_buscar.pack(side="left", padx=10)

        # Cesta
        self.frame_cesta = ctk.CTkFrame(self)
        self.frame_cesta.pack(fill="both", expand=True, padx=20, pady=10)

        self.label_cesta = ctk.CTkLabel(
            self.frame_cesta,
            text="CESTA DE COMPRA",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.label_cesta.pack(pady=10)

        # Cabeceras
        self.frame_cabeceras = ctk.CTkFrame(self.frame_cesta, fg_color="transparent")
        self.frame_cabeceras.pack(fill="x", padx=10)

        cabeceras = [("Codigo", 100), ("Producto", 200), ("Cant.", 60), ("Precio", 80), ("Subtotal", 80), ("", 60)]
        for texto, ancho in cabeceras:
            label = ctk.CTkLabel(
                self.frame_cabeceras,
                text=texto,
                font=ctk.CTkFont(size=12, weight="bold"),
                width=ancho
            )
            label.pack(side="left", padx=5)

        # Frame productos
        self.frame_productos = ctk.CTkScrollableFrame(self.frame_cesta, height=250)
        self.frame_productos.pack(fill="both", expand=True, padx=10, pady=10)

        self.filas_cesta = []

        # Total
        self.frame_total = ctk.CTkFrame(self)
        self.frame_total.pack(fill="x", padx=20, pady=10)

        self.label_total = ctk.CTkLabel(
            self.frame_total,
            text="TOTAL:  0.00 EUR",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        self.label_total.pack(pady=10)

        # Botones pago
        self.frame_pago = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_pago.pack(pady=20)

        self.btn_tarjeta = ctk.CTkButton(
            self.frame_pago,
            text="TARJETA",
            command=self.pagar_tarjeta,
            width=150,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#3498db",
            hover_color="#2980b9"
        )
        self.btn_tarjeta.pack(side="left", padx=20)

        self.btn_efectivo = ctk.CTkButton(
            self.frame_pago,
            text="EFECTIVO",
            command=self.pagar_efectivo,
            width=150,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#27ae60",
            hover_color="#1e8449"
        )
        self.btn_efectivo.pack(side="left", padx=20)

        self.btn_cancelar = ctk.CTkButton(
            self.frame_pago,
            text="CANCELAR",
            command=self.cancelar_venta,
            width=150,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#e74c3c",
            hover_color="#c0392b"
        )
        self.btn_cancelar.pack(side="left", padx=20)

    def escanear_producto(self, event=None):
        codigo = self.entry_codigo.get().strip().upper()

        if not codigo:
            return

        producto = obtener_producto_por_codigo(codigo)

        if not producto:
            messagebox.showerror("Error", "Producto '" + codigo + "' no encontrado.")
            self.entry_codigo.delete(0, "end")
            return

        for item in self.cesta:
            if item["codigo"] == codigo:
                item["cantidad"] += 1
                item["subtotal"] = item["cantidad"] * item["precio_unitario"]
                self.actualizar_cesta()
                self.entry_codigo.delete(0, "end")
                return

        nuevo_item = {
            "codigo": producto[0],
            "nombre": producto[1],
            "precio_unitario": producto[2],
            "cantidad": 1,
            "subtotal": producto[2]
        }
        self.cesta.append(nuevo_item)

        self.actualizar_cesta()
        self.entry_codigo.delete(0, "end")

    def actualizar_cesta(self):
        for fila in self.filas_cesta:
            for widget in fila:
                widget.destroy()
        self.filas_cesta.clear()

        for i, item in enumerate(self.cesta):
            fila = []

            lbl_codigo = ctk.CTkLabel(self.frame_productos, text=item["codigo"], width=100)
            lbl_codigo.grid(row=i, column=0, padx=5, pady=3)
            fila.append(lbl_codigo)

            lbl_nombre = ctk.CTkLabel(self.frame_productos, text=item["nombre"], width=200)
            lbl_nombre.grid(row=i, column=1, padx=5, pady=3)
            fila.append(lbl_nombre)

            lbl_cantidad = ctk.CTkLabel(self.frame_productos, text=str(item["cantidad"]), width=60)
            lbl_cantidad.grid(row=i, column=2, padx=5, pady=3)
            fila.append(lbl_cantidad)

            precio_texto = formato_precio(item["precio_unitario"]) + " EUR"
            lbl_precio = ctk.CTkLabel(self.frame_productos, text=precio_texto, width=80)
            lbl_precio.grid(row=i, column=3, padx=5, pady=3)
            fila.append(lbl_precio)

            subtotal_texto = formato_precio(item["subtotal"]) + " EUR"
            lbl_subtotal = ctk.CTkLabel(self.frame_productos, text=subtotal_texto, width=80)
            lbl_subtotal.grid(row=i, column=4, padx=5, pady=3)
            fila.append(lbl_subtotal)

            btn_eliminar = ctk.CTkButton(
                self.frame_productos,
                text="X",
                width=50,
                fg_color="#e74c3c",
                hover_color="#c0392b",
                command=lambda c=item["codigo"]: self.eliminar_de_cesta(c)
            )
            btn_eliminar.grid(row=i, column=5, padx=5, pady=3)
            fila.append(btn_eliminar)

            self.filas_cesta.append(fila)

        self.total = sum(item["subtotal"] for item in self.cesta)
        total_texto = "TOTAL: " + formato_precio(self.total) + " EUR"
        self.label_total.configure(text=total_texto)

    def eliminar_de_cesta(self, codigo):
        self.cesta = [item for item in self.cesta if item["codigo"] != codigo]
        self.actualizar_cesta()

    def cancelar_venta(self):
        if self.cesta:
            if messagebox.askyesno("Confirmar", "Cancelar la venta actual?"):
                self.cesta.clear()
                self.actualizar_cesta()

    def pagar_tarjeta(self):
        if not self.cesta:
            messagebox.showwarning("Atencion", "La cesta esta vacia.")
            return
        VentanaPagoTarjeta(self, self.total, self.cesta.copy(), self.venta_completada)

    def pagar_efectivo(self):
        if not self.cesta:
            messagebox.showwarning("Atencion", "La cesta esta vacia.")
            return
        VentanaPagoEfectivo(self, self.total, self.cesta.copy(), self.venta_completada)

    def venta_completada(self):
        self.cesta.clear()
        self.actualizar_cesta()

    def abrir_gestion_productos(self):
        VentanaGestionProductos(self)


def main():
    inicializar_base_datos()
    app = CajaRegistradora()
    app.mainloop()


if __name__ == "__main__":
    main()