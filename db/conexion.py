import psycopg2

def obtener_conexion():
    return psycopg2.connect(
        host='localhost',
        database='wms',
        user='postgres',
        password='tu_contraseña_aqui'
    )