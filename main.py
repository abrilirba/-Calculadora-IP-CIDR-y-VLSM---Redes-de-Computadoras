from vlsm.interfaz import ejecutar_vlsm
from cidr.interfaz import ejecutar_cidr


def menu_principal():
    print("\n" + "=" * 55)
    print("     Calculadora de Subredes IPv4")
    print("=" * 55)
    print("  1. Calculadora CIDR")
    print("  2. Calculadora VLSM")
    print("  3. Salir")
    print("=" * 55)

    while True:
        opcion = input("Selecciona una opción: ").strip()
        if opcion in ["1", "2", "3"]:
            return opcion
        print("  Opción no válida. Elige 1, 2 o 3.")


def main():
    while True:
        opcion = menu_principal()

        if opcion == "1":
            ejecutar_cidr()
        elif opcion == "2":
            ejecutar_vlsm()
        elif opcion == "3":
            print("\n  Hasta luego.\n")
            break


if __name__ == "__main__":
    main()
