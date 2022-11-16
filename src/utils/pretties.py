import pandas as pd
import IPython.display as ip_disp
from itertools import chain, cycle
from IPython.core.display import HTML
from IPython.display import display


def max_data_frame_columns(n: int = None):
    pd.set_option('display.max_columns', n)

def display_html(html: str):
    display(html)

def printt(txt, size=40, color="black"):
    html_font = f'<font style="font-size:{size}px" color={color}>{txt}</font>'
    display(HTML(html_font))

def hr(line_width=1):
    display_html(f'<hr style="height:1px;border-width:{line_width};color:#333;background-color:#333;" />')

def display_side_by_side(*args, titles=cycle([''])):
    html_str = ''
    for df, title in zip(args, chain(titles, cycle(['</br>']))):
        html_str += '<th style="text-align:center"><td style="vertical-align:top">'
        html_str += f'<h2>{title}</h2><br>'
        html_str += df.to_html().replace('table', 'table style="display:inline"')
        html_str += '</td></th>'
    ip_disp.display_html(html_str, raw=True)

def hr(line_width=1):
    display(HTML(f'<hr style="height:1px;border-width:{line_width};color:#333;background-color:#333;" />'))

def md(txt, size="#", cor="black"):
    html_size = round(len(size.split("#")) * 12.5)
    printt(txt, size=html_size, color=cor)
