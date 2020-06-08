# Generated by Django 3.0.4 on 2020-05-13 16:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gerenciador_de_empresas', '0021_empresa_is_instituicao_de_ensino'),
    ]

    operations = [
        migrations.AddField(
            model_name='contrato',
            name='cargo',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='gerenciador_de_empresas.Cargo'),
            preserve_default=False,
        ),
    ]
