from ipaddress import IPv4Address, IPv4Network
from .validaciones import validar_red_cidr, validar_prefijo, validar_numero_subredes


# calcula toda la info de una red a partir de su notacion CIDR
def calcular_info_red(red_cidr):
    red = validar_red_cidr(red_cidr)

    bits_host = 32 - red.prefixlen
    total_direcciones = red.num_addresses
    hosts_utilizables = max(total_direcciones - 2, 0)

    return {
        "red": str(red.network_address),
        "prefijo": red.prefixlen,
        "mascara": str(red.netmask),
        "mascara_wildcard": str(red.hostmask),
        "broadcast": str(red.broadcast_address),
        "primer_host": str(IPv4Address(int(red.network_address) + 1)) if hosts_utilizables > 0 else "N/A",
        "ultimo_host": str(IPv4Address(int(red.broadcast_address) - 1)) if hosts_utilizables > 0 else "N/A",
        "total_direcciones": total_direcciones,
        "hosts_utilizables": hosts_utilizables,
        "bits_host": bits_host,
        "clase": obtener_clase(red.network_address),
        "tipo": obtener_tipo(red),
    }


# divide una red base en N subredes iguales del mismo tamano
def dividir_en_subredes(red_cidr, num_subredes):
    red = validar_red_cidr(red_cidr)
    num_subredes = validar_numero_subredes(str(num_subredes))

    # calculamos cuantos bits extra necesitamos para tener suficientes subredes
    bits_extra = 0
    while 2 ** bits_extra < num_subredes:
        bits_extra += 1

    nuevo_prefijo = red.prefixlen + bits_extra

    if nuevo_prefijo > 32:
        raise ValueError(
            f"No es posible dividir la red en {num_subredes} subredes. "
            f"El prefijo resultante ({nuevo_prefijo}) supera /32."
        )

    # generamos todas las subredes posibles con el nuevo prefijo
    subredes_posibles = list(red.subnets(new_prefix=nuevo_prefijo))

    bits_host = 32 - nuevo_prefijo
    total_dir = 2 ** bits_host
    hosts_util = max(total_dir - 2, 0)

    resultados = []
    for i, subred in enumerate(subredes_posibles):
        net_int = int(subred.network_address)
        resultados.append({
            "indice": i + 1,
            "red": str(subred.network_address),
            "prefijo": nuevo_prefijo,
            "mascara": str(subred.netmask),
            "primer_host": str(IPv4Address(net_int + 1)) if hosts_util > 0 else "N/A",
            "ultimo_host": str(IPv4Address(net_int + total_dir - 2)) if hosts_util > 0 else "N/A",
            "broadcast": str(subred.broadcast_address),
            "hosts_utilizables": hosts_util,
            "total_direcciones": total_dir,
        })

    return {
        "red_base": str(red),
        "prefijo_original": red.prefixlen,
        "bits_extra": bits_extra,
        "nuevo_prefijo": nuevo_prefijo,
        "subredes_solicitadas": num_subredes,
        "subredes_generadas": len(subredes_posibles),
        "subredes": resultados,
    }


# dado un prefijo objetivo, calcula cuantas subredes se pueden obtener
# y cuantos hosts tiene cada una a partir de una red base
def calcular_subredes_por_prefijo(red_cidr, nuevo_prefijo):
    red = validar_red_cidr(red_cidr)
    nuevo_prefijo = validar_prefijo(str(nuevo_prefijo))

    if nuevo_prefijo < red.prefixlen:
        raise ValueError(
            f"El prefijo /{nuevo_prefijo} es mas grande que la red base /{red.prefixlen}."
        )

    subredes = list(red.subnets(new_prefix=nuevo_prefijo))
    bits_host = 32 - nuevo_prefijo
    total_dir = 2 ** bits_host
    hosts_util = max(total_dir - 2, 0)

    resultados = []
    for i, subred in enumerate(subredes):
        net_int = int(subred.network_address)
        resultados.append({
            "indice": i + 1,
            "red": str(subred.network_address),
            "prefijo": nuevo_prefijo,
            "mascara": str(subred.netmask),
            "primer_host": str(IPv4Address(net_int + 1)) if hosts_util > 0 else "N/A",
            "ultimo_host": str(IPv4Address(net_int + total_dir - 2)) if hosts_util > 0 else "N/A",
            "broadcast": str(subred.broadcast_address),
            "hosts_utilizables": hosts_util,
            "total_direcciones": total_dir,
        })

    return {
        "red_base": str(red),
        "prefijo_original": red.prefixlen,
        "nuevo_prefijo": nuevo_prefijo,
        "cantidad_subredes": len(subredes),
        "hosts_por_subred": hosts_util,
        "subredes": resultados,
    }


# dice a que clase (A, B, C, D, E) pertenece la direccion
def obtener_clase(ip_address):
    primer_octeto = int(str(ip_address).split(".")[0])
    if primer_octeto < 128:
        return "A"
    elif primer_octeto < 192:
        return "B"
    elif primer_octeto < 224:
        return "C"
    elif primer_octeto < 240:
        return "D (Multicast)"
    else:
        return "E (Reservada)"


# indica si la red es privada, loopback, link-local o publica
def obtener_tipo(red):
    if red.is_private:
        return "Privada"
    elif red.is_loopback:
        return "Loopback"
    elif red.is_link_local:
        return "Link-local"
    else:
        return "Publica"
