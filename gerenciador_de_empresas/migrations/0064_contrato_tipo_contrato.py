# Generated by Django 3.0.4 on 2020-05-19 20:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gerenciador_de_empresas', '0063_tipocontrato_codigo'),
    ]

    operations = [
        migrations.AddField(
            model_name='contrato',
            name='tipo_contrato',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='gerenciador_de_empresas.TipoContrato'),
        ),
    ]
