# Generated by Django 3.0.4 on 2020-05-19 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gerenciador_de_empresas', '0072_empresa_datas_pagamento'),
    ]

    operations = [
        migrations.AddField(
            model_name='empresa',
            name='numero_matricula',
            field=models.FloatField(blank=True, null=True),
        ),
    ]