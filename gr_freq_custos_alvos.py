
import dash_html_components as html

from funcoes_de_apoio import *

import plotly.graph_objs as go

help_gr_freq_custos_alvos = html.Div([
        "Para cada alvo registrado, este gráfico mostra um círculo cuja localização é determinada pelo ",
        "valor médio dos atendimentos no alvo e pelo número de atendimentos realizados. ",
        "Círculos correspondentes a alvos ambulatoriais e hospitalares são mostrados em cores distintas, "
        "e o alvo escolhido é mostrado em destaque.",
        html.Br(),
        "A área de cada círculo é proporcional ao valor total gasto no alvo correspondente. ",
        html.Ul([
        html.Li(["Experimente clicar sobre as legendas..."]),
        html.Li(["Experimente também os ícones no canto superior direito, que dão acesso a diversas funcionalidades interessantes."
                 ])
        ])
        ])

def gera_gr_freq_custos_alvos(dg, ds):
    
    hover_text = []
    for index, row in dg.df_EMA_g_A.iterrows():
        hover_text.append(row['Cod_Alvo'] + ' ' + row['Alvo'] + f"<br>Valor total: {row['Valor_EMA']:,.2f}")
    dg.df_EMA_g_A['hover_text'] = hover_text
    
    df_alvos_H = dg.df_EMA_g_A[(dg.df_EMA_g_A['Registro'] == 'H') &
                               (dg.df_EMA_g_A['Cod_Alvo'] != ds.Cod_Alvo_em_foco)]
    df_alvos_A = dg.df_EMA_g_A[(dg.df_EMA_g_A['Registro'] == 'A') &
                               (dg.df_EMA_g_A['Cod_Alvo'] != ds.Cod_Alvo_em_foco)]
    df_alvo_em_foco = dg.df_EMA_g_A[dg.df_EMA_g_A['Cod_Alvo'] == ds.Cod_Alvo_em_foco]
    
    sizeref = 1.* dg.df_EMA_g_A['Valor_EMA'].max()/(80.**2)
    sizemin = 4
    
    H_trace = go.Scatter(
            x=df_alvos_H['Qtd_EMA'],
            y=df_alvos_H['Valor_Médio'],
            name="Alvos Hospitalares",
            hovertemplate = 
                             '<b>%{text}</b><br>' +
                             '<b>Atendimentos</b>: %{x:,d}<br>' +
                             '<b>Valor médio</b>: R$%{y:,.2f}',
                             text = df_alvos_H['hover_text'].tolist(),
                             mode='markers',
                             marker=dict(
                                 size=df_alvos_H['Valor_EMA'],
                                 sizemode='area',
                                 sizeref=sizeref,
                                 sizemin=sizemin
                                 )
            )
                             
    A_trace = go.Scatter(
            x=df_alvos_A['Qtd_EMA'],
            y=df_alvos_A['Valor_Médio'],
            name="Alvos Ambulatoriais",
            hovertemplate = 
                             '<b>%{text}</b><br>' +
                             '<b>Atendimentos</b>: %{x:,d}<br>' +
                             '<b>Valor médio</b>: R$%{y:,.2f}',
                             text = df_alvos_A['hover_text'].tolist(),
                             mode='markers',
                             marker=dict(
                                 size=df_alvos_A['Valor_EMA'],
                                 sizemode='area',
                                 sizeref=sizeref,
                                 sizemin=sizemin
                                 )
            )          
                             
    Alvo_trace = go.Scatter(
            x=df_alvo_em_foco['Qtd_EMA'],
            y=df_alvo_em_foco['Valor_Médio'],
            name=wrap(ds.Cod_Alvo_em_foco + ' ' + ds.A_em_foco, 35),
            hovertemplate = 
                             '<b>%{text}</b><br>' +
                             '<b>Atendimentos</b>: %{x:,d}<br>' +
                             '<b>Valor médio</b>: R$%{y:,.2f}',
                             text = df_alvo_em_foco['hover_text'].tolist(),
                             mode='markers',
                             marker=dict(
                                 size=df_alvo_em_foco['Valor_EMA'],
                                 sizemode='area',
                                 sizeref=sizeref,
                                 sizemin=sizemin
                                 )
            )
                             
    data = [H_trace, A_trace, Alvo_trace]
    
    layout = go.Layout(
            title={
                    'text': 'Frequência x Valor Médio de Atendimentos' ,
                    'x':0.5,
                    'xanchor': 'center'
                    },
            xaxis = dict(
                    title='Número de Atendimentos',
                    type='log'
                    ),
            yaxis=dict(
                    title='Valor Médio de Atendimentos',
                    type='log'
                    )
            )
            
    return go.Figure(data=data, layout=layout)