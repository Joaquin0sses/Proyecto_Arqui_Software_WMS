import socket
from config import SERVICIOS
from utils.protocolo import interpretar_mensaje

HOST, PORT = SERVICIOS["productos"]

def manejar(accion, datos):
    if accion == "listar":
        return {"productos": ["Caja", "Palet", "Bolsa"]}
    elif accion == "crear":
        return {"mensaje": f"Producto '{datos.get('nombre')}' registrado"}
    else:
        return {"error": "Acción no reconocida"}

def iniciar_servicio():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"[Servicio Productos] Escuchando en {PORT}")
        while True:
            conn, addr = s.accept()
            with conn:
                mensaje = conn.recv(4096).decode()
                peticion = interpretar_mensaje(mensaje)
                respuesta = manejar(peticion.get("accion"), peticion.get("datos"))
                conn.sendall(json.dumps(respuesta).encode())

if __name__ == "__main__":
    iniciar_servicio()