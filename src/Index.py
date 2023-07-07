import os
from threading import Timer
import webbrowser

from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc

import pandas as pd
import pathlib

# Connect to main app.py file
from App import app
from App import server

# Connect to your app pages
from Apps import Main_Page, Balance_Sheet, Income_Statement, Cash_Flow_Statement, Ratios, Guru_Page, Instructions


######################################################################################################################
# NEW BLOCK - Pre app setup
######################################################################################################################

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../src/Data").resolve()
df = pd.read_csv(DATA_PATH.joinpath('Financial_Statement.csv'))

# Create starting list of company names
company_drop =  df['company'].unique()

company_drop_list = []
for comp in company_drop:
    string = str(comp)
    company_drop_list.append(string)
    
company_drop = company_drop_list
company_drop.sort()
company_search_options1 = [{'label': comp, 'value': comp} for comp in company_drop]


# Create starting list of financial statement accounts applicable to current set value
accounts_drop = df.loc[(df['company'] == '3M')]
accounts_drop = accounts_drop['financial_accounts'].unique()

accounts_drop_list = []
for acc in accounts_drop:
    string = str(acc)
    accounts_drop_list.append(string)
    
accounts_drop = accounts_drop_list
accounts_drop.sort()
accounts_search_options2 = [{'label': acc, 'value': acc} for acc in accounts_drop]
value = accounts_search_options2[0]
value = value['value']


######################################################################################################################
# NEW BLOCK - App layout
######################################################################################################################

app.layout = html.Div([

    # Header by company
    html.Div([

        html.H2(
            'Financial Trends & Accounting for US Companies',
            style = {
                'padding':10,
                'margin':0,
                'font-family':'Arial, Helvetica, sans-serif',
                'background':'#00008B',
                'color':'#FFFFFF',
                'textAlign':'center'
            }
        )
    ]),
    
    dcc.Location(
        id = 'url', 
        refresh = False
    ),

    html.Div([
        
        dmc.Center(
        
            dbc.Row([

                dbc.Col(

                    dcc.Link(

                        dbc.Button(
                            'Click for Financial Visulization', 
                            style = {
                                'font-family':'Arial, Helvetica, sans-serif', 
                            }
                        ),
                        href = '/apps/Main_Page', 
                        refresh = False
                    ),

                    width = "auto"

                ),
                
                # Balance Sheet
                dbc.Col(

                    dcc.Link(

                        dbc.Button(
                            'Click for Balance Sheet',
                            style = {
                                'font-family':'Arial, Helvetica, sans-serif', 
                            }
                        ), 

                        href = '/apps/Balance_Sheet', 
                        refresh = False
                    ),

                    width = "auto"

                ),
                
                # Income Statement
                dbc.Col(

                    dcc.Link(

                        dbc.Button(
                            'Click for Income Statement',
                            style = {
                                'font-family':'Arial, Helvetica, sans-serif', 
                            }
                        ), 

                        href = '/apps/Income_Statement', 
                        refresh = False
                    ),

                    width = "auto"

                ),
                
                # Cash-Flow Statement
                dbc.Col(

                    dcc.Link(

                        dbc.Button(
                            'Click for Cash-Flow Statement',
                            style = {
                                'font-family':'Arial, Helvetica, sans-serif', 
                            }
                        ), 

                        href = '/apps/Cash_Flow_Statement', 
                        refresh = False
                    ),

                    width = "auto"

                ),
                
                # Ratios
                dbc.Col(

                    dcc.Link(

                        dbc.Button(
                            'Click for Financial Ratios',
                            style = {
                                'font-family':'Arial, Helvetica, sans-serif', 
                            }
                        ), 

                        href = '/apps/Ratios', 
                        refresh = False
                    ),

                    width = "auto"

                ),
                
                # Gurus
                dbc.Col(

                    dcc.Link(

                        dbc.Button(
                            'Click for Guru Educational Videos',
                            style = {
                                'font-family':'Arial, Helvetica, sans-serif', 
                            }
                        ), 

                        href = '/apps/Guru_Page', 
                        refresh = False
                    ),

                    width = "auto"

                ),

                # Application Instructions
                dbc.Col(

                    dcc.Link(

                        dbc.Button(
                            'Click for Application Instructions',
                            style = {
                                'font-family':'Arial, Helvetica, sans-serif', 
                            }
                        ), 
                        href = '/apps/Instructions', 
                        refresh = False
                    ),

                    width = "auto"

                )
            ], style = {'padding-top': 18})
        )
    
    ], 
        className = 'd-grid gap-2 d-md-block'
    
    ),    
    
    # Dynamic header by company
    html.Div([
        
        html.H2(
            id = 'header',
            style = {
                'padding-top': 40,
                'padding':10,
                'margin':0,
                'font-family':'Arial, Helvetica, sans-serif',
                'textAlign':'center'
            }
        )
    ], style = {'padding-top': 10}),
    
    # Compnay dropdown menu
    html.Div([
        
        # Radio buttons companies in or out of Value Index
        html.Div([
            dcc.RadioItems(
                id = 'rate',
                
                options = [
                    {'label': 'Balance Sheet', 'value': 1},
                    {'label': 'Income Statement', 'value': 2},
                    {'label': 'Cash-Flow Statement', 'value': 3}
                ],
                
                value = 1,
                labelStyle = {'display': 'inline-block'},
                inputStyle = {"margin-left": 20},
                style = {
                    'textAlign':'center',
                    'padding-top':10,
                    'padding-bottom':15,
                    'padding-right': 15,
                    'font-family':'Arial, Helvetica, sans-serif'
                }
            )
        ]),

        dbc.Row([

            dbc.Col(

                html.H5(
                    'Choose a Company',
                    style = {'textAlign':'center'}
                )
            ),
            
            dbc.Col(

                html.H5(
                    'Choose an Account',
                    style = {'textAlign':'center'}
                )
            )
        ]),
        
        dbc.Row([

            dbc.Col(
                # Company dropdown menu
                dcc.Dropdown(
                    id = 'company',
                    options = company_search_options1,
                    value = '3M',
                    style = {
                        'border-color': 'black',
                        'font-size':'90%'
                    },
                    persistence = True
                )
            ),
            
            # Account dropdown menu
            dbc.Col(
                dcc.Dropdown(
                    id = 'account',
                    optionHeight = 55,
                    options = accounts_search_options2,
                    value = value,
                    style = {
                        'border-color': 'black',
                        'font-size':'90%'
                    },
                    persistence = True
                )
            )
        ])
    ],
        
        style = {
            'font-family':'Arial, Helvetica, sans-serif',
            'padding-top':10,
            'padding-right':'5%',
            'padding-left':'5%',
            'textAlign':'left'
        }
    ),
    
    html.Div(
        id = 'page-content', 
        children = []
    ),
    
    # Stores filtered data
    dcc.Store(id = 'filtered_data', storage_type = 'session'),
    
    # Stores account data
    dcc.Store(id = 'account_value', storage_type = 'session'),
    
    # Stores ticker data
    dcc.Store(id = 'ticker_value', storage_type = 'session'),
    
    # Stores rate data
    dcc.Store(id = 'rate_value', storage_type = 'session'),
    
])


