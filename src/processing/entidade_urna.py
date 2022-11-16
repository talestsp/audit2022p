COLS_PIV = [('13', 2009), ('22', 2009),
            ('13', 2010), ('22', 2010),
            ('13', 2011), ('22', 2011),
            ('13', 2013), ('22', 2013),
            ('13', 2015), ('22', 2015),
            ('13', 2020), ('22', 2020),
            'qtd_modelos']

COLS_PIV_STR = ['13_2009', '22_2009',
                '13_2010', '22_2010',
                '13_2011', '22_2011',
                '13_2013', '22_2013',
                '13_2015', '22_2015',
                '13_2020', '22_2020',
                'qtd_modelos']

COLOR_GRADIENT_URNA_OUTROS_MODELOS = {(0.998, 1): "#0162A7", (0.9, 0.998): "#2B7CB6",
                                      (0.8, 0.9): "#5696C4", (0.7, 0.8): "#80B1D3",
                                      (0.6, 0.7): "#AACBE2", (0.5, 0.6): "#D5E5F0"}

COLOR_GRADIENT_URNA_MODELO_2020 = {(0.998, 1): "#F3AA20", (0.9, 0.998): "#F5B845",
                                   (0.8, 0.9): "#F7C66A", (0.7, 0.8): "#F9D590",
                                   (0.6, 0.7): "#FBE3B5", (0.5, 0.6): "#FDF1DA"}

COLOR_MODELO_URNA_BIN = {"modelo 2020": "#f3aa20", "modelo anterior": "#0162a7"}
COLOR_MODELO_URNA = {"2020": "#f3aa20", "2015": "#0162a7", "2013": "#0162a7",
                     "2011": "#0162a7", "2010": "#0162a7", "2009": "#0162a7"}



def in_faixa(num, faixas):
    for faixa in faixas:
        if num > faixa[0] and num <= faixa[1]:
            return faixa
    return None


def cor_gradiente(row):
    if row["modelo_urna_binario"] == "modelo 2020":
        faixa = in_faixa(row["Relativo"], COLOR_GRADIENT_URNA_MODELO_2020.keys())
        if faixa == None:
            cor = None
        else:
            cor = COLOR_GRADIENT_URNA_MODELO_2020[faixa]

    elif row["modelo_urna_binario"] == "modelo anterior":
        faixa = in_faixa(row["Relativo"], COLOR_GRADIENT_URNA_OUTROS_MODELOS.keys())

        if faixa == None:
            cor = None
        else:
            cor = COLOR_GRADIENT_URNA_OUTROS_MODELOS[faixa]

    return cor


def intersection(list_a, list_b):
    # inplace
    intersection_list = []

    for el in list_a:
        if el in list_b:
            intersection_list.append(el)

    return intersection_list


def count_votacao_por_endereco_modelo_urna(df, cols_endereco):
    return df.groupby(cols_endereco + ["modelo_urna"])[["13", "22"]].sum()


def count_unique_modelos_por_endereco(df, cols_endereco):
    return df.groupby(cols_endereco)["modelo_urna"].nunique().sort_values(ascending=False).to_frame("qtd_modelos")


def pivot_votacao_por_endereco_modelo_urna(df, cols_endereco):
    d = count_votacao_por_endereco_modelo_urna(df, cols_endereco).reset_index()
    return d.pivot(index=cols_endereco,
                   values=["13", "22"],
                   columns="modelo_urna")


def tuple_columns_to_str_column(tuple_columns):
    columns = [[col[0], str(col[1])] for col in tuple_columns]
    return ["_".join(col) if col[1] != "" else col[0] for col in columns]


def votacao_por_endereco_modelo_urna_com_contagem_modelos(df, cols_endereco):
    votacao_pivot = pivot_votacao_por_endereco_modelo_urna(df, cols_endereco).reset_index()
    votacao_pivot.columns = tuple_columns_to_str_column(votacao_pivot.columns.tolist())

    modelos_count = count_unique_modelos_por_endereco(df, cols_endereco).reset_index()
    votacao_pivot = votacao_pivot.merge(modelos_count, on=cols_endereco, how="left")

    use_cols_piv = intersection(COLS_PIV_STR, votacao_pivot.columns)

    return votacao_pivot[cols_endereco + use_cols_piv]


def str_apostrofe(term):
    return term.replace("d'", "d ")