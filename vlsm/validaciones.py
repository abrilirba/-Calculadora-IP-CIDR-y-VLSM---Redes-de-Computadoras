from ipaddress import IPv4Address, IPv4Network

def validar_red_base(texto):
    """
    Valida la red base ingresada por el usuario.

    Recibe una direccion de red en formato CIDR
    Ejemplo: 192.168.0.0/24

    Devuelve un objeto IPv4Network si la red es valida.
    """

    texto = texto.strip()

    # separamos la direccion IP del prefijo
    partes = texto.split("/")
    if len(partes) != 2:
        raise ValueError(
            "Ingresa la red en formato CIDR, "
            "ejemplo 192.168.0.0/24"
        )

    ip, prefijo = partes

    # validamos la direccion IPv4
    try:
        direccion = IPv4Address(ip)
    except ValueError:
        raise ValueError(
            "La direccion IP ingresada no es valida."
        )

    # validamos el prefijo
    if not prefijo.isascii() or not prefijo.isdecimal():
        raise ValueError(
            "El prefijo debe ser un numero entero."
        )
    prefijo = int(prefijo)

    if not 0 <= prefijo <= 32:
        raise ValueError(
            "El prefijo debe estar entre 0 y 32."
        )

    # obtenemos la red a la que pertenece la direccion
    red = IPv4Network((direccion, prefijo), strict=False)

    # comprobamos que se ingreso una direccion de red
    if direccion != red.network_address:
        raise ValueError(
            f"La direccion IP ingresada no es una direccion de red. "
            f"Utiliza {red}."
        )

    return red


# funcion para validar la cantidad de hosts
def validar_hosts(texto):

    # convertimos la entrada a texto y eliminamos espacios
    texto = str(texto).strip()

    # comprobamos que se ingreso algun valor
    if not texto:
        raise ValueError(
            "Debes ingresar la cantidad de hosts."
        )

    # comprobamos que sea un numero entero positivo
    if not texto.isascii() or not texto.isdecimal():
        raise ValueError(
            "La cantidad de hosts debe ser un numero entero positivo."
        )

    # convertimos el texto a un numero entero
    hosts = int(texto)

    # no permitimos cantidades iguales a cero
    if hosts == 0:
        raise ValueError(
            "La cantidad de hosts debe ser mayor a cero."
        )

    # comprobamos el limite maximo de hosts para una red IPv4
    if hosts > 2**32 - 2:
        raise ValueError(
            "La cantidad de hosts supera el limite maximo para una red IPv4 (4,294,967,294)."
        )

    return hosts
