import socket

SERVICIOS = {
    "productos": ("localhost", 9001),
    "pedidos": ("localhost", 9002),  # si tuvieras más servicios
}

HOST = 'localhost'
PORT = 8000  # Puerto del bus

def redirigir_a_servicio(servicio_clave, mensaje):
    if servicio_clave not in SERVICIOS:
        return "Servicio no disponible."
    
    ip, puerto = SERVICIOS[servicio_clave]
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((ip, puerto))
        s.sendall(mensaje.encode())
        return s.recv(1024).decode()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"[ESB] Escuchando en puerto {PORT}")
    while True:
        conn, addr = s.accept()
        with conn:
            print(f"[ESB] Conexión desde {addr}")
            data = conn.recv(1024).decode()
            print(f"[ESB] Solicitud: {data}")
            try:
                servicio, comando = data.split(":", 1)
                respuesta = redirigir_a_servicio(servicio, comando)
            except Exception as e:
                respuesta = f"Error en formato: {str(e)}"
            conn.sendall(respuesta.encode())
            