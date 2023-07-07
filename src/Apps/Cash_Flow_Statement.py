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
            'Cash-Flow Statement',
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
        
        html.Div(id = 'cash_flow_statement')
    ]),
])


######################################################################################################################
# NEW BLOCK - App callbacks
######################################################################################################################

# Pull 
#####################################################
@app.callback(
    Output('cash_flow_statement','children'),
    Input('filtered_data', 'data')
)

def cash_flow_statement(jsonified_cleaned_data):
    
    # Get filtered data
    filtered_data = pd.read_json(jsonified_cleaned_data, orient = 'split')
    
    try:
        # Cash-Flow statement
        table = filtered_data.loc[(filtered_data['financial_statement'] == 'Cash-Flow Statement')]

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
            'Net Income',
            'Depreciation And Amortization',
            'Deferred Income Tax',
            'Stock Based Compensation',
            'Change In Working Capital',
            'Accounts Receivables',
            'Inventory',
            'Accounts Payables',
            'Other Working Capital',
            'Other Non Cash Items',
            'Net Cash Provided By Operating Activities',
            '',
            'Investments In Property Plant And Equipment',
            'Acquisitions Net',
            'Purchases Of Investments',
            'Sales Maturities Of Investments',
            'Other Investing Activites',
            'Net Cash Used For Investing Activites',
            '',
            'Debt Repayment',
            'Common Stock Issued',
            'Common Stock Repurchased',
            'Dividends Paid',
            'Other Financing Activites',
            'Net Cash Used Provided By Financing Activities',
            '',
            'Effect Of Forex Changes On Cash',
            'Net Change In Cash',
            'Cash At End Of Period',
            'Cash At Beginning Of Period',
            'Operating Cash Flow',
            'Capital Expenditure',
            'Free Cash Flow',
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
            style_data_conditional = [
                {'if': {'filter_query': '{Account} = "Net Cash Provided By Operating Activities"'}, 'fontWeight': 'bold'},
                {'if': {'filter_query': '{Account} = "Net Cash Used For Investing Activites"'}, 'fontWeight': 'bold'},
                {'if': {'filter_query': '{Account} = "Net Cash Used Provided By Financing Activities"'}, 'fontWeight': 'bold'},
                {'if': {'filter_query': '{Account} = "Operating Cash Flow"'}, 'fontWeight': 'bold'},
                {'if': {'filter_query': '{Account} = "Capital Expenditure"'}, 'fontWeight': 'bold'},
                {'if': {'filter_query': '{Account} = "Free Cash Flow"'}, 'fontWeight': 'bold'}
            ]
        )
    ],
        
        style = {
            'padding-top': 10,
            'padding-left': 10,
            'padding-right': 15,
            'padding-bottom': 10,
        })

