# Generated by Django 3.0.4 on 2020-05-19 18:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gerenciador_de_empresas', '0044_auto_20200519_1629'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tipocontrato',
            name='codigo',
        ),
    ]