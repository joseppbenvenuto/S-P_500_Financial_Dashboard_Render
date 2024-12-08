# Import packages
# from dash_labs.plugins.pages import register_page
from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objs as go

from App import app

import re

import numpy as np
import numpy_financial as npf

import pandas as pd

from bs4 import BeautifulSoup
import requests
import yfinance as yf


######################################################################################################################
# NEW BLOCK - App layout
######################################################################################################################

# App layout
layout = html.Div([
    
    # Live market price for company stock
    html.Div([

        html.H6(
            'Market Price:',
            style = {
                'display':'inline-block',
                'padding-left':20,
                'padding-top':10
            }
        ),
        
        html.H6(
            id = 'price',
            style = {
                'display':'inline-block',
                'padding-left':10
            }
        ),
        
        # Live market price to earnings of company stock
        html.H6(
            'TTM Price To Earnings:',
            style = {
                'display':'inline-block',
                'padding-left':40,
                'padding-top':10
            }
        ),
        
        html.H6(
            id = 'ttm_pe',
            style = {
                'display':'inline-block',
                'padding-left':10
            }
        ),
        
        # Current earnings per share of company stock in $
        html.H6(
            'FWD Price to Earnings:',
            style = {
                'display':'inline-block',
                'padding-left':40,
                'padding-top':10
            }
        ),
        
        html.H6(
            id = 'fwd_pe',
            style = {
                'display':'inline-block',
                'padding-left':10
            }
        ),
        
        # Current earnings per share of company stock %
        html.H6(
            'Dividend Yield:',
            style = {
                'display':'inline-block',
                'padding-left':40,
                'padding-top':10
            }
        ),
        
        html.H6(
            id = 'div',
            style = {
                'display':'inline-block',
                'padding-left':10
            }
        )
    ],
        
        style = {
            'font-family':'Arial, Helvetica, sans-serif',
            'padding-top':30,
            'textAlign':'center'
        }
    ),
    
    # Divider
    html.Hr(
        style = {
            'padding-bottom' : 20,
            'borderColor': 'black',
            'width' : '90%'
        }
    ),
    
    # Historical data for chosen field
    html.Div([

        dbc.Row([

            dbc.Col(

                dbc.Card(
                    dcc.Graph(id = 'scat1'), 
                    body = True, 
                    color = "dark", 
                    outline = True,
                    style = {'height':'37.5vh'}
                ),
                
                width = {
                    "size": 8,
                    "order": 1
                }
            ),
            
            # Calculator for compound rate of return
            dbc.Col(

                dbc.Card(

                    html.Div([

                        html.H5(
                            'Compound Rate of Return Calculator',
                            style = {
                                'padding-bottom': 10,
                                'padding-top': 10,
                                'font-family':'Arial, Helvetica, sans-serif'
                            }
                        ),
                        
                        # Input1
                        dbc.Row([

                            dbc.Input(
                                id = "input1",
                                placeholder = "Present Value, e.g., 1000",
                                type = "number",
                                persistence = True
                            )
                        ],
                            style = {
                                'padding-bottom': 5,
                                'padding-left': 10,
                                'padding-right': 10
                            }
                        ),
                        
                        # Input2
                        dbc.Row([

                            dbc.Input(
                                id = "input2",
                                placeholder = "Future Value, e.g., 2000",
                                type = "number",
                                persistence = True
                            )
                        ],
                            
                            style = {
                                'padding-bottom': 5,
                                'padding-left': 10,
                                'padding-right': 10
                            }
                        ),
                        
                        # Input3
                        dbc.Row([

                            dbc.Input(
                                id = "input3",
                                placeholder = "Years, e.g., 10",
                                type = "number",
                                persistence = True
                            )
                        ],
                            
                            style = {
                                'padding-bottom': 5,
                                'padding-left': 10,
                                'padding-right': 10
                            }
                        ),
                        
                        # Submit button
                        dbc.Row([

                            dbc.Button(
                                'Submit',
                                id = 'submit-val',
                                style = {'font-family':'Arial, Helvetica, sans-serif'}
                            ), 
                        ], 
                            className = 'd-grid gap-2 d-md-block',
                            style = {
                                'padding-top': 20,
                                'padding-left': 10,
                                'padding-right': 10
                            }
                        ),
                        
                        # Output
                        dbc.Row([

                            html.Label(
                                'Compounded Rate of Return:'
                            ),
                            html.Div(
                                id = 'output',
                                style = {
                                    'padding-left': 10
                                }
                            )
                        ],
                            
                            style = {
                                'padding-top': 10,
                                'padding-left': 10,
                                'padding-right': 10
                            }
                        )
                    ]),
                    
                    body = True,
                    color = "dark",
                    outline = True,
                    style = {'height':'37.5vh'}
                ),
                
                width = {
                    "size": 4,
                    "order": 2
                }
            )
        ])
    ],
        style = {
            'padding-left': 20,
            'padding-right': 20,
            'padding-top': 20,
            'padding-bottom': 30
        }
    ),
    
    # Company summary
    html.Div([

        html.H2(
            'Company Summary',
            style = {
                'padding':10,
                'padding-top':10,
                'margin':0,
                'font-family':'Arial, Helvetica, sans-serif',
                'background':'#00008B',
                'color':'#FFFFFF',
                'textAlign':'center'
            }
        ),
        
        html.Div(
            id = 'company_summary',
            style = {
                'padding':30,
                'font-family':'Arial, Helvetica, sans-serif',
                'line-height':30,
                'textAlign':'center',
                'fontSize':20
            }
        )
    ])
    
],
    style = {
        'margin':0
    }
)


