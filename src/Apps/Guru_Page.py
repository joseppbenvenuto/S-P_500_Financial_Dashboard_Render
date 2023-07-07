from dash import html, dcc
import dash_bootstrap_components as dbc


######################################################################################################################
# NEW BLOCK - App layout
######################################################################################################################

layout = html.Div([
    
    # Instructions
    html.Div([
        
        dbc.Row([
        
            dcc.Link(

                dbc.Button(
                    'Click for Warren Buffett Sermon', 
                    color = 'primary',
                    className = "me-1",
                    style = {
                        'font-family':'Arial, Helvetica, sans-serif', 
                        'margin-left':'15px', 
                        'margin-top':'18px', 
                        'margin-bottom':'5px'
                    }
                ),
                href = 'https://www.youtube.com/watch?v=2a9Lx9J8uSs', 
                target='_blank',
                refresh = False
            )
        ], justify = "center"),
        
        dbc.Row([

            dcc.Link(

                dbc.Button(
                    'Click for Charlie Munger Sermon', 
                    color = 'primary',
                    className = "me-1",
                    style = {
                        'font-family':'Arial, Helvetica, sans-serif', 
                        'margin-left':'15px', 
                        'margin-top':'30px', 
                        'margin-bottom':'5px'
                    }
                ),
                href = 'https://www.youtube.com/watch?v=5U0TE4oqj24', 
                target='_blank',
                refresh = False
            )
        ], justify = "center",),
        
        dbc.Row([
        
            dcc.Link(

                dbc.Button(
                    'Click for Li Lu Sermon', 
                    color = 'primary',
                    className = "me-1",
                    style = {
                        'font-family':'Arial, Helvetica, sans-serif', 
                        'margin-left':'15px', 
                        'margin-top':'30px', 
                        'margin-bottom':'5px'
                    }
                ),
                href = 'https://www.youtube.com/watch?v=y3c2PKupiu8&list=WL&index=20', 
                target='_blank',
                refresh = False
            )
        ], justify = "center",),
        
        dbc.Row([
        
            dcc.Link(

                dbc.Button(
                    'Click for Howard Marks Sermon', 
                    color = 'primary',
                    className = "me-1",
                    style = {
                        'font-family':'Arial, Helvetica, sans-serif', 
                        'margin-left':'15px', 
                        'margin-top':'30px', 
                        'margin-bottom':'5px'
                    }
                ),
                href = 'https://www.youtube.com/watch?v=6WroiiaVhGo', 
                target='_blank',
                refresh = False
            )
        ], justify = "center"),
        
        dbc.Row([
        
            dcc.Link(

                dbc.Button(
                    'Click for Monish Purbai Sermon', 
                    color = 'primary',
                    className = "me-1",
                    style = {
                        'font-family':'Arial, Helvetica, sans-serif', 
                        'margin-left':'15px', 
                        'margin-top':'30px', 
                        'margin-bottom':'5px'
                    }
                ),
                href = 'https://www.youtube.com/watch?v=b9ioA0J-p2M', 
                target='_blank',
                refresh = False
            )
        ], justify = "center")
        
    ], 
        
    style = {
        'padding-top': 80
    })
])
        