######################################################################################################################
# NEW BLOCK - App callbacks
######################################################################################################################

# Multi-page functionality
#####################################################
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)

def display_page(pathname):
    if pathname == '/apps/Main_Page':
        return Main_Page.layout
    
    if pathname == '/apps/Balance_Sheet':
        return Balance_Sheet.layout
    
    if pathname == '/apps/Income_Statement':
        return Income_Statement.layout

    if pathname == '/apps/Cash_Flow_Statement':
        return Cash_Flow_Statement.layout
    
    if pathname == '/apps/Ratios':
        return Ratios.layout
    
    if pathname == '/apps/Guru_Page':
        return Guru_Page.layout

    if pathname == '/apps/Instructions':
        return Instructions.layout
    
    else:
        return Main_Page.layout


# App function for dropdown menu and header
#####################################################
@app.callback(
    Output('account','options'),
    Output('account','value'),
    Output('header','children'),
    Input('company','value'),
    Input('rate','value')
)

def field_dropdown(company, rate):
    # Account per company
    accounts = df.copy()
    
    # Balance Sheet
    if rate == 1:
        accounts = accounts.loc[
            (accounts['company'] == company) & 
            (accounts['financial_statement'] == 'Balance Sheet')
        ]
    
    # Income Statement
    if rate == 2:
        accounts = accounts.loc[
            (accounts['company'] == company) & 
            (accounts['financial_statement'] == 'Income Statement')
        ]    
        
    # Cash-Flow Statement
    if rate == 3:
        accounts = accounts.loc[
            (accounts['company'] == company) & 
            (accounts['financial_statement'] == 'Cash-Flow Statement')
        ] 
     
    
    # Preprocess search options
    accounts = accounts['financial_accounts'].unique()
    new_accounts = []
    for account in accounts:
        string = str(account)
        new_accounts.append(string)

    accounts = new_accounts
    accounts.sort()
    accounts_search_options2 = [{'label': account, 'value': account} for account in accounts]
    value = accounts_search_options2[0]
    value = value['value']
    
    # Header
    header =  f"{company}"
    
    return accounts_search_options2, value, header


# Filter data to be used across the app
#####################################################
@app.callback(
    Output('filtered_data', 'data'),
    Output('account_value', 'data'),
    Output('ticker_value', 'data'),
    Output('rate_value', 'data'),
    Input('company','value'),
    Input('account','value'),
    Input('rate','value')
)

def filter_data(company, account, rate):
    # Parse data
    filtered_data = df.copy()
    filtered_data = filtered_data.loc[(filtered_data['company'] == company)].reset_index(drop = True)
    ticker = filtered_data['ticker'].unique()[0]
    
    return filtered_data.to_json(date_format = 'iso', orient = 'split'), account, ticker, rate


if __name__ == '__main__':
    app.run_server()

    