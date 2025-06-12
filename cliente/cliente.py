import socket
from config import ESB_HOST, ESB_PORT

def enviar_mensaje(mensaje):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ESB_HOST, ESB_PORT))
        s.sendall(mensaje.encode())
        respuesta = s.recv(4096).decode()
        print(f"[CLIENTE] Respuesta: {respuesta}")

if __name__ == "__main__":
    enviar_mensaje("productos|crear|Camisa|0.1|0.3|Ropa|alta")