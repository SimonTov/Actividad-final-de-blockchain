# -*- coding: utf-8 -*-
"""
Demo por consola del registro de emision y verificacion de titulos
academicos. Simula la historia completa de un titulo: se emite, un
empleador lo verifica, se homologa en otro pais y se corrige un dato
oficial -- cada evento sellado por la red de nodos autorizados via PoA
--, despues verifico que la cadena esta integra, y al final simulo un
intento de alterar la historia para mostrar que la verificacion lo
detecta.
"""
from cadena_procedencia import CadenaTitulo
from nodo import red_por_defecto
from red import RedVerificacion
from titulos import TITULOS, listar_titulares


def elegir_titulo():
    print("\nTitulos disponibles:")
    for i, titular in enumerate(listar_titulares()):
        print(f"  {i + 1}. {titular}")
    while True:
        try:
            opcion = int(input("Elegi un titulo (numero): "))
            if 1 <= opcion <= len(TITULOS):
                return dict(TITULOS[opcion - 1])
        except ValueError:
            pass
        print("Opcion invalida.")


def menu():
    titulo = elegir_titulo()
    cadena = CadenaTitulo(titulo)
    red = RedVerificacion(red_por_defecto())
    print(f"\nCadena creada para el titulo de '{titulo['titular']}'.")

    while True:
        print("\n--- MENU: titulo de '" + titulo["titular"] + "' ---")
        print("1. Registrar verificacion solicitada por un empleador")
        print("2. Registrar homologacion/convalidacion internacional")
        print("3. Registrar correccion oficial (ej. cambio de nombre)")
        print("4. Ver historia completa (leer todos los eventos)")
        print("5. Verificar integridad de la cadena")
        print("6. Simular alteracion de un evento pasado (demo de deteccion)")
        print("7. Borrar un evento")
        print("8. Guardar cadena en disco")
        print("9. Exportar reporte HTML")
        print("0. Salir")
        opcion = input("Elegi una opcion: ").strip()

        if opcion == "1":
            empleador = input("Empleador que solicita la verificacion: ")
            resultado = input("Resultado (valido/no_encontrado): ")
            red.proponer_evento(cadena, "verificacion_empleador", {
                "empleador": empleador, "resultado": resultado,
            })
        elif opcion == "2":
            pais = input("Pais donde se homologa el titulo: ")
            entidad = input("Entidad que otorga la homologacion: ")
            red.proponer_evento(cadena, "homologacion_internacional", {
                "pais": pais, "entidad": entidad,
            })
        elif opcion == "3":
            campo = input("Campo a corregir (ej. nombre_titular): ")
            valor_nuevo = input("Valor corregido: ")
            motivo = input("Motivo de la correccion: ")
            red.proponer_evento(cadena, "correccion_oficial", {
                "campo": campo, "valor_nuevo": valor_nuevo, "motivo": motivo,
            })
        elif opcion == "4":
            for i in range(len(cadena.cadena)):
                cadena.leer_bloque(i)
        elif opcion == "5":
            valida, errores = cadena.verificar_cadena()
            if valida:
                print("La cadena esta integra: nadie ha alterado la historia del titulo.")
            else:
                print("La cadena NO es valida. Se encontraron problemas:")
                for e in errores:
                    print(f"  - {e}")
        elif opcion == "6":
            indice = int(input("Indice del evento a alterar (0 es la emision, se puede editar solo para la demo): "))
            nuevo_valor = input("Nuevo valor falso para 'detalle' (texto libre): ")
            cadena.modificar_bloque(indice, {"alterado": nuevo_valor})
            print("Ahora corre la opcion 5 (verificar) para ver como la cadena detecta el cambio.")
        elif opcion == "7":
            indice = int(input("Indice del evento a borrar: "))
            cadena.borrar_bloque(indice)
        elif opcion == "8":
            cadena.guardar()
        elif opcion == "9":
            ruta = cadena.exportar_html()
            print(f"Reporte generado en {ruta}")
        elif opcion == "0":
            break
        else:
            print("Opcion invalida.")


if __name__ == "__main__":
    menu()
