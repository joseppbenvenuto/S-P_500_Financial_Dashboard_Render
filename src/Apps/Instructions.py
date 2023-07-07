from dash import html


######################################################################################################################
# NEW BLOCK - App layout
######################################################################################################################

layout = html.Div([
    
    # Instructions
    html.Div([

        html.H2(
            'Instructions',
            style = {
#                 'padding':10,
                'padding-top':10,
                'margin-top':50,
                'font-family':'Arial, Helvetica, sans-serif',
                # 'background':'#00008B',
                # 'color':'#FFFFFF',
                'textAlign':'center'
            }
        ),
        
        html.Div(

            html.P([
                "The dashboard provides data for 502 of the S&P 500 Index's companies American publicly traded companies. The dashboard \
                 aims to help users \
                 observe multi-year company financial data regarding the balance sheet, income, and cash-flow statements, and \
                 The user can choose a company and an account from each statement type, and the trend for the selected account will be \
                 displayed as a line chart.",
                 html.Br(),
                 html.Br(),
                "The dashboard provides live stock prices, price-to-earnings, earnings-per-share, and company summaries.",
                 html.Br(),
                 html.Br(),
                "Additionally, suppose the user toggles the tab buttons. In that case, they can observe a more structured balance sheet, \
                 income statement, cash-flow statements per selected company, financial ratios, and links to famous guru sermons.",
                 html.Br(),
                 html.Br(),
                "This tool should be used to analyze any single company along with that company's quarterly or annual filings."
            ]),
            
            style = {
                'padding-top':40,
                'padding-left':70,
                'padding-right':70,
                'font-family':'Arial, Helvetica, sans-serif',
                'line-height':30,
                'textAlign':'center',
                'fontSize':20
            }
        )
    ]),
])

