
from rest_framework.permissions import AllowAny
from django.conf.urls import url
from django.contrib import admin
from django.urls import include,path
from rest_framework import routers
from  gerenciador_de_empresas.views  import *
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view
from gerenciador_de_empresas.authentication import *
from rest_framework_swagger.views import get_swagger_view
# from classificacao_tributaria.views import ClassTributViewSet
# from tblcooperativa.views import CooperativaViewSet

router = routers.DefaultRouter()
router.register('empresas/apelidos', EmpresaApelidoViewSet)
router.register('empresas/seguradoras',SeguradoraViewSet)
router.register('empresas/search/apelido',EmpresaByApelido)
router.register('empresas/instituicoes_de_ensino',InstituicoesDeEnsinoViewSet)
router.register('empresas', EmpresaViewSet)
router.register('naturezas_juridicas', Natureza_juridicaViewSet )
router.register('classificacoes_tributarias', ClassTributViewSet)
router.register('codigos_gps', CodGpsViewSet)
router.register('cnaes', CnaeViewSet)
router.register('enderecos', EnderecoViewSet)
router.register('cod_municipios', CodMunicipioViewSet)
router.register('ufs/cod_municipio', CodMunicipioUfViewSet)
router.register('sexos', SexoViewSet)
router.register('estados_civis',EstadoCivilViewSet)
router.register('tipos_sanguineos',TipoSanguineoViewSet)
router.register('tipos_docs',TipoDocViewSet)
router.register('orgaos_emissores_documentos',OrgaoEmissorDocumentoViewSet)
router.register('pessoas/nome', PessoaNomeViewSet)
router.register('pessoas',PessoaViewSet)
router.register('ufs',UfViewSet)
router.register('documentos', DocumentoViewSet)
router.register('permissoes', PermViewSet, basename='PermViewSet')
router.register('contratos/pessoa',ContratoPessoaViewSet)
router.register('contratos/tipos_contratos',TipoContratoViewSet)
router.register('contratos/cbos', CboViewSet)
router.register('contratos/proventos/periodicidades',PeriodicidadeViewSet)
router.register('contratos/proventos/tipos_proventos',TiposProventosViewSet)
router.register('contratos/proventos',ProventosViewSet)
router.register('contratos/pessoas',ContratoPessoaViewSet)
router.register('cargos', CargoViewSet)
router.register('contratos',ContratoViewSet)
router.register('apolices',ApoliceViewSet)
router.register('feriados',FeriadosViewSet)

schema_view = get_swagger_view(title='Folha API')


urlpatterns = [
    path('api/',include(router.urls)),
    path('api/admin/', admin.site.urls),
    path('api/docs',schema_view )

]
