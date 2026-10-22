# ¿Ha llegado la misma partida?

El equipo de análisis recibe partidas de otros jugadores. Antes de trabajar con ellas quiere comprobar que los archivos recibidos conservan el contenido que tenían al preparar el envío.

Trabajad **por parejas**, alternando los papeles de emisor y receptor. Enviaréis dos copias de un JSONL: una intacta y otra modificada después de registrar su huella. **Duración orientativa: 20–25 minutos.**

## Teoría de apoyo

Una huella SHA-256 depende del contenido, no del nombre ni de la carpeta del archivo. Para verificar una copia necesitamos una huella de referencia calculada **antes** de modificarla o enviarla.

| Operación de Python                | Utilidad                                   |
| ---------------------------------- | ------------------------------------------ |
| `Path('ruta')`                     | Identificar el archivo que vamos a leer.   |
| `path.read_bytes()`                | Leer su contenido como bytes.              |
| `sha256(...).hexdigest()`          | Calcular la huella y obtenerla como texto. |
| `huella_actual == huella_esperada` | Comprobar si ambas huellas coinciden.      |
| `path.stat().st_size`              | Consultar el tamaño en bytes.              |

Solo necesitas `hashlib` y `pathlib`, incluidos en Python. No hace falta pandas ni ejecutar el pipeline del tema 09.

## 1. Prepara dos copias y registra su referencia

El emisor prepara **dos copias del mismo archivo original**, no dos partidas diferentes. Puedes hacerlo desde el explorador de archivos:

1. Elige **un solo JSONL** de una partida finalizada que tengas en `data/raw`.
2. Crea la carpeta `data/intercambio/envio` dentro de `bigdata-game`.
3. Copia el JSONL elegido a esa carpeta y renombra **la copia** como `partida_A.jsonl`.
4. Dentro de `data/intercambio/envio`, duplica `partida_A.jsonl` y llama a esa segunda copia `partida_B.jsonl`.

Ahora A y B contienen exactamente los mismos datos y solo cambia su nombre. El JSONL original permanece en `data/raw`, con su nombre y contenido intactos. Todas las modificaciones posteriores se harán sobre una de las copias de `envio`.

Antes de modificar ninguna de las dos copias:

1. Calcula sus huellas y tamaños mediante un pequeño script `scripts/actividades/06_verificar_envio.py`.
2. Comprueba que las dos huellas coinciden aunque los nombres sean diferentes.
3. Guarda los resultados en `referencia.txt`, indicando nombre, tamaño y SHA-256 de cada archivo.
4. Envía esa referencia a tu compañero por el canal de clase. El receptor debe conservarla sin modificar: será la referencia anterior a los cambios.

Puedes empezar con este bloque y adaptarlo para comprobar ambos archivos:

```python
from pathlib import Path
from hashlib import sha256

# Esta ruta se interpreta desde la raíz de bigdata-game.
path = Path('data/intercambio/envio/partida_A.jsonl')
# La huella representa los bytes del archivo que acabamos de leer.
huella = sha256(path.read_bytes()).hexdigest()
print(path.name, path.stat().st_size, huella)
```

Ejecuta desde la raíz de `bigdata-game`:

```powershell
python scripts/actividades/06_verificar_envio.py
```

### Mi respuesta

Partida utilizada: `20261005_182759_558220143806760042_5ebf59dd10ea42d99f3df8b17025b9db`.

RAW: `data/raw/nevworld_558220143806760042_20261005_182759.jsonl`.
El original permanece intacto. Las dos copias están en
`data/intercambio/ronda01/envio/`. Cada una ocupa **1049948 bytes**.

Antes de modificar una copia, ambas tenían la misma huella SHA-256:

```text
a37c42b322c6dacc8e76b34f2fc4a9529c76dd977c3fdad2d0e954757bd6dd28
```

La referencia previa se conserva en `data/intercambio/ronda01/referencia.txt`
y se adjunta una copia en esta carpeta de entrega. El script impide
sobrescribirla al registrar de nuevo.

Salida de consola al registrar las copias intactas:

