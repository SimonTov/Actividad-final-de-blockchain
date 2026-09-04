# Entrega 4 -- Registro de emision y verificacion de titulos academicos

Esta entrega la construi sobre el motor de cadena de bloques que ya
habia hecho en las actividades 1 y 2 (bloque con hash SHA-256 enlazado
al anterior, JSON canonico para que el hash sea siempre el mismo,
verificacion de la cadena, y consenso entre varios nodos en vez de que
uno solo pueda escribir). Le agregue el caso de uso completo que pide
esta entrega.

## 1. Caso de uso y por que necesita blockchain

**Caso de uso:** un registro de la historia completa de un titulo
academico -- desde que la universidad lo emite, hasta cada verificacion
que un empleador solicita, cada homologacion internacional y cada
correccion oficial que recibe con el tiempo.

**Por que esta app necesita blockchain y no otra solucion:**

Hoy, cuando un empleador (sobre todo en otro pais) quiere confirmar que
un titulo es real, tiene que llamar o escribirle directamente a la
universidad, esperar dias o semanas, y confiar en un certificado en
papel o PDF que la propia universidad puede haber emitido de forma
irregular (o que puede haber sido falsificado por el candidato). El
problema de fondo es el mismo que en cualquier caso de procedencia:
**varias partes que no confian del todo entre si necesitan estar de
acuerdo sobre UN solo historial**, y ese historial tiene que poder
verificarse sin depender de que una sola de esas partes sea honesta.
Aca los actores son la universidad que emite el titulo, la entidad
estatal que acredita a esa universidad, y el empleador o verificador
internacional que necesita confirmar la validez sin tener via directa
y confiable a la fuente original.

Compare tres soluciones:

- **Base de datos centralizada de la universidad (lo que existe hoy):**
  es rapida y simple, pero exige que el empleador confie ciegamente en
  que la universidad no altero un registro despues de los hechos (por
  ejemplo, subir el promedio de un egresado, o inventar un titulo que
  nunca se completo). Cualquiera con acceso administrativo a esa base
  puede editar un registro sin dejar rastro verificable por terceros.
- **Base de datos con una tabla de auditoria (append-only log):** es
  una mejora, pero el log sigue viviendo en el mismo servidor y bajo el
  mismo dueno que la tabla principal -- quien controla la base de datos
  tambien puede editar o borrar su propio log de auditoria.
- **Certificado fisico o PDF con sello notarial (lo que se usa hoy en
  la practica):** es precisamente el punto debil que permite la
  falsificacion de titulos -- el documento se puede escanear, editar y
  volver a imprimir, y verificarlo a distancia (sobre todo entre
  paises) es lento y depende de que alguien conteste un correo.

Una cadena de bloques resuelve especificamente el problema de que la
universidad, la entidad acreditadora y el verificador internacional
puedan estar de acuerdo sobre un unico historial sin que ninguno de
los tres dependa ciegamente de los otros dos, y hace que cualquier
intento de reescribir un evento pasado (por ejemplo, cambiar el
resultado de una verificacion, o esconder que un titulo fue anulado)
se pueda detectar de inmediato verificando la cadena. Eso es
exactamente lo que demuestro en la seccion 4 de este documento: alterar
un evento pasado rompe el enlace con el siguiente bloque y
`verificar_cadena()` lo marca como invalido al instante.

**Por que Proof of Authority y no Proof of Work o Proof of Stake:**
en las entregas 1 y 2 ya implemente los tres algoritmos de consenso.
Para este caso de uso especificamente elegi PoA porque los
participantes NO son anonimos como en Bitcoin -- son instituciones
identificables y acreditadas (una universidad reconocida, un ente
estatal, un verificador internacional). No tiene sentido gastar energia
computacional en un acertijo (PoW) cuando ya sabemos quienes son las
partes autorizadas a validar; y tampoco tiene sentido ponderar por
"cuanto capital tiene invertido" cada uno (PoS), porque la autoridad
aqui viene de la acreditacion institucional, no de dinero en juego.
Ademas sigo exigiendo mayoria simple entre los nodos autorizados para
sellar un evento (igual que en la entrega 2), asi que ninguna
institucion por si sola puede escribir la historia del titulo --
necesita que otra este de acuerdo.

## 2. Implementacion

Todo esta en Python, reutilizando y adaptando el motor de las
actividades 1 y 2:

- `titulos.py`: catalogo de titulos academicos de ejemplo (titular,
  programa, tipo de titulo, universidad, ano) que funciona como el
  catalogo de activos que se pueden registrar en la demo.
- `bloque.py`: la clase `Bloque`, con el mismo mecanismo de hash SHA-256
  sobre JSON canonico de las entregas anteriores, pero con campos
  ajustados al caso de uso (`tipo_evento`, `detalle`, `validador`) en
  vez de los campos de minado (`dificultad`, `nonce`) que ya no
  necesito porque no hay Proof of Work.
- `nodo.py`: los nodos autorizados (universidad emisora, entidad
  acreditadora estatal y verificador internacional de credenciales).
- `red.py`: la red de nodos y el algoritmo de consenso PoA con
  votacion por mayoria, adaptado de `red.py` de la entrega 2.
- `cadena_procedencia.py`: la clase `CadenaTitulo`, con las 6
  operaciones basicas (crear/genesis, adicionar via consenso, verificar,
  leer, modificar, borrar) mas persistencia en JSON.
