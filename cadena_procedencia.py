# -*- coding: utf-8 -*-
"""
Cadena de verificacion de un titulo academico: cada instancia de esta
clase es la historia completa y verificable de UN titulo, desde su
emision hasta cada verificacion, homologacion o correccion posterior.

Mantengo las mismas operaciones basicas que use en las entregas 1 y 2
(crear/genesis, adicionar, verificar, leer, modificar, borrar), pero
"adicionar" ahora pasa siempre por la red de consenso (red.py) en vez
de sellarse sola, porque en este caso de uso ninguna institucion por
si sola deberia poder escribir la historia del titulo.
"""
import json
import os

from bloque import Bloque


class CadenaTitulo:

    def __init__(self, titulo, archivo_persistencia=None):
        self.titulo = titulo  # dict con titular, programa, tipo_titulo, universidad, anio, descripcion
        self.archivo_persistencia = archivo_persistencia or self._nombre_archivo(titulo["titular"])
        self.cadena = []
        self._crear_bloque_genesis()

    @staticmethod
    def _nombre_archivo(titular):
        slug = "".join(c if c.isalnum() else "_" for c in titular.lower())
        return f"titulo_{slug}.json"

    # 1) Crear la cadena (bloque genesis = emision del titulo) -------------
    def _crear_bloque_genesis(self):
        genesis = Bloque(
            indice=0,
            tipo_evento="emision_titulo",
            detalle={
                "titular": self.titulo["titular"],
                "programa": self.titulo["programa"],
                "tipo_titulo": self.titulo["tipo_titulo"],
                "universidad": self.titulo["universidad"],
                "anio": self.titulo["anio"],
                "descripcion": self.titulo["descripcion"],
                "nota": "Registro fundacional de la emision del titulo.",
            },
            hash_anterior="0" * 64,
            validador=self.titulo["universidad"],
        )
        self.cadena.append(genesis)

    # 2) Adicionar un bloque -------------------------------------------------
    # Se hace a traves de red.proponer_evento(cadena, tipo, detalle), que
    # aplica PoA y exige mayoria de nodos autorizados de acuerdo antes de
    # aceptar el evento. Dejo tambien un metodo manual para pruebas
    # rapidas sin la red (no deberia usarse en el flujo real).
    def adicionar_evento_manual(self, tipo_evento, detalle, validador="manual"):
        anterior = self.cadena[-1]
        nuevo = Bloque(
            indice=len(self.cadena),
            tipo_evento=tipo_evento,
            detalle=detalle,
            hash_anterior=anterior.hash_bloque,
            validador=validador,
        )
        self.cadena.append(nuevo)
        return nuevo

    # 3) Verificar cadena -----------------------------------------------------
    def verificar_cadena(self):
        errores = []
        for i in range(1, len(self.cadena)):
            actual = self.cadena[i]
            anterior = self.cadena[i - 1]
            if actual.hash_bloque != actual.calcular_hash():
                errores.append(f"Bloque {i}: el hash no coincide con su contenido (el evento fue alterado).")
            if actual.hash_anterior != anterior.hash_bloque:
                errores.append(f"Bloque {i}: no enlaza con el hash del bloque anterior (cadena rota).")
        return (len(errores) == 0), errores

    # 4) Leer bloque ------------------------------------------------------------
    def leer_bloque(self, indice):
        if not (0 <= indice < len(self.cadena)):
            print("Ese evento no existe.")
            return None
        bloque = self.cadena[indice]
        print(f"\n--- EVENTO {indice} ---")
        for clave, valor in bloque.a_dict().items():
            print(f"{clave}: {valor}")
        return bloque

    # 5) Modificar bloque ---------------------------------------------------------
    # A proposito NO se vuelve a sellar automaticamente: asi se evidencia,
    # al verificar la cadena, que alguien intento reescribir la historia
    # del titulo (esa es justamente la propiedad que quiero demostrar con
    # este caso de uso).
    def modificar_bloque(self, indice, nuevo_detalle):
        if not (0 <= indice < len(self.cadena)):
            print("Ese evento no existe.")
            return False
        bloque = self.cadena[indice]
        bloque.detalle = nuevo_detalle
        bloque.actualizar_hash()
        print("Evento modificado (hash recalculado localmente, pero ningun otro "
              "nodo autorizado aprobo este cambio -- la cadena quedara marcada "
              "como invalida al verificarla, porque el hash_anterior del "
              "siguiente bloque ya no coincide).")
        return True

    # 6) Borrar bloque -----------------------------------------------------------
    def borrar_bloque(self, indice):
        if indice == 0:
            print("No se puede borrar el registro fundacional de emision del titulo.")
            return False
        if not (0 <= indice < len(self.cadena)):
            print("Ese evento no existe.")
            return False
        self.cadena.pop(indice)
        for i in range(indice, len(self.cadena)):
            self.cadena[i].indice = i
        print("Evento eliminado (los enlaces siguientes quedan rotos hasta re-sellarlos con la red).")
        return True

    # Persistencia -------------------------------------------------------------
    def guardar(self):
        data = {"titulo": self.titulo, "cadena": [b.a_dict() for b in self.cadena]}
        with open(self.archivo_persistencia, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Cadena guardada en {self.archivo_persistencia}")

    def cargar(self):
        if not os.path.exists(self.archivo_persistencia):
            print("No hay archivo de persistencia todavia para este titulo.")
            return False
        with open(self.archivo_persistencia, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.titulo = data["titulo"]
        self.cadena = [Bloque.desde_dict(b) for b in data["cadena"]]
        print("Cadena cargada.")
        return True

    def exportar_html(self, archivo_salida=None):
        from demo_web.generar_reporte import generar_html
        archivo_salida = archivo_salida or f"reporte_{self._nombre_archivo(self.titulo['titular'])[:-5]}.html"
        return generar_html(self, archivo_salida)
