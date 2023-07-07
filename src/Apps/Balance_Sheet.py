from dash import html, dash_table, Input, Output
from App import app
import pandas as pd
from datetime import date


######################################################################################################################
# NEW BLOCK - App layout
######################################################################################################################

layout = html.Div([
    
    # Table header
    html.Div([

        html.H2(
            'Balance Sheet',
            style = {
                'padding':10,
                'padding-top':10,
                'margin-top':50,
                'font-family':'Arial, Helvetica, sans-serif',
                # 'background':'#00008B',
                # 'color':'#FFFFFF',
                'textAlign':'left'
            }
        ),
        
        html.Div(id = 'balance_sheet')
    ]),
])

######################################################################################################################
# NEW BLOCK - App callbacks
######################################################################################################################

# Pull 
#####################################################
@app.callback(
    Output('balance_sheet','children'),
    Input('filtered_data', 'data')
)

def balance_sheet(jsonified_cleaned_data):
    # Get filtered data
    filtered_data = pd.read_json(jsonified_cleaned_data, orient = 'split')
    
    try:
        table = filtered_data.loc[(filtered_data['financial_statement'] == 'Balance Sheet')]

        table = table[[
            'financial_accounts',
            'calendar_year',
            'financial_values'
        ]]

        table['financial_values'] = table.apply(lambda x: "{:,}".format(x['financial_values']), axis = 1)
        table['calendar_year'] = table['calendar_year'].astype(str)

        # Pivot table
        table = table.pivot(
            index = 'financial_accounts', 
            columns = 'calendar_year',
            values = 'financial_values'
        )

        # Rename columns to remove multi-index column names
        table = table.reset_index()
        table = table.rename(columns = {'financial_accounts': 'Account'})

        # Reset index
        table = table.set_index(['Account'])

        # Reindex rows
        table = table.reindex([
            '',
            'Cash And Cash Equivalents',
            'Short Term Investments',
            'Cash And Short Term Investments',
            'Net Receivables',
            'Inventory',
            'Other Current Assets',
            'Total Current Assets',
            '',
            'Property Plant Equipment Net',
            'Goodwill',
            'Intangible Assets',
            'Goodwill And Intangible Assets',
            'Long Term Investments',
            'Tax Assets',
            'Other Non Current Assets',
            'Total Non Current Assets',
            'Other Assets',
            'Total Assets',
            '',
            'Account Payables',
            'Short Term Debt',
            'Tax Payables',
            'Deferred Revenue',
            'Other Current Liabilities',
            'Total Current Liabilities',
            '',
            'Long Term Debt',
            'Deferred Revenue Non Current',
            'Deferred Tax Liabilities Non Current',
            'Other Non Current Liabilities',
            'Total Non Current Liabilities',
            'Other Liabilities',
            'Capital Lease Obligations',
            'Total Liabilities',
            '',
            'Preferred Stock',
            'Common Stock',
            'Retained Earnings',
            'Accumulated Other Comprehensive Income Loss',
            'Othertotal Stockholders Equity',
            'Total Stockholders Equity',
            'Total Liabilities And Stockholders Equity',
            'Minority Interest',
            'Total Equity',
            'Total Liabilities And Total Equity',
            'Total Investments',
            'Total Debt',
            'Net Debt',
            ''
        ])

        table = table.fillna('').reset_index()
        
    except:
        table = pd.DataFrame([{
            'Account': '-',
            str(date.today().year - 4): '-',
            str(date.today().year - 3): '-',
            str(date.today().year - 2): '-',
            str(date.today().year - 1): '-'
        }])
        
    
    # Return table
    return html.Div([
        dash_table.DataTable(
            data = table.to_dict('records'),
            columns = [{'id': c, 'name': c} for c in table.columns],
            style_cell_conditional = [{'if': {'column_id': c},'textAlign': 'left'} for c in ['Account']],
            style_cell = {'font-family':'Arial, Helvetica, sans-serif'},
            style_as_list_view = True,
            style_header = {
                'font-family':'Arial, Helvetica, sans-serif',
                'font-size': 24,
                'backgroundColor': 'white',
                'fontWeight': 'bold'
            },
            style_data_conditional = [{'if': {'filter_query': '{Account} contains "Total"' }, 'fontWeight': 'bold'}]
        )
    ],
        
        style = {
            'padding-top': 10,
            'padding-left': 10,
            'padding-right': 15,
            'padding-bottom': 10,
        })

