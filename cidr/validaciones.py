from ipaddress import IPv4Address, IPv4Network


def validar_red_cidr(texto):
    texto = texto.strip()

    # necesitamos el formato IP/prefijo
    partes = texto.split("/")
    if len(partes) != 2:
        raise ValueError(
            "Ingresa la red en formato CIDR, "
            "ejemplo: 192.168.1.0/24"
        )

    ip, prefijo = partes

    # validamos que la IP sea valida
    try:
        direccion = IPv4Address(ip)
    except ValueError:
        raise ValueError(
            "La direccion IP ingresada no es valida."
        )

    # el prefijo tiene que ser un numero
    if not prefijo.isascii() or not prefijo.isdecimal():
        raise ValueError(
            "El prefijo debe ser un numero entero."
        )
    prefijo = int(prefijo)

    if not 0 <= prefijo <= 32:
        raise ValueError(
            "El prefijo debe estar entre 0 y 32."
        )

    # obtenemos la red correcta (strict=False acepta hosts dentro de la red)
    red = IPv4Network((direccion, prefijo), strict=False)

    # avisamos si ingresaron una IP de host en lugar de la direccion de red
    if direccion != red.network_address:
        raise ValueError(
            f"La direccion ingresada no es una direccion de red. "
            f"Quisiste decir {red}?"
        )

    return red


def validar_prefijo(texto):
    texto = str(texto).strip()

    if not texto:
        raise ValueError(
            "Debes ingresar un prefijo."
        )

    if not texto.isascii() or not texto.isdecimal():
        raise ValueError(
            "El prefijo debe ser un numero entero positivo."
        )

    prefijo = int(texto)

    if not 0 <= prefijo <= 32:
        raise ValueError(
            "El prefijo debe estar entre 0 y 32."
        )

    return prefijo


def validar_numero_subredes(texto):
    texto = str(texto).strip()

    if not texto:
        raise ValueError(
            "Debes ingresar la cantidad de subredes."
        )

    if not texto.isascii() or not texto.isdecimal():
        raise ValueError(
            "La cantidad de subredes debe ser un numero entero positivo."
        )

    n = int(texto)

    if n == 0:
        raise ValueError(
            "La cantidad de subredes debe ser mayor a cero."
        )

    if n > 2**32:
        raise ValueError(
            "La cantidad de subredes es demasiado grande."
        )

    return n
