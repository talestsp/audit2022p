import pandas as pd
import os
import gc
from src.utils import dflib

DFV_DTYPE = {"DT_ELEICAO": str, "SG_UF": str, "NR_ZONA": str, "NR_SECAO":str, "NR_LOCAL_VOTACAO": str,
             "NM_LOCAL_VOTACAO": str, "NM_MUNICIPIO": str, "NR_VOTAVEL": str, "modelo_urna": str,
             "NR_FAIXA_INICIAL": int, "NR_FAIXA_INICIAL.1": int}


def load_df_votacao(turno, estado="Brasil", usecols="*"):
    ################################
    # link pros dados
    # https://cdn.tse.jus.br/estatistica/sead/odsele/votacao_secao/votacao_secao_2022_BR.zip

    FILEPATH = "data/votacao_secao_2022_BR/votacao_secao_2022_BR.csv"
    ESTADO_FILEPATH = f"data/votacao_secao_2022_BR/votacao_secao_2022_{estado}.csv"

    dfv = load_tse_data(FILEPATH, ESTADO_FILEPATH, estado=estado, usecols=usecols)

    if turno == 1:
        dfv = dfv[dfv["DT_ELEICAO"] == "02/10/2022"]
    elif turno == 2:
        dfv = dfv[dfv["DT_ELEICAO"] == "30/10/2022"]

    return dfv

def load_df_votacao_boletim_urna_presidente(turno, estado="Brasil", usecols="*"):
    ################################
    # link pros dados
    # https://dadosabertos.tse.jus.br/dataset/resultados-2022-boletim-de-urna

    FILEPATH = "data/bus/presidente.csv"
    ESTADO_FILEPATH = f"data/bus/processados_estado/presidente_{estado}.csv"

    dfbu = load_tse_data(FILEPATH, ESTADO_FILEPATH, estado=estado, usecols=usecols)

    if turno == 1:
        dfbu = dfbu[dfbu["NR_TURNO"] == 1]
    elif turno == 2:
        dfbu = dfbu[dfbu["NR_TURNO"] == 2]

    return dfbu

def load_tse_data(filepath, estado_filepath, estado, usecols):

    if os.path.exists(estado_filepath):
        print(f"{estado} já processado, carregando")
        df = pd.read_csv(estado_filepath, encoding='latin1',
                           sep=";", dtype=DFV_DTYPE)
    else:
        print(f"{estado} não processado ainda, processando")
        df = pd.read_csv(filepath,
                           encoding='latin1', sep=";", dtype=DFV_DTYPE)

        if estado != "Brasil":
            df = df[df["SG_UF"] == estado]

        df["NM_MUNICIPIO"] = dflib.remove_acento_list(df["NM_MUNICIPIO"].str.upper())

        df.to_csv(estado_filepath,
                    encoding='latin1', sep=";")

    if usecols != "*":
        df = df[usecols]

    gc.collect()
    return df

def load_df_modelos_urna():
    ################################
    # link pros dados
    # https://cdn.tse.jus.br/estatistica/sead/odsele/modelo_urna/modelourna_numerointerno.zip
    dfu = pd.read_csv("data/modelourna_numerointerno/modelourna_numerointerno.csv",
                      sep=";", encoding='latin1', dtype=DFV_DTYPE)

    dfu["DS_MODELO_URNA"] = dfu["DS_MODELO_URNA"].astype(str).astype(int)
    dfu = dfu.set_index("DS_MODELO_URNA")

    for num_cols in ["NR_FAIXA_INICIAL", "NR_FAIXA_INICIAL.1"]:
        dfu[num_cols] = dfu[num_cols].fillna(0).astype(int)

    print("shape", dfu.shape)

    return dfu