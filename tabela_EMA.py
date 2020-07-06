from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_table
from datetime import datetime
import dash_bootstrap_components as dbc
import dash

from dash_app import app
from dados import dg, dados_sessão
from gr_evolucao_mensal import gera_gr_evolução_mensal
from histograma_taxas import gera_histograma_taxas
from gr_pop_atendimentos import gera_gr_pop_atendimentos
from graficos_EMA import gera_gráficos_EMA
from relatorio_EMA import gera_relatório_EMA

PAGE_SIZE = 8

help_escolha_EMA = html.Div([
        'Escolha na tabela acima um estabelecimento, um município e um alvo para análise, ',
        'e aperte "PROCESSAR ESCOLHA" para obter tabelas e gráficos.',
        html.Br(),
        'As entradas estão ordenadas pela coluna "ESCORE EXCESSO", que é o produto '
        'do número de atendimentos que nosso tratamento estatístico considerou excessivos, '
        'pelo valor médio do atendimento. '
        'Para mais detalhes, '
        'veja a seção Metodologia na aba SUSano.',
        html.Br(),
        'Você pode filtrar os registros da tabela por valores em cada coluna. Por exemplo, se você quiser selecionar',
        html.Ul([
                html.Li('Apenas registros de estabelecimentos na Bahia, digite "ba" (com ou sem as aspas) '
                        'na linha de filtro da coluna UF do estabelecimento, e aperte enter'),
                html.Li(['Registros com alvos do subgrupo 0406/Cirurgia do Aparelho Circulatório, digite "0406" (',
                        html.Em('com '),
                        'as aspas) na linha de filtro da coluna de código do alvo '
                        '(este filtro irá incluir alvos como 030406 Quimioterapia Curativa, que contêm '
                        '"0406" em seu código)'
                        ]),
                html.Li('Apenas registros do estabelecimento de CNES 1234567, digite "1234567" (com as aspas) na linha de filtro da coluna CNES do estabelecimento')
                ]),
        'Você deve usar aspas sempre que sua chave de filtragem for composta somente por algarismos'
        ])

tabela_EMA = dash_table.DataTable(
                        id='tabela-EMA',
        #                data=df_EMA.to_dict('records'),
                        columns=[
                                {"name": ["ESCORE","EXCESSO (R$)"], "id": 'strValor_Excesso'},
                                {"name": ["ESTABELECIMENTO", "Nome"], "id": "Abrev_Estab"},
                                {"name": ["ESTABELECIMENTO", "CNES"], "id": "CNES"},
                                {"name": ["ESTABELECIMENTO", "Município"], "id": "Mun_Estab"},
                                {"name": ["ESTABELECIMENTO", "IBGE"], "id": "IBGE_Estab"},
                                {"name": ["ESTABELECIMENTO", "UF"], "id": "UF_Estab"},
                                {"name": ["MUNICÍPIO DE RESIDÊNCIA", "Município"], "id": "Mun_Res"},
                                {"name": ["MUNICÍPIO DE RESIDÊNCIA", "IBGE"], "id": "IBGE_Res"},
                                {"name": ["MUNICÍPIO DE RESIDÊNCIA", "UF"], "id": "UF_Res"},
                                {"name": ["ALVO - FORMA DE ORGANIZAÇÃO", "Código"], "id": "Cod_Alvo"},
                                {"name": ["ALVO - FORMA DE ORGANIZAÇÃO", "Descrição"], "id": "Abrev_Alvo"}
                        ],
                        merge_duplicate_headers=True,
                        style_data={
                                'border': '1px solid black'
                                },
                        style_data_conditional=[
                            {
                                'if': {'row_index': 'odd'},
                                'backgroundColor': 'rgb(210, 210, 210)'
                            }
                        ],
                        style_header={
                            'backgroundColor': 'rgb(200, 200, 230)',
                            'fontWeight': 'bold',
                            'border': '1px solid black'
                        },
                        style_filter={
                                'backgroundColor': 'rgb(252, 252, 187)',
                                'border': '1px solid black'
                        },        
                        style_cell_conditional=[
                            {
                                'if': {'column_id': c},
                                'textAlign': 'left'
                            } for c in ['Abrev_Estab',
                                        'Mun_Estab',
                                        'Mun_Res',
                                        'Abrev_Alvo']
                        ],
                        style_header_conditional=[
                                {'if': {'header_index': 0},
                                 'textAlign': 'center'}],
                        page_current=0,
                        page_size=PAGE_SIZE,
                        page_action='custom',
                        row_selectable='single',
                        filter_action='custom',
                        filter_query='',
                        selected_rows =[0],
                        sort_action='none',
                        sort_mode='multi',
                        sort_by=[]
                    )


