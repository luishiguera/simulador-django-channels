# Generated by Django 3.1.5 on 2021-01-16 13:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dispositivo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identificador', models.CharField(max_length=4)),
                ('umbral_minimo', models.PositiveSmallIntegerField()),
                ('umbral_maximo', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Registro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temperatura', models.PositiveSmallIntegerField()),
                ('timestamp', models.CharField(max_length=12)),
                ('dispositivo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registros', to='registros.dispositivo')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Alerta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temperatura', models.PositiveSmallIntegerField()),
                ('timestamp', models.CharField(max_length=12)),
                ('opcion', models.CharField(choices=[('umbral', 'Umbral'), ('live', 'live')], default='umbral', max_length=6)),
                ('dispositivo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='alertas', to='registros.dispositivo')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]