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
            'Income Statement',
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
        
        html.Div(id = 'income_statement')
    ]),
])


######################################################################################################################
# NEW BLOCK - App callbacks
######################################################################################################################

# Pull 
#####################################################
@app.callback(
    Output('income_statement','children'),
    Input('filtered_data', 'data')
)

def income_statement(jsonified_cleaned_data):
    # Get filtered data
    filtered_data = pd.read_json(jsonified_cleaned_data, orient = 'split')
    
    try:
        # Income statement
        table = filtered_data.loc[(filtered_data['financial_statement'] == 'Income Statement')]

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
            'Revenue',
            'Cost Of Revenue',
            'Gross Profit',
            'Gross Profit Ratio',
            '',
            'Research And Development Expenses',
            'General And Administrative Expenses',
            'Selling And Marketing Expenses',
            'Selling General And Administrative Expenses',
            'Other Expenses',
            'Operating Expenses',
            'Cost And Expenses',
            'Operating Income',
            'Operating Income Ratio',
            '',
            'Interest Income',
            'Interest Expense',
            'Depreciation And Amortization',
            'Ebitda',
            'Ebitdaratio',
            'Total Other Income Expenses Net',
            'Income Before Tax',
            'Income Before Tax Ratio',
            'Income Tax Expense',
            '',
            'Net Income',
            'Net Income Ratio',
            'Eps',
            'Epsdiluted',
            'Weighted Average Shs Out',
            'Weighted Average Shs Out Dil',
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
                {'if': {'filter_query': '{Account} = "Gross Profit"'}, 'fontWeight': 'bold'},
                {'if': {'filter_query': '{Account} = "Gross Profit Ratio"'}, 'fontWeight': 'bold'},
                {'if': {'filter_query': '{Account} = "Operating Income"'}, 'fontWeight': 'bold'},
                {'if': {'filter_query': '{Account} = "Operating Income Ratio"'}, 'fontWeight': 'bold'},
                {'if': {'filter_query': '{Account} = "Income Before Tax"'}, 'fontWeight': 'bold'},
                {'if': {'filter_query': '{Account} = "Income Before Tax Ratio"'}, 'fontWeight': 'bold'},
                {'if': {'filter_query': '{Account} = "Income Tax Expense"'}, 'fontWeight': 'bold'},
                {'if': {'filter_query': '{Account} = "Net Income"'}, 'fontWeight': 'bold'},
                {'if': {'filter_query': '{Account} = "Net Income Ratio"'}, 'fontWeight': 'bold'}
            ]
        )
    ],
        
        style = {
            'padding-top': 10,
            'padding-left': 10,
            'padding-right': 15,
            'padding-bottom': 10,
        })

