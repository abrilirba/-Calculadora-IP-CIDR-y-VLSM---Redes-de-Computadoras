from .calculos import calcular_info_red, dividir_en_subredes, calcular_subredes_por_prefijo


SEPARADOR = "-" * 55


def mostrar_info_red(resultado):
    print(f"\n{'=' * 55}")
    print(f"  Informacion de la Red")
    print(f"{'=' * 55}")
    print(f"  Direccion de red   : {resultado['red']}/{resultado['prefijo']}")
    print(f"  Mascara de subred  : {resultado['mascara']}")
    print(f"  Wildcard mask      : {resultado['mascara_wildcard']}")
    print(f"  Broadcast          : {resultado['broadcast']}")
    print(f"  Primer host        : {resultado['primer_host']}")
    print(f"  Ultimo host        : {resultado['ultimo_host']}")
    print(f"  Hosts utilizables  : {resultado['hosts_utilizables']}")
    print(f"  Total direcciones  : {resultado['total_direcciones']}")
    print(f"  Bits de host       : {resultado['bits_host']}")
    print(f"  Clase              : {resultado['clase']}")
    print(f"  Tipo               : {resultado['tipo']}")
    print(f"{'=' * 55}\n")


def mostrar_subredes(data):
    subredes = data["subredes"]

    print(f"\n{'=' * 55}")
    print(f"  Red base: {data['red_base']}")

    if "subredes_solicitadas" in data:
        print(f"  Subredes solicitadas : {data['subredes_solicitadas']}")
        print(f"  Subredes generadas   : {data['subredes_generadas']}")
        print(f"  Bits extra usados    : {data['bits_extra']}")
    else:
        print(f"  Cantidad de subredes : {data['cantidad_subredes']}")
        print(f"  Hosts por subred     : {data['hosts_por_subred']}")

    print(f"  Nuevo prefijo        : /{data['nuevo_prefijo']}")
    print(f"{'=' * 55}")

    for s in subredes:
        print(f"\n  Subred #{s['indice']}")
        print(f"  {SEPARADOR}")
        print(f"  Red        : {s['red']}/{s['prefijo']}")
        print(f"  Mascara    : {s['mascara']}")
        print(f"  Primer host: {s['primer_host']}")
        print(f"  Ultimo host: {s['ultimo_host']}")
        print(f"  Broadcast  : {s['broadcast']}")
        print(f"  Hosts      : {s['hosts_utilizables']}")

    print(f"\n{'=' * 55}\n")


def pedir_opcion(opciones_validas):
    while True:
        opcion = input("Selecciona una opcion: ").strip()
        if opcion in opciones_validas:
            return opcion
        print(f"  Opcion no valida. Elige entre: {', '.join(opciones_validas)}")


def menu_cidr():
    print("\n" + "=" * 55)
    print("       Calculadora IP CIDR")
    print("=" * 55)
    print("  1. Informacion de una red (CIDR)")
    print("  2. Dividir red en N subredes iguales")
    print("  3. Subredes por prefijo")
    print("  4. Volver al menu principal")
    print("=" * 55)

    return pedir_opcion(["1", "2", "3", "4"])


def ejecutar_cidr():
    while True:
        opcion = menu_cidr()

        if opcion == "1":
            print("\n-- Informacion de red CIDR --")
            red_cidr = input("  Ingresa la red (ej. 192.168.1.0/24): ").strip()
            try:
                resultado = calcular_info_red(red_cidr)
                mostrar_info_red(resultado)
            except ValueError as e:
                print(f"\n  Error: {e}\n")

        elif opcion == "2":
            print("\n-- Dividir red en N subredes --")
            red_cidr = input("  Ingresa la red base (ej. 10.0.0.0/8): ").strip()
            num = input("  En cuantas subredes quieres dividirla?: ").strip()
            try:
                resultado = dividir_en_subredes(red_cidr, num)
                mostrar_subredes(resultado)
            except ValueError as e:
                print(f"\n  Error: {e}\n")

        elif opcion == "3":
            print("\n-- Subredes por prefijo --")
            red_cidr = input("  Ingresa la red base (ej. 172.16.0.0/16): ").strip()
            prefijo = input("  Ingresa el nuevo prefijo (ej. 24): ").strip()
            try:
                resultado = calcular_subredes_por_prefijo(red_cidr, prefijo)
                mostrar_subredes(resultado)
            except ValueError as e:
                print(f"\n  Error: {e}\n")

        elif opcion == "4":
            break
