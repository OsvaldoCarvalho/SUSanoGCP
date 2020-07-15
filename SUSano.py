import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import dash_core_components as dcc

from dash_app import app

seleção = dcc.Dropdown(
        id='SUSano-o-que-mostrar',
        options=[
                {"label": "Sobre", "value": "sobre"},
                {"label": "Metodologia", "value": "metodologia"},
                {"label": "Contato", "value": "contato"},
                {"label": "Créditos", "value": "créditos"}
                ],
        value='sobre'
        )

body = dbc.Container([
        dbc.Row([
                dbc.Col([
                        html.Img(src="./assets/logoSUSano.png",
                                 width=70,
                                 height=70)
                        ], width=1),
                dbc.Col([
                    html.Div([
                            html.H4("SUSano - Detecção de Taxas Extraordinárias de Atendimento pelo SUS")
                            ]),
                    ], width=6)]),
        dbc.Row([
                dbc.Col([seleção], width={"size": 4, "offset": 1})
                ])
        ])

texto_sobre = html.Div([
        "O sistema SUSano oferece análises da produção do SUS registrada "
        "nas bases SIA e SIH em 2018. Em particular, o SUSano permite encontrar com facilidade ocorrências "
        "de taxas extraordinárias de atendimentos por habitante prestados "
        "pelo SUS.",
        html.Ul([
                html.Li('Utilize a aba "Escolha" para especificar uma tripla '
                '(Estabelecimento, Município, Alvo) e obter tabelas '
                'e gráficos.')
                ])
        ])

texto_créditos = html.Div([
        "As ideias exploradas no SUSano amadureceram durante o projeto ",
        html.A("InfoSAS", href="http://revista.tcu.gov.br/ojs/index.php/RTCU/article/view/1378"),
        ", um trabalho conjunto de professores e técnicos da UFMG, "
        "e de sanitaristas do Ministério da Saúde e da Prefeitura de "
        "Belo Horizonte. ",
        html.Br(),
        "Douglas Mesquita (douglasrm.azevedo@gmail.com) desenvolveu a parte "
        "mais importante: um módulo em R que, a partir dos dados "
        "disponibilizados pelo DATASUS, ANS e IBGE, faz as estimativas "
        "dos parâmetros de cada distribuição log-normal, e produz os dados "
        "aqui utilizados.",
        html.Br(),
        "O aplicativo Python/Dash foi desenvolvido por Osvaldo Carvalho "
        "(osvaldo@dcc.ufmg.br, osvaldosfcarvalho@gmail.com), "
        "professor associado voluntário do Departamento de Ciência da Computação "
        "da UFMG."
        ])

texto_contato = html.Div([
        "Por favor, envie críticas, sugestões e erros que eventualmente perceber para",
        html.Br(),
        html.A("osvaldosfcarvalho@gmail.com",
               href="mailto:osvaldosfcarvalho@gmail.com",
               )
        ])
        
texto_metodologia = html.Div([
        "Nossa metodologia é muito simples, consistindo em: ",
        html.Ul([
                html.Li(["contabilizar os registros nas bases SIA e SIH "
                        "segundo ",
                        html.Em("alvos de mineração "),
                        ]),
                html.Li("utilizar métodos estatísticos para classificar as taxas de "
                        "atendimentos por habitante-SUS de cada município como "
                        "excessivas ou não"),
                html.Li("atribuir os atendimentos considerados excessivos aos "
                        "prestadores que atenderam ao município.")
                ]),
        "Nesta implantação, um alvo de mineração corresponde a uma "
        "Forma de Organização, o terceiro nível hierárquico da ",
        html.A("Tabela do SUS",
               href="http://sigtap.datasus.gov.br/tabela-unificada/app/sec/inicio.jsp",
               ),
        html.P("Para a classificação de atendimentos como excessivos nós partimos da constatação de que, "
        "para quase todos os alvos que estudamos, a distribuição das "
        "taxas de atendimento por habitante observadas nos municípios "
        "ajusta-se bem a uma distribuição log-normal, como os  exemplos mostrados na Figura 1." ),
        html.Figure([
                html.Img(src="./assets/ajuste_LogNormal.png",
                         width="70%",
#                         height=400,
                         className="figBorderCenter"),
                html.Figcaption("Figura 1", style={"text-align": "center"})
                ]),
        html.P(
        "Isso nos permitiu definir, para qualquer alvo "
        "e para qualquer município, um ponto de corte para o que "
        "consideramos como normal ou anormal em uma taxa de "
        "atendimentos por habitante." ),
        html.P(
        'Decidimos então arbitrar que taxas de atendimento por '
        'habitante serão consideradas anormais quando se situarem '
        'à direita do ponto que divide a área sob a curva em '
        'uma parte “normal”, com 99% de probabilidade; e em uma '
        'parte “anormal”, com 1% de probabilidade. Esse limiar de '
        'anormalidade que escolhemos poderá ser ajustado para mais ou para menos, '
        'em função de resultados de auditorias que eventualmente sejam realizadas '
        'por órgãos de controle.'),
        html.Figure([
                html.Img(src="./assets/limite_LogNormal.png",
                         width="50%",
                         className="figBorderCenter"),
                html.Figcaption("Figura 2", style={"text-align": "center"})
                ]),
        html.P(
        "Para o exemplo da Figura 2, taxas acima de 3,2 atendimentos "
        "por 1.000 habitantes/mês são consideradas anormais. Suponhamos "
        "que para o alvo em questão, um município de 100.000 habitantes "
        "tenha recebido 400 atendimentos em um dado mês. Pela taxa limite "
        "de 3,2 atendimentos/1.000 habitantes, a população desse município "
        "deveria ter recebido, no máximo, 320 atendimentos. Nós consideramos, "
        "então, que o município teve 80 atendimentos anômalos, que "
        "devem ser atribuídos aos prestadores que atenderam a este município." 
        ),
        html.P(
        "A regra de atribuição que adotamos foi de atribuição mínima: "
        "para o exemplo acima, se um prestador produziu 340 atendimentos, "
        "e como o limite de normalidade do município é de 320 atendimentos, "
        "a este prestador nós atribuímos 20=340-320 atendimentos em excesso. "
        "O valor monetário desse excesso é calculado multiplicando-se por 20 "
        "o valor médio dos atendimentos pelo prestador no alvo e no mês "
        "em questão. Aos outros prestadores responsáveis pelos 60 outros "
        "atendimentos o excesso atribuído é zero."
        ),
        html.P(
        "É importante observar que limiares e excessos são calculados "
        "mês a mês, e que a um prestador podem ser atribuídos valores "
        "significativos mesmo que sua média anual esteja dentro da "
        "normalidade."        
        )
        ])

help_SUSano = {}
help_SUSano["sobre"] = texto_sobre
help_SUSano["créditos"] = texto_créditos
help_SUSano["contato"] = texto_contato
help_SUSano["metodologia"] = texto_metodologia

@app.callback(Output('help-SUSano', 'data'),
              [Input('SUSano-o-que-mostrar', 'value')])
def set_help(o_que_mostrar):
    return help_SUSano[o_que_mostrar]

def SUSano():
    return html.Div([body])