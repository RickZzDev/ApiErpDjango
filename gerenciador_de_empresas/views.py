# -*- coding: utf-8 -*-
from rest_framework import viewsets
from .models import *
from .serializers import *
from .permissions import *
from django.http import HttpResponse
from rest_framework.response import Response
# from classificacao_tributaria.serializers import ClassTributSerializer
from .authentication import TokenAuth
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
import requests
import json
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.decorators import api_view, permission_classes
import os


class PermViewSet(viewsets.ViewSet):
    def list(self, request):
        token = request.headers['Token']
        decoded = jwt.decode(token, verify=False)  
        if 'cognito:groups' in decoded:
            if os.getenv("FOLHA_PROD"):
                if "FOLHA" in decoded['cognito:groups']:
                    return Response({"perms":['all']})
                else:
                    return Response({"perms":[]})
            else:
                if "FOLHA" or "FOLHA_DEV" in decoded['cognito:groups']:
                    return Response({"perms":['all']})
                else:
                    return Response({"perms":[]})    
        else:
            return Response({"perms":[]})
         
class EmpresaViewSet(viewsets.ModelViewSet):
    authentication_classes=(TokenAuth,)
    permission_classes = [PermClass]



    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer

class EmpresaApelidoViewSet(viewsets.ModelViewSet):
    authentication_classes=(TokenAuth,)
    permission_classes = [PermClass]

    queryset = Empresa.objects.all()
    serializer_class = EmpresaApelidoSerializer

class EmpresaByApelido(viewsets.ModelViewSet):
    authentication_classes=(TokenAuth,)
    permission_classes = [PermClass]

    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer

    def create(self,request):
        queryset = Empresa.objects.filter(apelido=request.data['apelido'])
        serialier_class = EmpresaSerializer(queryset,many=True)
        return Response(serialier_class.data)

class Natureza_juridicaViewSet(viewsets.ModelViewSet):
    authentication_classes=(TokenAuth,)
    permission_classes = [PermClass]
    

    queryset = Natureza_juridica.objects.all()
    serializer_class = Natureza_juridicaSerializer

class CodGpsViewSet(viewsets.ModelViewSet):
    permission_classes = [PermClass]
    authentication_classes=(TokenAuth,)

    queryset = CodGps.objects.all()  
    serializer_class = CodGpsSerializer

class ClassTributViewSet(viewsets.ModelViewSet):
    permission_classes = [PermClass]
    authentication_classes=(TokenAuth,)

    queryset = Classificacao_tributaria.objects.all()
    serializer_class = ClassTributSerializer

class CnaeViewSet(viewsets.ModelViewSet):
    permission_classes = [PermClass]
    authentication_classes=(TokenAuth,)

    queryset = Cnae.objects.all()
    serializer_class = CnaeSerializer

class EnderecoViewSet(viewsets.ModelViewSet):
    permission_classes = [PermClass]
    authentication_classes=(TokenAuth,)

    queryset = Endereco.objects.all()
    serializer_class = EnderecoSerializer

class CodMunicipioViewSet(viewsets.ModelViewSet):
    permission_classes = [PermClass]
    authentication_classes=(TokenAuth,)

    queryset = CodMunicipio.objects.all()
    serializer_class = CodMunicipioSerializer
    
class CodMunicipioUfViewSet(viewsets.ModelViewSet):
    permission_classes = [PermClass]
    authentication_classes=(TokenAuth,)

    queryset = CodMunicipio.objects.all()
    serializer_class = CodMunicipioSerializer
    def create(self,request):
        queryset = CodMunicipio.objects.filter(uf=request.data['id'])
        serializer_class = CodMunicipioSerializer(queryset, many=True)
        return Response(serializer_class.data)

class UfViewSet(viewsets.ModelViewSet):
    permission_classes = [PermClass]
    authentication_classes=(TokenAuth,)

    queryset = Uf.objects.all()
    serializer_class = UfSerializer

class SexoViewSet(viewsets.ModelViewSet):
    permission_classes = [PermClass]
    authentication_classes=(TokenAuth,)

    fields = ('label')
    queryset = Sexo.objects.all()
    serializer_class = SexoSerializer

class EstadoCivilViewSet(viewsets.ModelViewSet):
    permission_classes = [PermClass]
    authentication_classes=(TokenAuth,)

    queryset = EstadoCivil.objects.all()
    serializer_class = EstadoCivilSerializer

class TipoSanguineoViewSet(viewsets.ModelViewSet):
    permission_classes = [PermClass]
    authentication_classes=(TokenAuth,)

    queryset = TipoSanguineo.objects.all()
    serializer_class = TipoSanguineoSerializer
  
class OrgaoEmissorDocumentoViewSet(viewsets.ModelViewSet):
    permission_classes = [PermClass]
    authentication_classes=(TokenAuth,)

    queryset = OrgaoEmissorDocumento.objects.all()
    serializer_class = OrgaoEmissorSerializer

class TipoDocViewSet(viewsets.ModelViewSet):
    permission_classes = [PermClass]
    authentication_classes=(TokenAuth,)

    queryset = TipoDocumento.objects.all()
    serializer_class = TipoDocumentoSerializer                 

