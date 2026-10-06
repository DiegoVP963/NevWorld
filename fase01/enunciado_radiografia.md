# Radiografía de una partida de NevWorld

Has terminado una partida y el juego ha generado un archivo JSONL. Tu misión es abrirlo con pandas y preparar una ficha que permita a otra persona comprender qué contiene ese registro.

Utiliza **los datos de tu propia partida** y las operaciones vistas en el tema. No modifiques el archivo RAW.

## Teoría de apoyo

JSONL guarda un evento en cada línea. pandas lo carga con `pd.read_json(..., lines=True)` en un **DataFrame**, una tabla de filas y columnas. La variable `df` recibe ese nombre como abreviatura de DataFrame: cada fila representa un evento y cada columna, un campo.

| Para…                               | Utiliza…                     |
| ----------------------------------- | ---------------------------- |
| Representar y comprobar la ruta     | `Path(...)` y `exists()`     |
| Ver los primeros eventos            | `df.head()`                  |
| Obtener filas y columnas            | `df.shape`                   |
| Consultar los nombres de los campos | `df.columns.tolist()`        |
| Contar eventos de cada tipo         | `df['type'].value_counts()`  |
| Leer un valor de la primera fila    | `df['campo'].iloc[0]`        |
| Obtener los extremos de los ticks   | `df['tick'].min()` y `max()` |

Los eventos pueden tener campos diferentes: un `NaN` representa una ausencia, no necesariamente un error ni un cero. El tick mide tiempo simulado; varios eventos pueden compartirlo.

## Enunciado

Crea `scripts/actividades/01_radiografia.py` en tu proyecto `bigdata-game`. Carga el JSONL que has guardado en `data/raw`, comprobando antes que la ruta existe. Puedes apoyarte en el script del tema.

Aplica las cuatro validaciones básicas del tema: que la tabla no esté vacía, que existan las columnas principales, que no se repita la pareja `run_id` y `event_index`, y que los ticks no retrocedan al ordenar por `event_index`. Hazlo antes de consultar la primera fila.

Después, muestra las primeras filas y obtén los datos necesarios para completar esta ficha:

| Dato de mi partida                                         | Resultado |
| ---------------------------------------------------------- | --------- |
| Nombre del archivo JSONL                                   |           |
| Número total de eventos                                    |           |
| Número de columnas                                         |           |
| Nombres de las columnas                                    |           |
| Tipo del primer evento registrado                          |           |
| Tipo de evento más frecuente y cantidad                    |           |
| Recuento de todos los tipos de evento                      |           |
| `run_id`, semilla y versión del esquema de la primera fila |           |
| Tick mínimo y tick máximo                                  |           |
| Resultado de las validaciones                              |           |

Termina la ficha respondiendo con tus palabras:

1. ¿Qué te permite afirmar el recuento sobre tu partida? ¿Por qué el tipo más frecuente no tiene que ser el más importante?
2. ¿Por qué una celda vacía no significa necesariamente que el registro esté mal?
3. ¿Qué sabes ahora del archivo y qué pregunta sobre tu partida necesitaría un análisis posterior?

Ejecuta desde la raíz de `bigdata-game`, con el entorno de Python que tenga pandas instalado:

```powershell
python scripts/actividades/01_radiografia.py
```

**Entrega:** Cread un repositorio en Github con una carpeta llamada NevWorld, y una subcarpeta llamada fase01, en la que incluiréis el script y la ficha en un archivo de texto, con tus respuestas y resultados reales. Si alguna validación falla, anota el error y explica qué comprobación no se cumple; no alteres el RAW para hacerla pasar.
