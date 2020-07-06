import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

from gr_evolucao_mensal import gera_gr_evolução_mensal, help_gr_evolução_mensal
from histograma_taxas import gera_histograma_taxas, help_histograma_taxas
from gr_pop_atendimentos import gera_gr_pop_atendimentos, help_gr_pop_atendimentos
from gr_freq_custos_alvos import gera_gr_freq_custos_alvos, help_gr_freq_custos_alvos

import plotly.graph_objs as go


from dash_app import app

from funcoes_de_apoio import *

EMPTY_FIGURE = go.Figure(data=[], layout=go.Layout(title='Sem dados para exibir. Por favor, use a aba "Escolha EMA" para selecionar uma tripla (Estabelecimento, Município, Alvo)'))

seleção = dcc.Dropdown(
                       id = "gráficos-o-que-mostrar",
                       options=[
                               {"label": "Evolução mês a mês", "value": "evolução"},
                               {"label": "Histograma municípios x taxas", "value": "histograma-taxas"},
                               {"label": "População SUS x Qtd Atendimentos", "value": "pop-atendimentos"},
                               {"label": "Frequência x Custo de Alvos", "value": "freq-custos-alvos"}
                               ],
                       value="evolução",
                       className='dropdownColor',
                       placeholder='Escolha um gráfico'
                       )

help_gráficos_EMA = {}
help_gráficos_EMA['evolução'] = help_gr_evolução_mensal
help_gráficos_EMA['histograma-taxas'] = help_histograma_taxas
help_gráficos_EMA['pop-atendimentos'] = help_gr_pop_atendimentos
help_gráficos_EMA['freq-custos-alvos'] = help_gr_freq_custos_alvos

    
def gera_gráficos_EMA(dg, ds):
    return {"evolução": gera_gr_evolução_mensal(dg, ds),
            "histograma-taxas": gera_histograma_taxas(dg, ds),
            "pop-atendimentos": gera_gr_pop_atendimentos(dg, ds),
            "freq-custos-alvos": gera_gr_freq_custos_alvos(dg, ds)
            }
    
body = dbc.Container([dbc.Row([dbc.Col(html.Div([dcc.Graph(id='gr-EMA')
                                       ], className='divBorder'), md=12)
                              ])
                     ])

@app.callback([Output('gr-EMA', 'figure'),
               Output('help-gráficos-EMA', 'data')],
              [Input('gráficos-o-que-mostrar', 'value')],
              [State('store-análise', 'data')])
def mostra_gráfico(o_que_mostrar, store_análise):
    if store_análise is None:
        return html.P('gráficos_EMA: store_análise is None!!'), 'Ajuda gráficos'
    try:
        print(f'mostra_gráfico: {type(store_análise["Gráficos_EMA"][o_que_mostrar])}')
        print(f'store_análise.keys() = {store_análise.keys()}')
        print(f'store_análise["Gráficos_EMA"].keys() = {store_análise["Gráficos_EMA"].keys()}')
        
        print(f'store_análise["Gráficos_EMA"][o_que_mostrar].keys() = {store_análise["Gráficos_EMA"][o_que_mostrar].keys()}')
        return store_análise['Gráficos_EMA'][o_que_mostrar], help_gráficos_EMA[o_que_mostrar]
    except:
        print('except executado')
        return [html.P(str(store_análise['Gráficos_EMA'])),
                html.P(o_que_mostrar)], \
               html.P(f'Help gráficos: {o_que_mostrar}') 



def Gráficos_EMA():
    return html.Div([seleção,
                     body])