```text
partida_A.jsonl 1049948 a37c42b322c6dacc8e76b34f2fc4a9529c76dd977c3fdad2d0e954757bd6dd28
partida_B.jsonl 1049948 a37c42b322c6dacc8e76b34f2fc4a9529c76dd977c3fdad2d0e954757bd6dd28
Referencia guardada. Ahora se puede modificar una sola copia.
```

## 2. Introduce un cambio pequeño y envía los archivos

El emisor deja una copia intacta y modifica **solo la otra** con VS Code. No le digas todavía al receptor cuál has elegido.

- Cambia un único dígito de un valor numérico, por ejemplo `100` por `900`, si encuentras ese valor. También puedes cambiar otro dígito por uno distinto manteniendo un número JSON válido.
- No cambies `schema_version`, `run_id` ni `event_index`. No añadas ni elimines líneas y conserva la codificación y los saltos de línea.
- Guarda la copia modificada. **No actualices las huellas de `referencia.txt`: deben seguir siendo las calculadas antes del cambio.**

Anota en privado la línea, el campo y el valor anterior y posterior. Envía ambos JSONL como archivos adjuntos o en un ZIP; no pegues su contenido como texto en un mensaje. El receptor los guardará en `data/intercambio/recibido`.

### Mi respuesta

He preparado una copia intacta y otra con un único dígito numérico cambiado.
Se mantienen el tamaño, las líneas, la codificación y los campos
`schema_version`, `run_id` y `event_index`. La línea, el campo y los valores
anterior y posterior están anotados en `data/intercambio/ronda01/cambio_privado.txt`.
No se debe entregar esa nota antes de que el receptor verifique los archivos;
se añadirá a la entrega final después de la comprobación.

El ZIP listo para enviar es `data/intercambio/ronda01/archivos_para_companero.zip`.
Contiene ambos JSONL y la referencia previa; no incluye la nota privada.
El envío real al compañero está pendiente.

## 3. Verifica lo recibido

El receptor adapta su script para recorrer los dos archivos recibidos y comparar cada huella actual con la referencia correspondiente. Las huellas esperadas pueden guardarse en un diccionario de Python, con el nombre de archivo como clave.

Debe mostrar para cada archivo:

- Nombre y tamaño recibido.
- Huella esperada y huella calculada.
- `COINCIDE` o `NO COINCIDE`.

Si falta un archivo, indica `NO RECIBIDO`; no lo clasifiques como una coincidencia. No calcules las huellas esperadas a partir de los archivos recibidos: eso compararía el archivo consigo mismo.

Antes de que el emisor revele el cambio, completa:

| Archivo         | Tamaño esperado | Tamaño recibido | ¿Coincide SHA-256? | Conclusión                                          |
| --------------- | --------------- | --------------- | ------------------ | --------------------------------------------------- |
| partida_A.jsonl | 1049948 bytes   | Pendiente       | Pendiente          | Falta la verificación real del compañero (ronda 01) |
| partida_B.jsonl | 1049948 bytes   | Pendiente       | Pendiente          | Falta la verificación real del compañero (ronda 01) |

Lo esperado es que una copia coincida y la otra no. Si ambas coinciden, revisad si se guardó y envió el cambio o se recalculó la referencia. Si ninguna coincide, revisad si el editor o el envío modificaron también la codificación o los saltos de línea. No ajustéis la referencia para conseguir el resultado esperado.

### Mi respuesta

En la ronda 01 soy el emisor y Joselu es el receptor; falta
recibir sus resultados. La tabla anterior corresponde
a los archivos que he preparado, no a una recepción realizada por mí.

El receptor conserva la referencia previa y ejecuta:

```powershell
python scripts/actividades/06_verificar_envio.py --ronda ronda01
```

El script muestra los tamaños, las dos huellas y el estado de cada archivo,
y guarda la tabla en `data/intercambio/ronda01/resultados.txt`.
La salida de consola del intercambio real está pendiente.

## 4. Intercambia los papeles y explica

Repetid el ejercicio cambiando emisor y receptor. Usad subcarpetas distintas para cada ronda, conservando sus referencias y resultados.