######################################################################################################################
# NEW BLOCK - App callbacks
######################################################################################################################


# Graphics funtion
#####################################################
@app.callback(
    Output('scat1','figure'),
    Input('filtered_data', 'data'),
    Input('account_value', 'data'),
    Input('rate_value', 'data')
)

def graphs(jsonified_cleaned_data, account_value, rate_value):
    filtered_data = pd.read_json(jsonified_cleaned_data, orient = 'split')
    
    # Balance Sheet
    if rate_value == 1:
        filtered_data = filtered_data.loc[(filtered_data['financial_statement'] == 'Balance Sheet')]
    
    # Income Statement
    if rate_value == 2:
        filtered_data = filtered_data.loc[(filtered_data['financial_statement'] == 'Income Statement')]    
        
    # Cash-Flow Statement
    if rate_value == 3:
        filtered_data = filtered_data.loc[(filtered_data['financial_statement'] == 'Cash-Flow Statement')] 
    
    
    filtered_data = filtered_data.loc[(filtered_data['financial_accounts'] == account_value)].reset_index(drop = True)
    filtered_data['calendar_year'] = filtered_data['calendar_year'].astype(int)
    X = filtered_data['calendar_year']
    y = round(filtered_data['financial_values'], 2)

    # Make vis dynamic to show point with only 1 data point and not line
    if len(y) <= 1:
        mode = 'lines+markers'

    else:
        mode = 'lines'
        
    # Create vis
    data1 = go.Figure(
        data = go.Scatter(
            x = X,
            y = y,
            mode = mode,
            marker = {
                'size':12,'line':{
                    'width':2,
                    'color':'DarkSlateGrey'
                },
                'color':'#00008B'
            },
            name = 'Accounts'
        ),

        layout = go.Layout(
            paper_bgcolor = 'rgba(0,0,0,0)',
            plot_bgcolor = 'rgba(0,0,0,0)',
            font = {'color': '#111111'},
            height = 260
        )
    )

    # Set title
    data1.update_layout(
        title = str(filtered_data['company'].unique()[0]) + "'s <br>" + str(filtered_data['financial_accounts'].unique()[0]) + ' Over Years',
        title_font_family = 'Arial, Helvetica, sans-serif',
        title_font_size = 16, 
        title_font_color = 'Black', 
        title_x = 0.5,
        xaxis_range = [X.min() - 0.5, X.max() + 0.5],
        xaxis = {
            'dtick': 1
        }
    )

    return data1


