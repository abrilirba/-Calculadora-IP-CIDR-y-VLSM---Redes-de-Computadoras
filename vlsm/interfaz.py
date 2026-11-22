from .calculos import calcular_vlsm, calcular_bloque


SEPARADOR = "-" * 55


def mostrar_resultados_vlsm(data):
    print(f"\n{'=' * 55}")
    print(f"  Red base: {data['red_base']}")
    print(f"  Direcciones totales   : {data['direcciones_totales']}")
    print(f"  Direcciones asignadas : {data['direcciones_asignadas']}")
    print(f"  Direcciones restantes : {data['direcciones_restantes']}")
    print(f"  Hosts solicitados     : {data['hosts_solicitados']}")
    print(f"  Hosts utilizables     : {data['hosts_utilizables']}")
    print(f"  Hosts sobrantes       : {data['hosts_sobrantes']}")
    print(f"{'=' * 55}")

    for s in data["subredes"]:
        print(f"\n  Subred: {s['nombre']}")
        print(f"  {SEPARADOR}")
        print(f"  Red        : {s['red']}/{s['prefijo']}")
        print(f"  Máscara    : {s['mascara']}")
        print(f"  Primer host: {s['primer_host']}")
        print(f"  Último host: {s['ultimo_host']}")
        print(f"  Broadcast  : {s['broadcast']}")
        print(f"  Hosts sol. : {s['hosts_solicitados']}")
        print(f"  Hosts util.: {s['hosts_utilizables']}")
        print(f"  Sobrantes  : {s['hosts_sobrantes']}")

    print(f"\n{'=' * 55}\n")


def pedir_opcion(opciones_validas):
    while True:
        opcion = input("Selecciona una opción: ").strip()
        if opcion in opciones_validas:
            return opcion
        print(f"  Opción no válida. Elige entre: {', '.join(opciones_validas)}")


def menu_vlsm():
    print("\n" + "=" * 55)
    print("       Calculadora IP VLSM")
    print("=" * 55)
    print("  1. Calcular VLSM para una red")
    print("  2. Calcular bloque para N hosts")
    print("  3. Volver al menú principal")
    print("=" * 55)

    return pedir_opcion(["1", "2", "3"])


def ejecutar_vlsm():
    while True:
        opcion = menu_vlsm()

        if opcion == "1":
            print("\n-- Calculadora VLSM --")
            red_cidr = input("  Ingresa la red base (ej. 192.168.0.0/24): ").strip()

            requerimientos = []
            print("  Ingresa las subredes (nombre y hosts). Escribe 'listo' cuando termines.")

            while True:
                nombre = input("  Nombre de la subred (o 'listo'): ").strip()
                if nombre.lower() == "listo":
                    break
                hosts = input(f"  Hosts para '{nombre}': ").strip()
                requerimientos.append((nombre, hosts))

            try:
                resultado = calcular_vlsm(red_cidr, requerimientos)
                mostrar_resultados_vlsm(resultado)
            except ValueError as e:
                print(f"\n  Error: {e}\n")

        elif opcion == "2":
            print("\n-- Bloque para N hosts --")
            hosts = input("  ¿Cuántos hosts necesitas?: ").strip()
            try:
                resultado = calcular_bloque(hosts)
                print(f"\n  Hosts solicitados  : {resultado['hosts_solicitados']}")
                print(f"  Bits de host       : {resultado['bits_host']}")
                print(f"  Prefijo            : /{resultado['prefijo']}")
                print(f"  Total direcciones  : {resultado['total_direcciones']}")
                print(f"  Hosts utilizables  : {resultado['hosts_utilizables']}")
                print(f"  Hosts sobrantes    : {resultado['hosts_sobrantes']}\n")
            except ValueError as e:
                print(f"\n  Error: {e}\n")

        elif opcion == "3":
            break
