import socket
from config import ESB_HOST, ESB_PORT
from utils.protocolo import construir_mensaje

def enviar_solicitud(servicio, accion, datos=None):
    mensaje = construir_mensaje(servicio, accion, datos)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ESB_HOST, ESB_PORT))
        s.sendall(mensaje.encode())
        respuesta = s.recv(4096).decode()
        print(f"[Cliente] Respuesta: {respuesta}")

# Prueba: obtener lista de productos
if __name__ == "__main__":
    enviar_solicitud("productos", "listar")
    enviar_solicitud("productos", "crear", {"nombre": "Estantería"})