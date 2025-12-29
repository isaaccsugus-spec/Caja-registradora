# 🏪 Caja Registradora

Aplicación de punto de venta (TPV) desarrollada en Python con CustomTkinter. 

![Python](https://img.shields.io/badge/Python-3.8+-blue. svg)
![CustomTkinter](https://img.shields.io/badge/CustomTkinter-5.0+-green.svg)

## 🎮 Características

- Sistema de caja registradora completo
- Gestión de productos: 
  - **Añadir** productos con código, nombre y precio
  - **Editar** productos existentes
  - **Eliminar** productos de la base de datos
- Sistema de ventas:
  - Escanear/buscar productos por código
  - Cesta de compra con cantidades
  - Eliminar productos de la cesta
- Métodos de pago: 
  - **Efectivo** - Cálculo automático de cambio
  - **Tarjeta** - Confirmación de pago
- Generación de tickets en PDF
- Base de datos SQLite integrada
- Interfaz gráfica moderna (tema oscuro)

## 🚀 Instalación

1. Clona el repositorio: 
```bash
git clone https://github.com/isaaccsugus-spec/Caja-registradora.git
cd Caja-registradora
```

2. Instala las dependencias: 
```bash
pip install -r requirements. txt
```

3. Ejecuta la aplicación:
```bash
python main.py
```

## 🎯 Cómo usar

- **Escanear producto**: Escribe el código y pulsa Enter o click en "Buscar"
- **Añadir cantidad**: Escanea el mismo producto varias veces
- **Eliminar de cesta**: Click en "X" junto al producto
- **Pago efectivo**: Introduce cantidad recibida, muestra el cambio
- **Pago tarjeta**: Confirma el pago
- **Gestión productos**: Click en "Productos" para añadir/editar/eliminar

## 🛠️ Tecnologías

- Python 3.8+
- CustomTkinter 5.0+
- SQLite3
- FPDF

## 📁 Estructura

```
Caja-registradora/
├── database/
│   └── productos.db      # Base de datos
├── tickets/
│   └── ticket_xxx.pdf    # Tickets generados
├── database.py           # Lógica de base de datos
├── gestion_productos.py  # Ventana de gestión
├── main.py               # Aplicación principal
└── README.md
```

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. 
