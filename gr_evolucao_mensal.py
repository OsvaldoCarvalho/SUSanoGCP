
import dash_html_components as html

from funcoes_de_apoio import *

import plotly.graph_objs as go


help_gr_evolução_mensal = html.Div([
        "O gráfico mostra a evolução mensal do número de atendimentos no alvo escolhido, ",
        "prestados a residentes do município escolhido. ",
        "É também mostrada a participação do estabelecimento escolhido nesse atendimento. ",
        html.Br(),
        "A linha ", html.Em("Taxa da capital x população SUS de ..."),
        " é construída multiplicando-se a taxa de atendimentos por habitante-SUS da ",
        "capital pela população SUS do município escolhido. ",
        "Em outras palavras, essa linha corresponde ao número esperado de atendimentos ",
        "ao município escolhido segundo a taxa da capital. ",
        "As linhas correspondentes à taxas da UF e do Brasil têm interpretação análoga.",
        html.Br(),
        "A linha ", html.Em("Limiar log-normal "),
        "se refere ao número a partir do qual consideramos ter havido atendimentos em excesso. ",
        "Você pode ignorar essa linha, mas se tiver interesse, veja a explicação na aba ",
        html.Em("SUSano"),
        ", seção ",
        html.Em("Metodologia"),
        ".",
        html.Ul([html.Li(["Experimente clicar sobre as legendas..."]),
                 html.Li(["Experimente também os ícones no canto superior direito, que dão acesso a diversas funcionalidades interessantes."])])
        ])


def gera_gr_evolução_mensal(dg, ds):
    meses = 'Jan Fev Mar Abr Mai Jun Jul Ago Set Out Nov Dez'.split()
    
    WRAP = 40
    
    M_trace = go.Scatter(x=meses,
                         y=ds.qtds_mensais_MA,
                         name=f'Em {ds.M_Res_em_foco}',
                         opacity=0.5,
                         line={'width':6})
    
    E_trace = go.Scatter(x=meses,
                         y=ds.qtds_mensais_EMA,
                         name=wrap(f'Por {ds.E_em_foco} a residentes de {ds.M_Res_em_foco}', WRAP),
                         opacity=0.5)
    
    qtd_mensal_média_EMA = sum(ds.qtds_mensais_EMA) / 12
    média_trace = go.Scatter(x=meses,
                             y=[qtd_mensal_média_EMA] * 12,
                             name='Média do atendimento mensal pelo prestador',
                             opacity=0.5)
    
    
    limiar_trace = go.Scatter(x=meses, y=ds.expec_limiares_mensais, 
                        name='Limiar log-normal', 
                        opacity = 0.5)
    

    capital_trace = go.Scatter(x=meses, y=ds.expec_taxas_Capital,
                               name=wrap(f'Taxa {ds.Capital_em_foco} x população SUS de {ds.M_Res_em_foco}', WRAP))
    
    
    UF_trace = go.Scatter(x=meses, y=ds.expec_taxas_UF,
                          name=wrap(f'Taxa {ds.nome_UF_Res_em_foco} x população SUS de {ds.M_Res_em_foco}', WRAP))
    
    
    Br_trace = go.Scatter(x=meses, y=ds.expec_taxas_Br,
                          name=wrap(f'Taxa Brasil x população SUS de {ds.M_Res_em_foco}', WRAP))
    
    data = [M_trace, E_trace, média_trace, limiar_trace, 
            capital_trace, UF_trace, Br_trace]
    
    título = f"Atendimentos por mês de {dg.ano_em_foco} a residentes em <b>{ds.M_Res_em_foco + ', ' + ds.UF_M_Res_em_foco}</b>, {f_int(ds.pop_SUS_M_Res_em_foco)} habitantes-SUS" + \
         f'<br>Prestador: <b>{ds.E_em_foco}</b>, CNES {ds.CNES_em_foco}, {ds.M_E_em_foco}, {ds.UF_E_em_foco}' 


                
    layout = go.Layout(title={
                            "text":título,
                            'x':0.5,
                            'xanchor': 'center'},
                       font=dict(size=10),
                       yaxis={'title':f"Número de atendimentos",
                             'rangemode': 'tozero',
                             'autorange': True},
                       xaxis={'title': ds.alvo_completo ,
                             'range': [0, 11],
                             'tick0': 1,
                             'dtick': 1,
                             'ticklen': 1})

    return go.Figure(data=data, layout=layout)
   
    
def Gráfico_Evolução_Mensal():
    layout = html.Div([
                        body
                     ])
    return layout 