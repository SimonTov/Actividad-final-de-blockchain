# -*- coding: utf-8 -*-
"""
Genera un reporte HTML autocontenido (sin servidor) con la historia de
verificacion de un titulo academico.

Aprendi en la entrega anterior que crypto.subtle.digest() no funciona
si el archivo se abre con doble clic (protocolo file://), porque esa
funcion solo corre en "contextos seguros" (https:// o localhost). Por
eso aqui el HTML NO recalcula ningun hash en el navegador: Python ya
calculo todos los hashes de antemano y el reporte simplemente los
muestra como datos incrustados. Asi el reporte funciona abriendolo
directamente con doble clic, sin necesidad de levantar un servidor.
"""
import json


def generar_html(cadena, archivo_salida="reporte_titulo.html"):
    valida, errores = cadena.verificar_cadena()
    bloques_json = json.dumps([b.a_dict() for b in cadena.cadena], ensure_ascii=False, indent=2)

    filas = ""
    for b in cadena.cadena:
        detalle_html = "<br>".join(f"<b>{k}:</b> {v}" for k, v in b.detalle.items())
        filas += f"""
        <div class="bloque">
          <div class="bloque-header">
            <span class="indice">#{b.indice}</span>
            <span class="evento">{b.tipo_evento}</span>
          </div>
          <div class="cuerpo">
            <p>{detalle_html}</p>
            <p class="meta"><b>Fecha:</b> {b.marca_tiempo}</p>
            <p class="meta"><b>Sellado por:</b> {b.validador}</p>
            <p class="hash"><b>Hash:</b> {b.hash_bloque}</p>
            <p class="hash"><b>Hash anterior:</b> {b.hash_anterior}</p>
          </div>
        </div>
        """

    estado = "VALIDA" if valida else "NO VALIDA"
    color_estado = "#2e7d32" if valida else "#c62828"
    lista_errores = "".join(f"<li>{e}</li>" for e in errores)

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Verificacion de titulo -- {cadena.titulo['titular']}</title>
<style>
  body {{ font-family: Arial, Helvetica, sans-serif; background: #f4f6f8; color: #1e2a35; max-width: 800px; margin: 40px auto; padding: 0 20px; }}
  h1 {{ font-size: 1.6em; border-bottom: 3px solid #1a4d8f; padding-bottom: 10px; }}
  .subtitulo {{ color: #555; margin-top: -8px; }}
  .estado {{ display: inline-block; padding: 6px 14px; border-radius: 4px; color: white; background: {color_estado}; font-weight: bold; margin: 12px 0; }}
  .bloque {{ border: 1px solid #cfd8e3; border-left: 6px solid #1a4d8f; background: white; margin-bottom: 16px; border-radius: 4px; overflow: hidden; }}
  .bloque-header {{ background: #e8eef6; padding: 8px 14px; display: flex; justify-content: space-between; font-weight: bold; }}
  .cuerpo {{ padding: 10px 14px; }}
  .meta {{ color: #555; font-size: 0.9em; }}
  .hash {{ font-family: monospace; font-size: 0.78em; word-break: break-all; color: #444; }}
  ul {{ color: #c62828; }}
</style>
</head>
<body>
  <h1>Historial de verificacion: {cadena.titulo['titular']}</h1>
  <p class="subtitulo">{cadena.titulo['programa']} ({cadena.titulo['tipo_titulo']}) -- {cadena.titulo['universidad']}, {cadena.titulo['anio']}</p>
  <div class="estado">Cadena {estado}</div>
  {"<ul>" + lista_errores + "</ul>" if errores else ""}
  {filas}
  <script id="datos-cadena" type="application/json">{bloques_json}</script>
</body>
</html>"""

    with open(archivo_salida, "w", encoding="utf-8") as f:
        f.write(html)
    return archivo_salida
