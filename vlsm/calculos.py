from .validaciones import validar_hosts
from ipaddress import IPv4Address, IPv4Network
from .validaciones import validar_red_base, validar_hosts

# calcula el bloque necesario para una cantidad de hosts
def calcular_bloque(hosts_solicitados):

    # validamos la cantidad de hosts
    hosts_solicitados = validar_hosts(hosts_solicitados)

    # comenzamos con la cantidad minima de bits
    bits_host = 2

    # buscamos los bits necesarios para acomodar los hosts
    while (2 ** bits_host - 2) < hosts_solicitados:
        bits_host += 1

    # calculamos el prefijo de la subred
    prefijo = 32 - bits_host

    # calculamos el total de direcciones del bloque
    total_direcciones = 2 ** bits_host

    # calculamos los hosts utilizables
    hosts_utilizables = total_direcciones - 2

    # calculamos los hosts que sobran
    hosts_sobrantes = hosts_utilizables - hosts_solicitados

    # retornamos los resultados
    return {
        "hosts_solicitados": hosts_solicitados,
        "bits_host": bits_host,
        "prefijo": prefijo,
        "total_direcciones": total_direcciones,
        "hosts_utilizables": hosts_utilizables,
        "hosts_sobrantes": hosts_sobrantes
    }


# funcion principal para asignar subredes mediante VLSM
def calcular_vlsm(red_base, requerimientos):

    # validamos la red base
    red = validar_red_base(red_base)

    # lista para almacenar los bloques necesarios
    bloques = []

    # calculamos el bloque necesario para cada subred
    for nombre, hosts in requerimientos:

        nombre = nombre.strip()

        if not nombre:
            raise ValueError(
                "Cada subred debe tener un nombre."
            )
        bloque = calcular_bloque(hosts)
        bloque["nombre"] = nombre
        bloques.append(bloque)

    # comprobamos que exista al menos una subred
    if not bloques:
        raise ValueError(
            "Debes ingresar al menos una subred."
        )

    # ordenamos los bloques de mayor a menor
    bloques.sort(
        key=lambda bloque: bloque["hosts_solicitados"],
        reverse=True
    )

    # calculamos las direcciones necesarias
    total_asignado = sum(
        b["total_direcciones"] for b in bloques
    )

    # verificamos que todos los bloques quepan en la red
    if total_asignado > red.num_addresses:
        raise ValueError(
            f"Espacio insuficiente: se necesitan "
            f"{total_asignado} direcciones, pero la red "
            f"solo tiene {red.num_addresses}."
        )

    # convertimos la direccion inicial a un entero
    actual = int(red.network_address)

    # lista para almacenar las subredes calculadas
    resultados = []

    # asignamos cada bloque consecutivamente
    for bloque in bloques:

        # creamos la subred con su prefijo
        subred = IPv4Network(
            (actual, bloque["prefijo"])
        )

        # guardamos los resultados de la subred
        resultado = {
            **bloque,
            "red": str(subred.network_address),
            "mascara": str(subred.netmask),
            "primer_host": str(
                IPv4Address(actual + 1)
            ),
            "ultimo_host": str(
                IPv4Address(
                    actual + bloque["total_direcciones"] - 2
                )
            ),
            "broadcast": str(subred.broadcast_address)
        }

        resultados.append(resultado)

        # avanzamos al inicio del siguiente bloque
        actual += bloque["total_direcciones"]

    # retornamos las subredes y un resumen
    return {
        "red_base": str(red_base),
        "subredes": resultados,
        "direcciones_totales": red.num_addresses,
        "direcciones_asignadas": total_asignado,
        "direcciones_restantes": (
            red.num_addresses - total_asignado
        ),
        "hosts_solicitados": sum(
            b["hosts_solicitados"] for b in bloques
        ),
        "hosts_utilizables": sum(
            b["hosts_utilizables"] for b in bloques
        ),
        "hosts_sobrantes": sum(
            b["hosts_sobrantes"] for b in bloques
        )
    }
