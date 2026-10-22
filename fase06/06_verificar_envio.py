# Apartado 1. Registrar la referencia antes de modificar las copias
from argparse import ArgumentParser
from hashlib import sha256
from pathlib import Path

parser = ArgumentParser(description='Registrar o verificar un intercambio real de partidas.')
parser.add_argument('--ronda', choices=['ronda01', 'ronda02'], default='ronda01')
parser.add_argument('--registrar', action='store_true', help='Registrar las copias intactas una sola vez.')
args = parser.parse_args()
base = Path('data/intercambio') / args.ronda
reference = base / 'referencia.txt'
names = ['partida_A.jsonl', 'partida_B.jsonl']

if args.registrar:
    rows = []
    for name in names:
        path = base / 'envio' / name
        content = path.read_bytes()
        rows.append((name, len(content), sha256(content).hexdigest()))
    if rows[0][2] != rows[1][2]:
        raise ValueError('Las dos copias deben ser idénticas antes de registrar la referencia')
    # Modo x: nunca sobrescribir una referencia que ya existe.
    with reference.open('x', encoding='utf-8') as output:
        output.write('archivo\tbytes\tsha256\n')
        for name, size, checksum in rows:
            output.write(f'{name}\t{size}\t{checksum}\n')
            print(name, size, checksum)
    print('Referencia guardada. Ahora se puede modificar una sola copia.')
else:
    # Apartado 2. El emisor envía la referencia previa y las dos copias.
    # El receptor coloca la referencia en la carpeta de la ronda, y los JSONL
    # en recibido. El script no modifica ninguno de esos archivos.

    # Apartado 3. Verificar los archivos recibidos contra la referencia conservada
    expected = {}
    for line in reference.read_text(encoding='utf-8-sig').splitlines()[1:]:
        name, size, checksum = line.split('\t')
        expected[name] = (int(size), checksum)
    results = ['Archivo\tTamaño esperado\tTamaño recibido\tSHA-256 esperado\tSHA-256 calculado\tEstado']
    for name in names:
        size, checksum = expected[name]
        path = base / 'recibido' / name
        if not path.is_file():
            actual_size, actual_checksum, status = '-', '-', 'NO RECIBIDO'
        else:
            content = path.read_bytes()
            actual_size = len(content)
            actual_checksum = sha256(content).hexdigest()
            status = 'COINCIDE' if actual_checksum == checksum else 'NO COINCIDE'
        print(f'\n{name} | tamaño esperado: {size} | recibido: {actual_size}')
        print('Huella esperada:', checksum)
        print('Huella calculada:', actual_checksum)
        print(status)
        results.append(f'{name}\t{size}\t{actual_size}\t{checksum}\t{actual_checksum}\t{status}')
    (base / 'resultados.txt').write_text('\n'.join(results) + '\n', encoding='utf-8')

# Apartado 4. Intercambiar papeles y explicar
# Usar --ronda ronda02 para conservar por separado la segunda referencia.
# Las huellas dependen del contenido, no del nombre. Un dígito distinto puede
# mantener el tamaño y cambiar la huella. La huella no identifica el campo
# cambiado: hay que comparar los contenidos. La referencia anterior al cambio
# permite detectar diferencias; coincidir con ella no prueba que los datos
# de la partida sean correctos. Las respuestas completas están en ejercicio6.md.
