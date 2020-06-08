# Generated by Django 3.0.4 on 2020-05-19 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gerenciador_de_empresas', '0037_contrato'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tipocontrato',
            name='name',
        ),
        migrations.AddField(
            model_name='tipocontrato',
            name='codigo',
            field=models.CharField(default=1, max_length=85, unique=True),
            preserve_default=False,
        ),
    ]