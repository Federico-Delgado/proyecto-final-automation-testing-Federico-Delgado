import csv
import json
import pathlib

def leer_csv_login(ruta_archivo):
    """Lee el CSV de login y devuelve tuplas para pytest.mark.parametrize"""
    datos = []
    ruta = pathlib.Path(ruta_archivo)
    with open(ruta, newline='', encoding='utf-8') as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            esperado = fila['esperado_exitoso'].lower() == 'true'
            datos.append((fila['usuario'], fila['clave'], esperado, fila['descripcion']))
    return datos

def leer_json_productos(ruta_archivo):
    """Lee el JSON de productos y devuelve tuplas (nombre, precio)"""
    ruta = pathlib.Path(ruta_archivo)
    with open(ruta, 'r', encoding='utf-8') as archivo:
        productos = json.load(archivo)
    return [(p['nombre'], p['precio']) for p in productos]