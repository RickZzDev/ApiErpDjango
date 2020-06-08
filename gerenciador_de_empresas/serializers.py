from rest_framework import serializers
from django.shortcuts import render, get_object_or_404
from .models import *
from rest_framework.validators import UniqueValidator
from rest_framework.response import Response
from .validators import *
# from classificacao_tributaria.serializers import ClassTributSerializer

class ClassTributSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classificacao_tributaria
        fields = ['codigo','descricao']

class Natureza_juridicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Natureza_juridica
        fields = ['cod_subcategoria','nome_subcategoria']

class UfSerializer(serializers.ModelSerializer):

    class Meta:
        model = Uf
        fields = ['id','label']

class EnderecoSerializer(serializers.ModelSerializer):
    uf = UfSerializer(required = False, allow_null=True)

    class Meta:
        model = Endereco
        fields = '__all__'

    def create(self, validated_data):
        uf_data = validated_data.pop('uf')
        ufSelected = Uf.objects.get(label=uf_data['label'])
        endereco = Endereco.objects.create(uf = ufSelected,**validated_data)
        return endereco

    def update(self, instance, validated_data):
        uf_data = validated_data.pop('uf')

        instance.uf = Uf.objects.get(label = uf_data['label'])

        instance.cep = validated_data['cep']
        instance.logradouro = validated_data['logradouro']
        instance.bairro = validated_data['bairro']
        instance.numero = validated_data['numero']
        instance.complemento = validated_data['complemento']
        instance.cidade = validated_data['cidade']
        instance.pais = validated_data['pais']                                                  
        

        instance.save()    
        return instance
    
class CnaeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cnae
        fields = ['codigo','descricao']       

class CodGpsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodGps
        fields = ['codGps','especificacao']

class EmpresaSerializer2(serializers.ModelSerializer):
    endereco = EnderecoSerializer()
    cod_gps = CodGpsSerializer(many=True)
    cnae_principal = CnaeSerializer(required=False)
    naturezas_juridicas = Natureza_juridicaSerializer(required=False)
    classificacao_tributaria = ClassTributSerializer(required=False)

    class Meta:
        model = Empresa
        fields = '__all__'
        extra_kwargs={
            'apelido':{'validators':[]},
            'cnpj':{'validators':[]}
        }

class DataPagamentoSerializer(serializers.ModelSerializer):
    empresa = serializers.SlugRelatedField(queryset=Empresa.objects.all(),slug_field="apelido",required=False)
    id = serializers.IntegerField(required=False)

    class Meta:
        model = DataPagamento
        fields = '__all__'

