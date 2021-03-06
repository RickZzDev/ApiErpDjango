# Generated by Django 3.0.4 on 2020-05-29 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gerenciador_de_empresas', '0087_auto_20200528_2022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contrato',
            name='numero_matricula',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='datapagamento',
            name='data_pagamento',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='proventos',
            name='data_fim',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='proventos',
            name='data_inicio',
            field=models.DateField(blank=True, null=True),
        ),
    ]
