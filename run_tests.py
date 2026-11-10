"""Pruebas portables: salida exacta y código de retorno, sin herramientas Unix."""
from pathlib import Path
import subprocess
import os
import sys
import difflib

ROOT = Path(__file__).resolve().parent


def main():
    fallos = 0
    casos = sorted((ROOT / 'tests').glob('*.txt'))
    for caso in casos:
        esperado = (ROOT / 'tests/esperado' / (caso.stem + '.out')).read_text(encoding='utf-8')
        resultado = subprocess.run([sys.executable, str(ROOT / 'main.py'), str(caso)],
                                   capture_output=True, text=True, encoding='utf-8',
                                   env={**os.environ, 'PYTHONUTF8': '1'})
        codigo = 1 if '=== ERRORES' in esperado else 0
        salida = resultado.stdout + resultado.stderr
        correcto = salida == esperado and resultado.returncode == codigo
        print(('OK     ' if correcto else 'FALLA  ') + caso.stem)
        if not correcto:
            fallos += 1
            print(''.join(difflib.unified_diff(esperado.splitlines(True), salida.splitlines(True),
                                             fromfile='esperado', tofile='obtenido')))
            print(f'Código esperado: {codigo}; obtenido: {resultado.returncode}')
    regresion = subprocess.run([sys.executable, '-m', 'unittest', 'discover', '-s', 'tests',
                               '-p', 'test_regresiones.py', '-v'], cwd=ROOT)
    fallos += int(regresion.returncode != 0)
    print(f'{len(casos)} casos de salida comprobados; {fallos} bloque(s) fallido(s).')
    return int(fallos != 0)


if __name__ == '__main__':
    sys.exit(main())
