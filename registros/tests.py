import pytest
from django.test import TestCase
from channels.testing import WebsocketCommunicator

from registros.models import Dispositivo, Registro, Alerta
from registros.consumers import CrearConsumer, RegistroConsumer, AlertaConsumer
from config.asgi import application

# Create your tests here.
class DispositivoTest(TestCase):

    def test_dispositivo_crearcion(self):
        dispositivo = Dispositivo.objects.create(
            identificador='743A',
            umbral_minimo=30,
            umbral_maximo=50
        )

        self.assertTrue(isinstance(dispositivo, Dispositivo))
        self.assertEqual(dispositivo.__str__(), f"Identificador: {dispositivo.identificador} Min: {dispositivo.umbral_minimo} - Max: {dispositivo.umbral_maximo}")

class RegistroTest(TestCase):

    def test_registro_crearcion(self):
        dispositivo = Dispositivo.objects.create(
            identificador='743A',
            umbral_minimo=30,
            umbral_maximo=50
        )

        registro = Registro.objects.create(
            dispositivo=dispositivo,
            temperatura=35,
            timestamp=1610814541
        )

        self.assertTrue(isinstance(registro, Registro))
        self.assertEqual(registro.__str__(), f"Registro del dispositivo: {registro.dispositivo.id}")

class AlertaTest(TestCase):

    def test_alerta_crearcion(self):
        dispositivo = Dispositivo.objects.create(
            identificador='743A',
            umbral_minimo=30,
            umbral_maximo=50
        )

        alerta = Alerta.objects.create(
            dispositivo=dispositivo,
            temperatura=66,
            timestamp=1610814541,
            opcion='umbral'
        )

        self.assertTrue(isinstance(alerta, Alerta))
        self.assertEqual(alerta.__str__(), f"Alerta del dispositivo: {alerta.dispositivo.id} - TS: {alerta.timestamp}")

@pytest.mark.asyncio
async def test_crear_consumer():
    communicator = WebsocketCommunicator(application, '/crear/')
    connected, subprotocol = await communicator.connect()
    assert connected
    await communicator.disconnect()

@pytest.mark.asyncio
async def test_registro_consumer():
    communicator = WebsocketCommunicator(application, '/registro/')
    connected, subprotocol = await communicator.connect()
    assert connected
    await communicator.disconnect()

@pytest.mark.asyncio
async def test_alerta_consumer():
    communicator = WebsocketCommunicator(application, '/alerta/')
    connected, subprotocol = await communicator.connect()
    assert connected
    await communicator.disconnect()