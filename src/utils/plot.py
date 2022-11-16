import os
os.system("pip install matplotlib-venn")
import matplotlib.pyplot as plt
from matplotlib_venn import venn2


def sep(pause_time=0.1):
    plt.pause(pause_time)

def plot_venn2(series1, series2, label1=None, label2=None, title="", figsize=None):
    if label1 is None:
        label1 = series1.name
    if label2 is None:
        label2 = series2.name

    set1 = set(series1.drop_duplicates())
    set2 = set(series2.drop_duplicates())
    intersection = set1.intersection(set2)

    len_set1 = len(set1 - intersection)
    len_set2 = len(set2 - intersection)

    plt.title(title + f" ({series1.append(series2).nunique()})")

    if not figsize is None:
        plt.figure(figsize=figsize)
    return venn2(subsets=(len_set1, len_set2, len(intersection)),
                 set_labels=(label1, label2),
                 set_colors=('#3c89d0', '#FFB20A'),
                 alpha=0.7)