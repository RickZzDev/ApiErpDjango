# Generated by Django 3.0.4 on 2020-05-28 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gerenciador_de_empresas', '0084_auto_20200528_1509'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ano',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=35)),
                ('label', models.CharField(max_length=35)),
            ],
        ),
        migrations.DeleteModel(
            name='Calendario',
        ),
    ]
