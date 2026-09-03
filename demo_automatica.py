# -*- coding: utf-8 -*-
"""
Corre un flujo completo sin pedir input por consola, para dejar dos
reportes HTML de ejemplo listos en la entrega:
  - reporte_valido.html: la cadena completa e integra.
  - reporte_alterado.html: la misma cadena despues de que alguien
    intento reescribir un evento pasado, para mostrar que la
    verificacion lo detecta de inmediato.
"""
from cadena_procedencia import CadenaTitulo
from nodo import red_por_defecto
from red import RedVerificacion
from titulos import TITULOS


def main():
    titulo = TITULOS[0]  # Camila Restrepo Uribe
    cadena = CadenaTitulo(titulo)
    red = RedVerificacion(red_por_defecto())

    red.proponer_evento(cadena, "verificacion_empleador", {
        "empleador": "TechCorp Alemania",
        "resultado": "valido",
    })
    red.proponer_evento(cadena, "homologacion_internacional", {
        "pais": "Alemania",
        "entidad": "Zentralstelle fur auslandisches Bildungswesen (ZAB)",
    })
    red.proponer_evento(cadena, "correccion_oficial", {
        "campo": "nombre_titular",
        "valor_nuevo": "Camila Restrepo Uribe de Hoffmann",
        "motivo": "Cambio de apellido por matrimonio",
    })

    valida, _ = cadena.verificar_cadena()
    print("Cadena valida:", valida)
    cadena.guardar()
    cadena.exportar_html("reporte_valido.html")

    # Simulo que alguien intenta alterar el resultado de la verificacion
    # despues de los hechos (un caso real de fraude de credenciales).
    cadena.modificar_bloque(1, {
        "empleador": "TechCorp Alemania",
        "resultado": "valido_pero_con_honores_falsos",
    })
    valida2, errores2 = cadena.verificar_cadena()
    print("Cadena valida tras la alteracion:", valida2, errores2)
    cadena.exportar_html("reporte_alterado.html")


if __name__ == "__main__":
    main()
