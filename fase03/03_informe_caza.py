from pathlib import Path

import pandas as pd


DATA_DIR = Path('data/processed')
hunts = pd.read_csv(DATA_DIR / 'hunts.csv')
resources = pd.read_csv(DATA_DIR / 'resources.csv')

# 1. Comprueba las columnas, los valores y la partida de origen.
for name, table, columns in [
    ('hunts', hunts, ['run_id', 'event_index', 'prey_type', 'simulation_day']),
    ('resources', resources, ['run_id', 'event_index', 'resource_type', 'amount_delta']),
]:
    assert set(columns).issubset(table.columns), f'Faltan columnas en {name}'
    assert table[columns].notna().all().all(), f'Hay valores ausentes en {name}'
    assert not table.duplicated(['run_id', 'event_index']).any(), f'Hay eventos duplicados en {name}'

run_ids = pd.concat([hunts['run_id'], resources['run_id']]).unique()
assert len(run_ids) <= 1, 'Los datos contienen partidas diferentes'

# 2. Resume el parte de caza.
print('\nTOTAL DE CACERÍAS COMPLETADAS REGISTRADAS')
print(len(hunts))
print('Cada fila representa una cacería completada registrada.')

hunts_counts = hunts['prey_type'].value_counts()
hunts_percent = (hunts['prey_type'].value_counts(normalize=True) * 100).round(1)
hunts_days_count = hunts['simulation_day'].value_counts().sort_index()

if hunts.empty:
    print('No hay cacerías completadas registradas.')
else:
    print('\nRECUENTO POR PRESA (DE MAYOR A MENOR)')
    print(hunts_counts.to_string())
    print('\nPORCENTAJE DE CADA PRESA')
    print(hunts_percent.to_string())
    print('El denominador es el total de cacerías completadas registradas:', len(hunts))
    print('\nCACERÍAS POR DÍA (ORDEN CRONOLÓGICO)')
    print(hunts_days_count.to_string())

print('Un día ausente no demuestra que se observaran cero cacerías ese día.')

# 3. Examina los cambios de comida.
food = resources[resources['resource_type'] == 'food']
food_gains = food[food['amount_delta'] > 0]['amount_delta'].sum()
food_reductions = food[food['amount_delta'] < 0]['amount_delta'].abs().sum()
food_net_change = food['amount_delta'].sum()

if food.empty:
    print('\nNo hay eventos de comida registrados; las sumas son cero.')
    print('Esto no demuestra que el mundo no tuviera comida.')

print('\nINCREMENTOS DE COMIDA REGISTRADOS')
print(food_gains)
print('\nREDUCCIONES DE COMIDA (MAGNITUD POSITIVA)')
print(food_reductions)
print('\nBALANCE NETO DE COMIDA')
print(food_net_change)
