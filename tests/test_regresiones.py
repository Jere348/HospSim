"""Regresiones con resultados calculados a mano, no generados por el compilador."""
import subprocess
import os
import sys
import tempfile
import unittest
from pathlib import Path
from backend.modelo import Modelo, Etapa, Llegada
from backend.simulador import simular

ROOT = Path(__file__).resolve().parents[1]


class Regresiones(unittest.TestCase):
    def compilar(self, texto, *args):
        with tempfile.TemporaryDirectory() as carpeta:
            fuente = Path(carpeta) / 'prueba.txt'
            fuente.write_text(texto, encoding='utf-8')
            return subprocess.run([sys.executable, str(ROOT / 'main.py'), *args, str(fuente)],
                                  capture_output=True, text=True, encoding='utf-8',
                                   env={**os.environ, 'PYTHONUTF8': '1'})

    def test_recurso_compartido_no_se_reserva_en_el_futuro(self):
        m = Modelo({'a': 1, 'b': 1},
                   {'largo': [Etapa('e1', 'a', 100), Etapa('e2', 'b', 1)],
                    'corto': [Etapa('e', 'b', 1)]},
                   [Llegada('largo', 1000), Llegada('corto', 1000)], 10)
        resultado = simular(m)
        self.assertEqual(resultado['pacientes_atendidos'], 1)
        self.assertEqual(resultado['ocupacion']['b'], 10)

    def test_fifo_del_recurso_y_espera(self):
        # Largo llega a b en t=2; corto ya lo ocupa de 0 a 5.
        # Largo termina en 6 tras esperar 3 minutos. Promedio: (0+3)/2.
        m = Modelo({'a': 1, 'b': 1},
                   {'largo': [Etapa('e1', 'a', 2), Etapa('e2', 'b', 1)],
                    'corto': [Etapa('e', 'b', 5)]},
                   [Llegada('largo', 100), Llegada('corto', 100)], 10)
        resultado = simular(m)
        self.assertEqual(resultado['pacientes_atendidos'], 2)
        self.assertEqual(resultado['espera_promedio'], 1.5)
        self.assertEqual(resultado['ocupacion']['b'], 60)

    def test_reentrada_al_mismo_recurso_respeta_cola(self):
        # A: etapa1 0-2; B: etapa1 2-4; A: etapa2 4-6; B: etapa2 6-8.
        m = Modelo({'r': 1}, {'p': [Etapa('a', 'r', 2), Etapa('b', 'r', 2)]},
                   [Llegada('p', 1)], 2)
        m.llegadas = [Llegada('p', 100), Llegada('p', 100)]
        m.duracion = 8
        resultado = simular(m)
        self.assertEqual(resultado['pacientes_atendidos'], 2)
        self.assertEqual(resultado['espera_promedio'], 3)
        self.assertEqual(resultado['ocupacion']['r'], 100)

    def test_fin_en_horizonte_cuenta_llegada_en_horizonte_no(self):
        m = Modelo({'r': 1}, {'p': [Etapa('a', 'r', 5)]}, [Llegada('p', 5)], 10)
        self.assertEqual(simular(m)['pacientes_atendidos'], 2)

    def test_sin_llegadas(self):
        m = Modelo({'r': 1}, {'p': [Etapa('a', 'r', 5)]}, [], 10)
        self.assertEqual(simular(m), {'pacientes_atendidos': 0, 'espera_promedio': 0,
                                     'ocupacion': {'r': 0}})

    def test_capacidad_casi_cero_rechazada(self):
        resultado = self.compilar('recurso m = 0.0000000001; simular durante 10 minutos;')
        self.assertEqual(resultado.returncode, 1)
        self.assertIn('número entero', resultado.stdout)
        self.assertNotIn('Traceback', resultado.stderr)

    def test_redondeo_decimal_valido(self):
        resultado = self.compilar('recurso m = 0.1 * 30; simular durante 10 minutos;', '--ir')
        self.assertEqual(resultado.returncode, 0)
        self.assertIn('RESOURCE m 3', resultado.stdout)

    def test_proceso_llamado_global(self):
        resultado = self.compilar("""recurso m = 1;
proceso global { etapa m usa m durante 1 minuto; }
generar pacientes cada 5 minutos hacia global;
simular durante 10 minutos;
mostrar pacientes_atendidos;""")
        self.assertEqual(resultado.returncode, 0, resultado.stdout + resultado.stderr)
        self.assertIn('pacientes_atendidos = 2', resultado.stdout)

    def test_numero_no_finito_rechazado(self):
        resultado = self.compilar('recurso m = ' + '9' * 400 + '; simular durante 1 hora;')
        self.assertEqual(resultado.returncode, 1)
        self.assertIn('finito', resultado.stdout)
        self.assertNotIn('Traceback', resultado.stderr)

    def test_ir_exacto_y_guardado(self):
        with tempfile.TemporaryDirectory() as carpeta:
            salida = Path(carpeta) / 'modelo.ir'
            resultado = self.compilar("""recurso medicos = 1;
proceso atencion { etapa consulta usa medicos durante 15 minutos; }
generar pacientes cada 5 minutos hacia atencion;
simular durante 1 hora;
mostrar pacientes_atendidos;
mostrar espera_promedio;
mostrar ocupacion(medicos);""", '--ir', '--guardar-ir', str(salida))
            esperado = (ROOT / 'ejemplos/atencion.ir').read_text(encoding='utf-8')
            self.assertEqual(resultado.returncode, 0)
            self.assertEqual(resultado.stdout, esperado)
            self.assertEqual(salida.read_text(encoding='utf-8'), esperado)

    def test_error_no_emite_ir(self):
        resultado = self.compilar('recurso m = 0; simular durante 10 minutos;', '--ir')
        self.assertEqual(resultado.returncode, 1)
        self.assertNotIn('RESOURCE', resultado.stdout)
