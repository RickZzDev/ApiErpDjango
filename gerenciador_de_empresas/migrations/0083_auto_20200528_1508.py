# Generated by Django 3.0.4 on 2020-05-28 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gerenciador_de_empresas', '0082_auto_20200528_1507'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='data',
            field=models.DateField(),
        ),
    ]
