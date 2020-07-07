import dash
import dash_html_components as html
from dash.dependencies import Input, Output, State, MATCH, ALL
import dash_bootstrap_components as dbc
import dash_core_components as dcc

from datetime import datetime

from dash_app import app
from SUSano import SUSano
from tabela_EMA import Tabela_EMA, tabela_EMA, spinner_análise
from relatorio_EMA import Relatório_EMA, EMPTY_REPORT
from graficos_EMA import Gráficos_EMA, EMPTY_FIGURE

app.config.suppress_callback_exceptions = True

body = dbc.Container([
                dbc.Row([
                    dbc.Col([

                        dbc.Tabs(
                            [
                                dbc.Tab(label="SUSano", tab_id="susano"),
                                dbc.Tab(label="Escolha", tab_id="escolha-EMA", 
                                        label_style={"color": "#00AEF9"}),
                                dbc.Tab(label="Tabelas", tab_id="relatório-EMA"),
                                dbc.Tab(label="Gráficos", tab_id="gr-EMA")
                            ],
                            id="tabs",
                            active_tab="susano",
                            persistence=True,
                            persistence_type='local'
                        ),
                        html.Div(id="tab-content"),
                        html.P("", className='horizontalGap'),
                        dbc.Alert(id="help-alert", color='warning', className='helpText'),
#                        dbc.Alert(id='console-main')
                           ])
                        ])
                    ])

aviso_escolha = 'Sem dados para exibir. Por favor, use a aba "Escolha EMA" para selecionar uma tripla (Estabelecimento, Município, Alvo)'

store_div = html.Div([ dcc.Store(id='last-tab', data={'when':0,
                                                       'from_tab': 'init',
                                                       'to_tab': 'init'}),
                        dcc.Store(id='store-análise', data={'when': 0,
                                                            'Relatório_EMA': {
                                                                    "município": EMPTY_REPORT},
                                                            'Gráficos_EMA': {
                                                                    'evolução': EMPTY_FIGURE}
                                                            }),
                        dcc.Store(id='store-update-tabela-EMA', data={'when': 0,
                                                                      'page_current': 0,
                                                                      'filter': ""}),
                        dcc.Store(id='store-update-seleção-EMA', data={'when': 0}),
                        dcc.Store(id='help-SUSano', 
                                  data='Ajuda SUSano'),
                        dcc.Store(id='help-relatórios-EMA', 
                                  data='Ajuda Relatórios'),
                        dcc.Store(id='help-escolha-EMA',
                                  data='Ajuda Escolha'),
                        dcc.Store(id='help-gráficos-EMA',
                                   data='Ajuda Gráficos')
                        ])

app.layout = html.Div([store_div, body])

@app.callback(Output('help-alert', 'children'),
              [Input('help-relatórios-EMA', 'data'),
               Input('help-escolha-EMA', 'data'),
               Input('help-gráficos-EMA', 'data'),
               Input('help-SUSano', 'data')])
def set_help(data_relatórios, data_escolha, data_gráficos, data_SUSano):
    ctx = dash.callback_context
#    print(f'ctx.triggered = {ctx.triggered}')
    return ctx.triggered[0]['value']

@app.callback(Output('console-main', 'children'),
              [Input('last-tab', 'data'),
               Input('store-análise', 'data'),
               Input('store-update-tabela-EMA', 'data'),
               Input('store-update-seleção-EMA', 'data')
               ])
def console_main(data_tabs, data_análise, data_tabela, data_seleção):
    
    return html.Div([html.P(f"last-tab:  {data_tabs['when']}"),
                     html.P(f"store-análise: {data_análise['when']}"),
                     html.P(f"store-update_tabela_EMA:  {data_tabela['when']}"),
                     html.P(f"store-update-seleção-EMA: {data_seleção['when']}")
                     ], className='divBorder')

@app.callback([Output("tab-content", "children"),
               Output("last-tab", 'data')],
              [Input("tabs", "active_tab")],
              [State("last-tab", "data")])
def switch_tab(at, last_tabs):
    if at is None:
        raise dash.exceptions.PreventUpdate
        
    when = datetime.timestamp(datetime.now())
    if last_tabs is None:
        from_tab = 'init'
    else:
        from_tab = last_tabs['to_tab']
    switch_rec = {'when': when,
                  'from_tab': from_tab,
                  'to_tab': at}
    
    if at == 'susano':
        return SUSano(), switch_rec
    elif at == "escolha-EMA":
        return Tabela_EMA(), switch_rec
    elif at == "relatório-EMA":
        return Relatório_EMA(), switch_rec
    elif at == "gr-EMA":
        return Gráficos_EMA(), switch_rec


if __name__ == '__main__':
    app.run_server(debug=False, port=8056)