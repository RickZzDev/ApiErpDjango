# Generated by Django 3.0.4 on 2020-05-19 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gerenciador_de_empresas', '0056_remove_tipocontrato_codigo'),
    ]

    operations = [
        migrations.AddField(
            model_name='tipocontrato',
            name='codigo',
            field=models.CharField(max_length=85, null=True),
        ),
    ]