# Compound rate of return function
#####################################################
@app.callback(
    Output('output', 'children'),
    Input('submit-val', 'n_clicks'),
    State('input1', 'value'),
    State('input2', 'value'),
    State('input3', 'value')
)

def compute(n_clicks, input1, input2, input3):
    # Set default input values
    if input1 == None:
        input1 = 1
    if input2 == None:
        input2 = 1
    if input3 == None:
        input3 = 1
    
    # Compound rate of return solution
    solution = npf.rate(
        nper = float(input3), 
        pmt = 0, 
        pv = float(input1) * -1, 
        fv = float(input2)
    )
    
    solution = round(solution * 100, 2)

    return '{}%'.format(solution)


# Live stock data function
#####################################################
@app.callback(
    Output('price','children'),
    Output('ttm_pe','children'),
    Output('fwd_pe','children'),
    Output('div','children'),
    Output('company_summary','children'),
    Input('filtered_data', 'data'),
    Input('ticker_value', 'data')
    )

def stock_data(jsonified_cleaned_data, ticker_value):
    # Import parsed data
    filtered_data = pd.read_json(jsonified_cleaned_data, orient = 'split')
    ticker = ticker_value

    ticker = yf.Ticker(ticker)
    info = ticker.info

    # Establish web-scraper
    # url = f'https://ca.finance.yahoo.com/quote/{ticker}'
    # response = requests.get(url)
    # soup = BeautifulSoup(response.text, 'html.parser')

    try:
        # Scrape live stock prices
        ###########################################################################
        # price = soup.find('div', class_='container yf-1tejb6')
        # price = [x.get_text().strip() for x in price]
        # price = price[0]
        # price = re.sub('[^a-zA-Z0-9.-]+', ' ', price)
        # price = price.replace(" ", "")

        price = ticker.info['currentPrice']

        # Debug
        if price == 'N/A':
            price = '-'
        else:
            price = price

        # Scarpe live pe stock data
        ###########################################################################
        # pe = soup.select('fin-streamer')
        # pe = [x.get_text().strip() for x in pe]
        # pe = pe[12]

        ttm_pe = ticker.info.get('trailingPE', 'N/A')

        # Debug
        if ttm_pe == 'N/A':
            ttm_pe = '-'
        else:
            ttm_pe = ttm_pe

        fwd_pe = ticker.info.get('forwardPE', 'N/A')

        # Debug
        if fwd_pe == 'N/A':
            fwd_pe = '-'
        else:
            fwd_pe = fwd_pe

        # # Debug
        # try:
        #     eps = round(float(price) / float(pe), 2)
        # except (ZeroDivisionError, ValueError):
        #     eps = '-'


        # # Debug
        # try:
        #     eps_percent = round((float(eps) / float(price)) * 100, 2)
        # except (ZeroDivisionError, ValueError):
        #     eps_percent = '-'

        div = round(ticker.info.get('dividendYield', 'N/A')*100,2)

        # Debug
        if div == 'N/A':
            div = '-'
        else:
            div = div

        # Scrape company summary
        ###########################################################################
        # summary = soup.find('p', class_='yf-1q2tqwv')
        # summary = [x.get_text().strip() for x in summary]
        # summary = summary[0]

        summary = info['longBusinessSummary']

        # Debug
        if summary == '':
            summary = '-'
        else:
            summary = summary
            
    except:
        price = '-'
        ttm_pe = '-'
        fwd_pe = '-'
        div = '-'
        summary = '-'

    return f'${price}', ttm_pe, fwd_pe, f'{div}%', summary

    
