# El informe de caza: de las tablas a las conclusiones

El creador de NevWorld ya tiene tu parte de caza, pero necesita un resumen: **qué presas aparecen más, cómo se reparten las cacerías registradas por día y cómo cambió la comida disponible**. Además, quiere comprobar esta afirmación: «Si aumentó la comida, fue gracias a la caza».

Tu misión es calcular métricas y explicar qué permiten afirmar. Utiliza los datos de tu propia partida y las operaciones del tema 06. No necesitas gráficas, unir tablas ni modificar el RAW o los CSV procesados.

## Teoría de apoyo

Python es el lenguaje; pandas es la biblioteca que permite trabajar con tablas. `pd.read_csv()` devuelve un DataFrame. Al seleccionar una columna, como `hunts['prey_type']`, obtienes una Series. Los siguientes métodos pertenecen a pandas:

| Para…                                       | Operación que puedes reutilizar            |
| ------------------------------------------- | ------------------------------------------ |
| Contar las apariciones de cada valor        | `tabla['columna'].value_counts()`          |
| Obtener porcentajes                         | `value_counts(normalize=True) * 100`       |
| Redondear a un decimal                      | `.round(1)`                                |
| Seleccionar filas que cumplen una condición | `tabla[tabla['columna'] == valor]`         |
| Agrupar y sumar una cantidad                | `tabla.groupby('grupo')['cantidad'].sum()` |
| Ordenar una Series por sus etiquetas        | `.sort_index()`                            |
| Obtener cantidades sin signo negativo       | `.abs()`                                   |
| Saber si una tabla no tiene filas           | `.empty`                                   |
| Exportar una tabla sin su índice interno    | `.to_csv(ruta, index=False)`               |

**Una operación nueva:** `.sort_index()` ordena por las etiquetas de la Series. Si las etiquetas son días, permite mostrarlos cronológicamente. `.sort_values()` ordenaría por los valores de la métrica. Por ejemplo, con día 2 → 5 cacerías y día 1 → 2 cacerías, ordenar por índice muestra primero el día 1.

`len()`, `print()`, `if`, `for`, las listas y los diccionarios pertenecen a Python. Una máscara de comparación selecciona filas; una agrupación organiza filas para calcular un resumen. No son la misma operación.

## 1. Prepara las preguntas y los datos

Crea `scripts/actividades/03_informe_caza.py` dentro de `bigdata-game`. Carga `data/processed/hunts.csv`, creado en la actividad 02, y `data/processed/resources.csv`, generado en la teoría. Ambos deben corresponder a la misma partida. Si falta `hunts.csv`, termina la actividad anterior; no lo sustituyas por datos inventados.

Antes de calcular, completa esta ficha:

| Pregunta                                                         | Tabla y columnas necesarias                                                | Operación y motivo                                                                                                                                                                                                                                                                 |
| ---------------------------------------------------------------- | -------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ¿Cuántas cacerías completadas se registraron?                    | hunts.csv                                                                  | len(hunts) ; Si existe registro es por que se completó. Miro cuantos registros tiene el archivo.                                                                                                                                                                                   |
| ¿Cuántas corresponden a cada tipo de presa?                      | sheep = 11 ; deer = 3                                                      | hunts_counts = hunts['prey_type'].value_counts() ; Extraigo todos los valores de la tabla, aunque se repitan y con value.counts cuento cuantas veces aparece.                                                                                                                      |
| ¿Qué porcentaje representa cada presa?                           | 78.6% sheep ; 21.4% deer                                                   | hunts_percent = (hunts['prey_type'].value_counts(normalize=True) \* 100).round(1) ; Con normalize obtenemos las proporciones y redondeamos a 1 decimal para que no aparezca un número largo.                                                                                       |
| ¿Cuántas cacerías se registraron en cada día observado?          | Día 1: 1 Día 2: 4 Día 3 : 1 Día 4: 1 Día 5: 3 Día 6: 1 Día 10: 1 Día 11: 2 | hunts_days_count = hunts['simulation_day'].value_counts().sort_values(ascending=False) ; Parecido a lo que hemos hecho anteriormente, contamos cuantas veces aparece cada cacería en el día.                                                                                       |
| ¿Cuánto aumentó, disminuyó y cambió en términos netos la comida? | Incrementos = 301 ; Reducciones = 132 ; Balance neto = 169                 | Filtrar los eventos con `resource_type == 'food'`. Sumar los `amount_delta` positivos con `.sum()` para los incrementos; los negativos con `.abs().sum()` para mostrar las reducciones como cantidad positiva; y todos con `.sum()`, conservando sus signos, para el balance neto. |

