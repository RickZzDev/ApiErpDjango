# Generated by Django 3.0.4 on 2020-05-13 18:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gerenciador_de_empresas', '0024_remove_contrato_cargo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cbo',
            old_name='codigoCbo',
            new_name='codigo_cbo',
        ),
        migrations.RenameField(
            model_name='cbo',
            old_name='tituloCbo',
            new_name='titulo_cbo',
        ),
    ]