class EmpresaSerializer(serializers.ModelSerializer):
    endereco = EnderecoSerializer()
    cod_gps = CodGpsSerializer(many=True)
    cnae_principal = CnaeSerializer(required=False)
    naturezas_juridicas = Natureza_juridicaSerializer(required=False)
    classificacao_tributaria = ClassTributSerializer(required=False)
    datas_pagamento = DataPagamentoSerializer(required=False,many=True)

    class Meta:
        model = Empresa
        fields = '__all__'

    def create(self, validated_data):
        classficacaoData = validated_data.pop('classificacao_tributaria')
        classifcacao_get = Classificacao_tributaria.objects.get(codigo = classficacaoData['codigo'])
        naturezaData = validated_data.pop('naturezas_juridicas')
        natureza_get = Natureza_juridica.objects.get(cod_subcategoria = naturezaData['cod_subcategoria'])
        cnaeData = validated_data.pop('cnae_principal')
        cnae_get = Cnae.objects.get(codigo = cnaeData['codigo'])
        endereco = validated_data.pop('endereco')
        uf_data = endereco.pop('uf')
        uf_get = Uf.objects.get(label = uf_data['label'])
        endereco_created = Endereco.objects.create(uf = uf_get,**endereco)
        

     
        dataPagamentoData = validated_data.pop('datas_pagamento')
        codGpsData = validated_data.pop('cod_gps')

        result = validateDataInicioFim(dataPagamentoData,'data_inicial_referencia','data_final_referencia')

        if result == True:
            pass
        else:
            raise serializers.ValidationError({"Mensagem de erro":result})


        empresa = Empresa.objects.create(endereco = endereco_created,classificacao_tributaria = classifcacao_get,
                                        cnae_principal = cnae_get,naturezas_juridicas = natureza_get,**validated_data )
        
        for data in dataPagamentoData:
            DataPagamento.objects.create(empresa = empresa,**data)

        for codGps in codGpsData:
            cod = CodGps.objects.get(codGps = codGps['codGps'])
            empresa.cod_gps.add(cod)
        return empresa 

    def update(self, instance, validated_data):

        cnaeData = validated_data.pop('cnae_principal')
        endereco_data = validated_data.pop('endereco')
        ufSelected = endereco_data.pop('uf')
        codGpsData = validated_data.pop('cod_gps')
        classificacaoData = validated_data.pop('classificacao_tributaria')
        naturezaData = validated_data.pop('naturezas_juridicas')
        dataPagamentoData = validated_data.pop('datas_pagamento')

        result = validateDataColisao(dataPagamentoData,'data_inicial_referencia','data_final_referencia')

        if result == True:
            pass
        else:
            raise serializers.ValidationError({"Mensagem de erro":result})

        
        instance.cnae_principal = Cnae.objects.get(codigo = cnaeData['codigo'])
        instance.naturezas_juridicas = Natureza_juridica.objects.get(cod_subcategoria=naturezaData['cod_subcategoria'])
        instance.classificacao_tributaria = Classificacao_tributaria.objects.get(codigo = classificacaoData['codigo'])
        ufInstance = Uf.objects.get(label = ufSelected['label'])

        for data in dataPagamentoData:
            if 'id' in data:
               DataPagamento.objects.filter(id=data['id']).update(**data)
               dataAtualizada = DataPagamento.objects.get(id=data['id'])
               instance.datas_pagamento.add(dataAtualizada)
            else:
                dataAtualizada = DataPagamento.objects.create(**data)
                instance.datas_pagamento.add(dataAtualizada)

        for codGps in codGpsData:
            cod = CodGps.objects.get(codGps = codGps['codGps'])
            instance.cod_gps.add(cod)
            
        Endereco.objects.filter(id=instance.endereco.id).update(logradouro=endereco_data["logradouro"],
                                                                cep = endereco_data["cep"],
                                                                numero = endereco_data["numero"],
                                                                complemento = endereco_data["complemento"],
                                                                bairro = endereco_data["bairro"],
                                                                cidade = endereco_data["cidade"],
                                                                pais = endereco_data["pais"],
                                                                uf = ufInstance)
        instance.apelido = validated_data['apelido']
        instance.razao_social = validated_data['razao_social']
        instance.nome_fantasia = validated_data['nome_fantasia']
        instance.telefone_ddd = validated_data['telefone_ddd']
        instance.email = validated_data['email']
        instance.registro_empregrado = validated_data['registro_empregrado']
        instance.indicativo_desoneracao = validated_data['indicativo_desoneracao']
        instance.optante_simples = validated_data['optante_simples']
        instance.cnpj = validated_data['cnpj']
        instance.is_instituicao_de_ensino = validated_data['is_instituicao_de_ensino']
        
        instance.save()
        return instance

class EmpresaApelidoSerializer(serializers.ModelSerializer):

    apelido = serializers.CharField(allow_blank=True, allow_null=True)

    class Meta:
        model = Empresa
        fields = ['apelido']
        extra_kwargs={
            'apelido':{'validators':[]},
            'cnpj':{'validators':[]}
        }

class CodMunicipioSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodMunicipio
        fields = '__all__'

class SexoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sexo
        fields = '__all__'  

class EstadoCivilSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoCivil
        fields = '__all__'  

class TipoSanguineoSerializer(serializers.ModelSerializer):

    class Meta:
        model = TipoSanguineo
        fields = '__all__'  
        
class OrgaoEmissorSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrgaoEmissorDocumento
        fields = '__all__'
     
class TipoDocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoDocumento
        fields = '__all__'

class DocumentoSerializer(serializers.ModelSerializer):
    uf = UfSerializer(required=False, allow_null=True)
    orgao_emissor = OrgaoEmissorSerializer(required = False,allow_null=True)

    class Meta:
        model = Documento
        fields = '__all__'

