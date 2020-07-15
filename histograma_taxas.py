import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import numpy as np

from funcoes_de_apoio import *

import plotly.graph_objs as go

from dash_app import app

help_histograma_taxas = html.Div([
        "Este gráfico mostra o número de municípios brasileiros com taxas de atendimento ",
        "por habitante-SUS correspondente ao valor no eixo dos x. ",
        "As linhas verticais marcam as posições das taxas do município escolhido, ",
        "da capital e do estado, e também do Brasil. ",
        html.Br(),
        "Somente são contabilizados municípios com pelo menos 1 atendimento no período.",
        html.Br(),
        "A linha ", html.Em("Limiar log-normal "),
        "se refere à taxa a partir da qual consideramos ter havido atendimentos em excesso. ",
        "Você pode ignorar essa linha, mas se tiver interesse, veja a explicação na aba ",
        html.Em("SUSano"),
        ", seção ",
        html.Em("Metodologia"),
        "."
        ])

def gera_histograma_taxas(dg, ds):
    
    taxa_municipal_máxima_no_alvo = ds.df_M_Alvo_em_foco['Taxa_por_hab_SUS'].max()
    
    hist, bin_edges = np.histogram(ds.df_M_Alvo_em_foco['Taxa_por_hab_SUS'])
    mean_count = np.mean(hist) / 2 # para regular a altura das linhas marcadoras verticais
    
    taxa_município_em_foco_trace = \
           go.Scatter(x=[ds.taxa_anual_M_Res * ds.denominador_populacional]*2,
                      y=[0, mean_count],
                      name=wrap(f'Taxa em {ds.M_Res_em_foco}', 30),
                      mode='lines',
                      line = dict(width=2),
                      hoverinfo='skip',
                      opacity=0.9)  
    
    taxa_BR_trace = go.Scatter(x = [ds.taxa_anual_Br * ds.denominador_populacional]*2,
                               y = [0, mean_count],
                               name=wrap(f'Taxa Brasil', 30),
                               mode='lines',
                               line = dict(width=1),
                               hoverinfo='skip',
                               opacity=0.9)
    
    taxa_capital_trace = go.Scatter(x = [ds.taxa_anual_Capital * ds.denominador_populacional]*2,
                           y = [0, mean_count],
                           name=wrap(f'Taxa {ds.Capital_em_foco}', 30),
                           mode='lines',
                           line = dict(width=1),
                           hoverinfo='skip',
                           opacity=0.9)
    
    taxa_UF_trace = go.Scatter(x = [ds.taxa_anual_UF * ds.denominador_populacional]*2,
                           y = [0, mean_count],
                           name=wrap(f'Taxa {ds.UF_M_Res_em_foco}', 30),
                           mode='lines',
                           line = dict(width=1),
                           hoverinfo='skip',
                           opacity=0.9)
    
    taxa_limiar_trace = go.Scatter(x=[ds.taxa_anual_limiar * ds.denominador_populacional]*2,
                      y=[0, mean_count],
                      name=wrap(f'Limiar log-normal', 30),
                      mode='lines',
                      line = dict(width=1),
                      hoverinfo='skip',
                      opacity=0.9)
    
    df_M_Alvo_em_foco_qtd_maior_que_zero = ds.df_M_Alvo_em_foco[ds.df_M_Alvo_em_foco['Qtd_EMA'] > 0]
    
    data = [go.Histogram(x=df_M_Alvo_em_foco_qtd_maior_que_zero['Taxa_por_hab_SUS'] * ds.denominador_populacional,
                         name='Número de municípios'), 
            taxa_BR_trace,
            taxa_UF_trace,
            taxa_capital_trace,
            taxa_limiar_trace,
            taxa_município_em_foco_trace
           ]
    
    layout = go.Layout(title={
            "text":f'Histograma de taxas de Atendimentos em {dg.ano_em_foco} no alvo <br>{ds.alvo_completo}',
            'x':0.5,
            'xanchor': 'center'},
                       font=dict(size=10),
                       yaxis={'title':f"Número de municípios"},
                       xaxis={'title': f'Atendimentos / {f_int(ds.denominador_populacional)} Habitantes SUS'},
                        )
    
    return go.Figure(data=data, layout=layout)

body = dbc.Container([dbc.Row([dbc.Col([dcc.Graph(id='histograma-taxas')
                                       ], md=12)
                              ])
                     ])
    
#botão_histograma_taxas = dbc.Button('HISTOGRAMA', id='botão-histograma-taxas', 
#                                      n_clicks=0, color='success')

@app.callback(Output('histograma-taxas', 'figure'),
#              [Input('botão-histograma-taxas', 'n_clicks')],
              [Input('store-análise', 'data')])
def mostra_histograma_taxas(store_análise):
    if store_análise is None:
        return go.Figure(data=[], layout=go.Layout(title='Sem dados para exibição'))
    return store_análise['Histograma_Taxas']
    
def Histograma_Taxas():
    layout = html.Div([ #botão_histograma_taxas,
                        body
                     ])
    return layout