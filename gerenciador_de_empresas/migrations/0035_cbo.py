# Generated by Django 3.0.4 on 2020-05-13 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gerenciador_de_empresas', '0034_apoliceseguro'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cbo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigoCbo', models.CharField(max_length=85)),
                ('titulo_cbo', models.CharField(max_length=85)),
            ],
        ),
    ]
