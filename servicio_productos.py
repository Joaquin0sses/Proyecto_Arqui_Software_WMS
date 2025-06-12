import socket

HOST = 'localhost'
PORT = 9001  # Puerto único del servicio

def handle_request(data):
    if data == "obtener_productos":
        return "Lista de productos: [Producto1, Producto2]"
    return "Comando no reconocido."

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"[Servicio Productos] Esperando conexiones en {PORT}")
    while True:
        conn, addr = s.accept()
        with conn:
            print(f"[Servicio Productos] Conexión desde {addr}")
            data = conn.recv(1024).decode()
            print(f"[Servicio Productos] Solicitud recibida: {data}")
            response = handle_request(data)
            conn.sendall(response.encode())