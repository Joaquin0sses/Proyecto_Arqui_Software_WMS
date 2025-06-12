def parsear_mensaje(mensaje):
    partes = mensaje.strip().split('|')
    if len(partes) < 2:
        return None, None, []
    modulo = partes[0].lower()
    accion = partes[1].lower()
    argumentos = partes[2:]
    return modulo, accion, argumentos