- `main.py`: demo interactiva por consola (menu en espanol) para
  registrar verificaciones de empleadores, homologaciones
  internacionales y correcciones oficiales sobre un titulo elegido de
  una lista.
- `demo_automatica.py`: corre un flujo completo sin pedir input y deja
  listos `reporte_valido.html` y `reporte_alterado.html`.
- `demo_web/generar_reporte.py`: genera un reporte HTML autocontenido
  (tarjetas por evento, indicador verde/rojo de si la cadena es
  valida).

### Como usarlo

Requiere solo Python 3 (sin dependencias externas).

```bash
cd verificacion_diplomas

# Demo interactiva por consola
python3 main.py

# O la demo automatica que genera los dos reportes de ejemplo
python3 demo_automatica.py

# o quieres probarlo desde la pagina web:
start demo_web\sitio_interactivo.html
```

Al correr `main.py`, elegis un titulo del catalogo, y desde el menu
podes registrar eventos (verificacion de un empleador, homologacion,
correccion oficial), verificar la integridad de la cadena, simular una
alteracion para ver como se detecta, y exportar el reporte HTML
(`opcion 9`) para abrirlo directamente con doble clic en el navegador.

## 3. Formato de la entrega

Codigo en Python (consola) mas un reporte HTML estatico generado por el
mismo Python, que se puede abrir directamente con doble clic sin
necesitar servidor.

## 4. Limitaciones y dificultades

- **El problema de `crypto.subtle` que ya habia tenido en la entrega
  anterior:** en ese momento la demo web intentaba recalcular los
  hashes directamente en el navegador con `crypto.subtle.digest()`,
  pero esa funcion solo corre en "contextos seguros" (https:// o
  localhost) y fallaba en silencio al abrir el archivo con doble clic
  (protocolo file://). Para esta entrega evite el problema desde el
  diseno: el HTML nunca recalcula nada, solo muestra los hashes que
  Python ya calculo de antemano.
- **Simulacion de red, no red real:** igual que en la entrega 2, los
  nodos autorizados no son procesos ni maquinas distintas con sockets,
  sino objetos en el mismo programa. Es una simplificacion razonable
  para demostrar como funciona el consenso, pero en un despliegue real
  cada institucion (universidad, ente acreditador, verificador
  internacional) tendria que correr su propio nodo de verdad.
- **Una cadena por titulo:** decidi que cada titulo tenga su propia
  cadena independiente (en vez de una sola cadena gigante con todos los
  titulos mezclados) porque asi verificar el historial de UN titulo
  especifico no requiere recorrer el historial de todos los demas. La
  desventaja es que no hay todavia una vista consolidada de "todos los
  titulos emitidos por la universidad" -- para esta entrega no la
  necesitaba, pero seria el siguiente paso logico.
- **Los nodos autorizados estan fijos en el codigo:** en un sistema
  real, agregar o quitar una institucion autorizada (por ejemplo, si un
  verificador internacional pierde su acreditacion) tendria que ser en
  si mismo un proceso gobernado y auditable, no un cambio directo en
  `nodo.py`. Lo deje simple a proposito porque no era el foco de esta
  entrega.

## 5. Como usar la implementacion

Ver la seccion 2 ("Como usarlo") mas arriba. En resumen: `python3
main.py` para la demo interactiva, o `python3 demo_automatica.py` para
generar de una vez los reportes HTML de ejemplo (uno con la cadena
valida y otro mostrando la deteccion de una alteracion).

## 6. Referencias

- Fundamentos de Blockchain y Sistemas DLT (Sergio Steven Ramirez Rico,
  material del curso Blockchain 1, EAFIT) -- estructura de bloque y
  requisitos de consenso.
- Satoshi Nakamoto, *Bitcoin: A Peer-to-Peer Electronic Cash System*
  (whitepaper de Bitcoin) -- referencia general de Proof of Work, que
  ya use en las entregas anteriores y que sirvio de contraste para
  justificar por que en este caso de uso elegi PoA en vez de PoW.
- Documentacion oficial de Python sobre el modulo `hashlib` (SHA-256) y
  `json` (serializacion con `sort_keys` para JSON canonico).
- Trabajo propio de las entregas 1 y 2 de esta misma actividad (motor
  de bloque, verificacion de cadena y algoritmos de consenso), que es
  la base directa sobre la que construi esta entrega.

## 7. Uso de IA

Use IA (Claude, de Anthropic) como asistente de programacion durante
esta entrega, principalmente para:

- Adaptar el motor de bloque y de consenso PoA que ya tenia de las
  entregas 1 y 2 al nuevo caso de uso (cambiar los campos del bloque de
  minado a eventos de verificacion academica, y simplificar `red.py`
  para que solo use PoA en vez de los tres algoritmos).
- Redactar el generador de reporte HTML (`demo_web/generar_reporte.py`),
  evitando repetir el error de `crypto.subtle` que ya habia identificado
  en la entrega anterior.
- Ayudarme a estructurar y redactar este README con la justificacion
  del caso de uso, las limitaciones y las referencias.

La logica de negocio del caso de uso (que eventos registrar, que
institucion actua como cada nodo autorizado, y por que PoA es el
algoritmo correcto para este escenario en particular) la defini yo; la
IA me ayudo a implementarla en codigo y a organizar la documentacion.
