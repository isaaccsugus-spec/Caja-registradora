# 🏪 Caja Registradora

Aplicación de caja registradora con interfaz gráfica desarrollada en Python. 

## ✨ Funcionalidades

- 📦 Gestión de productos (añadir, editar, eliminar)
- 🔍 Escanear productos por código
- 🛒 Cesta de compra
- 💵 Pago en efectivo (con cálculo de cambio)
- 💳 Pago con tarjeta
- 🧾 Generación de tickets en PDF

## 🛠️ Tecnologías

- Python 3
- CustomTkinter (interfaz gráfica)
- SQLite (base de datos)
- FPDF (generación de PDFs)

## 📦 Instalación

```bash
# Clonar repositorio
git clone https://github.com/isaaccsugus-spec/Caja-registradora.git
cd Caja-registradora

# Instalar dependencias
pip install customtkinter fpdf

# Ejecutar
python main.py
```

## 📁 Estructura

```
Caja-registradora/
├── database/
│   └── productos.db
├── tickets/
│   └── (tickets generados)
├── database.py
├── gestion_productos. py
├── main.py
└── README.md
```

## 👤 Autor

- [@isaaccsugus-spec](https://github.com/isaaccsugus-spec)
