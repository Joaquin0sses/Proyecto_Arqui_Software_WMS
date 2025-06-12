import socket
from config import ESB_HOST, ESB_PORT, SERVICIOS
from utils.parser import parsear_mensaje

def redirigir(modulo, mensaje):
    if modulo not in SERVICIOS:
        return "[ERROR] Servicio no disponible"
    host, port = SERVICIOS[modulo]
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(mensaje.encode())
        return s.recv(4096).decode()

def iniciar_bus():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((ESB_HOST, ESB_PORT))
        s.listen()
        print(f"[ESB] Escuchando en puerto {ESB_PORT}")
        while True:
            conn, addr = s.accept()
            with conn:
                mensaje = conn.recv(4096).decode()
                modulo, _, _ = parsear_mensaje(mensaje)
                respuesta = redirigir(modulo, mensaje)
                conn.sendall(respuesta.encode())

if __name__ == "__main__":
    iniciar_bus()