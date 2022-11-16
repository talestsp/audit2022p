# dados de seções
URL_VOTACAO_SECAO = "https://cdn.tse.jus.br/estatistica/sead/odsele/votacao_secao/votacao_secao_2022_BR.zip"

# dados de seções com modelo de urna no Segundo Turno
# https://dadosabertos.tse.jus.br/dataset/resultados-2022-boletim-de-urna
URL_BU_PADRAO = "https://cdn.tse.jus.br/estatistica/sead/eleicoes/eleicoes2022/buweb/bweb_2t_{SIGLA_ESTADO}_311020221535.zip"

# dados modelo de urna
URL_MODELO_URNA = "https://cdn.tse.jus.br/estatistica/sead/odsele/modelo_urna/modelourna_numerointerno.zip"

# shapefile dos municipios
URL_SHP_MUNICIPIOS = "https://geoftp.ibge.gov.br/organizacao_do_territorio/malhas_territoriais/malhas_municipais/municipio_2021/Brasil/BR/BR_Municipios_2021.zip"


def get_url_votacao_secao():
    return URL_VOTACAO_SECAO

def get_url_votacao_secao_filename():
    return get_url_votacao_secao().split("/")[-1]

def get_url_bu_estado(sigla_estado):
    return URL_BU_PADRAO.replace("{SIGLA_ESTADO}", sigla_estado.upper())

def get_url_bu_estado_filename(sigla_estado):
    return get_url_bu_estado(sigla_estado).split("/")[-1]

def get_url_modelo_urna():
    return URL_MODELO_URNA

def get_url_modelo_urna_filename():
    return URL_MODELO_URNA.split("/")[-1]

def get_url_todos_os_estados(siglas):
    url_bu_estados = []
    for sigla in siglas:

        url_bu_estados.append(get_url_bu_estado(sigla))

    return url_bu_estados

def get_url_shapefile_municipios():
    return URL_SHP_MUNICIPIOS

def get_url_shapefile_municipios_filename():
    return get_url_shapefile_municipios().split("/")[-1]