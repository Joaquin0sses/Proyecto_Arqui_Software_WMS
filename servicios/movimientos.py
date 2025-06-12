import socket
from db.conexion import obtener_conexion
from utils.parser import parsear_mensaje

HOST = 'localhost'
PORT = 9003

def registrar(id_producto, tipo, observacion=""):
    conn = obtener_conexion()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO movimiento (id_producto, tipo_movimiento, observaciones) VALUES (%s, %s, %s)",
        (id_producto, tipo, observacion)
    )
    conn.commit()
    cur.close()
    conn.close()
    return f"Movimiento '{tipo}' registrado para producto {id_producto}."

def iniciar_servicio():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"[Servicio Movimientos] Escuchando en {PORT}")
        while True:
            conn, addr = s.accept()
            with conn:
                mensaje = conn.recv(4096).decode()
                modulo, accion, args = parsear_mensaje(mensaje)
                if accion == "ingresar" and len(args) >= 1:
                    respuesta = registrar(args[0], "entrada", args[1] if len(args) > 1 else "")
                elif accion == "salir" and len(args) >= 1:
                    respuesta = registrar(args[0], "salida", args[1] if len(args) > 1 else "")
                else:
                    respuesta = "Acción no válida o parámetros incorrectos."
                conn.sendall(respuesta.encode())

if __name__ == "__main__":
    iniciar_servicio()