# Generated by Django 3.0.4 on 2020-05-20 16:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gerenciador_de_empresas', '0079_auto_20200520_1615'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contrato',
            name='proventos',
        ),
        migrations.AddField(
            model_name='proventos',
            name='contrato',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='proventos', to='gerenciador_de_empresas.Contrato'),
        ),
    ]
