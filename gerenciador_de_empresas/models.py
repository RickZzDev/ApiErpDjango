# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from rest_framework import serializers


class CodGps(models.Model):
    codGps = models.CharField(max_length=5)
    especificacao = models.TextField()

    def __str__(self):
        return self.codGps

class Natureza_juridica(models.Model):
    nome_categoria = models.CharField(max_length=100)
    cod_subcategoria = models.CharField(max_length=5)
    nome_subcategoria = models.CharField( max_length=150)
    representante_entidade = models.CharField(max_length=150)
    qualificacao = models.CharField(max_length=25)

    def __str__(self):
        return self.nome_categoria

class Classificacao_tributaria(models.Model):
    codigo = models.CharField(max_length=50)
    descricao = models.TextField()

    def __str__(self):
        return self.descricao   
      
class Cnae(models.Model):
    codigo  = models.CharField(max_length=50)
    descricao = models.TextField(default='desc')

    def __str__(self):
        return self.codigo  

class Uf(models.Model):
    label = models.CharField(max_length=45)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.label        

class Endereco(models.Model):
    cep = models.CharField(max_length=15)
    logradouro = models.CharField(max_length=45)
    numero = models.CharField(max_length=15)
    complemento = models.CharField(max_length=45, null = True, blank=True)
    bairro = models.CharField(max_length=45)
    cidade = models.CharField(max_length=50)
    uf = models.ForeignKey(Uf,on_delete=models.SET_NULL,null=True)
    pais = models.CharField(max_length=45,null=True)

    def __str__(self):
        return self.cep

class Empresa(models.Model):
    endereco =  models.OneToOneField(Endereco,on_delete=models.CASCADE, null=True)
    apelido = models.CharField(max_length=150, unique=True)
    razao_social = models.CharField(max_length=50)
    nome_fantasia = models.CharField(max_length=50,null=True,blank=True)
    data_abertura = models.DateField(null=True, blank=True)
    telefone_ddd  = models.CharField(max_length=45)
    email = models.CharField(max_length=50)
    registro_empregrado = models.BooleanField()
    indicativo_desoneracao = models.BooleanField()
    cnae_principal = models.ForeignKey(Cnae, on_delete=models.CASCADE, null=True)
    optante_simples = models.BooleanField()
    classificacao_tributaria = models.ForeignKey(Classificacao_tributaria,on_delete=models.SET_NULL,null=True)
    naturezas_juridicas = models.ForeignKey(Natureza_juridica, on_delete=models.SET_NULL,null=True)
    cod_gps = models.ManyToManyField(CodGps,blank=True)
    cnpj = models.CharField(max_length=18,unique=True)
    is_instituicao_de_ensino = models.BooleanField(default=0)
    

    def __str__(self):
        return str(self.apelido)  

class DataPagamento(models.Model):
    data_pagamento = models.DateField(null=True)
    data_inicial_referencia = models.DateField()
    data_final_referencia = models.DateField()
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name="datas_pagamento", null=True)

    def __str__(self):
        return str(self.data_pagamento)

#OBJETOS RELACIONADOS A PESSOAS ////////////////////////////////////////////////////////////////////////
class CodMunicipio(models.Model):
    nome = models.CharField(max_length=50,unique=True)
    codigo = models.CharField(max_length=80,unique=True)
    uf = models.ForeignKey(Uf,on_delete=models.PROTECT)

    def __str__(self):
        return  self.nome        

class Sexo(models.Model):
    label = models.CharField(max_length=45)
    name = models.CharField(max_length=45)

    def __str__(self):
        return self.label

class EstadoCivil(models.Model):
    label = models.CharField(max_length=45)
    name = models.CharField(max_length=45)

    def __str__(self):
        return self.label

class TipoSanguineo(models.Model):
    sigla = models.CharField(max_length=45, blank=True)
    nome_completo = models.CharField(max_length=45, blank=True)

    def __str__(self):
        return self.sigla
                       
class OrgaoEmissorDocumento(models.Model):
    label = models.CharField(max_length=85)
    name = models.CharField(max_length=85)

    def __str__(self):
        return self.label

class Pessoa(models.Model):
    nome = models.CharField(max_length=85, unique=True)
    endereco = models.OneToOneField(Endereco,on_delete=models.SET_NULL,null=True, blank = True)
    tipo_sanguineo = models.ForeignKey(TipoSanguineo,on_delete=models.SET_NULL,null=True,blank=True)
    estado_civil = models.ForeignKey(EstadoCivil,on_delete=models.SET_NULL,null=True,blank=True)
    sexo = models.ForeignKey(Sexo, on_delete=models.SET_NULL,null=True)
    


    def __str__(self):
        return self.nome

