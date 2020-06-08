# Generated by Django 3.0.4 on 2020-05-19 20:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gerenciador_de_empresas', '0070_datapagamento'),
    ]

    operations = [
        migrations.CreateModel(
            name='Periodicidade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=85, unique=True)),
                ('label', models.CharField(max_length=85, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='TipoProvento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=85, unique=True)),
                ('label', models.CharField(max_length=85, unique=True)),
                ('incideImpostoDeRenda', models.BooleanField()),
                ('isBaseInss', models.BooleanField()),
                ('isBaseContribuicaoSindical', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Proventos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.IntegerField()),
                ('data_inicio', models.DateField()),
                ('data_fim', models.DateField()),
                ('periodicidade', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gerenciador_de_empresas.Periodicidade')),
                ('tipo_provento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gerenciador_de_empresas.TipoProvento')),
            ],
        ),
    ]
