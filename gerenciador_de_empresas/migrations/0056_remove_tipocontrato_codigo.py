# Generated by Django 3.0.4 on 2020-05-19 18:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gerenciador_de_empresas', '0055_tipocontrato_codigo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tipocontrato',
            name='codigo',
        ),
    ]
