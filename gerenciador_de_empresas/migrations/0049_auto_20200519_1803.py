# Generated by Django 3.0.4 on 2020-05-19 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gerenciador_de_empresas', '0048_tipocontrato_codigo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tipocontrato',
            name='codigo',
            field=models.CharField(max_length=85),
        ),
    ]
