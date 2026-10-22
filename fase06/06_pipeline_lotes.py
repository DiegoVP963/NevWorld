# Apartado 1. Preparar el pipeline de lotes
from hashlib import sha256
from pathlib import Path
from time import perf_counter

import pandas as pd

RAW_DIR = Path('data/raw')
OUTPUT_DIR = Path('data/processed')
REPORTS_DIR = Path('reports')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(exist_ok=True)
files = sorted(RAW_DIR.glob('nevworld_*.jsonl'))
if not files:
    raise FileNotFoundError('No hay JSONL en data/raw')
start = perf_counter()
frames = []
manifest = []

# Apartado 2. Leer y registrar cada archivo
for path in files:
    checksum = sha256(path.read_bytes()).hexdigest()
    frame = pd.read_json(path, lines=True)
    valid_schema = (
        'schema_version' in frame.columns
        and not frame.empty
        and frame['schema_version'].eq(2).all()
    )
    manifest.append({
        'file': path.name,
        'bytes': path.stat().st_size,
        'rows': len(frame),
        'sha256': checksum,
        'status': 'accepted' if valid_schema else 'rejected',
    })
    if valid_schema:
        frame['source_file'] = path.name
        frames.append(frame)

# Apartado 3. Unir y comprobar las sesiones
if not frames:
    raise ValueError('Ningún archivo utiliza el esquema 2')
events = pd.concat(frames, ignore_index=True)
duplicates = events.duplicated(['run_id', 'event_index']).sum()
if duplicates:
    raise ValueError(f'Se detectaron {duplicates} eventos duplicados')
events = events.sort_values(['run_id', 'event_index'])

# Apartado 4. Guardar resultados y métricas
events.to_parquet(OUTPUT_DIR / 'all_events.parquet', index=False)
pd.DataFrame(manifest).to_csv(REPORTS_DIR / 'manifest.csv', index=False)
elapsed = perf_counter() - start
run_report = pd.DataFrame([{
    'files_found': len(files),
    'files_accepted': len(frames),
    'sessions': events['run_id'].nunique(),
    'events': len(events),
    'seconds': round(elapsed, 3),
}])
run_report.to_csv(REPORTS_DIR / 'pipeline_run.csv', index=False)
print(run_report.to_string(index=False))
