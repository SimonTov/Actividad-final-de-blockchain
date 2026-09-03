# -*- coding: utf-8 -*-
"""
Bloque de la cadena de verificacion de titulos.

Reutilizo el mismo motor de hashing que use en las entregas 1 y 2: cada
bloque guarda el hash del bloque anterior, el contenido se serializa a
JSON con las claves ordenadas alfabeticamente antes de aplicar SHA-256
(para que el resultado sea siempre el mismo sin importar el orden en
que se hayan asignado los datos), y el hash resultante es el que se usa
para enlazar la cadena.

Lo que cambio frente a la entrega 2 es que aqui no hay minado por
Proof of Work: el sello del bloque lo da un NODO AUTORIZADO (ver
red.py) dentro del algoritmo de Proof of Authority, asi que no necesito
los campos de dificultad ni nonce, y en cambio agrego 'tipo_evento' y
'detalle' para describir que le paso al titulo en ese punto de su
historia (verificacion de un empleador, homologacion internacional,
correccion oficial, etc).
"""
import hashlib
import json
from datetime import datetime, timezone


class Bloque:

    def __init__(self, indice, tipo_evento, detalle, hash_anterior,
                 marca_tiempo=None, validador=None, hash_bloque=None):
        self.indice = indice
        self.tipo_evento = tipo_evento
        self.detalle = detalle
        self.hash_anterior = hash_anterior
        self.marca_tiempo = marca_tiempo or datetime.now(timezone.utc).isoformat()
        self.validador = validador
        self.hash_bloque = hash_bloque or self.calcular_hash()

    def _contenido_serializado(self):
        payload = {
            "indice": self.indice,
            "tipo_evento": self.tipo_evento,
            "detalle": self.detalle,
            "hash_anterior": self.hash_anterior,
            "marca_tiempo": self.marca_tiempo,
            "validador": self.validador,
        }
        return json.dumps(payload, sort_keys=True, ensure_ascii=False)

    def calcular_hash(self):
        return hashlib.sha256(self._contenido_serializado().encode("utf-8")).hexdigest()

    def actualizar_hash(self):
        self.hash_bloque = self.calcular_hash()
        return self.hash_bloque

    def a_dict(self):
        return {
            "indice": self.indice,
            "tipo_evento": self.tipo_evento,
            "detalle": self.detalle,
            "hash_anterior": self.hash_anterior,
            "marca_tiempo": self.marca_tiempo,
            "validador": self.validador,
            "hash_bloque": self.hash_bloque,
        }

    @classmethod
    def desde_dict(cls, d):
        return cls(
            indice=d["indice"],
            tipo_evento=d["tipo_evento"],
            detalle=d["detalle"],
            hash_anterior=d["hash_anterior"],
            marca_tiempo=d["marca_tiempo"],
            validador=d.get("validador"),
            hash_bloque=d["hash_bloque"],
        )

    def __repr__(self):
        return f"Bloque(#{self.indice}, evento={self.tipo_evento}, validador={self.validador})"
