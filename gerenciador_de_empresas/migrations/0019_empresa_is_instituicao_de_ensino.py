# Generated by Django 3.0.4 on 2020-05-13 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gerenciador_de_empresas', '0018_remove_empresa_is_instituicao_de_ensino'),
    ]

    operations = [
        migrations.AddField(
            model_name='empresa',
            name='is_instituicao_de_ensino',
            field=models.BooleanField(default=0),
        ),
    ]