operators = [['ge ', '>='],
             ['le ', '<='],
             ['lt ', '<'],
             ['gt ', '>'],
             ['ne ', '!='],
             ['eq ', '='],
             ['contains '],
             ['datestartswith ']]


def split_filter_part(filter_part):
    for operator_type in operators:
        for operator in operator_type:
            if operator in filter_part:
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find('{') + 1: name_part.rfind('}')]

                value_part = value_part.strip()
                v0 = value_part[0]
                if (v0 == value_part[-1] and v0 in ("'", '"', '`')):
                    value = value_part[1: -1].replace('\\' + v0, v0)
                else:
                    try:
                        value = float(value_part)
                    except ValueError:
                        value = value_part

                # word operators need spaces after them in the filter string,
                # but we don't want these later
                return name, operator_type[0].strip(), value

    return [None] * 3

def update_table(page_current, page_size, sort_by, filter):
    filtering_expressions = filter.split(' && ')
    dff = dg.df_EMA
    for filter_part in filtering_expressions:
        col_name, operator, filter_value = split_filter_part(filter_part)

        if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
            # these operators match pandas series operator method names
            dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
        elif operator == 'contains':
            dff = dff.loc[dff[col_name].str.contains(filter_value, case=False)]
        elif operator == 'datestartswith':
            # this is a simplification of the front-end filtering logic,
            # only works with complete fields in standard format
            dff = dff.loc[dff[col_name].str.startswith(filter_value)]

    if len(sort_by):
        dff = dff.sort_values(
            [col['column_id'] for col in sort_by],
            ascending=[
                col['direction'] == 'asc'
                for col in sort_by
            ],
            inplace=False
        )

    return dff.iloc[ 
        page_current*page_size: (page_current + 1)*page_size
    ].to_dict('records')
    
    
@app.callback(
    [Output('tabela-EMA', "data"),
     Output('tabela-EMA', 'selected_rows'),
     Output('store-update-tabela-EMA', "data"),
     Output('help-escolha-EMA', 'data')],
    [Input('tabela-EMA', "page_current"),
     Input('tabela-EMA', "page_size"),
     Input('tabela-EMA', "sort_by"),
     Input('tabela-EMA', "filter_query")],
    [State('store-update-tabela-EMA', 'data'),
     State('last-tab', 'data')]
    )
def atualiza_tabela(page_current, page_size, sort_by, filter, data_tabela, data_tab):
    when = datetime.timestamp(datetime.now())
    print(f'filter = {filter}')
    if data_tab['when'] > data_tabela['when']:
        filter = data_tabela['filter']
        page_current = data_tabela['page_current']
    return update_table(page_current, page_size, sort_by, filter), \
           [0], \
           {'when': when,
            'page_current': page_current,
            'filter': filter,
            'what': f'p_c = {page_current}, p_s = {page_size}, sort = {sort_by}, filter = {filter}'}, \
            help_escolha_EMA

@app.callback(
     Output('store-update-seleção-EMA', 'data'),
    [Input('tabela-EMA', "derived_virtual_data"),
     Input('tabela-EMA', "derived_virtual_selected_rows")],
    [State('last-tab', 'data')])