Comprueba que existen las columnas necesarias, que no se repite `run_id` y `event_index` dentro de cada tabla y que los campos usados en los cálculos no tienen valores ausentes. Si detectas un problema, explica el error sin borrar filas para ocultarlo. No mezcles partidas.

## 2. Resume el parte de caza

Muestra en la consola:

1. El total de cacerías completadas registradas.
2. El recuento por `prey_type`, de mayor a menor frecuencia.
3. El porcentaje de cada tipo de presa, redondeado a un decimal.
4. El recuento por `simulation_day`, ordenado por día, no por frecuencia.

Explica qué representa una fila de `hunts.csv` y cuál es el denominador de los porcentajes.

Si la tabla está vacía, muestra un mensaje indicando que no hay cacerías completadas registradas. El total será cero; no intentes acceder al primer elemento de un recuento vacío ni inventes una presa predominante. Un día que no aparece en el recuento no es automáticamente un día observado con cero cacerías: este archivo no determina por sí solo todo el periodo de observación.

### Respuestas

Se registraron **14 cacerías completadas**.

| Presa | Recuento | Porcentaje |
| ----- | -------: | ---------: |
| sheep |       11 |     78,6 % |
| deer  |        3 |     21,4 % |

Uso `hunts['prey_type'].value_counts()` para contar las presas de mayor a menor frecuencia. Para los porcentajes uso `(hunts['prey_type'].value_counts(normalize=True) * 100).round(1)`.

| Día | Cacerías |
| --: | -------: |
|   1 |        1 |
|   2 |        4 |
|   3 |        1 |
|   4 |        1 |
|   5 |        3 |
|   6 |        1 |
|  10 |        1 |
|  11 |        2 |

Uso `hunts['simulation_day'].value_counts().sort_index()` para ordenar por día.

Una fila de `hunts.csv` representa una cacería completada registrada, con el aldeano, la presa y el momento en que ocurrió. El denominador de los porcentajes es el total de **14 cacerías registradas**; no es el número de aldeanos ni el tiempo dedicado a cazar.

Los días que no aparecen no demuestran que hubiera cero cacerías durante un día observado, porque esta tabla no define todo el periodo de observación.

## 3. Examina los cambios de comida

Filtra las filas de `resources` cuyo `resource_type` sea `food`. Después calcula:

- **Incrementos registrados:** suma de los `amount_delta` positivos.
- **Reducciones registradas:** suma de las magnitudes de los `amount_delta` negativos; muéstrala como número positivo.
- **Balance neto:** suma de todos los `amount_delta` de comida.

Ejemplo inventado: +12, −5 y +3 producen incrementos de 15, reducciones de 5 y balance de +10. No es el resultado que debes entregar: usa tus datos.

Si no hay eventos de comida, las tres sumas serán cero, pero muestra también un aviso. Ese cero significa que no hay variaciones registradas que sumar. Esto demuestra que el mundo no tuviera comida.

### Respuestas

Filtro la comida con `food = resources[resources['resource_type'] == 'food']`.

- **Incrementos registrados: 301 unidades.** Uso `food[food['amount_delta'] > 0]['amount_delta'].sum()` para sumar los cambios positivos.
- **Reducciones registradas: 132 unidades.** Uso `food[food['amount_delta'] < 0]['amount_delta'].abs().sum()` para sumar los cambios negativos como cantidades positivas.
- **Balance neto: +169 unidades.** Uso `food['amount_delta'].sum()` para sumar todos los cambios conservando su signo. Coincide con `301 - 132 = 169`.

Hay eventos de comida registrados, así que no se aplica el aviso de ausencia de datos. El balance describe el cambio registrado, no las existencias finales ni el origen de los incrementos.

## 4. Comprueba y guarda el informe

Comprueba con `assert` que:

- La suma de los recuentos por presa coincide con el total de cacerías.
- La suma de los recuentos por día también coincide con ese total.
- Los incrementos menos las reducciones coinciden con el balance de comida.

Si hay cacerías, revisa que los porcentajes sin redondear sumen aproximadamente 100. Los porcentajes redondeados pueden no sumar exactamente 100. Para comparar números decimales puedes usar `abs(a - b) < 0.000001`: aquí `abs()` es una función de Python que mide la magnitud de la diferencia.

Crea un DataFrame de resumen con dos columnas, `metric` y `value`, y estas cinco filas:

| metric               | Qué guardar en value                          |
| -------------------- | --------------------------------------------- |
| `hunt_events`        | Total de cacerías completadas registradas     |
| `food_change_events` | Número de eventos de cambio de comida         |
| `food_gains`         | Incrementos de comida registrados             |
| `food_reductions`    | Reducciones de comida, como cantidad positiva |
| `food_net_change`    | Balance neto de comida                        |

