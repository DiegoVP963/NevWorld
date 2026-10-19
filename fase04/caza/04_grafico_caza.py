from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


DATA_DIR = Path('data/processed')
CHARTS_DIR = Path('reports/charts')
CHARTS_DIR.mkdir(parents=True, exist_ok=True)
output = CHARTS_DIR / '05_hunts_by_prey.png'

hunts = pd.read_csv(DATA_DIR / 'hunts.csv')
campos_obligatorios = ['run_id', 'event_index', 'prey_type']
assert set(campos_obligatorios).issubset(hunts.columns), 'Faltan columnas obligatorias'
assert hunts[campos_obligatorios].notna().all().all(), 'Hay campos obligatorios sin informar'
assert hunts['prey_type'].str.strip().ne('').all(), 'Hay presas sin informar'
assert not hunts.duplicated(['run_id', 'event_index']).any(), 'Hay cacerías duplicadas'
assert hunts['run_id'].nunique() <= 1, 'Hay cacerías de partidas diferentes'

counts = hunts['prey_type'].value_counts()
assert counts.sum() == len(hunts), 'El recuento por presa no coincide con el total'

if hunts.empty:
    if output.exists():
        output.unlink()
    print('No hay cacerías completadas registradas. No se genera el gráfico.')
else:
    plt.figure(figsize=(8, 4))
    counts.plot.bar(color='steelblue')
    plt.title('Cacerías completadas registradas por presa')
    plt.xlabel('Tipo de presa')
    plt.ylabel('Número de cacerías completadas')
    plt.xticks(rotation=30, ha='right')
    plt.tight_layout()
    plt.savefig(output)
    plt.close()
    print(counts.to_string())
    print('Total de cacerías:', len(hunts))
    print('Comprobación del recuento: OK')
    print('Gráfico guardado:', output)
