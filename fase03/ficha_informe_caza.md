# Informe de caza: apartados 2 y 3

Datos: `data/processed/hunts.csv` y `data/processed/resources.csv`.
RAW de origen: `nevworld_558220143806760042_20261005_182759.jsonl`.
Partida: `20261005_182759_558220143806760042_5ebf59dd10ea42d99f3df8b17025b9db`.

## 2. Resume el parte de caza

Hay **14 cacerías completadas registradas**. Cada fila de `hunts.csv` representa una cacería completada, con su presa, aldeano y momento de la partida.

| Presa | Cacerías | Porcentaje |
| --- | ---: | ---: |
| sheep | 11 | 78,6 % |
| deer | 3 | 21,4 % |

Los recuentos se obtienen con `value_counts()`, que los ordena de mayor a menor frecuencia. El denominador de los porcentajes es el total de 14 cacerías completadas registradas. Se calculan con `value_counts(normalize=True) * 100` y se redondean a un decimal con `.round(1)`.

| Día | Cacerías registradas |
| ---: | ---: |
| 1 | 1 |
| 2 | 4 |
| 3 | 1 |
| 4 | 1 |
| 5 | 3 |
| 6 | 1 |
| 10 | 1 |
| 11 | 2 |

Para ordenar los días cronológicamente se usa `value_counts().sort_index()`. Los días ausentes no se presentan como días observados con cero cacerías: esta tabla no determina todo el periodo de observación.

## 3. Examina los cambios de comida

Se seleccionan los eventos con `resource_type == 'food'`.

| Métrica | Unidades de comida |
| --- | ---: |
| Incrementos registrados | 301 |
| Reducciones registradas, como cantidad positiva | 132 |
| Balance neto | +169 |

Los incrementos son la suma de los `amount_delta` positivos. Las reducciones son la suma de las magnitudes de los negativos, usando `.abs().sum()`. El balance es la suma de todos los cambios conservando sus signos: 301 − 132 = 169.

Estos resultados describen variaciones registradas. El balance no representa por sí solo las existencias finales ni demuestra que los incrementos procedan de la caza.

El script comprueba columnas necesarias, valores ausentes, eventos duplicados y que ambas tablas pertenecen a una misma partida. Incluye avisos para tablas sin cacerías o sin eventos de comida.

Los apartados 4 y 5 y la ampliación quedan pendientes.
