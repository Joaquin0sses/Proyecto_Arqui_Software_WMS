import socket
from db.conexion import obtener_conexion
from utils.parser import parsear_mensaje

HOST = 'localhost'
PORT = 9001

def crear(nombre, tamano, peso, categoria, rotacion):
    conn = obtener_conexion()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO producto (nombre, tamano, peso, categoria, rotacion) VALUES (%s, %s, %s, %s, %s)",
        (nombre, tamano, peso, categoria, rotacion)
    )
    conn.commit()
    cur.close()
    conn.close()
    return "Producto creado con éxito."

def iniciar_servicio():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"[Servicio Productos] Escuchando en {PORT}")
        while True:
            conn, addr = s.accept()
            with conn:
                mensaje = conn.recv(4096).decode()
                modulo, accion, args = parsear_mensaje(mensaje)
                if accion == "crear" and len(args) == 5:
                    respuesta = crear(*args)
                else:
                    respuesta = "Acción no reconocida o parámetros incorrectos."
                conn.sendall(respuesta.encode())

if __name__ == "__main__":
    iniciar_servicio()