class DocumentoViewSet(viewsets.ModelViewSet):
    permission_classes = [PermClass]
    authentication_classes=(TokenAuth,)
    
    queryset = Documento.objects.all()
    serializer_class = DocumentoSerializer

class PessoaViewSet(viewsets.ModelViewSet):
    permission_classes = [PermClass]
    authentication_classes=(TokenAuth,)

    queryset = Pessoa.objects.all()
    serializer_class = PessoaSerializer

    
    def retrieve(self,request,pk = None):
        queryset = Pessoa.objects.all()
        pessoa = get_object_or_404(queryset, pk=pk)
        serializer_class = PessoaSerializer(pessoa)
        return Response(serializer_class.data)

class ContratoViewSet(viewsets.ModelViewSet):
    authentication_classes=(TokenAuth,)
    permission_classes = [PermClass]

    queryset = Contrato.objects.all()
    serializer_class = ContratoSerializer

class TipoContratoViewSet(viewsets.ModelViewSet):
    authentication_classes=(TokenAuth,)
    permission_classes = [PermClass]


    queryset = TipoContrato.objects.all()
    serializer_class = TipoContratoSerializer

class InstituicoesDeEnsinoViewSet(viewsets.ModelViewSet):

    authentication_classes=(TokenAuth,)
    permission_classes = [PermClass]

    queryset = Empresa.objects.all()
    serializer_class = EmpresaApelidoSerializer

    def list(self,request):
        queryset = Empresa.objects.filter(is_instituicao_de_ensino=1)
        serializer_class = EmpresaApelidoSerializer(queryset, many=True)
        return Response(serializer_class.data)

class SeguradoraViewSet(viewsets.ModelViewSet):
    authentication_classes=(TokenAuth,)
    permission_classes = [PermClass]

    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer

    def list(self,request):
        queryset = Empresa.objects.filter(cnae_principal__codigo = '6622-3/00')
        serializer_class2 = EmpresaSerializer(queryset,many=True)
        return Response(serializer_class2.data)

class ContratoPessoaViewSet(viewsets.ModelViewSet):
    authentication_classes=(TokenAuth,)
    permission_classes = [PermClass]

    queryset = Contrato.objects.all()
    serializer_class = ContratoSerializer

    def create(self, request, *args, **kwargs):
        queryset = Contrato.objects.filter(contratado = request.data['id'])
        serializer_class = ContratoSerializer(queryset,many=True)
        return Response(serializer_class.data)

class ApoliceViewSet(viewsets.ModelViewSet):
    authentication_classes=(TokenAuth,)
    permission_classes = [PermClass]

    queryset = ApoliceSeguro.objects.all()
    serializer_class = ApoliceSerializer

class PessoaNomeViewSet(viewsets.ModelViewSet):
    authentication_classes=(TokenAuth,)
    permission_classes = [PermClass]

    queryset = Pessoa.objects.all()
    serializer_class = PessoaNomeSerializer

class CargoViewSet(viewsets.ModelViewSet):

    authentication_classes=(TokenAuth,)
    permission_classes = [PermClass]

    queryset = Cargo.objects.all()
    serializer_class = CargoSerialier

class CboViewSet(viewsets.ModelViewSet):

    authentication_classes=(TokenAuth,)
    permission_classes = [PermClass]

    queryset = Cbo.objects.all()
    serializer_class = CboSerializer

class PeriodicidadeViewSet(viewsets.ModelViewSet):

    authentication_classes=(TokenAuth,)
    permission_classes = [PermClass]

    queryset = Periodicidade.objects.all()
    serializer_class = PeriodicidadeSerializer

class TiposProventosViewSet(viewsets.ModelViewSet):
    authentication_classes=(TokenAuth,)
    permission_classes = [PermClass]

    queryset = TipoProvento.objects.all()
    serializer_class = TipoProventoSerializer

class ProventosViewSet(viewsets.ModelViewSet):
    authentication_classes=(TokenAuth,)
    permission_classes = [PermClass]

    queryset = Proventos.objects.all()
    serializer_class = ProventoSerializer

class ContratoPessoaViewSet(viewsets.ModelViewSet):
    authentication_classes=(TokenAuth,)
    permission_classes = [PermClass]

    queryset = Contrato.objects.all()
    serializer_class = ContratoSerializer

    def create(self, request, *args, **kwargs):
        queryset = Contrato.objects.filter(contratante__apelido = request.data['apelido'])
        serializer_class = ContratoSerializer(queryset,many=True)
        return Response(serializer_class.data)

class FeriadosViewSet(viewsets.ModelViewSet):
    authentication_classes=(TokenAuth,)
    permission_classes = [PermClass]

    queryset = Calendario.objects.all()
    serializer_class = CalendarioSerializer

    def create(self, request, *args, **kwargs):
        queryset = Calendario.objects.filter(feriado__data__month = request.data['mes'])
        serializer_class = CalendarioSerializer(queryset,many=True)
        return Response(serializer_class.data)       