Guárdalo en `reports/hunting_summary.csv`, sin índice. Reutiliza `pd.DataFrame` con una lista de diccionarios como en la teoría. Los recuentos por presa y día y los porcentajes se incorporarán a la ficha, junto con la salida de las comprobaciones.

Ejecuta desde la raíz de `bigdata-game`, con el entorno que tenga pandas:

```powershell
python scripts/actividades/03_informe_caza.py
```

### Respuestas

He usado `assert` para comprobar que los resultados cuadran:

- Por presa: `11 + 3 = 14`, coincide con el total de cacerías.
- Por día: `1 + 4 + 1 + 1 + 3 + 1 + 1 + 2 = 14`, también coincide.
- Comida: `301 - 132 = 169`, coincide con el balance neto.
- Los porcentajes sin redondear suman aproximadamente 100. Lo compruebo con `abs(percentages.sum() - 100) < 0.000001`.

Al ejecutar el script aparece `Comprobaciones: OK`, así que han pasado todas.

Creo el resumen con `pd.DataFrame` y una lista de diccionarios. Después uso `summary.to_csv(REPORTS_DIR / 'hunting_summary.csv', index=False)` para guardarlo sin el índice de pandas.

| metric | value |
| --- | ---: |
| hunt_events | 14 |
| food_change_events | 125 |
| food_gains | 301 |
| food_reductions | 132 |
| food_net_change | 169 |

El archivo se guarda en `reports/hunting_summary.csv`. Los datos son de mi RAW `nevworld_558220143806760042_20261005_182759.jsonl`, de la partida `20261005_182759_558220143806760042_5ebf59dd10ea42d99f3df8b17025b9db`.

## 5. Defiende tus conclusiones

Responde utilizando tus resultados reales:

1. ¿Qué presa o presas tienen el mayor recuento? Si hay empate, indícalo; si no hay datos, explica por qué no puedes responder.
2. ¿El porcentaje de una presa representa porcentaje de cacerías, de aldeanos o de tiempo? Justifica el denominador.
3. ¿El día con más cacerías fue necesariamente el día en que se dedicó más tiempo a cazar?
4. ¿El balance neto indica las existencias finales de comida? ¿Qué información faltaría?
5. ¿Puedes demostrar que todos los incrementos de comida se deben a la caza? ¿Qué vínculo entre eventos necesitarías para justificarlo?

### Respuestas

1. La presa que más aparece es `sheep`, con 11 cacerías. `deer` aparece 3 veces, así que no hay empate.

2. Es el porcentaje de cacerías. Divido las cacerías de cada presa entre las 14 cacerías registradas y multiplico por 100. Por eso sale 78,6 % de `sheep` y 21,4 % de `deer`.

3. No necesariamente. El día 2 es el que tiene más cacerías completadas, con 4, pero no sé cuánto duró cada una. Puede haber otro día con menos cacerías pero en el que se pasó más tiempo cazando.

4. No. El balance de +169 me dice cuánto cambió la comida según los eventos registrados. Para saber la comida final tendría que conocer la cantidad inicial y comprobar que tengo todos los cambios del mismo periodo. Entonces sumaría la comida inicial y el balance.

5. No puedo demostrarlo solo con estas tablas. En `hunts.csv` veo que terminó una cacería, pero no cuánta comida dio. Necesitaría que el evento de cambio de comida indicara de qué cacería viene, por ejemplo con el identificador de esa cacería y la partida. Que los eventos ocurran cerca en el tiempo no basta para asegurar que todo el aumento viene de cazar.

## Ampliación para l@s más rápid@s: contrastar con las fotografías

Carga `snapshots.csv` de la misma partida, ordénalo por `tick` y `event_index` y calcula la diferencia de `food_stock` entre la primera y la última fotografía disponibles. Muestra también sus ticks.

Antes de usar `.iloc`, comprueba si hay filas. Con una sola fotografía, explica por qué la diferencia de cero no demuestra estabilidad durante toda la partida.

Compara esa diferencia con tu balance de comida. ¿Tienen necesariamente el mismo intervalo de observación? Explica por qué una discrepancia no prueba por sí sola un error. No fuerces la igualdad con un `assert`.

## Entrega y valoración

Entrega el script, `hunting_summary.csv` y una ficha con las decisiones de diseño, los recuentos y porcentajes, las comprobaciones y las cinco respuestas. Identifica el archivo RAW de origen y la partida utilizada. Si realizas la ampliación, incluye sus resultados y explicación.

Se valorará la elección razonada de operaciones, los cálculos correctos, el tratamiento de tablas vacías y la prudencia al interpretar resultados. Las cifras pueden variar entre partidas.
