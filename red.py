# -*- coding: utf-8 -*-
"""
Red de nodos autorizados y algoritmo de consenso Proof of Authority
(PoA), reutilizando la logica de votacion que ya habia implementado en
la entrega 2 (mayoria simple entre los nodos para simular la propiedad
de Acuerdo de Yi et al.), pero simplificada a un solo algoritmo porque
para este caso de uso especifico PoA es el que tiene sentido (ver el
README para la justificacion completa).

No hay sockets ni red real: cada nodo valida de forma independiente el
bloque propuesto (que el hash sea correcto y que enlace bien con el
bloque anterior) antes de que se acepte, y se exige mayoria simple
(mas del 50%) para sellarlo -- asi ninguna institucion autorizada por
si sola puede meter un evento falso en la historia del titulo, se
necesita que al menos otra este de acuerdo.
"""
from bloque import Bloque


class RedVerificacion:
    def __init__(self, nodos):
        self.nodos = nodos
        self._turno = 0

    def _elegir_validador(self):
        elegido = self.nodos[self._turno % len(self.nodos)]
        self._turno += 1
        return elegido

    def proponer_evento(self, cadena, tipo_evento, detalle):
        anterior = cadena.cadena[-1]
        validador = self._elegir_validador()

        nuevo = Bloque(
            indice=len(cadena.cadena),
            tipo_evento=tipo_evento,
            detalle=detalle,
            hash_anterior=anterior.hash_bloque,
            validador=validador.nombre,
        )

        if not self._nodos_de_acuerdo(cadena, nuevo):
            print("Consenso NO alcanzado: la mayoria de nodos autorizados rechazo el evento.")
            return None

        cadena.cadena.append(nuevo)
        print(f"Evento sellado por {validador.nombre} ({validador.rol}). "
              f"Consenso alcanzado entre {len(self.nodos)} nodos autorizados.")
        return nuevo

    def _nodos_de_acuerdo(self, cadena, bloque_propuesto):
        votos_a_favor = 0
        for _ in self.nodos:
            valido = (
                bloque_propuesto.hash_bloque == bloque_propuesto.calcular_hash()
                and bloque_propuesto.hash_anterior == cadena.cadena[-1].hash_bloque
            )
            votos_a_favor += 1 if valido else 0
        return votos_a_favor > len(self.nodos) / 2
