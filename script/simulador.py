import time
import json
from random import randrange
from websocket import create_connection

WS_CREAR = create_connection("ws://172.18.0.1:8000/crear/")
WS_ALERTA = create_connection("ws://172.18.0.1:8000/alerta/")
WS_REGISTRO = create_connection("ws://172.18.0.1:8000/registro/")

def crear_dispositivo():
    identificador = input("Ingrese identificador (4 digitos): ")
    umbral_minimo = int(input("Ingrese umbral minimo: "))
    umbral_maximo = int(input("Ingrese umbral maximo: "))

    datos = {
        'identificador': identificador[:4],
        'umbral_minimo': umbral_minimo,
        'umbral_maximo': umbral_maximo
    }

    WS_CREAR.send(json.dumps(datos))
    resultado = json.loads(WS_CREAR.recv())['creado']

    configurador = {
        'identificador': resultado['identificador'],
        'umbral_minimo': resultado['umbral_minimo'] - randrange(1, 5),
        'umbral_maximo': resultado['umbral_maximo'] + randrange(1, 5)
    }

    return configurador

conf = crear_dispositivo()

ID_DISPOSITIVO          = conf['identificador']
SEGUNDOS_HEART_BEAT     = 10
SEGUNDOS_TEMPERATURA    = 2.0
RANGO_MENOR_TEMP        = conf['umbral_minimo']
RANGO_MAYOR_TEMP        = conf['umbral_maximo']

def heart_beat():
    timestamp = int(time.time())

    datos = {
        'id_dispositivo': ID_DISPOSITIVO,
        'timestamp': timestamp,
        'opcion': 'live',
    }
    yield datos

def temperatura():
    timestamp = int(time.time())

    time.sleep(SEGUNDOS_TEMPERATURA)
    datos = {
        'id_dispositivo': ID_DISPOSITIVO,
        'temperatura': randrange(RANGO_MENOR_TEMP, RANGO_MAYOR_TEMP),
        'timestamp': timestamp,
    }
    yield datos

pasado = time.time()

# Colores terminal https://stackoverflow.com/a/54955094
VERDE   = '\033[32m'
AZUL    = '\033[34m'
ROJO    = '\033[31m'

while True:
    datos = next(temperatura())
    WS_REGISTRO.send(json.dumps(datos))
    respuesta = json.loads(WS_REGISTRO.recv())
    print(VERDE + f"Resultado de registro (Umbrales del dispositivo): {respuesta}")
    print(AZUL + f"Temperatura enviada {str(datos['temperatura']) + chr(176) + 'C'}")

    if datos['temperatura'] <= respuesta['umbral_minimo'] or datos['temperatura'] >= respuesta['umbral_maximo']:
        datos['opcion'] = 'umbral'
        WS_ALERTA.send(json.dumps(datos))
        print(ROJO + f"Alerta registrada Umbral: {WS_ALERTA.recv()}")

    if (time.time() - pasado) > SEGUNDOS_HEART_BEAT:
        beat = next(heart_beat())
        beat['temperatura'] = datos['temperatura']
        WS_ALERTA.send(json.dumps(beat))
        pasado = time.time()
        print(ROJO +f"Alerta registrada Beat: {WS_ALERTA.recv()}")