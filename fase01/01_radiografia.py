from pathlib import Path

import pandas as pd

DATASET = Path(
    'data/raw/nevworld_558220143806760042_20261005_182759.jsonl'
)

if not DATASET.exists():
    raise FileNotFoundError(
        f'No se encuentra: {DATASET.resolve()}'
    )

df = pd.read_json(DATASET, lines=True)

required = ['run_id', 'event_index', 'tick', 'type']

assert not df.empty, 'El dataset está vacío'
assert all(column in df.columns for column in required), 'Faltan columnas principales'
assert not df.duplicated(['run_id', 'event_index']).any(), 'Hay eventos duplicados'

ordered = df.sort_values('event_index')
assert ordered['tick'].is_monotonic_increasing, 'Los ticks retroceden'

# Primera inspección: no modificamos el archivo RAW.
print('Primeras filas:')
print(df.head())

nombre = DATASET.name
print("Nombre del archivo JSONL:" + nombre)
filas, columnas = df.shape
print('Número total de eventos:', filas)
print('Número de columnas:', columnas)
print('Nombres de las columnas:', df.columns.to_list())
print('Tipo del primer evento registrado:', df['type'].iloc[0])
print('Tipo de evento más frecuente y cantidad:', df['type'].value_counts().head(1))
print('Recuento de todos los tipos de evento:', df['type'].value_counts())
print('run_id de la primera fila:', df['run_id'].iloc[0])
print('Semilla de la primera fila:', df['seed'].iloc[0])
print('Versión del esquema de la primera fila:', df['schema_version'].iloc[0])
print('Tick mínimo:', df['tick'].min())
print('Tick máximo:', df['tick'].max())
print('Resultado de las validaciones: OK, las cuatro comprobaciones han salido correctas')
