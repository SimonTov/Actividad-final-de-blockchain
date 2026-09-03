# -*- coding: utf-8 -*-
"""
Nodo autorizado dentro de la red de Proof of Authority.

En este caso de uso, los nodos autorizados representan a las
instituciones acreditadas que participan del proceso de emision y
verificacion de titulos academicos: la universidad que emitio el
titulo, la entidad estatal que acredita a esa universidad, y un
verificador internacional de credenciales (el tipo de organizacion que
usan empleadores en otros paises para confirmar que un titulo
extranjero es real, sin tener que llamar directamente a la
universidad). No cualquiera puede sellar un bloque -- solo estos tres,
por turnos, y ademas se necesita que la mayoria de ellos valide el
bloque propuesto antes de aceptarlo (ver red.py). Esto imita el
proceso real de verificacion de credenciales, pero registrandolo en
una estructura que no se puede alterar en silencio.
"""


class NodoAutorizado:
    def __init__(self, nombre, rol):
        self.nombre = nombre
        self.rol = rol  # p.ej. "Universidad emisora", "Entidad acreditadora", "Verificador internacional"

    def __repr__(self):
        return f"<NodoAutorizado {self.nombre} ({self.rol})>"


def red_por_defecto():
    """Los tres nodos autorizados que uso en la demo."""
    return [
        NodoAutorizado("Universidad EAFIT", "Universidad emisora"),
        NodoAutorizado("Ministerio de Educacion Nacional", "Entidad acreditadora"),
        NodoAutorizado("Verificador Internacional de Credenciales", "Verificador internacional"),
    ]
