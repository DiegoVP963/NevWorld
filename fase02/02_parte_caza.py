from pathlib import Path

import pandas as pd

DATASET = Path(
    'data/raw/nevworld_558220143806760042_20261005_182759.jsonl'
)

OUTPUT_DIR = Path('data/processed')

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

if not DATASET.exists():
    raise FileNotFoundError(f'No se encuentra: {DATASET.resolve()}')

df = pd.read_json(DATASET, lines=True)
assert 'type' in df.columns, 'Falta la columna type'

print('Eventos por tipo:')
print(df['type'].value_counts())

def event_table(event_type, columns):

    selected = ['run_id', 'event_index', 'tick', *columns]

    available = [
        column for column in selected
        if column in df.columns
    ]

    table = df.loc[
        df['type'] == event_type,
        available,
    ].copy()

    # Conservamos las cabeceras aunque no haya cacerías o falte alguna columna.
    columnas_de_salida = selected
    table = table.reindex(columns=columnas_de_salida)

    # Añadimos la columna también cuando la tabla está vacía.
    table['simulation_day'] = table['tick'] // 12000

    return table

# Como en 02_transformar.py, guardamos las tablas en un diccionario.
# Para esta actividad solo necesitamos la tabla de cacerías.
tables = {
    'hunts': event_table('hunt_completed', [
        'villager_id', 'prey_type',
    ]),
}

# Seleccionamos la tabla que queremos comprobar.
hunts = tables['hunts']

campos_obligatorios = [
    'run_id', 'event_index', 'tick', 'villager_id', 'prey_type',
]

cantidad = (df['type'] == 'hunt_completed').sum()
assert len(hunts) == cantidad, 'El recuento de cacerías no coincide con el RAW'
assert not hunts.duplicated(['run_id', 'event_index']).any(), 'Hay cacerías duplicadas'

if not hunts.empty:
    assert hunts[campos_obligatorios].notna().all().all(), 'Faltan campos obligatorios de caza'

assert (hunts['simulation_day'] == hunts['tick'] // 12000).all(), 'Hay días de simulación incorrectos'

# Guardamos los CSV con el mismo bucle que en 02_transformar.py.
for name, table in tables.items():
    output = OUTPUT_DIR / f'{name}.csv'
    table.to_csv(output, index=False)
    print('Archivo generado:', output)
    print('Número de filas:', len(table))
print('Validaciones: OK')
