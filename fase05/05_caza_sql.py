# Apartado 1. Conserva la información en otro formato
from pathlib import Path

import pandas as pd
import duckdb


csv_path = Path('data/processed/hunts.csv')
parquet_path = Path('data/processed/parquet/hunts.parquet')
hunts = pd.read_csv(csv_path)
assert 'prey_type' in hunts.columns, 'Falta la columna prey_type'
assert hunts['prey_type'].notna().all(), 'Hay presas sin informar'
assert hunts['prey_type'].str.strip().ne('').all(), 'Hay presas vacías'

parquet_path.parent.mkdir(parents=True, exist_ok=True)
hunts.to_parquet(parquet_path, engine='pyarrow', index=False)
print('CSV:', csv_path.stat().st_size, 'bytes')
print('Parquet:', parquet_path.stat().st_size, 'bytes')

# Apartado 2. Pregunta por las presas con SQL
connection = duckdb.connect()
hunt_query = """
    SELECT
        prey_type,
        COUNT(*) AS hunt_count
    FROM read_parquet('data/processed/parquet/hunts.parquet')
    GROUP BY prey_type
    ORDER BY hunt_count DESC
"""
hunt_summary = connection.execute(hunt_query).fetchdf()
print('\nCACERÍAS POR PRESA CON SQL')
print(hunt_summary)

# Apartado 3. Comprueba y guarda
assert hunt_summary['hunt_count'].sum() == len(hunts), 'El total no coincide'
pandas_counts = hunts['prey_type'].value_counts().sort_index()
sql_counts = hunt_summary.set_index('prey_type')['hunt_count'].sort_index()
assert pandas_counts.to_dict() == sql_counts.to_dict(), 'Los recuentos no coinciden'
if hunts.empty:
    print('No hay cacerías registradas. Se guarda un resumen vacío.')
else:
    print('Comparación SQL con el recuento de pandas de las actividades 03 y 04: OK')
print('Total de cacerías:', len(hunts))
print('Comprobación de la suma: OK')

output = Path('reports/hunts_by_prey_sql.csv')
output.parent.mkdir(parents=True, exist_ok=True)
hunt_summary.to_csv(output, index=False)
connection.close()
print('Resumen guardado:', output)

# Apartado 4. Explica el resultado
# 1. Cada fila representa un tipo de presa y su número de cacerías completadas.
#    Cuenta eventos de caza, no unidades de comida.
# 2. AS hunt_count da nombre a la columna calculada por COUNT(*).
#    Si se cambia a total_cacerias, hay que actualizar ORDER BY y los accesos
#    a hunt_summary['hunt_count'] y a su columna en sql_counts.
#    La cabecera del CSV exportado también cambiará automáticamente.
# 3. En esta partida el CSV ocupa menos que el Parquet (ver tamaños impresos).
#    No demuestra que CSV sea siempre mejor: Parquet incluye metadatos que
#    pesan en tablas pequeñas y puede ser más eficiente en tablas grandes.
