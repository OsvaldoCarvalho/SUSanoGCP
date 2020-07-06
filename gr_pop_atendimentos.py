import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import numpy as np

from funcoes_de_apoio import *

import plotly.graph_objs as go

from dash_app import app

BUBLE_SIZE = 10

help_gr_pop_atendimentos = html.Div([
        "Este gráfico mostra em escala log-log o número de atendimentos no alvo escolhido ",
        "versus a população SUS de cada município do Brasil. ",
        "Os municípios da mesma UF do município escolhido são mostrados com uma cor distinta. ",
        html.Br(),
        "A linha ", html.Em("Limiar log-normal "),
        "se refere à taxa de atendimentos por habitante a partir da qual consideramos ter havido atendimentos em excesso. ",
        "Você pode ignorar essa linha, mas se tiver interesse, veja a explicação no manual do sistema.",
        html.Ul([
                html.Li(["Experimente clicar sobre as legendas..."]),
                html.Li(["Experimente também os ícones no canto superior direito, que dão acesso a diversas funcionalidades interessantes."
                         ])
        ])
    ])

def gera_gr_pop_atendimentos(dg, ds):
    
    hover_text = []
    for index, row in ds.df_M_Alvo_em_foco.iterrows():
        hover_text.append(f"{row['NOME_MUN']}, {row['SIGLA_UF']} <br>" +
                    f"População: {f_int(row['POP_MUN'])} <br>" +
                    f"População SUS :{f_int(row['POP_MUN_SUS'])}<br>" +
                    f"Atendimentos: {f_int(row['Qtd_EMA'])}<br>" +
                    f"Taxa por {ds.denominador_populacional} Hab. SUS: {f_float(row['Taxa_por_hab_SUS'] * ds.denominador_populacional)}")
    ds.df_M_Alvo_em_foco['hover_text'] = hover_text
    
    df_gráfico_BR = ds.df_M_Alvo_em_foco[ds.df_M_Alvo_em_foco['SIGLA_UF'] != ds.UF_M_Res_em_foco]
    
    df_gráfico_UF = ds.df_M_Alvo_em_foco[(ds.df_M_Alvo_em_foco['SIGLA_UF'] == ds.UF_M_Res_em_foco) &
                                         (ds.df_M_Alvo_em_foco['IBGE6_MUN'] != ds.IBGE_Res_em_foco)]
    
    df_gráfico_M_Res = ds.df_M_Alvo_em_foco[ds.df_M_Alvo_em_foco['IBGE6_MUN'] == ds.IBGE_Res_em_foco]
    
    BR_trace = go.Scatter(x=df_gráfico_BR.POP_MUN_SUS,
                      y=df_gráfico_BR.Qtd_EMA + 1,
                      name=wrap(f'Municípios do Brasil com exceção de {ds.UF_M_Res_em_foco}', 30),
                      hovertext=df_gráfico_BR.hover_text,
                      mode='markers',
                      marker=dict(color='royalblue'),
                      opacity=0.5)
    
    UF_trace = go.Scatter(x=df_gráfico_UF.POP_MUN_SUS,
                      y=df_gráfico_UF.Qtd_EMA + 1,
                      name=wrap(f'Municípios de {ds.UF_M_Res_em_foco}', 30),
                      text = df_gráfico_UF.hover_text,
                      mode='markers',
                      opacity=0.5)
    
    M_Res_trace = go.Scatter(x=df_gráfico_M_Res.POP_MUN_SUS,
                      y=df_gráfico_M_Res.Qtd_EMA + 1,
                      name=wrap(f'{ds.M_Res_em_foco}', 30),
                      text = df_gráfico_M_Res.hover_text,
                      mode='markers',
                      marker = dict(size=[BUBLE_SIZE],
                                                 color='red'),
                                   opacity = 1.0)
    
    pop_SUS_min = ds.df_M_Alvo_em_foco['POP_MUN_SUS'].min()
    pop_SUS_max = ds.df_M_Alvo_em_foco['POP_MUN_SUS'].max()
    
    limiar_trace = go.Scatter(x = [pop_SUS_min, pop_SUS_max],
                              y = [pop_SUS_min * ds.taxa_anual_limiar,
                                   pop_SUS_max * ds.taxa_anual_limiar],
                              name='Limiar log-normal',
                              mode='lines',
                              opacity=0.5)
    
    data = [BR_trace, UF_trace, M_Res_trace, limiar_trace]
    
    layout = go.Layout(title={
            'text': f'População SUS versus Atendimentos em {dg.ano_em_foco} no alvo <br>{ds.alvo_completo}',
            'x':0.5,
            'xanchor': 'center'},
                       font=dict(size=10),
                       yaxis={'title':f"Número de atendimentos + 1", 
                              'type': 'log'},
                       xaxis={'title': 'População SUS', 
                              'type': 'log'},
                       )
    
    
    return go.Figure(data=data, layout=layout)

body = dbc.Container([dbc.Row([dbc.Col([dcc.Graph(id='gr-pop-atend')
                                       ], md=12)
                              ])
                     ])
    
#botão_histograma_taxas = dbc.Button('HISTOGRAMA', id='botão-histograma-taxas', 
#                                      n_clicks=0, color='success')

@app.callback(Output('gr-pop-atend', 'figure'),
#              [Input('botão-histograma-taxas', 'n_clicks')],
              [Input('store-análise', 'data')])
def mostra_histograma_taxas(store_análise):
    if store_análise is None:
        return go.Figure(data=[], layout=go.Layout(title='Sem dados para exibição'))
    return store_análise['Gráfico_Pop_Atend']
    
def Gráfico_Pop_Atend():
    layout = html.Div([ #botão_histograma_taxas,
                        body
                     ])
    return layout