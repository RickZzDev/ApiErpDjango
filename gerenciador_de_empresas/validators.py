from rest_framework.validators import UniqueValidator,UniqueTogetherValidator
from .models import *
from rest_framework import serializers
from rest_framework.response import Response


def validateDataInicioFim(datas,dataInicio,dataFim):
        for data in datas:
            if data[dataInicio] < data[dataFim]:
                pass
            else:
                return serializers.ValidationError({"msg":"data final deve ser maior que a data inicial"})    

        return True

def validateDataColisao(datas,dataInicio,dataFim):
        #Pegar o ultimo indice do array
        novoInsertData = datas[-1]
        #Copia as datas para um novo array
        novoArray = [n for n in datas]
        #Deleta o ultimo indice desse array pois é o que vamos verificar
        del(novoArray[-1])
        #Quantos indices tem no array
        quantidadeDatas = len(novoArray)
        
        result = validateDataInicioFim(datas,dataInicio,dataFim)
        if result == True:
            for count in range(quantidadeDatas):
                if novoInsertData[dataInicio] < novoArray[count][dataInicio]:
                    if novoInsertData[dataFim] <= novoArray[count -1][dataInicio]:
                        pass
                    else:
                        return serializers.ValidationError({"msg":"Colisão de datas"})
                elif novoInsertData[dataInicio] >= novoArray[count][dataFim]:
                    pass
                else:
                    return serializers.ValidationError({"msg":"Colisão de datas"})
            return True              
        else:
            return serializers.ValidationError({"msg":"data final deve ser maior que a data inicial"})           

def confereNumeroMatricula(contratante,numero_matricula):
    numMatricula = Contrato.objects.filter(contratante__apelido = contratante, numero_matricula=numero_matricula)
    if len(numMatricula) == 0:
        return True
    else:
        return False

