from django.db import models
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

# Create your models here.

######################### Modelo comun para evitar la repeticion de campos

class Comun(models.Model):
    temperatura = models.PositiveSmallIntegerField()
    timestamp   = models.CharField(max_length=12)

    class Meta:
        abstract = True

######################### Modelo del dispositivo

class Dispositivo(models.Model):
    identificador = models.CharField(max_length=4)
    umbral_minimo = models.PositiveSmallIntegerField()
    umbral_maximo = models.PositiveSmallIntegerField()

    def __str__(self):
        return f"Identificador: {self.identificador} Min: {self.umbral_minimo} - Max: {self.umbral_maximo}"

######################### Modelo registro de cada evento del dispositivo

class Registro(Comun):
    dispositivo = models.ForeignKey(Dispositivo, related_name='registros', on_delete=models.CASCADE)

    def __str__(self):
        return f"Registro del dispositivo: {self.dispositivo.id}"

@receiver(models.signals.post_save, sender=Registro)
def nuevo_registro(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "registro", {
                "type": "nuevo.registro",
                "minimo": instance.dispositivo.umbral_minimo,
                "maximo": instance.dispositivo.umbral_maximo,
            }
        )

######################### Alerta por umbral de temperatura

class Alerta(Comun):
    UMBRAL      = 'umbral'
    KEEP_LIVE   = 'live'
    OPCIONES = [
        (UMBRAL, 'Umbral'),
        (KEEP_LIVE, 'live')
    ]
    opcion = models.CharField(max_length=6, choices=OPCIONES, default=UMBRAL)

    dispositivo = models.ForeignKey(Dispositivo, related_name='alertas', on_delete=models.CASCADE)

    def __str__(self):
        return f"Alerta del dispositivo: {self.dispositivo.id} - TS: {self.timestamp}"