# Generated by Django 3.0.4 on 2020-05-28 15:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gerenciador_de_empresas', '0081_calendario_data_mes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='data',
            name='mes',
        ),
        migrations.AddField(
            model_name='mes',
            name='feriados',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='gerenciador_de_empresas.Data'),
        ),
    ]
