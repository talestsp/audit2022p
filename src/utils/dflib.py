import numpy as np
import pandas as pd
import unicodedata
import math
from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype


def r_selec(df, random_value_from_colname, same_proba=False):
    series = df[random_value_from_colname]
    if same_proba:
        series = series.drop_duplicates()
    random_value = series.sample().item()
    return df[df[random_value_from_colname] == random_value]

def r_selec_n(df, random_value_from_colname, same_proba=False, n_samples=1):
    samples = pd.DataFrame()

    for i in range(n_samples):
        samples = samples.append(r_selec(df, random_value_from_colname, same_proba=same_proba))

    return samples

def normalize(series):
    return (series - series.min()) / (series.max() - series.min())

def categoricos_colname(df):
    colnames_categ = []

    for colname in df.columns:
        if df[colname].dtype == pd.Series([True, False]).dtype:
            colnames_categ.append(colname)

        if is_string_dtype(df[colname]):
            colnames_categ.append(colname)

    return colnames_categ

def numericos_colname(df):
    colnames_num = []

    for colname in df.columns:
        if df[colname].dtype == pd.Series([True, False]).dtype:
            continue

        if is_numeric_dtype(df[colname]):
            colnames_num.append(colname)

    return colnames_num

def drop_cols(df, cols):
    df = df.copy()
    for col in cols:
        if col in df.columns:
            del df[col]
    return df

def drop_index(df, index_list_to_drop):
    df = df.copy()

    for index_to_drop in index_list_to_drop:
        if index_to_drop in df.index.tolist():
            df = df.drop(index_to_drop)

    return df


def select_by_dict(df, dict_a):
    df = df.copy()

    for key_name in dict_a.keys():
        level = dict_a[key_name]
        df = df[df[key_name] == level]

    return df

def remove_acento_list(a_list):
    new_list = []

    for a_string in a_list:
        if not pd.Series(a_string).isna().item():
            colname_fixed = unicodedata.normalize('NFKD', a_string).encode('ascii', 'ignore').decode("utf-8")
            new_list.append(str(colname_fixed))
        else:
            new_list.append(a_string)

    return new_list

def remove_acento_nomes_colunas(df):
    map_colnames = {}
    for colname in df.columns:
        colname_fixed = unicodedata.normalize('NFKD', colname).encode('ascii', 'ignore').decode("utf-8")
        map_colnames[colname] = str(colname_fixed)
    df = df.rename(columns=map_colnames)
    return df

def rows_all_na(df):
    colnames = df.columns.tolist()
    df = df[df[colnames].apply(lambda row: row.isna().sum(), axis=1) == len(colnames)]
    return df

def is_num(str_value):
    try:
        float(str_value)
    except ValueError:
        return False

    return True

def is_valid_num(str_value):
    if is_num(str_value) and not math.isnan(float(str_value)):
        return True
    else:
        return False