def update_seleção_EMA(rows, derived_virtual_selected_rows, last_tab_switch):
    
    if last_tab_switch is None:
        return {'when': 0}

    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = [0]
 
    if rows is None:
        return {'when': 0}
    
    if derived_virtual_selected_rows is None:
        return {'when': 0}
    
    if len(derived_virtual_selected_rows) == 0:
        # Mantém valores das variáveis em foco
        return {'when': 0}
   
    i_selected_row = derived_virtual_selected_rows[0]
    selected_row = rows[i_selected_row]
    
    CNES_em_foco = selected_row['CNES']
    IBGE_Res_em_foco = selected_row['IBGE_Res']
    Cod_Alvo_em_foco = selected_row['Cod_Alvo']
    
    
    when = datetime.timestamp(datetime.now())
    
    return {'when': when,
            'CNES_em_foco': CNES_em_foco,
            'IBGE_Res_em_foco': IBGE_Res_em_foco,
            'Cod_Alvo_em_foco': Cod_Alvo_em_foco}
    
    
#botão_análise = dbc.Button('ANALISAR', id='botão-análise', n_clicks=0, color='success')


spinner_análise = html.Div(
        [dbc.Row([
                dbc.Col([dbc.Button("PROCESSAR ESCOLHA", 
                                    id="botão-análise", 
                                    color='info', 
                                    className="mr-2",
                                    block=True),
                ], width=6),
                dbc.Col([
                         dbc.Spinner(html.Div(id='spinner-análise'),
                                     size="sm")
                         ])       
                ], style={"padding-top":"5px"})
        ])




@app.callback(
     [Output("spinner-análise", "children"),
      Output('store-análise', 'data')
     ],
     [Input("botão-análise", "n_clicks")],
     [State('store-update-seleção-EMA', 'data')]
)
def click_botão_análise(n, escolha_EMA):
    
    if n is None:
        raise dash.exceptions.PreventUpdate
    
    if escolha_EMA is None:
        raise dash.exceptions.PreventUpdate
    
    CNES_em_foco = escolha_EMA['CNES_em_foco']
    IBGE_Res_em_foco = escolha_EMA['IBGE_Res_em_foco']
    Cod_Alvo_em_foco = escolha_EMA['Cod_Alvo_em_foco']
    
    ds = dados_sessão(dg, 
                      CNES_em_foco, 
                      IBGE_Res_em_foco, 
                      Cod_Alvo_em_foco)
    
    gr_evolução = gera_gr_evolução_mensal(dg, ds)
    histograma_taxas = gera_histograma_taxas(dg, ds)
    gr_pop_atend = gera_gr_pop_atendimentos(dg, ds)
    relatório = gera_relatório_EMA(dg, ds)
    gráficos_EMA = gera_gráficos_EMA(dg, ds)
    
    
    when = datetime.timestamp(datetime.now())
    
    dados_análise = {'when': when,
                     'Relatório_EMA': relatório,
                     'Gráfico_Evolução_Mensal': gr_evolução,
                     'Histograma_Taxas': histograma_taxas,
                     'Gráfico_Pop_Atend': gr_pop_atend,
                     'Gráficos_EMA': gráficos_EMA}
    
    saída = f"Tabelas e gráficos prontos."
    if n is None:
        return "Not clicked.", dados_análise
    else:
        return saída, dados_análise
    

    
def Tabela_EMA():
    return html.Div([tabela_EMA,
                     spinner_análise])
    
#              [State('tabela-EMA', 'derived_virtual_data'),
#               State('tabela-EMA', 'derived_virtual_selected_rows'),
#               State('tabela-EMA', 'page_current'),
#               State('tabela-EMA', 'page_size'),
#               State('tabela-EMA', "sort_by"),
#               State('tabela-EMA', "filter_query")])
    