class PessoaSerializer(serializers.ModelSerializer):
    documento = DocumentoSerializer(many=True)
    endereco = EnderecoSerializer()
    sexo = SexoSerializer()
    tipo_sanguineo = TipoSanguineoSerializer(required=False,allow_null=True)
    estado_civil = EstadoCivilSerializer()

    class Meta:
        model = Pessoa
        fields = '__all__'

    def create(self,validated_data):
        documentos_data = validated_data.pop('documento')
        endereco_data = validated_data.pop('endereco')
        estado_civil_data = validated_data.pop('estado_civil')
        uf = endereco_data.pop('uf')
        sexo_data = validated_data.pop('sexo')
        ufSelected = Uf.objects.get(label=uf['label'])
        estadoSelected = EstadoCivil.objects.get(name = estado_civil_data['name'])
        sexoSelected  = Sexo.objects.get(label=sexo_data['label'])
        endereco_create = Endereco.objects.create(uf = ufSelected,**endereco_data)
        tipo_sanguineo_data = validated_data.pop('tipo_sanguineo')
        if tipo_sanguineo_data == None:
            pessoa = Pessoa.objects.create(endereco = endereco_create,estado_civil = estadoSelected ,sexo = sexoSelected, **validated_data)
        else:
            tipoSelected = TipoSanguineo.objects.get(nome_completo = tipo_sanguineo_data['nome_completo'])
            pessoa = Pessoa.objects.create(endereco = endereco_create,estado_civil = estadoSelected ,sexo = sexoSelected, tipo_sanguineo = tipoSelected, **validated_data)
        for documento_data in documentos_data:
            if 'orgao_emissor' in documento_data and  'uf' in documento_data:
                if documento_data['uf'] != None and documento_data['orgao_emissor'] != None:
                    orgao_emissor = documento_data.pop('orgao_emissor')
                    ufDoc = documento_data.pop('uf')
                    ufDocSelected = Uf.objects.get(label = ufDoc['label'])
                    orgao_selected = OrgaoEmissorDocumento.objects.get(label = orgao_emissor['label'])
                    Documento.objects.create(uf = ufDocSelected ,orgao_emissor = orgao_selected, pessoa = pessoa,**documento_data)
                elif documento_data['uf'] != None:
                    ufDoc = documento_data.pop('uf')
                    ufDocSelected = Uf.objects.get(label = ufDoc['label'])
                    Documento.objects.create(uf = ufDocSelected,pessoa = pessoa,**documento_data)
                elif documento_data['orgao_emissor'] != None:
                    orgao_emissor = documento_data.pop('orgao_emissor')
                    orgao_selected = OrgaoEmissorDocumento.objects.get(label = orgao_emissor['label'])
                    Documento.objects.create(orgao_emissor = orgao_selected,pessoa = pessoa,**documento_data)
                else:
                    Documento.objects.create(pessoa = pessoa,**documento_data)
            elif 'orgao_emissor' in documento_data or  'uf' in documento_data:
                if documento_data['uf'] != None:
                    ufDoc = documento_data.pop('uf')
                    ufDocSelected = Uf.objects.get(label = ufDoc['label'])
                    Documento.objects.create(uf = ufDocSelected,pessoa = pessoa,**documento_data)
                elif documento_data['orgao_emissor'] != None:
                    orgao_emissor = documento_data.pop('orgao_emissor')
                    orgao_selected = OrgaoEmissorDocumento.objects.get(label = orgao_emissor['label'])
                    Documento.objects.create(orgao_emissor = orgao_selected,pessoa = pessoa,**documento_data)
                else:
                    Documento.objects.create(pessoa = pessoa,**documento_data)
            else:
                Documento.objects.create(pessoa = pessoa,**documento_data)
        return pessoa

    def update(self, instance, validated_data):
        documentos_data = validated_data.pop('documento')
        endereco_data = validated_data.pop('endereco')
        sexo_data = validated_data.pop('sexo')
        tipo_sanguineo_data = validated_data.pop('tipo_sanguineo')
        estado_civil_data = validated_data.pop('estado_civil')

        instance.estado_civil = EstadoCivil.objects.get(name = estado_civil_data['name'])
        if tipo_sanguineo_data == None:
            pass
        else:
            instance.tipo_sanguineo = TipoSanguineo.objects.get(nome_completo = tipo_sanguineo_data['nome_completo'])
        instance.sexo = Sexo.objects.get(label=sexo_data['label'])
        instance.nome = validated_data['nome']

        ufSelected = endereco_data.pop('uf')
        ufInstance = Uf.objects.get(label = ufSelected['label'])

        Endereco.objects.filter(id=instance.endereco.id).update(logradouro=endereco_data["logradouro"],
                                                                 cep = endereco_data["cep"],
                                                                 numero = endereco_data["numero"],
                                                                 complemento = endereco_data["complemento"],
                                                                 bairro = endereco_data["bairro"],
                                                                 cidade = endereco_data["cidade"],
                                                                 pais = endereco_data["pais"],
                                                                 uf = ufInstance)                                                  
        for documento in documentos_data:
            if 'uf' in documento and 'orgao_emissor' in documento:
                if documento['uf'] != None and documento['orgao_emissor'] != None:
                    ufDoc = documento.pop('uf')
                    ufDocSelected = Uf.objects.get(label = ufDoc['label'])
                    documento['uf'] = ufDocSelected

                    orgao_emissor = documento.pop('orgao_emissor')
                    orgao_selected = OrgaoEmissorDocumento.objects.get(label = orgao_emissor['label'])
                    documento['orgao_emissor'] = orgao_selected

                    documento, created = Documento.objects.filter(pessoa=instance.id).update_or_create(tipo_doc = documento["tipo_doc"],
                                                                            defaults = documento)
                    instance.documento.add(documento)
                elif documento['uf'] != None:
                    ufDoc = documento.pop('uf')
                    ufDocSelected = Uf.objects.get(label = ufDoc['label'])
                    documento['uf'] = ufDocSelected

                    documento, created = Documento.objects.filter(pessoa=instance.id).update_or_create(tipo_doc = documento["tipo_doc"],
                                                                            defaults = documento)
                    instance.documento.add(documento)
                elif documento['orgao_emissor'] != None:
                    orgao_emissor = documento.pop('orgao_emissor')
                    orgao_selected = OrgaoEmissorDocumento.objects.get(label = orgao_emissor['label'])
                    documento['orgao_emissor'] = orgao_selected

                    documento, created = Documento.objects.filter(pessoa=instance.id).update_or_create(tipo_doc = documento["tipo_doc"],
                                                                            defaults = documento)
                    instance.documento.add(documento)
                else:
                    documento, created = Documento.objects.filter(pessoa=instance.id).update_or_create(tipo_doc = documento["tipo_doc"],
                                                                            defaults = documento)
                    instance.documento.add(documento)
            elif 'orgao_emissor' in documento or  'uf' in documento:
                if documento['uf'] != None:            
                    ufDoc = documento.pop('uf')
                    ufDocSelected = Uf.objects.get(label = ufDoc['label'])
                    documento['uf'] = ufDocSelected

                    documento, created = Documento.objects.filter(pessoa=instance.id).update_or_create(tipo_doc = documento["tipo_doc"],
                                                                            defaults = documento)
                    instance.documento.add(documento)
                elif documento['orgao_emissor'] != None:
                    orgao_emissor = documento.pop('orgao_emissor')
                    orgao_selected = OrgaoEmissorDocumento.objects.get(label = orgao_emissor['label'])
                    documento['orgao_emissor'] = orgao_selected

                    documento, created = Documento.objects.filter(pessoa=instance.id).update_or_create(tipo_doc = documento["tipo_doc"],
                                                                            defaults = documento)
                    instance.documento.add(documento)
                else:
                    documento, created = Documento.objects.filter(pessoa=instance.id).update_or_create(tipo_doc = documento["tipo_doc"],
                                                                            defaults = documento)
                    instance.documento.add(documento)
            else:
                documento, created = Documento.objects.filter(pessoa=instance.id).update_or_create(tipo_doc = documento["tipo_doc"],
                                                                            defaults = documento)
                instance.documento.add(documento)          
            instance.save()    
        return instance

class TipoContratoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoContrato
        fields = '__all__'

class ApoliceSerializer(serializers.ModelSerializer):
    numero = serializers.CharField(allow_blank=True, allow_null=True)
    seguradora = serializers.SlugRelatedField(queryset=Empresa.objects.all(), slug_field='apelido')
    data_emissao = serializers.DateField(required=False,allow_null=True)
    data_validade = serializers.DateField(required=False,allow_null=True)


    class Meta:
        model = ApoliceSeguro
        fields = '__all__'

class PessoaNomeSerializer(serializers.ModelSerializer):
    #Permitindo exlusivamente que seja null nesse serializer
    nome = serializers.CharField(allow_blank=True, allow_null=True)

    class Meta:
        model = Pessoa
        fields  = ['nome']

class CboSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cbo
        fields = ['titulo_cbo','codigoCbo']

class CargoSerialier(serializers.ModelSerializer):
    #Usando or SlugRelated podemos trazer um campo com campo da model em questão ao inves da chave primaria
    #E usar o mesmo para fazer o post no banco 
    cbo = serializers.SlugRelatedField(queryset=Cbo.objects.all(),slug_field='titulo_cbo')

    class Meta:
        model = Cargo
        fields = '__all__'

class ProventoSerializer(serializers.ModelSerializer):
    periodicidade = serializers.SlugRelatedField(queryset=Periodicidade.objects.all(),slug_field='label')
    tipo_provento = serializers.SlugRelatedField(queryset=TipoProvento.objects.all(), slug_field='label')
    id = serializers.IntegerField(required=False)

    class Meta:
        model = Proventos
        fields = '__all__'

class ContratoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contrato
        fields = '__all__'

    tipo_contrato = serializers.SlugRelatedField(queryset=TipoContrato.objects.all(),slug_field='label')
    apolices_seguro = serializers.SlugRelatedField(queryset=ApoliceSeguro.objects.all(),slug_field='numero', allow_null=True)
    instituicao_de_ensino = serializers.SlugRelatedField(queryset=Empresa.objects.all(), slug_field='apelido' ,allow_null=True)
    supervisor_estagio = serializers.SlugRelatedField(queryset=Pessoa.objects.all(), slug_field='nome' ,allow_null=True)
    contratado = serializers.SlugRelatedField(queryset=Pessoa.objects.all(),slug_field='nome')
    contratante = serializers.SlugRelatedField(queryset=Empresa.objects.all(), slug_field='apelido')
    cargo = serializers.SlugRelatedField(queryset=Cargo.objects.all(),slug_field='label')
    proventos = ProventoSerializer(required = False, many=True, allow_null=True)

    def create(self,validated_data):
      

        if confereNumeroMatricula(validated_data['contratante'],validated_data['numero_matricula']) == True:
            pass
        else:
            raise serializers.ValidationError({"msg": "Este numero de matricula ja esta cadastrado"})
        
        
        proventoData = validated_data.pop('proventos')
        contrato = Contrato.objects.create(**validated_data)

        if proventoData == []:
            pass
        elif proventoData[0]['data_inicio'] != None and proventoData[0]['data_fim'] != None:
            print("AAAAAAAAAAAAAAAAa")
            result = validateDataInicioFim(proventoData,'data_inicio','data_fim')

            if result == True:
                for provento in proventoData:
                    Proventos.objects.create(contrato = contrato,**provento)
            else:
                raise serializers.ValidationError({"msg":result})
        else:
            pass    


   

        return contrato

    def update(self,instance,validated_data):
        # if confereNumeroMatricula(validated_data['contratante'],validated_data['numero_matricula']) == True:
        #     pass
        # else:
        #     raise serializers.ValidationError({"msg": "Este numero de matricula ja esta cadastrado"})
        
        proventoData = validated_data.pop('proventos')
        if proventoData == []:
            pass
        elif proventoData[0]['data_inicio'] != None and proventoData[0]['data_fim'] != None:
            result = validateDataInicioFim(proventoData,'data_inicio','data_fim')

            if result == True:
                pass
            else:
                raise serializers.ValidationError({"msg":result})
        else:
            pass    
        
        for provento in proventoData:
            if 'id' in provento:
                Proventos.objects.filter(id=provento['id']).update(**provento)
                proventoAtualizado = Proventos.objects.get(id=provento['id'])
                instance.proventos.add(proventoAtualizado)
            else:
                proventoNovo = Proventos.objects.create(**provento)
                instance.proventos.add(proventoNovo)    

        instance.tipo_contrato = TipoContrato.objects.get(label = validated_data['tipo_contrato']) 
        
        if validated_data['apolices_seguro'] != None:
            instance.apolices_seguro = ApoliceSeguro.objects.get(numero = validated_data['apolices_seguro']) 
        if  validated_data['instituicao_de_ensino'] != None:   
            instance.instituicao_de_ensino =Empresa.objects.get(apelido = validated_data['instituicao_de_ensino']) 
        if  validated_data['supervisor_estagio'] != None:   
            instance.supervisor_estagio =Pessoa.objects.get(nome = validated_data['supervisor_estagio']) 
        instance.contratado = Pessoa.objects.get(nome = validated_data['contratado']) 
        instance.contratante = Empresa.objects.get(apelido = validated_data['contratante']) 
        instance.cargo = validated_data['cargo']
        instance.salario = validated_data['salario']
        instance.data_admissao = validated_data['data_admissao']
        instance.data_termino_contratual = validated_data['data_termino_contratual']
        instance.data_termino_efetiva = validated_data['data_termino_efetiva']
        instance.horas_semanais = validated_data['horas_semanais']
        instance.horas_mensais = validated_data['horas_mensais']
        instance.numero_matricula = validated_data['numero_matricula']
        instance.save()
        return instance

class PeriodicidadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Periodicidade
        fields = ['label']

class TipoProventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoProvento
        fields = ['label']

class CalendarioSerializer(serializers.ModelSerializer):

    feriado = serializers.SlugRelatedField(queryset=Data.objects.all(),slug_field="data")
    class Meta:
        model = Calendario
        fields = '__all__'




