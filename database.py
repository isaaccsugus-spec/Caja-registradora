import sqlite3
import os

# Rutas de la base de datos
DATABASE_DIR = "database"
DATABASE_PATH = os.path.join(DATABASE_DIR, "productos.db")


def conectar():
    """
    Crea la conexión con la base de datos.
    Si la carpeta 'database' no existe, la crea. 
    """
    if not os.path.exists(DATABASE_DIR):
        os.makedirs(DATABASE_DIR)
    
    conexion = sqlite3.connect(DATABASE_PATH)
    return conexion


def crear_tabla():
    """
    Crea la tabla 'productos' si no existe.
    """
    conexion = conectar()
    cursor = conexion.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            codigo TEXT PRIMARY KEY,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL
        )
    ''')
    
    conexion.commit()
    conexion.close()


def insertar_productos_ejemplo():
    """
    Inserta productos de ejemplo si la tabla está vacía. 
    """
    conexion = conectar()
    cursor = conexion.cursor()
    
    # Verificamos si ya hay productos
    cursor.execute('SELECT COUNT(*) FROM productos')
    cantidad = cursor.fetchone()[0]
    
    # Solo insertamos si la tabla está vacía
    if cantidad == 0:
        productos_ejemplo = [
            ('PRD001', 'Coca Cola 2L', 1.50),
            ('PRD002', 'Pan Integral', 1.20),
            ('PRD003', 'Leche Entera 1L', 0.95),
            ('PRD004', 'Agua Mineral 1.5L', 0.60),
            ('PRD005', 'Galletas María', 1.80)
        ]
        
        cursor.executemany(
            'INSERT INTO productos (codigo, nombre, precio) VALUES (?, ?, ?)',
            productos_ejemplo
        )
        
        conexion.commit()
        print("✅ Productos de ejemplo insertados correctamente.")
    
    conexion.close()


# ============================================
# FUNCIONES CRUD
# ============================================

def crear_producto(codigo, nombre, precio):
    """
    Añade un nuevo producto a la base de datos.
    Devuelve True si se creó correctamente, False si hubo error. 
    """
    try: 
        conexion = conectar()
        cursor = conexion.cursor()
        
        cursor.execute(
            'INSERT INTO productos (codigo, nombre, precio) VALUES (?, ?, ?)',
            (codigo, nombre, precio)
        )
        
        conexion.commit()
        conexion.close()
        return True
        
    except sqlite3.IntegrityError:
        conexion.close()
        return False


def obtener_productos():
    """
    Devuelve una lista con todos los productos. 
    """
    conexion = conectar()
    cursor = conexion.cursor()
    
    cursor.execute('SELECT codigo, nombre, precio FROM productos ORDER BY codigo')
    productos = cursor.fetchall()
    
    conexion.close()
    return productos


def obtener_producto_por_codigo(codigo):
    """
    Busca un producto por su código. 
    Devuelve el producto o None si no existe.
    """
    conexion = conectar()
    cursor = conexion. cursor()
    
    cursor.execute(
        'SELECT codigo, nombre, precio FROM productos WHERE codigo = ? ',
        (codigo,)
    )
    producto = cursor. fetchone()
    
    conexion.close()
    return producto


def actualizar_producto(codigo, nombre, precio):
    """
    Actualiza un producto existente.
    Devuelve True si se actualizó, False si no existía.
    """
    conexion = conectar()
    cursor = conexion.cursor()
    
    cursor.execute(
        'UPDATE productos SET nombre = ?, precio = ?  WHERE codigo = ?',
        (nombre, precio, codigo)
    )
    
    filas_afectadas = cursor.rowcount
    
    conexion.commit()
    conexion.close()
    
    return filas_afectadas > 0


def eliminar_producto(codigo):
    """
    Elimina un producto por su código.
    Devuelve True si se eliminó, False si no existía. 
    """
    conexion = conectar()
    cursor = conexion.cursor()
    
    cursor.execute(
        'DELETE FROM productos WHERE codigo = ?',
        (codigo,)
    )
    
    filas_afectadas = cursor.rowcount
    
    conexion.commit()
    conexion.close()
    
    return filas_afectadas > 0


# ============================================
# INICIALIZACIÓN
# ============================================

def inicializar_base_datos():
    """
    Inicializa la base de datos: 
    1. Crea la tabla si no existe
    2. Inserta productos de ejemplo si está vacía
    """
    print("🔧 Inicializando base de datos...")
    crear_tabla()
    insertar_productos_ejemplo()
    print("✅ Base de datos lista.")