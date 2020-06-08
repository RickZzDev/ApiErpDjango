# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import *
from django.contrib import admin

# Register your models here.
admin.site.register(Empresa)
admin.site.register(Endereco)
admin.site.register(Documento)
admin.site.register(Sexo)
admin.site.register(Uf)
admin.site.register(CodMunicipio)
admin.site.register(EstadoCivil)
admin.site.register(TipoSanguineo)
admin.site.register(OrgaoEmissorDocumento)
admin.site.register(TipoDocumento)
admin.site.register(Pessoa)
admin.site.register(Natureza_juridica)
admin.site.register(CodGps)
admin.site.register(Classificacao_tributaria)
admin.site.register(Cnae)
admin.site.register(Cbo)
admin.site.register(Cargo)
admin.site.register(Contrato)
admin.site.register(TipoContrato)
admin.site.register(ApoliceSeguro)
admin.site.register(Proventos)
admin.site.register(Periodicidade)
admin.site.register(TipoProvento)
admin.site.register(DataPagamento)