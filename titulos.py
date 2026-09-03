# -*- coding: utf-8 -*-
"""
Catalogo de titulos academicos de ejemplo, usados como los activos que
la cadena rastrea en esta entrega: cada uno representa un titulo real
emitido por una universidad, sobre el que despues se pueden registrar
verificaciones de empleadores, homologaciones internacionales o
correcciones oficiales.
"""

TITULOS = [
    {"titular": "Camila Restrepo Uribe", "programa": "Ingenieria de Sistemas",
     "tipo_titulo": "Pregrado", "universidad": "Universidad EAFIT", "anio": "2022",
     "descripcion": "Titulo de pregrado en Ingenieria de Sistemas."},
    {"titular": "Juan David Zapata Mesa", "programa": "Administracion de Negocios",
     "tipo_titulo": "Pregrado", "universidad": "Universidad EAFIT", "anio": "2023",
     "descripcion": "Titulo de pregrado en Administracion de Negocios."},
    {"titular": "Valentina Gomez Arango", "programa": "Maestria en Ciencia de Datos",
     "tipo_titulo": "Posgrado", "universidad": "Universidad EAFIT", "anio": "2024",
     "descripcion": "Titulo de maestria en Ciencia de Datos."},
    {"titular": "Andres Felipe Correa", "programa": "Derecho",
     "tipo_titulo": "Pregrado", "universidad": "Universidad EAFIT", "anio": "2021",
     "descripcion": "Titulo de pregrado en Derecho."},
    {"titular": "Isabella Marin Vasquez", "programa": "Doctorado en Ingenieria",
     "tipo_titulo": "Doctorado", "universidad": "Universidad EAFIT", "anio": "2025",
     "descripcion": "Titulo de doctorado en Ingenieria."},
]


def buscar_titulo(titular):
    for t in TITULOS:
        if t["titular"].lower() == titular.lower():
            return dict(t)
    return None


def listar_titulares():
    return [t["titular"] for t in TITULOS]
