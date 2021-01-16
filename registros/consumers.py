import asyncio
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer

from channels.db import database_sync_to_async
from django.forms.models import model_to_dict

from registros.models import Dispositivo, Registro, Alerta

class CrearConsumer(AsyncJsonWebsocketConsumer):

    async def receive_json(self, content, **kwargs):
        resultado = await self.crear_dispositivo(content['identificador'], content['umbral_minimo'], content['umbral_maximo'])
        
        if resultado:
            await self.send_json({'creado': model_to_dict(resultado)})

    @database_sync_to_async
    def crear_dispositivo(self, identificador, umbral_minimo, umbral_maximo):
        return Dispositivo.objects.create(
            identificador=identificador,
            umbral_minimo=umbral_minimo,
            umbral_maximo=umbral_maximo
        )

class RegistroConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        await self.channel_layer.group_add("registro", self.channel_name)
        await self.accept()
    
    async def disconnect(self, code):
        await self.channel_layer.group_discard("registro", self.channel_name)

    async def receive_json(self, content, **kwargs):
        dispositivo = await self.obtener_dispositivo(content['id_dispositivo'])

        await self.registrar_temperatura(dispositivo, content['temperatura'], content['timestamp'])

    @database_sync_to_async
    def obtener_dispositivo(self, identificador):
        return Dispositivo.objects.get(identificador=identificador)

    @database_sync_to_async
    def registrar_temperatura(self, dispositivo, temperatura, timestamp):
        Registro.objects.create(
            dispositivo=dispositivo,
            temperatura=temperatura,
            timestamp=timestamp
        )

    async def nuevo_registro(self, notificacion):
        await self.send_json({
            'umbral_minimo': notificacion['minimo'],
            'umbral_maximo': notificacion['maximo'],
        })

class AlertaConsumer(AsyncJsonWebsocketConsumer):

    async def receive_json(self, content, **kwargs):
        dispositivo = await self.obtener_dispositivo(content['id_dispositivo'])

        alerta = await self.registrar_alerta(dispositivo, content['temperatura'], content['timestamp'], content['opcion'])

        await self.send_json(model_to_dict(alerta))

    @database_sync_to_async
    def obtener_dispositivo(self, identificador):
        return Dispositivo.objects.get(identificador=identificador)

    @database_sync_to_async
    def registrar_alerta(self, dispositivo, temperatura, timestamp, opcion):
        return Alerta.objects.create(
            dispositivo=dispositivo,
            temperatura=temperatura,
            timestamp=timestamp,
            opcion=opcion
        )