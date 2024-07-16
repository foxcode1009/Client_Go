# creamos la base de datos con sqlite

import sqlite3


def DDBB():
    # hacemos la conexion
    conexion = sqlite3.connect("client_GO.db")

    cursor = conexion.cursor()

    # craamos la tabla
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS productos(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Nombre TEXT,
        Talla TEXT,
        Unidades INTEGER,
        Precio_fabrica INTEGER,
        Precio_cliente INTEGER,
        Total_invertido INTEGER,
        Ganancia INTEGER,
        Descripcion TEXT,
        Imagen TEXT
                    )
    """)

    # creamos la tabla para el usuario
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombres TEXT NOT NULL,
        apellidos TEXT NOT NULL,
        email TEXT UNIQUE,
        password TEXT NOT NULL
                    )
    """)

    # creamos la tabla ventas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ventas(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        producto TEXT NOT NULL,
        id_prd TEXT NOT NULL,
        cantidad INTEGER NOT NULL,
        valor_uni INTEGER,
        total_vent INTEGER,
        ganancia INTEGER,
        fecha DATETIME NOT NULL
                    )
    """)

    # creamos la tabla para los gastos

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS gastos(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Nombre_gasto TEXT NOT NULL,
            Valor_gasto INTEGER NOT NULL,
            Fecha DATETIME NOT NULL
                        )
        """)

    # creamos tabla para reporte

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reportes(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Mes TEXT NOT NULL,
            Gastos INTEGER,
            Total_vendido INTEGER,
            Ganancia_mes INTEGER,
            Ganancia_final INTEGER,
            Fecha_reporte DATETIME
                        )
        """)

    # guardamos los cambio
    conexion.commit()

    # cerramos la base de datos para que no de errores
    conexion.close()


DDBB()
