import pandas as pd
import IPython.display as ip_disp


def freq(series, round_relative_n=None):
    freq_abs = series.value_counts()
    freq_rel = series.value_counts(normalize=True)

    if series.name is None:
        freq_abs.name = "Absoluto"
        freq_abs = freq_abs.to_frame()

        freq_rel.name = "Relativo"
        freq_rel = freq_rel.to_frame()

    else:
        freq_abs = freq_abs.to_frame().rename(columns={series.name: "Absoluto"})
        freq_rel = freq_rel.to_frame().rename(columns={series.name: "Relativo"})

    if not round_relative_n is None:
        freq_rel["Relativo"] = freq_rel["Relativo"].apply(lambda v: round(v, round_relative_n))

    return freq_abs.join(freq_rel)

def describe(series, metrics=["mean", "25%", "50%", "75%"]):
    return series.describe().to_frame().transpose()[metrics]

def filter_quantile(series, q_min, q_max):
    q_min_value = series.quantile(q_min)
    q_max_value = series.quantile(q_max)

    use_series = series[(series >= q_min_value) & (series <= q_max_value)]
    return use_series

def filter_value(series, min_value=None, max_value=None):
    if min_value is None:
        min_value = series.min()

    if max_value is None:
        max_value = series.max()

    use_series = series[(series >= min_value) & (series <= max_value)]
    return use_series

def describe_filter_quantile(series, title="", q_min=0, q_max=1, bins=100):
    use_series = filter_quantile(series, q_min, q_max)

    describe_all = series.describe().to_frame().transpose()
    describe_all.index = ["Todos os dados"]
    describe_select = use_series.describe().to_frame().transpose()
    describe_select.index = ["Dados filtrados por quantis"]

    describes = describe_all.append(describe_select)

    ip_disp.display(describes)
    use_series.plot.hist(title=title, bins=bins, figsize=(6, 3));
    p = describes[["25%", "50%", "75%"]].transpose().plot.bar(rot=0, figsize=(6, 3))
    p.set_ylabel("Frequency")

def flat_describe(series, name=None, metrics=None):
    describe_series = series.describe()

    if metrics is None:
        metrics = describe_series.index.tolist()
    if name is None:
        name = series.name

    describe_series.name = name
    describe_series_df = describe_series.to_frame().transpose()[metrics]
    return describe_series_df

def flat_describes(series_list, names=None, metrics=None):
    describes_df = pd.DataFrame()

    if names is None:
        names = [None] * len(series_list)

    for i in range(len(series_list)):
        describe_series = flat_describe(series_list[i], name=names[i], metrics=metrics)
        describes_df = describes_df.append(describe_series)

    return describes_df

