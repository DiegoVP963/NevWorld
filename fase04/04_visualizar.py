from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd


DATA_DIR = Path('data/processed')
CHARTS_DIR = Path('reports/charts')
CHARTS_DIR.mkdir(parents=True, exist_ok=True)

snapshots = pd.read_csv(DATA_DIR / 'snapshots.csv')
activities = pd.read_csv(DATA_DIR / 'activities.csv')
needs = pd.read_csv(DATA_DIR / 'needs.csv')
social = pd.read_csv(DATA_DIR / 'social.csv')

# Usamos las tablas de una misma partida.
run_ids = pd.concat([
    snapshots['run_id'], activities['run_id'],
    needs['run_id'], social['run_id'],
]).dropna().unique()
assert len(run_ids) <= 1, 'Las tablas contienen partidas diferentes'

# 1. Evolución de las existencias de recursos.
ordered = snapshots.sort_values(['tick', 'event_index'])
plt.figure(figsize=(10, 5))
if ordered.empty:
    print('Aviso: no hay snapshots para mostrar la evolución de recursos.')
    plt.text(0.5, 0.5, 'Sin fotografías registradas', ha='center', transform=plt.gca().transAxes)
else:
    plt.plot(ordered['tick'], ordered['wood_stock'], label='Madera')
    plt.plot(ordered['tick'], ordered['food_stock'], label='Comida')
    plt.plot(ordered['tick'], ordered['gold_stock'], label='Oro')
    plt.legend()
plt.title('Evolución de los recursos')
plt.xlabel('Tick (tiempo simulado)')
plt.ylabel('Cantidad disponible (unidades)')
plt.tight_layout()
plt.savefig(CHARTS_DIR / '01_resources_timeline.png')
plt.close()

# 2. Contamos cambios de actividad, no el tiempo dedicado a cada una.
activity_counts = activities['activity'].value_counts()
plt.figure(figsize=(10, 5))
if activity_counts.empty:
    print('Aviso: no hay cambios de actividad registrados.')
    plt.text(0.5, 0.5, 'Sin cambios de actividad registrados', ha='center', transform=plt.gca().transAxes)
else:
    activity_counts.plot.bar(color='steelblue')
plt.title('Cambios de actividad registrados')
plt.xlabel('Actividad')
plt.ylabel('Número de eventos')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(CHARTS_DIR / '02_activities.png')
plt.close()

# 3. Contamos eventos críticos, no aldeanos distintos ni duración.
critical = needs[needs['state'] == 'critical']
critical_counts = critical['need_type'].value_counts()
plt.figure(figsize=(7, 4))
if critical_counts.empty:
    print('Aviso: no hay eventos de necesidades críticas registrados.')
    plt.text(0.5, 0.5, 'Sin eventos críticos registrados', ha='center', transform=plt.gca().transAxes)
else:
    critical_counts.plot.bar(color='darkorange')
plt.title('Necesidades que alcanzaron estado crítico')
plt.xlabel('Necesidad')
plt.ylabel('Número de eventos')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(CHARTS_DIR / '03_critical_needs.png')
plt.close()

# 4. Frecuencia de cada tipo de interacción social.
interaction_counts = social['interaction_type'].value_counts()
plt.figure(figsize=(8, 4))
if interaction_counts.empty:
    print('Aviso: no hay interacciones sociales registradas.')
    plt.text(0.5, 0.5, 'Sin interacciones sociales registradas', ha='center', transform=plt.gca().transAxes)
else:
    interaction_counts.plot.bar(color='seagreen')
plt.title('Tipos de interacción social')
plt.xlabel('Interacción')
plt.ylabel('Número de eventos')
plt.xticks(rotation=30, ha='right')
plt.tight_layout()
plt.savefig(CHARTS_DIR / '04_social_interactions.png')
plt.close()

print('Cuatro gráficos guardados en reports/charts.')
