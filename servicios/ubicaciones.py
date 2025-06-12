import socket
from db.conexion import obtener_conexion
from utils.parser import parsear_mensaje

HOST = 'localhost'
PORT = 9002

def crear(codigo, capacidad, disponible):
    conn = obtener_conexion()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO ubicacion (codigo, capacidad, disponible) VALUES (%s, %s, %s)",
        (codigo, capacidad, disponible == '1')
    )
    conn.commit()
    cur.close()
    conn.close()
    return "Ubicación registrada correctamente."

def listar():
    conn = obtener_conexion()
    cur = conn.cursor()
    cur.execute("SELECT codigo, capacidad, disponible FROM ubicacion")
    filas = cur.fetchall()
    cur.close()
    conn.close()
    return "\n".join([f"Codigo: {c}, Capacidad: {cap}, Disponible: {d}" for c, cap, d in filas])

def iniciar_servicio():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"[Servicio Ubicaciones] Escuchando en {PORT}")
        while True:
            conn, addr = s.accept()
            with conn:
                mensaje = conn.recv(4096).decode()
                modulo, accion, args = parsear_mensaje(mensaje)
                if accion == "crear" and len(args) == 3:
                    respuesta = crear(*args)
                elif accion == "listar":
                    respuesta = listar()
                else:
                    respuesta = "Acción no válida o parámetros incorrectos."
                conn.sendall(respuesta.encode())

if __name__ == "__main__":
    iniciar_servicio()