En la segunda ronda Joselu es el emisor y yo (Diego) el receptor.
He guardado su referencia en `data/intercambio/ronda02/referencia.txt` y sus
archivos en `data/intercambio/ronda02/recibido/`. He ejecutado:

```powershell
python scripts/actividades/06_verificar_envio.py --ronda ronda02
```

| Archivo         | Tamaño esperado | Tamaño recibido | ¿Coincide SHA-256? | Conclusión                                    |
| --------------- | --------------- | --------------- | ------------------ | --------------------------------------------- |
| partida_A.jsonl | 860456 bytes | 860456 bytes | Sí: COINCIDE | Conserva el contenido de la referencia de Joselu |
| partida_B.jsonl | 860456 bytes | 860456 bytes | No: NO COINCIDE | El contenido cambió aunque mantiene el tamaño |

He recibido la referencia de Joselu: ambos archivos tienen una huella esperada
`41609645eb9f8b58d26c2ccf43b93e8bfa1518eb70d4e85b7b84b14311ed06bc`
y un tamaño esperado de 860456 bytes. Se conserva su referencia original y
una copia con los mismos valores adaptada al formato del script.
Los dos JSONL ya se han recibido y verificado con la referencia previa, sin modificarla.

Salida de consola de la ronda 02:

```text
partida_A.jsonl | tamaño esperado: 860456 | recibido: 860456
Huella esperada: 41609645eb9f8b58d26c2ccf43b93e8bfa1518eb70d4e85b7b84b14311ed06bc
Huella calculada: 41609645eb9f8b58d26c2ccf43b93e8bfa1518eb70d4e85b7b84b14311ed06bc
COINCIDE

partida_B.jsonl | tamaño esperado: 860456 | recibido: 860456
Huella esperada: 41609645eb9f8b58d26c2ccf43b93e8bfa1518eb70d4e85b7b84b14311ed06bc
Huella calculada: ebb5ff98a16c8a42e9f396c09db42626b2f2dbfc3e1de6db131de31eb15bda23
NO COINCIDE
```

Responded brevemente:

1. ¿Por qué pueden coincidir las huellas de dos archivos con distinto nombre?

   **Respuesta:** SHA-256 depende de los bytes del contenido, no del nombre ni de la carpeta. Antes del cambio, nuestras dos copias tenían la misma huella aunque sus nombres eran distintos.

2. ¿Puede un archivo mantener el tamaño y tener una huella diferente? Utilizad vuestro resultado.

   **Respuesta:** Sí. Los dos archivos recibidos de Joselu ocupan 860456 bytes. La huella de A coincide con la referencia y la de B no, por lo que B mantiene el tamaño pero tiene un contenido diferente.

3. ¿Permite la huella saber qué campo cambió? ¿Cómo comprobaríais el cambio concreto?

   **Respuesta:** No. La huella detecta una diferencia de contenido, pero no señala el campo. Compararía los archivos línea a línea y revisaría los campos JSON de la línea distinta.

4. ¿Por qué calculamos y conservamos la referencia antes de modificar la copia?

   **Respuesta:** Para conservar la huella del contenido original esperado. Si la recalculamos después del cambio, estaríamos usando el archivo modificado como referencia y no detectaríamos esa diferencia.

5. ¿Una coincidencia demuestra que los datos de la partida son correctos o solo que coinciden con la referencia?

   **Respuesta:** Solo comprueba que el contenido coincide con la referencia fiable. No demuestra que los datos registrados por el juego sean correctos.

## Entrega

Entregad el script de verificación, las referencias, las tablas de resultados de ambas rondas y las respuestas en un documento breve. Incluid el cambio realizado y la salida de consola. Identificad quién fue emisor y receptor en cada ronda.

**Utilidad:** habéis comprobado si lo recibido conserva el contenido registrado antes del envío. El manifiesto del tema 09 preparaba las huellas; en esta actividad las habéis utilizado para tomar una decisión. La referencia se considera fiable para el ejercicio: un checksum por sí solo no protege frente a alguien que sustituya tanto el archivo como su huella.
