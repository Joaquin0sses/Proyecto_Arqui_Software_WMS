import socket

HOST = 'localhost'
PORT = 8000  # Puerto del ESB

mensaje = "productos:obtener_productos"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(mensaje.encode())
    respuesta = s.recv(1024).decode()
    print(f"[Cliente] Respuesta del sistema: {respuesta}")