###############ENTIDADES PARA DADOS CONTRATUAIS#####################
class TipoContrato(models.Model):
    codigo = models.CharField(max_length=85,null=True)
    name = models.CharField(max_length=85, null=True)
    label = models.CharField(max_length=85)

    def __str__(self):
        return self.label

class ApoliceSeguro(models.Model):
    numero = models.CharField(max_length=85,unique=True)
    data_emissao = models.DateField()
    data_validade = models.DateField()
    seguradora = models.ForeignKey(Empresa, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.numero

class Cbo(models.Model):
    codigoCbo = models.CharField(max_length=85)
    titulo_cbo = models.CharField(max_length=85)

    def __str__(self):
        return self.codigoCbo

class Cargo(models.Model):
    label = models.CharField(max_length=85)
    cbo = models.ForeignKey(Cbo, on_delete=models.PROTECT)

    def __str__(self):
        return self.label

class Periodicidade(models.Model):
    name = models.CharField(max_length=85, unique=True)
    label = models.CharField(unique=True,max_length=85)

    def __str__(self):
        return self.name

class TipoProvento(models.Model):
    name = models.CharField(max_length=85,unique=True)
    label = models.CharField(max_length=85, unique=True)
    incideImpostoDeRenda = models.BooleanField()
    isBaseInss = models.BooleanField()
    isBaseFgts = models.BooleanField()
    isBaseContribuicaoSindical = models.BooleanField()

    def __str__(self):
        return self.name

class Contrato(models.Model):
    tipo_contrato = models.ForeignKey(TipoContrato, on_delete=models.SET_NULL, null=True)
    salario = models.CharField(max_length=85)
    data_admissao = models.DateField()
    data_termino_contratual = models.DateField()
    data_termino_efetiva = models.DateField(null=True,blank=True)
    horas_semanais = models.IntegerField(null=True,blank=True)
    horas_mensais = models.IntegerField(null=True,blank=True)
    instituicao_de_ensino = models.ForeignKey(Empresa, on_delete=models.SET_NULL, null=True,blank=True)
    apolices_seguro = models.ForeignKey(ApoliceSeguro, on_delete=models.SET_NULL, null=True,blank=True)
    supervisor_estagio = models.ForeignKey(Pessoa,related_name="supervisor_estagio", on_delete=models.CASCADE,null=True,blank=True)
    contratado = models.ForeignKey(Pessoa,on_delete=models.CASCADE)
    contratante = models.ForeignKey(Empresa, related_name="contratante", on_delete=models.CASCADE)
    cargo = models.ForeignKey(Cargo, on_delete=models.PROTECT)
    numero_matricula = models.CharField(max_length=10,blank=True, null=True)

    def __str__(self):
        return self.salario

class Proventos(models.Model):
    valor = models.IntegerField()
    periodicidade = models.ForeignKey(Periodicidade, on_delete=models.PROTECT)
    data_inicio = models.DateField(null=True, blank=True)
    data_fim = models.DateField(null=True, blank=True)
    tipo_provento = models.ForeignKey(TipoProvento, on_delete=models.PROTECT)
    contrato = models.ForeignKey(Contrato,related_name="proventos" ,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return str(self.valor)        

class TipoDocumento(models.Model):
    label = models.CharField(max_length=85)
    name = models.CharField(max_length=85)

    def __str__(self):
        return self.name

class Documento(models.Model):
    pessoa = models.ForeignKey(Pessoa,related_name='documento' ,on_delete=models.CASCADE, null=True)
    serie = models.CharField(max_length=85,null = True)
    tipo_doc = models.ForeignKey(TipoDocumento,on_delete=models.CASCADE,null=True)
    numero = models.CharField(max_length=85,null=True)
    data_emissao = models.CharField(max_length=85,null=True)
    data_vencimento = models.CharField(max_length=85,null=True)
    orgao_emissor = models.ForeignKey(OrgaoEmissorDocumento,on_delete=models.SET_NULL,null=True, blank=True)    
    uf = models.ForeignKey(Uf, on_delete=models.SET_NULL,null=True, blank =True)

    def __str__(self):
        return self.numero



class Data(models.Model):
    data = models.DateField(auto_now=False, null=True)


    def __str__(self):
        return str(self.data)

class Calendario(models.Model):
    name = models.CharField(max_length=35)
    label = models.CharField(max_length=35)
    feriado = models.ForeignKey(Data, on_delete=models.CASCADE)

    def __str__(self):
        return self.name         



